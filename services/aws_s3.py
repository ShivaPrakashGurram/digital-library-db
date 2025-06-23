from http.client import HTTPException
from botocore.exceptions import ClientError
import boto3
import os

s3 = boto3.client(
    's3',
    region_name=str(os.getenv("aws_region")),
    aws_access_key_id=str(os.getenv("aws_accesskey")),
    aws_secret_access_key=str(os.getenv("aws_secretkey")),
    
)

async def upload_file_to_s3(file, bucket, object_name):
    s3.upload_fileobj(file.file, bucket, object_name)
    return f"https://{bucket}.s3.amazonaws.com/{object_name}"

def generate_presigned_url(bucket_name: str, object_key: str, expiration=3600):
    try:
        presigned_url =s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration  # URL expires in 1 hour
        )
        return {"download_url": presigned_url}

    except ClientError as e:
        raise HTTPException(status_code=404, detail=str(e))