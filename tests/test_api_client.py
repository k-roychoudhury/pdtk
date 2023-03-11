r""" tests.test_api_client module """

import pprint as pp

import pytest

from py_google_patents.models import GoogleParseResponse
from py_google_patents.api_client import ApiSyncClient


# fixture definitions =========================================================
@pytest.fixture
def gp_client() -> ApiSyncClient:
    with ApiSyncClient() as sync_client:
        yield sync_client


@pytest.mark.parametrize(
    "sample_text",
    [
        "hybrid engine",
        "US9145048",
        "213123xvds325341",
        "US9567832 hybrid"
    ]
)
def test_text_query(sample_text: str, gp_client: ApiSyncClient) -> None:
    parse_resp: GoogleParseResponse = gp_client.text_query(sample_text)
    pp.pprint(parse_resp.dict(), width=150, compact=True)
    return None
