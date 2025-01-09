from Creds import S3_BUCKET_NAME, AWS_REGION
import json
import time
import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid


file_key = ''

async def save_to_ddb(data, url, ts):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('api_logs5')
    table.put_item(
        Item={
            'id': str(uuid.uuid4()),
            'city': data['name'],
            'timestamp': str(ts),
            'url_to_s3': url
        }
    )

async def save_to_s3(data, ts):
    s3 = boto3.resource('s3')
    ts = int(round(time.time()))

    s3object = s3.Object(S3_BUCKET_NAME, f'{data["name"]}-{ts}.json')
    s3object.put(Body=(bytes(json.dumps(data).encode('UTF-8'))))

    url = f'https://{AWS_REGION}.console.aws.amazon.com/s3/object/{S3_BUCKET_NAME}?region={AWS_REGION}&bucketType=general&prefix={data["name"]}-{ts}.json'
    await save_to_ddb(data, url, ts)


async def five_minute_check(ts, city):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('api_logs5')
    five_minutes_ago = str(ts - 300)

    response = table.scan(
        FilterExpression=Attr('timestamp').gt(five_minutes_ago) & Attr('city').eq(city)
    )

    items = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=Attr('timestamp').gt(five_minutes_ago),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response['Items'])

    if len(response['Items']) == 0:
        return False
    else:
        global file_key
        url = response['Items'][0].get('url_to_s3')
        start = url.find("prefix=") + 7
        file_key = url[start:]
        return True

async def get_weather_from_s3():
    s3 = boto3.resource('s3')

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