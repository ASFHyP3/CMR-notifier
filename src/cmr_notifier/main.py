import datetime
import json
import os

import boto3
import requests


sns = boto3.client('sns')
db = boto3.resource('dynamodb')


def already_exists(table_name: str, granule: str) -> bool:
    response = db.Table(table_name).get_item(Key={'granule_ur': granule})
    return 'Item' in response


def put_item(table_name: str, granule: str) -> None:
    db.Table(table_name).put_item(Item={'granule_ur': granule})


def get_granule_records_updated_since(updated_since: datetime.datetime) -> list[tuple[str, list]]:
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
        for item in response.text.splitlines()[1:]:
            granule_ur, _, _, _, access, _, _, _, _ = item.split(',')
            access_urls: list = access.split(',') if access else []
            granules.append((granule_ur, access_urls))

        if 'CMR-Search-After' not in response.headers:
            break
        headers['CMR-Search-After'] = response.headers['CMR-Search-After']
    return granules


def send_notification(topic_arn: str, message: dict) -> None:
    sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message),
    )


def send_notifications(topic_arn: str, table_name: str, window_in_seconds: int) -> None:
    updated_since = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(seconds=window_in_seconds)
    records = get_granule_records_updated_since(updated_since)

    for granule_ur, access_urls in records:
        message = {
            'granule_ur': granule_ur,
            'access_urls': access_urls,
        }

        if not already_exists(table_name, granule_ur):
            send_notification(topic_arn, message)
            put_item(table_name, granule_ur)


def lambda_handler(event: dict, context: dict) -> None:
    send_notifications(os.environ['TOPIC_ARN'], os.environ['TABLE_NAME'], event['window_in_seconds'])
