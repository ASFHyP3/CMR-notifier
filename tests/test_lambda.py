from datetime import datetime

import responses
from responses import matchers

import cmr_notifier


@responses.activate
def test_get_granules_updated_since(test_data_dir):
    params = {
        'provider': 'ASF',
        'short_name': [
            'SENTINEL-1A_SLC',
            'SENTINEL-1B_SLC',
            'SENTINEL-1C_SLC',
            'SENTINEL-1_BURSTS',
        ],
        'created_at': '2025-11-07T01:23:45,',
        'page_size': '2000',
    }
    resp1 = responses.get(
        url='https://cmr.earthdata.nasa.gov/search/granules.csv',
        match=[matchers.query_param_matcher(params)],
        body=(test_data_dir / 'cmr_response1.csv').read_text(),
        headers={'CMR-Search-After': 'foo'}
    )

    resp2 = responses.get(
        url='https://cmr.earthdata.nasa.gov/search/granules.csv',
        match=[
            matchers.query_param_matcher(params),
            matchers.header_matcher({'CMR-Search-After': 'foo'})
        ],
        body=(test_data_dir / 'cmr_response2.csv').read_text(),
    )

    updated_since = datetime(2025, 11, 7, 1, 23, 45)
    assert cmr_notifier.main.get_granules_updated_since(updated_since) == [
        'S1C_WV_SLC__1SSV_20250328T085056_20250328T085537_001639_002A31_AE2A-SLC',
        'S1C_IW_SLC__1SDV_20250328T121704_20250328T121731_001641_002A52_DF8B-SLC',
        'S1C_IW_SLC__1SDV_20250328T150900_20250328T150928_001643_002A70_B8D0-SLC',
        'S1_301495_IW3_20141003T054235_VV_D5C8-BURST',
        'S1_301495_IW3_20141003T054235_VH_D5C8-BURST',
        'S1_301496_IW1_20141003T054236_VH_D5C8-BURST',
    ]

    assert resp1.call_count == 1
    assert resp2.call_count == 1
