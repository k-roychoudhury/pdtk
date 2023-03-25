r""" py_google_patents.api_client module """

from typing import Self
import logging

from requests import (
    Session as RequestsSession,
    Response as RequestsResponse,
    HTTPError as RequestsHTTPError
)

from .config import get_module_logger
from .models import (
    GoogleParseResponse
)
from .utils.network import (
    get_parse_response
)

# module variables ============================================================
logger: logging.Logger = get_module_logger().getChild(__name__)


# class definitions ===========================================================
class ApiSyncClient(object):


    def __init__(self):
        self._blocking_session: RequestsSession = RequestsSession()


    def __del__(self):
        self._blocking_session.close()


    def __enter__(self) -> Self:
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self._blocking_session.close()


    def __aenter__(self):
        raise NotImplementedError("not intended to be used in an async context")


    def text_query(self, query: str) -> GoogleParseResponse:
        parse_response: RequestsResponse = get_parse_response(
            query, self._blocking_session
        )
        try:
            parse_response.raise_for_status()
        except RequestsHTTPError as http_error:
            logger.error(http_error, exc_info=(logger.level == logging.DEBUG))
            raise
        else:
            parse_object: GoogleParseResponse = GoogleParseResponse.parse_raw(
                parse_response.content
            )
            return parse_object


    pass  # end of ApiSyncClient
