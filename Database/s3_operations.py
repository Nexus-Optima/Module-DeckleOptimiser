from Constants.credentials import Credentials
from Constants.parameters import Storage
import os
import boto3

s3_client = boto3.client('s3', aws_access_key_id=Credentials.aws_access_key_id,
                         aws_secret_access_key=Credentials.aws_secret_access_key)


def upload_to_s3(file_name, folder_name):
    s3_key = f'{folder_name}/{os.path.basename(file_name)}'
    s3_client.upload_file(file_name, Storage.s3_bucket, s3_key)


def save_results_to_file(data, algorithm_name, result_type):
    file_name = f'/tmp/{algorithm_name}_{result_type}_results.csv'
    data.to_csv(file_name, index=False)
    upload_to_s3(file_name, algorithm_name)
