r""" pdtk.google_patents.utils.network module """


# importing standard modules ==================================================
import logging
from typing import Dict
from urllib.parse import (
    quote, 
    urlencode
)


# importing third-party modules ===============================================
from requests import (
    Session as RequestsSession,
    Response as RequestsResponse,
    ConnectionError as RequestsConnectionError
)
from aiohttp import (
    ClientSession as AsyncSession,
    ClientResponse as AsyncResponse,
    ClientConnectionError as AsyncConnectionError
)


# importing custom modules ====================================================
from ...config import (
    BASE_URL_GOOGLE_PATENTS
)


# module variables ============================================================
logger: logging.Logger = logging.getLogger(__name__)


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
        BASE_URL_GOOGLE_PATENTS,
        urlencode(params, safe="", quote_via=quote)
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
        BASE_URL_GOOGLE_PATENTS,
        urlencode(params, safe="()", quote_via=quote)
    )
    logger.debug("constructed parse text url: '{}'".format(url))
    return url


# -----------------------------------------------------------------------------
def get_result_response(
    id_url: str, blocking_session: RequestsSession
) -> RequestsResponse:
    r"""
    Method - Get Result Response
    - arguments:
        - `id_url`: a string representing a Google patent URL
            - example: 'patent/US9145048B2/en'
        - `blocking_session`: an object of type `requests.Session`
    - returns:
        - an object of type `requests.Response`
    - raises:
        - `requests.ConnectionError`
    - notes:
        - uses the `requests.Session` object to make a blocking http call or
        creates one if the `blocking_session` keyword argument is None
    """
    url: str = build_result_by_id_url(id_url)
    try:
        response: RequestsResponse = blocking_session.get(
            url, allow_redirects=False
        )
    except RequestsConnectionError as connection_error:
        logger.critical(
            connection_error, exc_info=(logger.level == logging.DEBUG)
        )
        raise
    else:
        return response


def get_parse_response(
    text: str, blocking_session: RequestsSession
) -> RequestsResponse:
    r"""
    Method - Get Parse Response
    - arguments:
        - `text`: strings input in the Google patents search box
        - `blocking_session`: an object of type `requests.Session`
    - returns:
        - an object of type `requests.Response`
    - raises:
        - `requests.ConnectionError`
    - notes:
        - uses the `requests.Session` object to make a blocking http call or
        creates one if the `blocking_session` keyword argument is None
    """
    url: str = build_parse_by_text_url(text)
    try:
        response: RequestsResponse = blocking_session.get(
            url, allow_redirects=False
        )
    except RequestsConnectionError as connection_error:
        logger.critical(
            connection_error, exc_info=(logger.level == logging.DEBUG)
        )
        raise
    else:
        return response


# ASYNC methods ===============================================================
async def get_result_response_async(
    id_url: str, async_session: AsyncSession
) -> AsyncResponse:
    r"""
    Method - Get Result Response Async
    - arguments:
        - `id_url`: a string representing a Google patent URL
            - example: 'patent/US9145048B2/en'
        - `async_session`: an object of type `aiohttp.ClientSession`
    - returns:
        - an object of type `aiohttp.ClientResponse`
    - raises:
        - `aiohttp.ClientConnectionError`
    - notes:
        - uses the `aiohttp.ClientSession` object to make an async http call
    """
    url: str = build_result_by_id_url(id_url)
    try:
        result_async_response: AsyncResponse = await async_session.get(
            url, allow_redirects=False
        )
    except AsyncConnectionError as connection_error:
        logger.critical(
            connection_error, exc_info=(logger.level == logging.DEBUG)
        )
        raise
    else:
        return result_async_response


async def get_parse_response_async(
    text: str, async_session: AsyncSession
) -> AsyncResponse:
    r"""
    Method - Get Parse Response Async
    - arguments:
        - `id_url`: a string representing a Google patent URL
            - example: 'patent/US9145048B2/en'
        - `async_session`: an object of type `aiohttp.ClientSession`
    - returns:
        - an object of type `aiohttp.ClientResponse`
    - raises:
        - `aiohttp.ClientConnectionError`
    - notes:
        - uses the `aiohttp.ClientSession` object to make an async http call
    """
    url: str = build_parse_by_text_url(text)
    try:
        result_async_response: AsyncResponse = await async_session.get(
            url, allow_redirects=False
        )
    except AsyncConnectionError as connection_error:
        logger.critical(
            connection_error, exc_info=(logger.level == logging.DEBUG)
        )
        raise
    else:
        return result_async_response
