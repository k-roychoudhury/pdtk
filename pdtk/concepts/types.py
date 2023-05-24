r""" pdtk.concepts.types module """


# importing standard modules ==================================================
from typing import(
    Annotated
)


# importing third-party modules ===============================================
from pydantic import Field


# type definitions ============================================================
LanguageCode = Annotated[str, Field(
    ...,
    title="language code",
    description="a two(2) character string; indicating the language",
    max_length=2,
    regex=r"[A-Z]{2}"
)]

HtmlMarkup = Annotated[str, Field(
    ...,
    title="html markup type",
    description="a string having an element markedup in html"
)]
