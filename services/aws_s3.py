import boto3
import os

s3 = boto3.client(
    's3',
    aws_access_key_id=str(os.getenv("aws_accesskey")),
    aws_secret_access_key=str(os.getenv("aws_secretkey")),
)

async def upload_file_to_s3(file, bucket, object_name):
    s3.upload_fileobj(file.file, bucket, object_name)
    return f"https://{bucket}.s3.amazonaws.com/{object_name}"

