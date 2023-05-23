r""" tests.google_patents.test_client module """


# importing standard modules ==================================================
import pprint as pp


# importing third-party modules ===============================================
import pytest


# importing custom modules ====================================================
from pdtk.concepts.patent_number import PatentNumber
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
def test_text_query(
    sample_text: str, 
    gp_client: GooglePatentsClient
) -> None:
    parse_resp: GoogleParseResponse = gp_client.text_query(sample_text)
    pp.pprint(parse_resp.dict(), width=150, compact=True)
    return None


@pytest.mark.parametrize(
    "patent_numbers", 
    [
        PatentNumber(
            country_code="US", patent_number="9145048", kind_code="B2"
        ),
        PatentNumber(
            country_code="JP", patent_number="2011213341", kind_code="A"
        ),
        "WO1999006665A1",
        "CN102205844B",
        "EP2371646B1",
        "ES2655892T3",
        "JP6389025B2",
        "US-6179873-B1"
    ]
)
def test_id_query(
    patent_numbers: PatentNumber, 
    gp_client: GooglePatentsClient
) -> None:
    content = gp_client.id_query(patent_numbers)
    pp.pprint(content.dict(), width=150, compact=True)
    return None
