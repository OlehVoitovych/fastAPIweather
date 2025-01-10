from Config import config
import json
import time
import boto3
import AWS_services.DDB_log

S3_BUCKET_NAME = config.BaseConfig.S3_BUCKET_NAME
AWS_REGION = config.BaseConfig.AWS_REGION

async def save_to_s3(data, ts):
    s3 = boto3.resource('s3')

    s3object = s3.Object(S3_BUCKET_NAME, f'{data["name"]}-{ts}.json')
    s3object.put(Body=(bytes(json.dumps(data).encode('UTF-8'))))

    url = f'https://{AWS_REGION}.console.aws.amazon.com/s3/object/{S3_BUCKET_NAME}?region={AWS_REGION}&bucketType=general&prefix={data["name"]}-{ts}.json'
    await AWS_services.DDB_log.save_to_ddb(data, url, ts)