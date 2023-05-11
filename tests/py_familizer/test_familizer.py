r""" tests.py_familizer.test_familizer module """


# importing standard modules ==================================================
from typing import List
import pprint as pp


# importing third-party modules ===============================================
import pytest
from requests import Session


# importing custom modules ====================================================
from concepts import PatentNumber
from py_familizer import (
    FamilizerApiResponse,
    get_patent_families
)


# test methods ================================================================
@pytest.mark.parametrize(
    "patent_numbers", 
    [
        [   
            PatentNumber.construct(
                country_code="US", patent_number="9145048", kind_code="B2"
            ),
            PatentNumber.construct(
                country_code="JP", patent_number="2011213341", kind_code="A"
            )
        ]
    ]
)
def test_get_patent_families(
    patent_numbers: List[PatentNumber], 
    sync_client_session: Session
) -> None:
    result: FamilizerApiResponse = get_patent_families(
        patent_numbers, sync_client_session
    )
    pp.pprint(result.dict(), width=150, compact=True)
    return None
