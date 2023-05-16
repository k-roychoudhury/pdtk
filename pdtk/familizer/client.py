r""" pdtk.familizer.client module """


# importing standard modules ==================================================
from typing import List, Dict, Union
import logging


# importing third-party modules ===============================================
from requests import (
    Session,
    Response,
    ConnectionError,
    HTTPError
)


# importing custom modules ====================================================
from ..concepts.patent_number import (
    PatentNumber
)
from ..config import (
    BASE_URL_FAMILIZER
)
from .models import (
    FamilizerApiResponse
)


# module variables ============================================================
logger: logging.Logger = logging.getLogger(__name__)
module_http_session: Session = Session()


# class definitions ===========================================================
class FamilizerClient(object):
    r""" client object to interface with 
        ### Blazing Dawn Software's Family-izer
    """


    def __init__(
        self, 
        *args, 
        http_session: Union[Session, None] = None
    ) -> None:
        self._session: Session = module_http_session \
            if http_session is None else http_session
        pass


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
    

    def __get_familizer_response__(
        self,
        patent_numbers: List[PatentNumber]
    ) -> Response:
        r""" Instance Private Method: Get Familizer Response 
        - arguments:
            - `patent_numbers`: a list of strings; representing patent numbers
            - `http_session`: an object of type `requests.Session`
        - raises:
            - `ConnectionError`
            - `HTTPError`
        - returns:
            - an object of type `requests.Response`
        - notes:
            - sends a POST request to remote application server for family data.
            - expects the patent numbers passed in the list to be without their 
            kind codes.
        """
        payload: Dict[str, str] = {
            "patno": "\n".join(map(
                lambda item: item.to_string(format="{country_code}{patent_number}"), 
                patent_numbers
            ))
        }
        headers: Dict[str, str] = {
            "content-type": "application/x-www-form-urlencoded",
            "accept-encoding": "gzip, deflate, br",
            "origin": "https://www.familyizer.com",
            "referer": "https://www.familyizer.com/index.html"
        }

        try:
            response: Response = self._session.post(
                BASE_URL_FAMILIZER, data=payload, headers=headers
            )
            response.raise_for_status()

        except ConnectionError as connection_error:
            logger.error(connection_error, exc_info=True)
            raise
            
        
        except HTTPError as http_error:
            logger.error(http_error, exc_info=True)
            raise

        else:
            return response

    
    def get_family(
        self, 
        patent_numbers: List[PatentNumber]
    ) -> FamilizerApiResponse:
        r""" Instance Method: Get Family
        - arguments:
            - `patent_numbers`: a list of strings; representing patent numbers
        - keyword arguments:
            - `http_session`: an object of type `requests.Session`
                - if `None`, uses the internal module `Session` object
        - returns:
            - an object of type `FamilizerApiResponse`
        - notes:
            - sends a POST request to remote application server for family data.
            - expects the patent numbers passed in the list to be without their 
            kind codes.
        """
        
        response: Response = self.__get_familizer_response__(
            patent_numbers
        )

        return FamilizerApiResponse.parse_familizer_response_content(
            response.content
        )


    pass # end of FamilizerClient
