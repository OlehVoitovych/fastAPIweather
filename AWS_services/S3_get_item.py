from Config import config
import json
import boto3

S3_BUCKET_NAME = config.BaseConfig.S3_BUCKET_NAME
AWS_REGION = config.BaseConfig.AWS_REGION
s3 = boto3.resource('s3')

file_key = ''

async def get_weather_from_s3():
    try:
        obj = s3.Object(S3_BUCKET_NAME, file_key)
        json_str =  obj.get()['Body'].read().decode('utf-8')
        json_str_with_quotes = '"{}"'.format(json_str)
        json_str_no_quotes = json_str_with_quotes[1:-1]
        json_obj = json.loads(json_str_no_quotes)
        return json_obj

    except s3.meta.client.exceptions.NoSuchKey:
        print(f"The file {file_key} does not exist in bucket {S3_BUCKET_NAME}.")
    except Exception as e:
        print(f"An error occurred: {e}")