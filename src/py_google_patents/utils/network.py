r""" py_google_patents.utils.network module """

import logging
from typing import Dict
from urllib.parse import quote, urlencode

from requests import (
    Session as RequestsSession,
    Response as RequestsResponse,
    ConnectionError as RequestsConnectionError
)

from ..config import get_module_logger

# module variables ============================================================
logger: logging.Logger = get_module_logger().getChild(__name__)
google_patents_api_base_url: str = "https://patents.google.com/xhr"


# method definitions ==========================================================
def build_result_by_id_url(id_url: str) -> str:
    r"""
    Method: Build Result By Id Url
    - arguments:
        - `id_url`: a string representing a Google patent URL
        example: 'patent/US9145048B2/en'
    - returns:
        - a URL string
    """
    params: Dict[str, str] = {"id": id_url}
    url: str = "{}/result?{}".format(
        google_patents_api_base_url, urlencode(params, safe="", quote_via=quote)
    )
    logger.debug("constructed result id url: '{}'".format(url))
    return url


def build_parse_by_text_url(text: str) -> str:
    r"""
    Method: Build Parse By Text Url
    - arguments:
        - `text`: strings input in the Google patents search box
    - returns:
        - a URL string
    """
    params: Dict[str, str] = {
        "text": text, "cursor": len(text), "exp": ""
    }
    url: str = "{}/parse?{}".format(
        google_patents_api_base_url, urlencode(params, safe="()", quote_via=quote)
    )
    logger.debug("constructed parse text url: '{}'".format(url))
    return url


def get_result_response(
        id_url: str, blocking_session: RequestsSession | None = None
) -> RequestsResponse:
    r"""
    Method - Get Result Response
    - arguments:
        - `id_url`: a string representing a Google patent URL
            - example: 'patent/US9145048B2/en'
    - keyword arguments:
        - `blocking_session`: an object of type `requests.Session` or None
    - returns:
        - an object of type `requests.Response`
    - raises:
        - `requests.ConnectionError`
    - notes:
        - uses the `requests.Session` object to make a blocking http call or
        creates one if the `blocking_session` keyword argument is None
    """
    url: str = build_result_by_id_url(id_url)
    if blocking_session is None:
        blocking_session = RequestsSession()
    try:
        response: RequestsResponse = blocking_session.get(url, allow_redirects=False)
    except RequestsConnectionError as connection_error:
        logger.critical(connection_error, exc_info=(logger.level == logging.DEBUG))
        raise
    else:
        return response
    finally:
        blocking_session.close()


def get_parse_response(
    text: str, blocking_session: RequestsSession | None = None
) -> RequestsResponse:
    r"""
    Method - Get Parse Response
    - arguments:
        - `text`: strings input in the Google patents search box
    - keyword arguments:
        - `blocking_session`: an object of type `requests.Session` or None
    - returns:
        - an object of type `requests.Response`
    - raises:
        - `requests.ConnectionError`
    - notes:
        - uses the `requests.Session` object to make a blocking http call or
        creates one if the `blocking_session` keyword argument is None
    """
    url: str = build_parse_by_text_url(text)
    if blocking_session is None:
        blocking_session = RequestsSession()
    try:
        response: RequestsResponse = blocking_session.get(url, allow_redirects=False)
    except RequestsConnectionError as connection_error:
        logger.critical(connection_error, exc_info=(logger.level == logging.DEBUG))
        raise
    else:
        return response
    finally:
        blocking_session.close()
