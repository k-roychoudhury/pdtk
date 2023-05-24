r""" pdtk.google_patents.models module """


# importing standard modules ==================================================
from typing import (
    List,
    Dict,
    Any
)


# importing third-party modules ===============================================
from pydantic import (
    Field,
    root_validator
)
from bs4 import (
    Tag,
    ResultSet,
    BeautifulSoup
)


# importing custom modules ====================================================
from ..concepts.types import (
    LanguageCode,
    HtmlMarkup
)
from ..models import OrjsonModel as GlobalBaseModel
from .exceptions import (
    ContentError
)


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


# -----------------------------------------------------------------------------
class RawPatentAbstract(GlobalBaseModel):
    r""" class representing an abstract data element of a raw patent document """

    language_code: LanguageCode
    load_source: str = Field(...)
    abstract_markup: HtmlMarkup


    @root_validator
    @classmethod
    def check_data_points(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        __language_code: str = data.get("language_code")
        data.update({"language_code": __language_code.strip().upper()})

        return data        


    pass # end of RawPatentAbstract


class GoogleRawPatent(GlobalBaseModel):
    r""" class representing the raw patent data obtained by and 'id' query """

    abstracts: List[RawPatentAbstract] = Field(...)


    def get_abstract_by_language_code(
        self, 
        lang_code: LanguageCode
    ) -> RawPatentAbstract:
        for item in self.abstracts:
            if item.language_code == lang_code:
                return item
        else:
            key_error_message: str = \
                "abstract with language code '{}' not found".format(lang_code)
            raise KeyError(key_error_message)


    def get_english_abstract(self) -> RawPatentAbstract:
        return self.get_abstract_by_language_code("EN")
        

    # -------------------------------------------------------------------------
    @classmethod
    def parse_bytes_content(cls, response_content: bytes) -> 'GoogleRawPatent':
        r""" Class Method: Parse Bytes Content
        - arguments:
            - `response_content`: an object of type `bytes`
        - returns:
            - an object of type `GoogleRawPatent`
        - notes:
        """
        content_soup: BeautifulSoup = BeautifulSoup(response_content, "lxml")
        article_tag: Tag = content_soup.find("article", {"class": "result"})
        if article_tag is None:
            content_error_message: str = "'response_content' does not have valid data"
            # the 'article' tag is not present in the response received 
            # from the google server
            raise ContentError(content_error_message)

        # ---------------------------------------------------------------------

        # parse abstract markup data ------------------------------------------
        patent_abstracts: List[RawPatentAbstract] = list()
        section_abstract: Tag = article_tag.find(
            "section", {"itemprop": "abstract"}
        )
        if section_abstract is not None:
            raw_abstracts: ResultSet[Tag] = \
                section_abstract.find_all_next("abstract")
            for __abstract_element in raw_abstracts:
                lang_code: str = __abstract_element.attrs.get("lang")
                load_source: str =  __abstract_element.attrs.get("load-source")
                abstract_markup: str = str(__abstract_element)

                patent_abstracts.append(RawPatentAbstract(
                    language_code=lang_code, 
                    load_source=load_source, 
                    abstract_markup=abstract_markup
                ))
            section_abstract.decompose()



        # ---------------------------------------------------------------------
        result: GoogleRawPatent = GoogleRawPatent(
            abstracts=patent_abstracts
        )

        return result


    pass # end of GoogleRawPatent
