r""" py_google_patents.models.response_models """


# importing standard modules ==================================================
from typing import Union, Optional, List


# importing third-party modules ===============================================
from pydantic import BaseModel


# model definitions ===========================================================
class PatentMetaData(BaseModel):
    r""" model representing a single result id from patents.google.com/xhr/parse """

    id: Union[str, None] = None
    number: Union[str, None] = None
    title: Union[str, None] = None

    pass # end of _PatentMetaData


class GoogleParsePatentResult(BaseModel):
    r""" model representing a single result id, if received, from 
    patents.google.com/xhr/parse """

    result: PatentMetaData

    pass # end of GoogleParsePatentResult


class GoogleParseQueryResult(BaseModel):
    r""" model representing a single query result from patents.google.com/xhr/parse """

    query_url: Union[str, None] = None

    pass # end of GoogleParseQueryResult


class GoogleParseResponse(BaseModel):
    r""" model defining the response received from patents.google.com/xhr/parse """

    error_no_patents_found: bool
    results: Optional[
        Union[
            List[GoogleParsePatentResult], 
            List[GoogleParseQueryResult]
        ]
    ]

    pass # end of GoogleParseResponse