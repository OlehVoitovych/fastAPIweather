import boto3
from boto3.dynamodb.conditions import Attr
import AWS_services.S3_get_item

async def five_minute_check(ts, city):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('api_logs')
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
        url = response['Items'][0].get('url_to_s3')
        start = url.find("prefix=") + 7
        AWS_services.S3_get_item.file_key = url[start:]
        return True

