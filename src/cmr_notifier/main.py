import datetime
import json
import os
import urllib.parse

import boto3
import requests


sns = boto3.client('sns')
db = boto3.resource('dynamodb')


def already_exists(table_name: str, granule: str) -> bool:
    response = db.Table(table_name).get_item(Key={'granule_ur': granule})
    return 'Item' in response


def put_item(table_name: str, granule: str) -> None:
    db.Table(table_name).put_item(Item={'granule_ur': granule})


def get_granule_records_updated_since(
    updated_since: datetime.datetime, cmr_provider: str, cmr_domain_name: str
) -> list[tuple[str, list]]:
    session = requests.Session()

    url = f'https://{cmr_domain_name}/search/granules.csv'

    params = {
        'provider': cmr_provider,
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


def construct_metadata_url(granule_ur: str, cmr_provider: str, cmr_domain_name: str) -> str:
    query_params = urllib.parse.urlencode(
        {'provider': cmr_provider, 'granule_ur': granule_ur}, quote_via=urllib.parse.quote
    )
    return f'https://{cmr_domain_name}/search/granules.umm_json?{query_params}'


def send_notifications(
    topic_arn: str, table_name: str, window_in_seconds: int, cmr_provider: str, cmr_domain_name: str
) -> None:
    updated_since = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(seconds=window_in_seconds)
    records = get_granule_records_updated_since(updated_since, cmr_provider, cmr_domain_name)

    for granule_ur, access_urls in records:
        metadata_url = construct_metadata_url(granule_ur, cmr_provider, cmr_domain_name)
        message = {
            'granule_ur': granule_ur,
            'metadata_url': metadata_url,
            'access_urls': access_urls,
        }

        if not already_exists(table_name, granule_ur):
            send_notification(topic_arn, message)
            put_item(table_name, granule_ur)


def lambda_handler(event: dict, context: dict) -> None:
    send_notifications(
        topic_arn=os.environ['TOPIC_ARN'],
        table_name=os.environ['TABLE_NAME'],
        window_in_seconds=event['window_in_seconds'],
        cmr_provider=os.environ['CMR_PROVIDER'],
        cmr_domain_name=os.environ['CMR_DOMAIN_NAME'],
    )
