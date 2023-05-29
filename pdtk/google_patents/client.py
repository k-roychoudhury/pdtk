r""" pdtk.google_patents.client module """


# importing standard modules ==================================================
from typing import (
    Self, 
    Dict,
    Any
)
import logging
from urllib.parse import (
    quote, 
    urlencode
)


# importing third-party modules ===============================================
from requests import (
    Session,
    Response,
    HTTPError
)


# importing custom modules ====================================================
from ..concepts.patent_number import PatentNumber
from ..config import BASE_URL_GOOGLE_PATENTS
from ..globals import get_http_session
from .models import (
    GoogleParseResponse,
    GoogleRawPatent
)


# module variables ============================================================
logger: logging.Logger = logging.getLogger(__name__)


# class definitions ===========================================================
class SyncClient(object):


    def __init__(
        self,
        *args,
        http_session: Session | None = None
    ):
        self._session: Session = get_http_session() \
            if http_session is None else http_session


    def __enter__(self) -> Self:
        return self


    def __exit__(self, exc_type, exc_val, exc_tb) -> Self:
        return self
    

    def __get_parse_response__(
        self,
        query_string: str
    ) -> Response:
        r""" Instance Private Method: Get Parse Response 
        - arguments:
            - `query_string`: a string; representing a user query
        - returns:
            - an object of type `requests.Response`
        - raises:
            - `ConnectionError`
            - `HTTPError`
        - notes:
            - sends a GET request to remote application server for search results.
        """
        params: Dict[str, Any] = {
            "text": query_string, "cursor": len(query_string), "exp": ""
        }
        uri: str = "{}/parse".format(BASE_URL_GOOGLE_PATENTS)

        try:
            response: Response = self._session.get(
                uri, params=urlencode(params, safe="()", quote_via=quote)
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


    def __get_result_response__(
        self, 
        id_url: str
    ) -> Response:
        r""" Instance Private Method: Get Result Response 
        - arguments:
            - `id_url`: a string representing a Google patent URL
                - example: 'patent/US9145048B2/en'
        - returns:
            - an object of type `requests.Response`
        - raises:
            - `ConnectionError`
            - `HTTPError`
        - notes:
            - sends a GET request to remote application server for search results.
        """
        params: Dict[str, str] = { "id": id_url }
        uri: str = "{}/result".format(BASE_URL_GOOGLE_PATENTS)

        try:
            response: Response = self._session.get(
                uri, params=params, allow_redirects=False
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


    def generate_id_url(
        self, 
        patent_number: str | PatentNumber, 
        lang_code: str = "en"
    ) -> str:
        r""" Instance Method: Generate Id Url
        - arguments:
            - `patent_number`: an object of type `str` or `PatentNumber`
            - `lang_code`: a string specifuing an ISO language code
                - default: 'en'
        - returns:
            - a string; representing a google patents id url
        - raises:
            - `TypeError`
        """
        if type(patent_number) not in (str, PatentNumber):
            type_error_msg: str = \
                "expected type 'str' or 'PatentNumber', got '{}'".format(
                    patent_number.__class__.__name__
            )
            raise TypeError(type_error_msg)

        __patent_number_object: PatentNumber = patent_number
        if type(patent_number) is str:
            __patent_number_object = PatentNumber.parse_string(patent_number)
        
        id_url: str = "/patent/{}/{}".format(
            __patent_number_object.to_string(
                format="{country_code}{patent_number}{kind_code}"
            ).strip(),
            lang_code.strip().lower()
        )
        return id_url
    

    # -------------------------------------------------------------------------
    def text_query(self, query: str) -> GoogleParseResponse:
        r""" Instance Method: Text Query
        - arguments:
            - `query_string`: a string; representing a user query 
        - returns:
            - an object of type `GoogleParseResponse`
        - raises:
            - `ConnectionError`
            - `HTTPError`
        """
        parse_response: Response = self.__get_parse_response__(query)
        parsed_object: GoogleParseResponse = GoogleParseResponse.parse_raw(
            parse_response.content
        )
        return parsed_object


    def id_query(self, patent_number: str | PatentNumber) -> GoogleRawPatent:
        r""" Instance Method: Id Query
        - arguments:
            - `patent_number`: an object of type `str` or `PatentNumber`
        - returns:
            - an object of type `GoogleRawPatent`
        - raises:
            - `ConnectionError`
            - `HTTPError`
        """
        id_url: str = self.generate_id_url(patent_number, lang_code="en")
        result_response: Response = self.__get_result_response__(id_url)
        parsed_patent_content: GoogleRawPatent = GoogleRawPatent.\
            parse_bytes_content(result_response.content)
        
        return parsed_patent_content


    pass  # end of SyncClient


class GooglePatentsClient(SyncClient):
    r""" Class implementing methods to interface with """
    pass # end of GooglePatentsClient
