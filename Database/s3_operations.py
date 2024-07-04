from Constants.credentials import Credentials
from Constants.parameters import Storage
import os
import boto3
import pandas as pd
import io

s3_client = boto3.client('s3', aws_access_key_id=Credentials.aws_access_key_id,
                         aws_secret_access_key=Credentials.aws_secret_access_key)


def upload_to_s3(file_name, folder_name):
    s3_key = f'{folder_name}/{os.path.basename(file_name)}'
    s3_client.upload_file(file_name, Storage.s3_bucket, s3_key)

def read_from_s3(client_name, product_name, product_type, algorithm_name, result_type):
    s3_key = f'{client_name}/{product_name}/{product_type}/{algorithm_name}/{algorithm_name}_{result_type}_results.csv'
    response = s3_client.get_object(Bucket=Storage.s3_bucket, Key=s3_key)
    content = response['Body'].read().decode('utf-8')
    return content


def parse_csv_to_json(csv_content):
    csv_buffer = io.StringIO(csv_content)
    df = pd.read_csv(csv_buffer)
    df = df.where(pd.notnull(df), 0)
    return df.to_dict(orient='records')


def save_results_to_file(client_metadata, data, algorithm_name, result_type):
    client_name = client_metadata['client_name']
    product_type = client_metadata['order_config'][0]
    product_config = str(client_metadata['order_config'][1]) + '_' + str(
        client_metadata['order_config'][2]) + '_' + str(client_metadata['order_config'][3])
    folder_path = client_name + '/' + product_type + '/' + product_config + '/' + algorithm_name
    file_name = f'/tmp/{algorithm_name}_{result_type}_results.csv'
    data.to_csv(file_name, index=False)
    upload_to_s3(file_name, folder_path)


def get_knives_results(client_name, product_name, product_type):
    plan_json = read_from_s3(client_name, product_name, product_type, 'knives_optimisation', 'planning_output')
    customer_json = read_from_s3(client_name, product_name, product_type, 'knives_optimisation', 'customer_output')
    metric_json = read_from_s3(client_name, product_name, product_type, 'knives_optimisation', 'metrics_output')

    customer_json = parse_csv_to_json(customer_json)
    plan_json = parse_csv_to_json(plan_json)
    metric_json = parse_csv_to_json(metric_json)

    return {'plan': plan_json, 'customer': customer_json, 'metric': metric_json}


def get_wastage_results(client_name, product_name, product_type):
    plan_json = read_from_s3(client_name, product_name, product_type, 'wastage_optimisation', 'planning_output')
    customer_json = read_from_s3(client_name, product_name, product_type, 'wastage_optimisation', 'customer_output')
    metric_json = read_from_s3(client_name, product_name, product_type, 'wastage_optimisation', 'metrics_output')

    customer_json = parse_csv_to_json(customer_json)
    plan_json = parse_csv_to_json(plan_json)
    metric_json = parse_csv_to_json(metric_json)

    return {'plan': plan_json, 'customer': customer_json, 'metric': metric_json}
