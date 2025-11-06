"""Script to set up a CMR ingest subscription."""

import argparse
import json
import os
from pathlib import Path

import requests


# TODO:
#  - inject SQS ARN into umm-sub instead of hard coding?
#  - inject earthdata username into umm-sub instead of hard coding?
#  - validate umm-sub with json schema?
def post_subscription(umm_sub_path: Path, token: str) -> None:
    """Create a CMR ingest subscription."""
    umm_sub = json.loads(umm_sub_path.read_text())

    url = f'https://cmr.earthdata.nasa.gov/search/subscriptions/{umm_sub_path.stem}'
    headers = {
        'Content-Type': 'application/vnd.nasa.cmr.umm+json',
        'Authorization': f'Bearer {token}',
    }
    response = requests.post(url, json=umm_sub, headers=headers)
    response.raise_for_status()
    print(response.text)


# TODO: Confirm subscription
#  - poll SQS for confirmation message
#  - "visit" (GET) "SubscribeURL" from confirmation message
#  - delete message from queue
def confirm_subscription() -> None:
    """Confirm a CMR ingest subscription."""
    pass


def main() -> None:
    """Set up a CMR ingest subscription."""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)
    parser.add_argument('umm_sub', help='UMM-Sub JSON file to submit')

    args = parser.parse_args()

    token = os.environ.get('EARTHDATA_TOKEN')
    if token is None:
        raise ValueError('EARTHDATA_TOKEN environment variable must be set.')

    post_subscription(args.umm_sub, token)


if __name__ == '__main__':
    main()
