r""" concepts.__init__ module """


# importing standard modules ==================================================
from typing import Union
from re import (
    compile,
    Match,
    Pattern
)


# importing third-party modules ===============================================
from pydantic import (
    BaseModel,
    Field,
    ValidationError
)


# module variables ============================================================
patent_number_regex: str = r"([A-Z]{2})[- \.]*((?:[A-Z]*)[0-9]+)[- \.]*([A-Z]{0,1}[0-9]*)"
patent_number_pattern: Pattern = compile(patent_number_regex)

# ifi_ucid_regex: str = r"^([A-Z]{2})[- \.]+((?:[A-Z]*)[0-9]+)[- \.]+((?:[A-Z0-9]){1,2})$"
# ifi_ucid_pattern: Pattern = compile(ifi_ucid_regex)


# type definitions ============================================================
class PatentNumber(BaseModel):
    r""" class representing a 'Patent Number' and associated methods and concepts """

    country_code: str = Field(..., regex=r"([A-Z]{2})")
    patent_number: str = Field(...)
    kind_code: str = Field(..., regex=r"((?:[A-Z0-9]){1,2})")


    def parse_string(
        probable_patent_number: str
    ) -> 'PatentNumber':
        r""" Instance Method: Parse String
        - arguments:
            - `probable_patent_number`: an object of type `str`
        - returns:
            - an object of type `PatentNumber`
        - raises:
            - `TypeError`
            - `ValidationError`
        """
        if type(probable_patent_number) is not str:
            type_error_msg: str = "expected type of `probable_patent_number` to be `str`"
            raise TypeError(type_error_msg)
        
        pattern_match: Union[Match, None] = patent_number_pattern.\
            match(probable_patent_number)
        if pattern_match is None:
            not_patent_number_like_error: str = \
                "'{}' does not match patent_number_regex".\
                    format(probable_patent_number)
            raise ValidationError(not_patent_number_like_error)
        
        __country_code: str = pattern_match.group(1)
        __patent_number: str = pattern_match.group(2)
        __kind_code: str = pattern_match.group(3)


        result_object: PatentNumber = PatentNumber(
            country_code=__country_code,
            patent_number=__patent_number,
            kind_code=__kind_code
        )

        return result_object


    def to_string(
        self, 
        *args, 
        format: str = "{country_code}-{patent_number}-{kind_code}"
    ) -> str:
        r""" Instance Method: To String 
        - keyword arguments:
            - `format`: a string; representing a format string to use to build the
            output `str` object 
        - returns:
            - a string
        """
        result: str = format.format(
            country_code=self.country_code, 
            patent_number=self.patent_number, 
            kind_code=self.kind_code
        )
        return result
    

    def __repr__(self) -> str:
        __repr_str: str = "{}({})".format(self.__class__.__name__, self.to_string())
        return __repr_str
    

    def __str__(self) -> str:
        return self.__repr__()
    

    pass # end of PatentNumber
