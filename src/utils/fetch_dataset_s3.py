import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def download_from_s3(bucket_name, object_key, local_path):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("REGION")
    )
    print(f"Downloading s3://{bucket_name}/{object_key} to {local_path}")
    s3.download_file(bucket_name, object_key, local_path)
    print(f"✅ Downloaded {object_key} to {local_path}")

if __name__ == "__main__":
    bucket = "genetic-algorithm-data-bucket"
    key = "datasets/advertising.csv"
    local_file = "src/data/advertising.csv"

    os.makedirs("src/data", exist_ok=True)
    download_from_s3(bucket, key, local_file)
