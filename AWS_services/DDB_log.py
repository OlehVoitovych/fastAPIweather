import boto3
import uuid

async def save_to_ddb(data, url, ts):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('api_logs')
    table.put_item(
        Item={
            'id': str(uuid.uuid4()),
            'city': data['name'],
            'timestamp': str(ts),
            'url_to_s3': url
        }
    )