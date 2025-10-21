import boto3
import requests
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

# URL file CSV (dùng raw link để tải đúng dữ liệu CSV)
url = "https://raw.githubusercontent.com/dauvannam1804/csv_data/main/advertising.csv"

response = requests.get(url)
response.raise_for_status()

# Kết nối S3
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="ap-southeast-2"
)

bucket_name = "genetic-algorithm-data-bucket"
object_key = "datasets/advertising.csv"

# Kiểm tra bucket, nếu chưa có thì tạo
existing_buckets = [b['Name'] for b in s3.list_buckets()['Buckets']]
if bucket_name not in existing_buckets:
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': 'ap-southeast-2'}
    )
    print(f"🪣 Created new bucket: {bucket_name}")

# Upload thẳng file CSV lên S3
s3.upload_fileobj(BytesIO(response.content), bucket_name, object_key)
print(f"✅ File uploaded successfully to s3://{bucket_name}/{object_key}")
