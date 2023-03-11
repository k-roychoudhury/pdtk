r""" py_google_patents.models module """

from typing import List

from pydantic import Field

from .config import OrjsonModel as GlobalBaseModel


# model definitions ===========================================================
class PatentMetaData(GlobalBaseModel):
    r""" model representing a single result id from patents.google.com/xhr/parse """

    id: str | None = Field(
        None,
        title="uri for probable patent document request",
        description="string containing a uri of the form "
                    "'patent/<patent_number>/<language_code>'"
    )

    number: str | None = Field(
        None,
        title="document publication ID",
        description="string containing the document publication ID"
    )

    title: str = Field(
        "",  # default empty string
        title="title of the patent document",
        description="string containing the title of the patent document"
    )

    pass  # end of PatentMetaData


class GoogleParsePatentResult(GlobalBaseModel):
    r""" model representing a single result id, if received, from
    patents.google.com/xhr/parse """

    result: PatentMetaData

    pass  # end of GoogleParsePatentResult


class GoogleParseQueryResult(GlobalBaseModel):
    r""" model representing a single query result from
    patents.google.com/xhr/parse """

    query_url: str | None = Field(
        None,
        title="formatted uri with the query keywords",
        description="string containing + quoted uri with the query keywords"
    )

    pass  # end of GoogleParseQueryResult


class GoogleParseResponse(GlobalBaseModel):
    r""" model defining the response received from patents.google.com/xhr/parse """

    error_no_patents_found: bool = Field(
        ...,
        title="boolean indicating if no patents can be recommended"
    )

    results: List[GoogleParsePatentResult] | List[GoogleParseQueryResult] | None = Field(
        None,
        title="key containing the response from the google patent api server"
    )

    pass  # end of GoogleParseResponse
