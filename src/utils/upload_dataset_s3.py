import boto3
import requests
from io import BytesIO
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

# URL file CSV (raw link)
url = "https://raw.githubusercontent.com/dauvannam1804/csv_data/main/advertising.csv"

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION = os.getenv("REGION", "ap-southeast-2")  # fallback nếu quên khai báo

# Kiểm tra key
if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
    raise EnvironmentError("❌ Missing AWS credentials in .env file")

# Tạo kết nối S3
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION
)

bucket_name = "genetic-algorithm-data-bucket"
object_key = "datasets/advertising.csv"


def bucket_exists(s3_client, bucket_name):
    buckets = [b["Name"] for b in s3_client.list_buckets()["Buckets"]]
    return bucket_name in buckets


def object_exists(s3_client, bucket_name, key):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise


def upload_csv_to_s3(url, bucket_name, key):
    response = requests.get(url)
    response.raise_for_status()

    if not bucket_exists(s3, bucket_name):
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': REGION}
        )
        print(f"🪣 Created new bucket: {bucket_name}")

    if object_exists(s3, bucket_name, key):
        print(f"⚠️ Object {key} existed in bucket {bucket_name}, bỏ qua upload.")
        return

    s3.upload_fileobj(BytesIO(response.content), bucket_name, key)
    print(f"✅ File uploaded successfully to s3://{bucket_name}/{key}")


if __name__ == "__main__":
    upload_csv_to_s3(url, bucket_name, object_key)
