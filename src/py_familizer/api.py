r""" py_familizer.api module """


# importing standard modules ==================================================
from typing import List, Union


# importing third-party modules ===============================================
from requests import Session


# importing custom modules ====================================================
from concepts.patent_number import (
    PatentNumber
)
from .client import (
    FamilizerApiResponse,
    FamilizerClient
)


# method definitions ==========================================================
def get_patent_families(
    patent_numbers: List[PatentNumber], 
    *args, 
    http_session: Union[Session, None] = None
) -> FamilizerApiResponse:
    r""" Module Method: Get Patent Families
    - arguments:
        - `patent_numbers`: a list of strings; representing patent numbers
    - returns:
        - an object of type `FamilizerApiResponse`
    """
    _client: FamilizerClient = FamilizerClient(http_session=http_session)
    return _client.get_family(patent_numbers)
