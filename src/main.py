import datetime
import json
import os

import boto3
import requests


sns = boto3.client('sns')
table = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])


def already_exists(granule: str) -> bool:
    response = table.get_item(Key={'granule_ur': granule})
    return 'Item' in response


def put_item(granule: str) -> None:
    table.put_item(Item={'granule_ur': granule})


def get_granules_updated_since(updated_since: datetime.datetime) -> list[str]:
    session = requests.Session()
    url = 'https://cmr.earthdata.nasa.gov/search/granules.csv'
    params = {
        'provider': 'ASF',
        'short_name': [
            'SENTINEL-1A_SLC',
            'SENTINEL-1B_SLC',
            'SENTINEL-1C_SLC',
            'SENTINEL-1_BURSTS',
        ],
        'created_at': f'{updated_since.isoformat()},',
        'page_size': '2000',
    }
    headers: dict = {}
    granules: list = []
    while True:
        response = session.get(url, params=params, headers=headers)
        response.raise_for_status()
        items = response.text.splitlines()[1:]
        granules.extend([item.split(',')[0] for item in items])

        if 'CMR-Search-After' not in response.headers:
            break
        headers['CMR-Search-After'] = response.headers['CMR-Search-After']
    return granules


def send_notification(topic_arn: str, granule: str) -> None:
    message = {
        'granule-ur': granule,
    }
    sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message),
    )


def send_notifications(topic_arn: str, window_in_seconds: int) -> None:
    updated_since = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(seconds=window_in_seconds)
    granules = get_granules_updated_since(updated_since)
    for granule in granules:
        if not already_exists(granule):
            send_notification(topic_arn, granule)
            put_item(granule)


def lambda_handler(event: dict, context: dict) -> None:
    send_notifications(os.environ['TOPIC_ARN'], int(os.environ['WINDOW_IN_SECONDS']))
