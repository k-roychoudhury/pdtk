r""" tests.test_api_client module """


# importing standard modules ==================================================
import pprint as pp


# importing third-party modules ===============================================
import pytest


# importing custom modules ====================================================
from pdtk.google_patents.models import GoogleParseResponse
from pdtk.google_patents.client import GooglePatentsClient


# fixture definitions =========================================================
@pytest.mark.parametrize(
    "sample_text",
    [
        "hybrid engine",
        "US9145048",
        "213123xvds325341",
        "US9567832 hybrid"
    ]
)
def test_text_query(sample_text: str, gp_client: GooglePatentsClient) -> None:
    parse_resp: GoogleParseResponse = gp_client.text_query(sample_text)
    pp.pprint(parse_resp.dict(), width=150, compact=True)
    return None
