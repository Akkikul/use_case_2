import boto3
import logging
import os
import zipfile
from botocore.exceptions import ClientError
from use_case_2.create_stack import create

region = 'eu-west-1'
host_bucket = 'use-case-2-31122019-host'
source_bucket = 'use-case-2-31122019-source'
stack_name = 'use-case-2'
template_name = 'use-case-2.yaml'
template_url = f"https://{host_bucket}.s3.{region}.amazonaws.com/{template_name}"
parameters = [dict(ParameterKey="HostBucket", ParameterValue=host_bucket),
              dict(ParameterKey="SourceBucket", ParameterValue=source_bucket)]
s3_client = boto3.client('s3', region_name=region)


def execute_script():
    try:
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=host_bucket, CreateBucketConfiguration=location)
        s3_client.upload_file(template_name, host_bucket, template_name)
        upload_zip(host_bucket, "copy_to_s3_function.py", "copy_to_s3_function.zip")
        return True
    except ClientError as e:
        logging.error(e)
        return False


def upload_zip(bucket_name, input_filename, output_filename):
    zip_file = zipfile.ZipFile(output_filename, "w")
    zip_file.write(input_filename, os.path.basename(input_filename))
    zip_file.close()
    s3_client.upload_file(output_filename, bucket_name, output_filename)
    os.remove(output_filename)


if __name__ == "__main__":
    response = execute_script()
    if response:
        create(stack_name, template_url, parameters)
    else:
        print('Stack Creation Failed')
