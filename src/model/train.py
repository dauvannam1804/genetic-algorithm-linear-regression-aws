import yaml
import pandas as pd
import numpy as np
import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from genetic_linear_regression import GeneticLinearRegression

load_dotenv()

def load_params(path="src/config/params.yml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_data(path, target_col):
    df = pd.read_csv(path)    
    cols_to_drop = [target_col]
    
    for col in df.columns:
        if 'Unnamed' in col or col.strip() == '':
            cols_to_drop.append(col)
    
    X = df.drop(columns=cols_to_drop).values
    y = df[target_col].values
        
    return X, y

def get_s3_client():
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    REGION = os.getenv("REGION", "ap-southeast-2")
    
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise EnvironmentError("❌ Missing AWS credentials in .env file")
    
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION
    )
    
    return s3, REGION

def bucket_exists(s3_client, bucket_name):
    try:
        buckets = [b["Name"] for b in s3_client.list_buckets()["Buckets"]]
        return bucket_name in buckets
    except Exception as e:
        print(f"⚠️ Error checking bucket: {e}")
        return False

def object_exists(s3_client, bucket_name, key):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise

def upload_model_to_s3(local_path, bucket_name, s3_key, s3_client, region):
    try:
        if not bucket_exists(s3_client, bucket_name):
            print(f"🪣 Creating new bucket: {bucket_name}")
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
            print(f"✅ Bucket created successfully!")
        
        print(f"📤 Uploading model to S3...")
        s3_client.upload_file(local_path, bucket_name, s3_key)
        
        print(f"✅ Model uploaded successfully to s3://{bucket_name}/{s3_key}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error uploading to S3: {e}")
        return False

def main():
    print("=" * 60)
    print("🧬 GENETIC ALGORITHM LINEAR REGRESSION - TRAINING")
    print("=" * 60)
    
    # 1️⃣ Load params
    params = load_params()
    print("\n✅ Loaded params:", params)

    # 2️⃣ Load data
    X, y = load_data(params["data_path"], params["target_col"])
    print(f"📊 Loaded dataset: X={X.shape}, y={y.shape}")

    # 3️⃣ Train model
    print(f"\n🚀 Starting training with {params['n_generations']} generations...")
    model = GeneticLinearRegression(
        pop_size=params["pop_size"],
        n_generations=params["n_generations"],
        crossover_rate=params["crossover_rate"],
        mutation_rate=params["mutation_rate"]
    )
    
    model.fit(X, y)

    # 4️⃣ Save model locally
    local_weights_path = "src/weights/genetic_lr_weights.npy"
    print(f"\n💾 Saving model locally to: {local_weights_path}")
    model.save_model(local_weights_path)

    # 5️⃣ Upload to S3
    print("\n" + "=" * 60)
    print("☁️  UPLOADING MODEL TO AWS S3")
    print("=" * 60)
    
    try:
        s3_client, region = get_s3_client()
        
        bucket_name = params.get("s3_bucket_name", "genetic-algorithm-data-bucket")
        s3_key = params.get("s3_model_key", "models/genetic_lr_weights.npy")
        
        print(f"📦 Bucket: {bucket_name}")
        print(f"🔑 Key: {s3_key}")
        
        success = upload_model_to_s3(
            local_path=local_weights_path,
            bucket_name=bucket_name,
            s3_key=s3_key,
            s3_client=s3_client,
            region=region
        )
        
        if success:
            print("\n" + "=" * 60)
            print("✨ TRAINING & UPLOAD COMPLETED SUCCESSFULLY!")
            print("=" * 60)
        else:
            print("\n⚠️ Training completed but upload failed. Model saved locally.")
            
    except Exception as e:
        print(f"\n⚠️ Could not upload to S3: {e}")
        print("💾 Model is still saved locally at:", local_weights_path)

if __name__ == "__main__":
    main()