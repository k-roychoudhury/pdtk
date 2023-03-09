r""" py_google_patents.api.data module """


# importing standard modules ==================================================
from typing import Dict, Any


# importing custom modules ====================================================
from ..models.response_models import GoogleParseResponse, GooglePatentResponse
from ..core.network import http_get_parse_endpoint_response, \
    http_get_result_endpoint_response
from ..core.data_parsers import parse_parse_endpoint_response_data, \
    parse_result_endpoint_response_data


# method definitions ==========================================================
async def getTextRecommendations(text: str) -> GoogleParseResponse:
    r""" Feature Function - Get Text Recommendations 
    - arguments:
        - text: a string to send to patents.google.com to get recommendations
    - returns:
        - an object of type 'GoogleParseResponse'
    """

    raw_data: Dict[str, Any] = await http_get_parse_endpoint_response( text )

    return parse_parse_endpoint_response_data( raw_data )


async def getPatentData(id_url: str) -> GooglePatentResponse:
    r""" Feature Function - Get Patent Data 
    - arguments:
        - id_url: a string containing the url of the patent to be extracted 
        from 'patents.google.com' 
            - examples:
                - 'patent/WO2022109623A1/fr' 
                - 'patent/<number>/<lang code>'
    - returns:
        - an object of type 'GooglePatentResponse'
    """

    raw_data: str = await http_get_result_endpoint_response( id_url )

    return parse_result_endpoint_response_data( raw_data )
