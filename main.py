import boto3
from boto3 import client

BUCKET_NAME = "developer-task"
PREFIX = "y-wing/"

s3_client = boto3.client("s3")

response = s3_client.list_objects_v2(
    Bucket=BUCKET_NAME,
    Prefix=PREFIX
)
for file in response.get("Contents"):
    print(file["Key"])
