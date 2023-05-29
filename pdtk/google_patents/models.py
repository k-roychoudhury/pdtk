r""" pdtk.google_patents.models module """


# importing standard modules ==================================================
from typing import (
    List,
    Dict,
    Any
)
from datetime import date


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
from ..concepts.patent_number import PatentNumber
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
class PublicationNumber(PatentNumber):
    r""" class representing a patent number along with other information """

    kind_code_description: str = Field("")

    pass # end of PublicationNumber


class RawPatentTitle(GlobalBaseModel):
    r""" class representing a title data element of a raw patent document """

    load_source: str = Field(...)
    title_text: str = Field(...)

    pass # end of RawPatentTitle


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


class DocumentReference(GlobalBaseModel):
    r""" class representing data elements of a document reference """

    patent_number: PatentNumber = Field(...)
    lang_code: LanguageCode
    id_url: str = Field(...)

    @classmethod
    def parse_id_url(cls, id_url: str) -> 'DocumentReference':
        r""" Class Method: Parse Id Url
        - arguments:
            - `id_url`: a string representing a Google patent URL
                - example: 'patent/US9145048B2/en'
        - returns:
            - an object of type `DocumentReference`
        """
        _, patnetNumber, langCode = list(
            filter(lambda x: x != "", id_url.strip().split("/"))
        )

        result: DocumentReference = DocumentReference(
            patent_number=PatentNumber.parse_string(patnetNumber),
            lang_code=langCode.strip().upper(),
            id_url=id_url
        )

        return result

    pass # end of DocumentReference


class LegalEvent(GlobalBaseModel):
    r""" class representing data elements of a legal event """

    event_date: date | None = Field(None)
    title: str = Field(...)
    event_type: str = Field(...)
    critical: bool = Field(False)
    document_reference: DocumentReference | None = Field(None)

    @classmethod
    def parse_event_dd_tag(cls, event_dd_tag: Tag) -> 'LegalEvent':
        r""" Class Method: Parse Event DD Tag
        - arguments:
            - `event_dd_tag`: an object of type `Tag`
        - returns:
            - an object of type `LegalEvent`
        """
        event_time_tag: Tag = event_dd_tag.find_next("time", {"itemprop": "date"})
        event_date_source: str = event_time_tag.attrs.get(
            "datetime", event_time_tag.get_text().strip()
        ).strip()
        try:
            event_date: date | None = date.fromisoformat(event_date_source) \
            if event_date_source != "" else None
        except ValueError:
            event_date = None

        event_title_tag: Tag = event_dd_tag.find_next("span", {"itemprop": "title"})
        event_title: str = event_title_tag.get_text().strip()

        event_type_tag: Tag = event_dd_tag.find_next("span", {"itemprop": "type"})
        event_type: str = event_type_tag.get_text().strip()

        # optional filed parsing, if available in source ----------------------
        critical_tag: Tag = event_time_tag.find_next_sibling(
            "span", {"itemprop": "critical"}
        )
        criticality: bool = critical_tag.attrs.get("content") == "true" \
            if critical_tag is not None else False

        documentId_tag: Tag = event_time_tag.find_next_sibling(
            "span", {"itemprop": "documentId"}
        )
        document_reference: DocumentReference | None = DocumentReference.parse_id_url(
            documentId_tag.get_text().strip()
        ) if documentId_tag is not None else None


        result: LegalEvent = LegalEvent(
            event_date=event_date,
            title=event_title,
            event_type=event_type,
            critical=criticality,
            document_reference=document_reference,
        )

        return result

    pass # end of LegalEvent


class MiscDetails(GlobalBaseModel):
    r""" class representing meta data elements """

    legal_status: str = Field(...)
    prior_art_keywords: List[str] = Field(...)
    other_languages: List[DocumentReference] = Field(...)
    other_versions: List[DocumentReference] = Field(...)
    legal_events: List[LegalEvent] = Field(...)

    pass # end of MiscDetails


class ImageMeta(GlobalBaseModel):
    r""" class representing data elements of an associated image """

    image_url: str = Field(...)

    @classmethod
    def parse_li_tag(cls, image_li_tag: Tag) -> 'ImageMeta':
        r""" Class Method: Parse Lis Tag
        - arguments:
            - `image_li_tag`: an object of type `Tag`
        - returns:
            - an object of type `ImageMeta`
        """
        image_url: str = image_li_tag.find_next(
            "meta", {"itemprop": "full"}
        ).attrs.get("content")

        result: ImageMeta = ImageMeta(
            image_url=image_url
        )

        return result

    pass # end of ImageMeta


class CpcClass(GlobalBaseModel):
    r""" class representing data elements of a classification """

    class_code: str = Field(...)
    description: str = Field(...)

    @classmethod
    def parse_ul_tag(cls, ul_tag: Tag) -> 'CpcClass':
        r""" Class Method: Parse UL Tag
        - arguments:
            - `ul_tag`: an object of type `Tag`
        - returns:
            - an object of type `Classifications`
        - notes:
            - returns the leaf classification element
        """
        for item in ul_tag.find_all_next("li", {"itemprop": "cpcs"}):
            code_span_tag: Tag = item.find_next(
                "span", {"itemprop": "Code"}
            )
            code: str = code_span_tag.get_text().strip()
            description: str = item.find_next(
                "span", {"itemprop": "Description"}
            ).get_text().strip()
            leaf_meta_tag: Tag = code_span_tag.find_next_sibling(
                "meta", {"itemprop": "Leaf"}
            )
            if leaf_meta_tag is None:
                continue
            else:
                result: CpcClass = CpcClass(
                    class_code=code,
                    description=description
                )
                break

        return result
    
    pass # end of CpcClass


class GoogleRawPatent(GlobalBaseModel):
    r""" class representing the raw patent data obtained by and 'id' query """
    
    document_number: PublicationNumber = Field(...)
    application_document_number: str = Field(...)

    prior_art_date: date = Field(...)
    priority_date: date = Field(...)
    filing_date: date = Field(...)
    publication_date: date = Field(...)

    titles: List[RawPatentTitle] = Field(...)
    abstracts: List[RawPatentAbstract] = Field(...)

    inventors: List[str] = Field(...)
    assignee_original: str = Field(...)
    assginee_current: str = Field(...)

    images: List[ImageMeta] = Field(...)

    cpc_classifications: List[CpcClass] = Field(...)
    
    misc_details: MiscDetails = Field(...)

    def get_abstract_by_language_code(
        self, 
        lang_code: LanguageCode
    ) -> RawPatentAbstract:
        r""" Instance Method: Get Abstract By Language Code
        - arguments:
            - `lang_code`: a well recognisable ISO language code
                - typically a 2 charater Uppercase string
        - returns:
            - a reference to a `RawPatentAbstract` object; if found
        - raises:
            - `KeyError`: if a `RawPatentAbstract` with `lang_code` is not found
        - notes:
            - performs a linear search on the interanl attribute `abstracts`
        """
        for item in self.abstracts:
            if item.language_code == lang_code:
                return item
        else:
            key_error_message: str = \
                "abstract with language code '{}' not found".format(lang_code)
            raise KeyError(key_error_message)


    def get_english_abstract(self) -> RawPatentAbstract:
        r""" Instance Method: Get English Abstract
        - arguments:
        - returns:
            - a reference to a `RawPatentAbstract` object; if found
        - raises:
            - `KeyError`: if an english `RawPatentAbstract` is not found
        """
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
        # else:
        #     # remove all 'NavigableString' objects that are not part of a 
        #     # leaf node in the soup
        #     for element in article_tag.descendants:
        #         if type(element) is Tag:
        #             if len(element.contents) == 1 \
        #                 and type(element.contents[0]) is NavigableString:
        #                 # element is a leaf tag
        #                 __tag_ref: NavigableString = element.contents[0]
        #                 __tag_ref.replace_with(
        #                     " ".join(
        #                         map(lambda x: x.strip(), __tag_ref.splitlines())
        #                     ).strip()
        #                 )
                        
        #             else:
        #                 # element is not a leaf node
        #                 for item in element.children:
        #                     if type(item) is NavigableString:
        #                         item.replace_with("")


        # ---------------------------------------------------------------------
        
        # parse title markup data ---------------------------------------------
        patent_titles: List[RawPatentTitle] = list()
        heading1_title: Tag = article_tag.find_next("h1", {"itemprop": "pageTitle"})
        if heading1_title is not None:
            title_markup: str = ""
            load_source: str = ""
            heading_title_markup: str = str(heading1_title.get_text()).\
                rsplit("-", 1)[0].split("-", 1)[-1].strip()

            span_title: Tag = heading1_title.find_next("span", {"itemprop": "title"})
            if span_title is not None:
                span_title_markup: str = str(span_title.get_text()).strip()
                title_markup = span_title_markup
                load_source = "span title"

            else:
                title_markup = heading_title_markup
                load_source = "page title"

            patent_titles.append(RawPatentTitle(
                load_source=load_source,
                title_text=title_markup
            ))

        # parse first 'dl' markup data ----------------------------------------
        first_dl_tag: Tag = article_tag.find_next("dl")
        if first_dl_tag is not None:
            publication_number_dt_tag: Tag = first_dl_tag.find_next("dt")
            publicationNumber: str = \
                first_dl_tag.find_next(
                    "dd", {"itemprop": "publicationNumber"}
                ).get_text()
            numberWithoutCodes: str = \
                first_dl_tag.find_next(
                    "meta", {"itemprop": "numberWithoutCodes"}
                ).attrs.get("content")
            kindCode: str = \
                first_dl_tag.find_next(
                    "meta", {"itemprop": "kindCode"}
                ).attrs.get("content")
            publicationDescription: str = \
                first_dl_tag.find_next(
                    "meta", {"itemprop": "publicationDescription"}
                ).attrs.get("content")
            
            country_code: str = publicationNumber.removesuffix(kindCode).\
                removesuffix(numberWithoutCodes)
            document_number: PublicationNumber = PublicationNumber(
                country_code=country_code,
                patent_number=numberWithoutCodes,
                kind_code=kindCode,
                kind_code_description=publicationDescription
            )


            authority_tag: Tag = publication_number_dt_tag.find_next_sibling("dt")
            countryCode: str = authority_tag.find_next(
                "dd", {"itemprop": "countryCode"}
            ).get_text()
            assert countryCode == document_number.country_code
            countryName: str = authority_tag.find_next(
                "dd", {"itemprop": "countryName"}
            ).get_text()

            prior_art_keywords_tag: Tag = authority_tag.find_next_sibling("dt")
            prior_art_keywords: List[str] = list()
            for item in prior_art_keywords_tag.find_all_next(
                "dd", {"itemprop": "priorArtKeywords"}
            ):
                prior_art_keywords.append(item.get_text().strip())

            prior_art_date_tag: Tag = prior_art_keywords_tag.find_next_sibling("dt")
            priorArtDate: str = prior_art_date_tag.find_next(
                "time", {"itemprop": "priorArtDate"}
            ).attrs.get("datetime").strip()
            prior_art_date: date = date.fromisoformat(priorArtDate)

            legal_status_tag: Tag = prior_art_date_tag.find_next_sibling("dt")
            if legal_status_tag is not None:
                legalStatusIfi: Tag = legal_status_tag.find_next(
                    "span", {"itemprop": "status"}
                )
                legal_status: str = legalStatusIfi.get_text().strip()
            else:
                legal_status: str = "Unknown"
            
            # end of processing of 'first_dl_tag' -----------------------------

            application_number_dt_tag: Tag = first_dl_tag.find_next_sibling("dt")
            applicationNumber: Tag = application_number_dt_tag.find_next(
                "dd", {"itemprop": "applicationNumber"}
            )
            application_number: str = applicationNumber.get_text().strip()

            tag_after: Tag = application_number_dt_tag
            other_languages: List[DocumentReference] = list()
            for item in application_number_dt_tag.find_next_siblings(
                "dd", {"itemprop": "otherLanguages"}
            ):
                id_url: str = item.find_next("a").attrs.get("href")
                # lang_code: str = item.find_next(
                #     "span", {"itemprop": "code"}
                # ).get_text().strip().upper()
                
                # other_languages.append(DocumentReference(
                #     patent_number=PatentNumber.parse_string(id_url.split("/")[2]),
                #     lang_code=lang_code,
                #     id_url=id_url
                # ))
                other_languages.append(DocumentReference.parse_id_url(id_url))
                tag_after = item
            
            other_versions: List[DocumentReference] = list()
            for item in application_number_dt_tag.find_next_siblings(
                "dd", {"itemprop": "directAssociations"}
            ):
                id_url: str = item.find_next("a").attrs.get("href")
                # lang_code: str = item.find_next(
                #     "span", {"itemprop": "primaryLanguage"}
                # ).get_text().strip().upper()
                
                # other_versions.append(DocumentReference(
                #     patent_number=PatentNumber.parse_string(id_url.split("/")[2]),
                #     lang_code=lang_code,
                #     id_url=id_url
                # ))
                other_languages.append(DocumentReference.parse_id_url(id_url))
                tag_after = item

            inventor_dt_tag: Tag = tag_after.find_next("dt")    # a data element that is always present
            inventors: List[str] = list()
            for item in inventor_dt_tag.find_next_siblings(
                "dd", {"itemprop": "inventor"}
            ):
                inventors.append(item.get_text().strip())
                tag_after = item
            
            # current assignee ------------------------------------------------
            current_assignee_dd_tag: Tag = tag_after.find_next(
                "dd", {"itemprop": "assigneeCurrent"}
            )
            current_assignee: str = current_assignee_dd_tag.get_text().strip() \
                if current_assignee_dd_tag is not None else ""

            # original assignee -----------------------------------------------
            original_assignee_dd_tag: Tag = tag_after.find_next(
                "dd", {"itemprop": "assigneeOriginal"}
            )
            original_assignee: str = original_assignee_dd_tag.get_text().strip()

            # priority date ---------------------------------------------------
            priorityDate_time_tag: Tag = tag_after.find_next(
                "time", {"itemprop": "priorityDate"}
            )
            priority_date_source: str = priorityDate_time_tag.attrs.get(
                "datetime", priorityDate_time_tag.get_text().strip()
            ).strip()
            priority_date: date = date.fromisoformat(priority_date_source)

            # filing date -----------------------------------------------------
            filingDate_time_tag: Tag = tag_after.find_next(
                "time", {"itemprop": "filingDate"}
            )
            filing_date_source: str = filingDate_time_tag.attrs.get(
                "datetime", filingDate_time_tag.get_text().strip()
            ).strip()
            filing_date: date = date.fromisoformat(filing_date_source)

            # publication date ------------------------------------------------
            publicationDate_time_tag: Tag = tag_after.find_next(
                "time", {"itemprop": "publicationDate"}
            )
            publication_date_source: str = publicationDate_time_tag.attrs.get(
                "datetime", publicationDate_time_tag.get_text().strip()
            ).strip()
            publication_date: date = date.fromisoformat(publication_date_source)

            # parse events ----------------------------------------------------
            legal_events: List[LegalEvent] = list()
            for item in publicationDate_time_tag.find_all_next(
                "dd", {"itemprop": "events"}
            ):
                legal_events.append(LegalEvent.parse_event_dd_tag(item))
                tag_after = item
            
            # image link parsing ----------------------------------------------
            images: List[ImageMeta] = list()
            classifications: List[CpcClass] = list()

            next_section_tag: Tag = tag_after.find_next("section")
            next_heading_tag: Tag = next_section_tag.find_next("h2")
            if next_heading_tag.get_text().strip().lower() == "images":
                for item in next_heading_tag.find_all_next(
                    "li", {"itemprop": "images"}
                ):
                    images.append(ImageMeta.parse_li_tag(item))
                next_section_tag = next_section_tag.find_next("section")
                next_heading_tag: Tag = next_section_tag.find_next("h2")

            if next_heading_tag.get_text().strip().lower() == "classifications":
                for item in next_heading_tag.find_all_next("ul", {"itemprop": "cpcs"}):
                    classifications.append(CpcClass.parse_ul_tag(item))


        else:
            content_error_message: str = "'article_tag' does not have first 'dl' tag"
            # the 'dl' tag is not present inside the 'article' tag 
            raise ContentError(content_error_message)
            

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
            document_number=document_number,
            application_document_number=application_number,
            prior_art_date=prior_art_date,
            priority_date=priority_date,
            filing_date=filing_date,
            publication_date=publication_date,
            titles=patent_titles,
            abstracts=patent_abstracts,
            inventors=inventors,
            assignee_original=original_assignee,
            assginee_current=current_assignee,
            images=images,
            cpc_classifications=classifications,
            misc_details=MiscDetails(
                legal_status=legal_status,
                prior_art_keywords=prior_art_keywords,
                other_languages=other_languages,
                other_versions=other_versions,
                legal_events=legal_events
            )
        )

        return result


    pass # end of GoogleRawPatent
