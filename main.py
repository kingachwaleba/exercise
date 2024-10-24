import os

import re
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
    regex = re.compile(pattern)
    response = s3_client.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=PREFIX
    )
    for file in response.get("Contents"):
        if regex.search(file.get("Key")):
            print(file.get("Key"))

@cli.command()
@click.argument('pattern')
def delete_files(pattern):
    response = s3_client.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=PREFIX
    )
    for file in response.get("Contents"):
        if pattern in file.get("Key"):
            s3_client.delete_object(Bucket=BUCKET_NAME, Key=file)
            print(f"{file.get("Key")} has been deleted")

if __name__ == "__main__":
    cli()
