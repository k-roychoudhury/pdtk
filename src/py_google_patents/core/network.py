r""" py_google_patents.core.network module """


# importing standard modules ==================================================
from typing import Dict, Union, Any
import urllib


# importing third-party modules ===============================================
import aiohttp, aiohttp.client_exceptions
from yarl import URL


# importing custom modules ====================================================
from ..common.config import getLibraryLogger


# module variables ============================================================
GOOGLE_PATENTS_BASE_URL: str = "https://patents.google.com"


# method definitions ==========================================================
async def http_get_parse_endpoint_response(text: str) -> Dict[str, Any]:
    r""" Functional Requirement - HTTP GET PARSE ENDPOINT RESPONSE
    - arguments:
        - text: a string containing the query to be made to 'patents.google.com'
    - returns:
        - a 'dict' object representing json returned by the '/xhr/parse' endpoint
    - raises:
    - notes:
    """

    _cursor: int = len(text)
    """ a url paramenter that needs to be sent. 
    The cursor value gives an indication of the length of the text being
    sent to the remote server.
    """

    _params: Dict[str, Union[str, int]] = {
        "text": text,
        "cursor": _cursor,
        "exp": ""
    }

    _data: Dict[str, Any] = None

    try:
        async with aiohttp.ClientSession(GOOGLE_PATENTS_BASE_URL) as session:
            async with session.get(
                "/xhr/parse", allow_redirects=False, params=_params
                ) as response:

                response.raise_for_status()
                _data = await response.json()
    
    except aiohttp.client_exceptions.ClientConnectorError as error:
        # caused by socket.gaierror
        getLibraryLogger().debug(error, exc_info=True)
        raise

    except aiohttp.client_exceptions.ClientConnectionError as error:
        getLibraryLogger().debug(error, exc_info=True)
        raise

    except aiohttp.client_exceptions.ClientResponseError as error:
        # handles or catches exceptions raises from the line 'response.raise_for_status()'
        getLibraryLogger().debug(error, exc_info=True)
        raise

    return _data


# -----------------------------------------------------------------------------
async def http_get_result_endpoint_response(id_url: str) -> str:
    r""" Functional Requirement - HTTP GET RESULT ENDPOINT RESPONSE
    - arguments:
        - id_url: a string containing the url of the patent to be extracted 
        from 'patents.google.com' 
            - examples:
                - 'patent/WO2022109623A1/fr' 
                - 'patent/<number>/<lang code>'
    - returns:
        - a 'str' object representing html returned by the '/xhr/result' endpoint
    - raises:
    - notes:
    """

    _params: Dict = {
        "id": id_url,
        "exp": ""
    }

    _endpoint_url: str = "{}{}".format(GOOGLE_PATENTS_BASE_URL, "/xhr/result?")
    _url: str = "{}{}".format(
        _endpoint_url, 
        urllib.parse.urlencode(
            _params, safe="", quote_via=urllib.parse.quote
        )
    )

    _data: str = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                URL(_url, encoded=True), allow_redirects=False
                ) as response:

                response.raise_for_status()
                _data: str = await response.text()
    
    except aiohttp.client_exceptions.ClientConnectorError as error:
        # caused by socket.gaierror
        getLibraryLogger().debug(error, exc_info=True)
        raise

    except aiohttp.client_exceptions.ClientConnectionError as error:
        getLibraryLogger().debug(error, exc_info=True)
        raise

    except aiohttp.client_exceptions.ClientResponseError as error:
        # handles or catches exceptions raises from the line 'response.raise_for_status()'
        getLibraryLogger().debug(error, exc_info=True)
        raise

    return _data