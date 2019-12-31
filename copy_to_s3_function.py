import boto3
import os
from botocore.exceptions import ClientError


source_bucket = os.environ['SOURCE_BUCKET']
destination_bucket = os.environ['DESTINATION_BUCKET']
key_name = os.environ['KEY_NAME']


def copy_to_s3(event, context):
    try:
        s3 = boto3.client('s3')
        copy_source = {'Bucket': source_bucket, 'Key': key_name}
        s3.copy_object(Bucket=destination_bucket, Key=key_name, CopySource=copy_source)
    except ClientError as e:
        print(e)
