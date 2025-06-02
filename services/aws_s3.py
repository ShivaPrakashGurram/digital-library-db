import boto3
import os

s3 = boto3.client(
    's3',
    aws_access_key_id="AKIA3UA3D5CMZMJ2HYMQ",
    aws_secret_access_key="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",
)

async def upload_file_to_s3(file, bucket, object_name):
    s3.upload_fileobj(file.file, bucket, object_name)
    return f"https://{bucket}.s3.amazonaws.com/{object_name}"

