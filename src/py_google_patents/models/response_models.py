r""" py_google_patents.models.response_models """


# importing standard modules ==================================================
from typing import Union, Optional, List


# importing third-party modules ===============================================
from pydantic import BaseModel, Field


# model definitions ===========================================================
class PatentMetaData(BaseModel):
    r""" model representing a single result id from patents.google.com/xhr/parse """

    id: Union[str, None] = Field(
        None, 
        title="uri for probable patent document request",
        description=\
            "string containing a uri of the form 'patent/<patent_number>/<language_code>'",
        regex=r"patent/[A-Z]{2}[A-Z0-9]+/[a-z]{2}"
    )

    number: Union[str, None] = Field(
        None,
        title="document publication ID",
        description="string containing the document publication ID",
        regex=r"[A-Z]{2}[A-Z0-9]+"
    )

    title: str = Field(
        "",     # default empty string
        title="title of the patent document",
        description="string containing the title of the patent document"
    )

    pass # end of _PatentMetaData


class GoogleParsePatentResult(BaseModel):
    r""" model representing a single result id, if received, from 
    patents.google.com/xhr/parse """

    result: PatentMetaData

    pass # end of GoogleParsePatentResult


class GoogleParseQueryResult(BaseModel):
    r""" model representing a single query result from patents.google.com/xhr/parse """

    query_url: Union[str, None] = Field(
        None,
        title="formatted uri with the query keywords",
        description="string containing formatted uri with the query keywords",
        regex=r"q=.+"
    )

    pass # end of GoogleParseQueryResult


class GoogleParseResponse(BaseModel):
    r""" model defining the response received from patents.google.com/xhr/parse """

    error_no_patents_found: bool = Field(
        False,
        title="boolean indicating if no patents can be recommended"
    )

    results: Optional[
        Union[
            List[GoogleParsePatentResult], 
            List[GoogleParseQueryResult]
        ]
    ]

    pass # end of GoogleParseResponse


# -----------------------------------------------------------------------------
class GooglePatentResponse(BaseModel):
    r""" model defining the response received from patents.google.com/xhr/result
    for a single 'id' url query parameter """


    pass # end of GooglePatentResponse