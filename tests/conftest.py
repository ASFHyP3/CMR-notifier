import os
from pathlib import Path

import pytest
from botocore.stub import Stubber
from cmr_notifier.main import sns, db


@pytest.fixture
def test_data_dir():
    here = Path(os.path.dirname(__file__))
    return here / 'data'


@pytest.fixture()
def sns_stubber():
    with Stubber(sns) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


@pytest.fixture()
def db_stubber():
    with Stubber(db.meta.client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()
