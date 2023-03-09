r""" py_google_patents.network module """

# importing standard modules ==================================================


# schema definitions ==========================================================
class PatentMetaData(BaseModel):
    r""" model representing a single result id from patents.google.com/xhr/parse """

    id: Union[str, None] = Field(
        None,
        title="uri for probable patent document request",
        description="string containing a uri of the form 'patent/<patent_number>/<language_code>'"
    )

    number: Union[str, None] = Field(
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


class GoogleParsePatentResult(BaseModel):
    r""" model representing a single result id, if received, from 
    patents.google.com/xhr/parse """

    result: PatentMetaData

    pass  # end of GoogleParsePatentResult


class GoogleParseQueryResult(BaseModel):
    r""" model representing a single query result from patents.google.com/xhr/parse """

    query_url: Union[str, None] = Field(
        None,
        title="formatted uri with the query keywords",
        description="string containing formatted uri with the query keywords"
    )

    pass  # end of GoogleParseQueryResult


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

    pass  # end of GoogleParseResponse


# method definitions ==========================================================
class AsyncNetworkInterface:
    r""" class serving as an asynchronous network interface """

    base_url: str = "https://patents.google.com/xhr"

    def __init__(
            self,
            http_client: ClientSession,
            logger: logging.Logger = None
    ):
        self._http_client: ClientSession = http_client
        self._logger: logging.Logger = logger \
            if logger is not None \
            else logging.getLogger("network_interface")
        return

    def getHttpClient(self) -> ClientSession:
        return self._http_client

    def getLogger(self) -> logging.Logger:
        return self._logger

    async def getResult(self, id_url: str) -> str:
        r""" Instance Method - Get Result 
        - arguments:
            - `id_url`: a string representing an google patent URL
            example: 'patent/US9145048B2/en'
        - returns:
            - a string containing the data response
        - raises:
        - notes:
            - uses the internal `_http_client` to send http requests 
        """

        url: str = "{}/result?id={}".format(
            self.base_url, urllib.parse.quote(id_url, safe="")
        )
        async with self.getHttpClient() \
                .get(url, allow_redirects=False) as response:
            self.getLogger().debug(response.headers)
            document_as_text: str = await response.text()

        return document_as_text

    async def getParse(self, text: str) -> GoogleParseResponse:
        r""" Instance Method - Get Parse
        - arguments:
            - `text`: strings entered in the google patents search box
        - returns:
            - an object of type `GoogleParseResponse`
        - raises:
        - notes:
            - uses the internal `_http_client` to send http requests 
        """
        url: str = "{}/parse?text={}&cursor={}&exp=".format(
            self.base_url, urllib.parse.quote(text, safe="()"), len(text)
        )
        async with self.getHttpClient() \
                .get(url, allow_redirects=False) as response:
            self.getLogger().debug(response.headers)
            result: GoogleParseResponse = GoogleParseResponse(
                **await response.json()
            )

        return result

    pass  # end of AsyncNetworkInterface
