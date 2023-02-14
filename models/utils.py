import os
import logging
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv


load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")
REGION = os.getenv("REGION")


def get_s3_presigned_url(key):
    s3_client = boto3.client('s3', region_name=REGION)
    action = 'get_object'
    params = { 
        'Bucket': BUCKET_NAME,
        'Key': key,
    }
    expire=3600
    return s3_client.generate_presigned_url(ClientMethod=action, Params=params, ExpiresIn=expire)


def upload_file(file_name, object_key):
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, BUCKET_NAME, object_key)
    except ClientError as e:
        logging.error(e)