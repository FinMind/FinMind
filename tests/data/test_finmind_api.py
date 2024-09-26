import os

import pytest

from FinMind.data import FinMindApi


@pytest.fixture(scope="module")
def api():
    token = os.environ.get("FINMIND_API_TOKEN", "")
    api = FinMindApi()
    api.login_by_token(token)
    return api


def test_api_usage(api):
    assert isinstance(api.api_usage, int)
