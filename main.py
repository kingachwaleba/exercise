import os

import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "developer-task"
PREFIX = "y-wing/"

s3_client = boto3.client("s3")

def list_files():
    response = s3_client.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=PREFIX
    )
    for file in response.get("Contents"):
        print(file["Key"])

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as error:
        print(error)
        return False
    return True

with open("FILE_NAME", "rb") as f:
    s3_client.upload_fileobj(f, "amzn-s3-demo-bucket", "OBJECT_NAME")
