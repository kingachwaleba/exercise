import boto3


BUCKET_NAME = "developer-task"
PREFIX = "y-wing/"

session = boto3.Session(profile_name="default")
s3 = session.resource("s3")

bucket = s3.Bucket(BUCKET_NAME)
for file in bucket.objects.filter(Prefix=PREFIX):
    print(file.key)
