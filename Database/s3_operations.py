from Constants.credentials import Credentials
from Constants.parameters import Storage
import os
import boto3
import pandas as pd
from flask import jsonify
import io

s3_client = boto3.client('s3', aws_access_key_id=Credentials.aws_access_key_id,
                         aws_secret_access_key=Credentials.aws_secret_access_key)


def upload_to_s3(file_name, folder_name):
    s3_key = f'{folder_name}/{os.path.basename(file_name)}'
    s3_client.upload_file(file_name, Storage.s3_bucket, s3_key)


def read_from_s3(algorithm_name, result_type):
    s3_key = f'{algorithm_name}/{algorithm_name}_{result_type}_results.csv'
    response = s3_client.get_object(Bucket=Storage.s3_bucket, Key=s3_key)
    content = response['Body'].read().decode('utf-8')
    return content


def parse_csv_to_json(csv_content):
    csv_buffer = io.StringIO(csv_content)
    df = pd.read_csv(csv_buffer)
    df = df.where(pd.notnull(df), 0)
    return df.to_dict(orient='records')


def save_results_to_file(data, algorithm_name, result_type):
    file_name = f'/tmp/{algorithm_name}_{result_type}_results.csv'
    data.to_csv(file_name, index=False)
    upload_to_s3(file_name, algorithm_name)


def get_knives_results():
    plan_json = read_from_s3('knives_optimisation', 'planning_output')
    customer_json = read_from_s3('knives_optimisation', 'customer_output')

    customer_json = parse_csv_to_json(customer_json)
    plan_json = parse_csv_to_json(plan_json)

    return {'plan': plan_json, 'customer': customer_json}


def get_wastage_results():
    plan_json = read_from_s3('wastage_optimisation', 'planning_output')
    customer_json = read_from_s3('wastage_optimisation', 'customer_output')

    customer_json = parse_csv_to_json(customer_json)
    plan_json = parse_csv_to_json(plan_json)

    return {'plan': plan_json, 'customer': customer_json}
