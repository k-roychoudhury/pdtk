r""" tests.google_patents.test_client module """


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


@pytest.mark.parametrize(
    "id_url",
    [
        "patent/US9145048B2/en"
    ]
)
def test_id_query(id_url: str, gp_client: GooglePatentsClient) -> None:
    content = gp_client.id_query(id_url)
    pp.pprint(content, width=150, compact=True)
    return None
