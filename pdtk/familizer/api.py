r""" pdtk.familizer.api module """


# importing standard modules ==================================================
from typing import List
import logging


# importing third-party modules ===============================================
from requests import Session


# importing custom modules ====================================================
from ..concepts.patent_number import (
    PatentNumber
)
from .client import (
    FamilizerApiResponse,
    FamilizerClient
)


# module variables ============================================================
logger: logging.Logger = logging.getLogger(__name__)


# method definitions ==========================================================
def get_patent_families(
    patent_numbers: List[str | PatentNumber], 
    *args, 
    http_session: Session | None = None
) -> FamilizerApiResponse:
    r""" Module Method: Get Patent Families
    - arguments:
        - `patent_numbers`: a list of strings; representing patent numbers
    - returns:
        - an object of type `FamilizerApiResponse`
    """
    _formatted_patent_numbers: List[PatentNumber] = list()
    for given_arg in patent_numbers:
        if type(given_arg) is str:
            _formatted_patent_numbers.append(PatentNumber.parse_string(given_arg))
        elif type(given_arg) is PatentNumber:
            _formatted_patent_numbers.append(given_arg)
        else:
            incorrect_type_msg: str = \
                "{} is not of type 'str' or 'PatentNumber'".format(repr(given_arg))
            logger.warning(incorrect_type_msg)
            continue
    
    with FamilizerClient(http_session=http_session) as _client:
        return _client.get_family(_formatted_patent_numbers)
