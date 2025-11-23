import os

import pytest

from FinMind.data import FinMindApi


@pytest.fixture(scope="module")
def api():
    token = os.environ.get("FINMIND_API_TOKEN", "")
    api = FinMindApi(token=token)
    return api


def test_api_usage(api):
    assert isinstance(api.api_usage, int)


def test_api_usage_limit(api):
    assert isinstance(api.api_usage_limit, int)
