r""" py_google_patents.core.data_parsers module """


# importing standard modules ==================================================
from typing import Dict, Any
import pprint as pp


# importing third-party modules ===============================================
from bs4 import BeautifulSoup, PageElement, Tag, NavigableString


# importing custom modules ====================================================
from ..common.config import getLibraryLogger
from ..models.response_models import GoogleParseResponse, GooglePatentResponse


# method definitions ==========================================================
def parse_parse_endpoint_response_data(
    data: Dict[str, Any]
    ) -> GoogleParseResponse:
    r""" Functional Requirement - PARSE PARSE ENDPOINT RESPONSE DATA
    - arguments:
        - data: json returned by the '/xhr/parse' endpoint
    - returns:
        - an object of type 'GoogleParseResponse'
    - raises:
    - notes:
    """

    _result: GoogleParseResponse = GoogleParseResponse(**data)
    # pydantic makes sure to insert the appropriate models in the sub-fields

    return _result


def parse_result_endpoint_response_data(data: str) -> GooglePatentResponse:
    r""" Functional Requirement - PARSE RESULT ENDPOINT RESPONSE DATA
    - arguments:
        - data: html returned (as str) by the '/xhr/result' endpoint
    - returns:
        - an object of type 'GooglePatentResponse'
    - raises:
    - notes:
    """

    soup: BeautifulSoup = BeautifulSoup(data, features="html5lib")
    document: Tag = soup.find_next(name="article").__copy__()
    del soup

    # find abstract section and remove from original document -----------------
    abstract_section: Tag = document.find_next(
        name="section", attrs={"itemprop": "abstract"}
    )
    if abstract_section:
        abstract_tag: Tag = abstract_section.__copy__()
        abstract_section.decompose()
        # pp.pprint(str(abstract_tag), width=150)
    else:
        getLibraryLogger().debug(
            "document.find_next(name='section', attrs={'itemprop': 'abstract'}) "
            "returned None"
        )
        # no abstract in patent raw source
        pass

    # find description section and remove from original document --------------
    description_section: Tag = document.find_next(
        name="section", attrs={"itemprop": "description"}
    )
    if description_section:
        description_tag: Tag = description_section.__copy__()
        description_section.decompose()
        # pp.pprint(str(description_tag), width=150)
    else:
        getLibraryLogger().debug(
            "document.find_next(name='section', attrs={'itemprop': 'description'}) "
            "returned None"
        )
        # no description in patent raw source
        pass

    # find claims section and remove from original document -------------------
    claims_section: Tag = document.find_next(
        name="section", attrs={"itemprop": "claims"}
    )
    if claims_section:
        claims_tag: Tag = claims_section.__copy__()
        claims_section.decompose()
        # pp.pprint(str(claims_tag), width=150)
    else:
        getLibraryLogger().debug(
            "document.find_next(name='section', attrs={'itemprop': 'claims'}) "
            "returned None"
        )
        # no claims in patent raw source
        pass

    # find application section and remove from original document ----------------
    application_section: Tag = document.find_next(
        name="section", attrs={"itemprop": "application"}
    )
    if application_section:
        application_tag: Tag = application_section.__copy__()
        application_section.decompose()
        # pp.pprint(str(application_tag), width=150)
    else:
        getLibraryLogger().debug(
            "document.find_next(name='section', attrs={'itemprop': 'application'}) "
            "returned None"
        )
        # no application in patent raw source
        pass

    # find family section and remove from original document ---------------------
    family_section: Tag = document.find_next(
        name="section", attrs={"itemprop": "family"}
    )
    if family_section:
        family_tag: Tag = family_section.__copy__()
        family_section.decompose()
        # pp.pprint(str(family_tag), width=150)
    else:
        getLibraryLogger().debug(
            "document.find_next(name='section', attrs={'itemprop': 'family'}) "
            "returned None"
        )
        # no family in patent raw source
        pass

    # find classification section and remove from original document -----------
    classifications_ul: Tag = document.find_next(
        name="ul", attrs={"itemprop": "cpcs"}
    )
    if classifications_ul:
        classification_section: Tag = classifications_ul.find_previous(
            name="section"
        )
        classification_tag: Tag = classification_section.__copy__()
        classification_section.decompose()
        # pp.pprint(str(classification_tag), width=150)
    else:
        getLibraryLogger().debug(
            "document.find_next(name='ul', attrs={'itemprop': 'cpcs'}) "
            "returned None"
        )
        # no classifications in patent raw source
        pass

    # # find image section and remove from original document --------------------
    # image_section: Tag = document.find_next(name="section")
    # image_tag: Tag = image_section.__copy__()
    # image_section.decompose()

    # pp.pprint(str(image_tag), width=150)
    
    
    pp.pprint(str(document), width=150)

    return None