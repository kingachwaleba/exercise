import os
from urllib.request import build_opener

import click
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "developer-task"
PREFIX = "y-wing/"

s3_client = boto3.client("s3")

@click.group()
def cli():
    pass

@cli.command()
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

@cli.command()
@click.argument('file_name')
@click.argument('bucket')
@click.argument('object_name')
def upload_file_final(file_name, bucket, object_name):
    with open(file_name, "rb") as file:
        s3_client.upload_fileobj(
            file,
            bucket,
            object_name
        )

@cli.command()
@click.argument('pattern')
def filter_files(pattern):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)
    for file in bucket.objects.filter(Prefix=pattern):
        print(file.key)

if __name__ == "__main__":
    cli()
