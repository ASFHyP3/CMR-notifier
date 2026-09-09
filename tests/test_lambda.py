from datetime import UTC, datetime

import responses
from responses import matchers

from cmr_notifier import main
from cmr_notifier.main import NISAR_SHORTNAMES, SENTINEL1_SHORTNAMES


@responses.activate
def test_get_granule_records_updated_since(test_data_dir):
    short_names = SENTINEL1_SHORTNAMES + NISAR_SHORTNAMES
    params = {
        'provider': 'ASF',
        'short_name': short_names,
        'created_at': '2025-11-01T01:23:45+00:00,',
        'page_size': '2000',
    }
    resp1 = responses.get(
        url='https://cmr.earthdata.nasa.gov/search/granules.csv',
        match=[matchers.query_param_matcher(params)],
        body=(test_data_dir / 'cmr_response1.csv').read_text(),
        headers={'CMR-Search-After': 'foo'},
    )
    resp2 = responses.get(
        url='https://cmr.earthdata.nasa.gov/search/granules.csv',
        match=[
            matchers.query_param_matcher(params),
            matchers.header_matcher({'CMR-Search-After': 'foo'}),
        ],
        body=(test_data_dir / 'cmr_response2.csv').read_text(),
    )

    updated_since = datetime(2025, 11, 1, 1, 23, 45, tzinfo=UTC)
    results = main.get_granule_records_updated_since(updated_since, 'ASF', 'cmr.earthdata.nasa.gov', short_names)

    assert results == [
        (
            'S1C_WV_SLC__1SSV_20250328T085056_20250328T085537_001639_002A31_AE2A-SLC',
            [
                'https://datapool.asf.alaska.edu/SLC/SC/S1C_WV_SLC__1SSV_20250328T085056_20250328T085537_001639_002A31_AE2A.zip'
            ],
        ),
        (
            'S1C_IW_SLC__1SDV_20250328T121704_20250328T121731_001641_002A52_DF8B-SLC',
            [
                'https://datapool.asf.alaska.edu/SLC/SC/S1C_IW_SLC__1SDV_20250328T121704_20250328T121731_001641_002A52_DF8B.zip'
            ],
        ),
        (
            'S1C_IW_SLC__1SDV_20250328T150900_20250328T150928_001643_002A70_B8D0-SLC',
            [
                'https://datapool.asf.alaska.edu/SLC/SC/S1C_IW_SLC__1SDV_20250328T150900_20250328T150928_001643_002A70_B8D0.zip'
            ],
        ),
        (
            'NISAR_L1_PR_RSLC_004_076_A_022_2005_QPDH_A_20251103T110514_20251103T110549_X05007_N_F_J_001',
            [
                'https://datapool.asf.alaska.edu/NISAR/NISAR_L1_RSLC_V1/NISAR_L1_PR_RSLC_004_076_A_022_2005_QPDH_A_20251103T110514_20251103T110549_X05007_N_F_J_001/NISAR_L1_PR_RSLC_004_076_A_022_2005_QPDH_A_20251103T110514_20251103T110549_X05007_N_F_J_001.h5'
            ],
        ),
        (
            'NISAR_L2_PR_GUNW_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001',
            [
                'https://datapool.asf.alaska.edu/NISAR/NISAR_L2_GUNW_V1/NISAR_L2_PR_GUNW_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001/NISAR_L2_PR_GUNW_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001.h5'
            ],
        ),
        (
            'NISAR_L2_PR_GSLC_004_064_D_130_7700_SHNA_A_20251102T160804_20251102T160837_X05007_N_P_J_001',
            [
                'https://datapool.asf.alaska.edu/NISAR/NISAR_L2_GSLC_V1/NISAR_L2_PR_GSLC_004_064_D_130_7700_SHNA_A_20251102T160804_20251102T160837_X05007_N_P_J_001/NISAR_L2_PR_GSLC_004_064_D_130_7700_SHNA_A_20251102T160804_20251102T160837_X05007_N_P_J_001.h5'
            ],
        ),
        (
            'NISAR_L2_PR_GOFF_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001',
            [
                'https://datapool.asf.alaska.edu/NISAR/NISAR_L2_GOFF_V1/NISAR_L2_PR_GOFF_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001/NISAR_L2_PR_GOFF_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001.h5'
            ],
        ),
        (
            'NISAR_L1_PR_RUNW_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001',
            [
                'https://datapool.asf.alaska.edu/NISAR/NISAR_L1_RUNW_V1/NISAR_L1_PR_RUNW_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001/NISAR_L1_PR_RUNW_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001.h5'
            ],
        ),
        (
            'NISAR_L3_PR_SME2_008_007_D_073_4005_DHDH_A_20251216T164223_20251216T164300_X05007_N_F_J_001',
            [
                'https://datapool.asf.alaska.edu/NISAR/NISAR_L3_SME2_V1/NISAR_L3_PR_SME2_008_007_D_073_4005_DHDH_A_20251216T164223_20251216T164300_X05007_N_F_J_001/NISAR_L3_PR_SME2_008_007_D_073_4005_DHDH_A_20251216T164223_20251216T164300_X05007_N_F_J_001.h5'
            ],
        ),
        (
            'NISAR_L1_PR_ROFF_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001',
            [
                'https://datapool.asf.alaska.edu/NISAR/NISAR_L1_ROFF_V1/NISAR_L1_PR_ROFF_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001/NISAR_L1_PR_ROFF_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001.h5'
            ],
        ),
        (
            'NISAR_L1_PR_RIFG_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001',
            [
                'https://datapool.asf.alaska.edu/NISAR/NISAR_L1_RIFG_V1/NISAR_L1_PR_RIFG_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001/NISAR_L1_PR_RIFG_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001.h5'
            ],
        ),
        ('S1_301495_IW3_20141003T054235_VV_D5C8-BURST', []),
        ('S1_301495_IW3_20141003T054235_VH_D5C8-BURST', []),
        ('S1_301496_IW1_20141003T054236_VH_D5C8-BURST', []),
        ('NISAR_L1_PR_RSLC_004_076_A_022_2005_QPDH_A_20251103T110514_20251103T110549_X05007_N_F_J_001', []),
        (
            'NISAR_L2_PR_GUNW_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001',
            [],
        ),
        ('NISAR_L2_PR_GSLC_004_064_D_130_7700_SHNA_A_20251102T160804_20251102T160837_X05007_N_P_J_001', []),
        (
            'NISAR_L2_PR_GOFF_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001',
            [],
        ),
        (
            'NISAR_L1_PR_RUNW_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001',
            [],
        ),
        ('NISAR_L3_PR_SME2_008_007_D_073_4005_DHDH_A_20251216T164223_20251216T164300_X05007_N_F_J_001', []),
        (
            'NISAR_L1_PR_ROFF_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001',
            [],
        ),
        (
            'NISAR_L1_PR_RIFG_003_064_D_130_004_7700_SH_20251021T160803_20251021T160836_20251102T160804_20251102T160837_X05007_N_P_J_001',
            [],
        ),
    ]

    assert resp1.call_count == 1
    assert resp2.call_count == 1


def test_send_notification(sns_stubber):
    sns_stubber.add_response(
        method='publish',
        expected_params={
            'TopicArn': 'myTopic',
            'Message': '{"granule_ur": "foo", "metadata_url": "fizz.buzz?granule_ur=foo", "access_urls": ["bar"]}',
        },
        service_response={},
    )

    message = {
        'granule_ur': 'foo',
        'metadata_url': 'fizz.buzz?granule_ur=foo',
        'access_urls': ['bar'],
    }

    main.send_notification('myTopic', message)


def test_construct_metadata_url():
    assert (
        main.construct_metadata_url('foo', 'ASF', 'cmr.earthdata.nasa.gov')
        == 'https://cmr.earthdata.nasa.gov/search/granules.umm_json?provider=ASF&granule_ur=foo'
    )

    assert (
        main.construct_metadata_url('fizz:buzz/3', 'FOO BAR', 'cmr.earthdata.nasa.gov')
        == 'https://cmr.earthdata.nasa.gov/search/granules.umm_json?provider=FOO%20BAR&granule_ur=fizz%3Abuzz%2F3'
    )


def test_already_exists(db_stubber):
    db_stubber.add_response(
        method='get_item',
        expected_params={
            'TableName': 'myTable',
            'Key': {'granule_ur': 'foo'},
        },
        service_response={},
    )
    assert not main.already_exists('myTable', 'foo')

    db_stubber.add_response(
        method='get_item',
        expected_params={
            'TableName': 'myOtherTable',
            'Key': {'granule_ur': 'bar'},
        },
        service_response={'Item': {}},
    )
    assert main.already_exists('myOtherTable', 'bar')


def test_put_item(db_stubber):
    db_stubber.add_response(
        method='put_item',
        expected_params={
            'TableName': 'myTable',
            'Item': {'granule_ur': 'foo', 'sent_at': 'now'},
        },
        service_response={},
    )
    main.put_item('myTable', 'foo', sent_at='now')
