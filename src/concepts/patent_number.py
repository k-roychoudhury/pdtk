r""" concepts.patent_number module """


# importing standard modules ==================================================
from typing import Union, Dict, Any
from re import Match
import logging


# importing third-party modules ===============================================
from pydantic import (
    BaseModel,
    Field,
    root_validator,
    ValidationError
)


# importing custom modules ====================================================
from .utils import (
    match_patent_number_pattern
)


# module variables ============================================================
logger: logging.Logger = logging.getLogger(__name__)


# type definitions ============================================================
class PatentNumber(BaseModel):
    r""" class representing a 'Patent Number' and associated methods and 
    concepts """


    country_code: str = Field(..., regex=r"([A-Z]{2})")
    patent_number: str = Field(...)
    kind_code: str = Field(..., regex=r"((?:[A-Z0-9]){1,2})")


    @classmethod
    def parse_string(
        cls,
        probable_patent_number: str
    ) -> 'PatentNumber':
        r""" Class Method: Parse String
        - arguments:
            - `probable_patent_number`: an object of type `str`
        - returns:
            - an object of type `PatentNumber`
        - raises:
            - `TypeError`
            - `ValidationError`
        """
        if type(probable_patent_number) is not str:
            type_error_msg: str = \
                "expected type of `probable_patent_number` to be `str`"
            raise TypeError(type_error_msg)
        
        pattern_match: Union[Match[str], None] = match_patent_number_pattern(
            probable_patent_number
        )
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
            - `format`: a string; representing a format string to use to build 
            the output `str` object 
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
        __repr_str: str = "{}({})".format(
            self.__class__.__name__, self.to_string()
        )
        return __repr_str
    

    def __str__(self) -> str:
        return self.__repr__()


    def __hash__(self) -> int:
        return hash(self.country_code + self.patent_number + self.kind_code)


    @root_validator(skip_on_failure=True)
    @classmethod
    def check_epo_number(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        r""" Root Validator: Check EPO Patent Number 
        - arguments:
            - `values`: an object of type `dict`
        - returns:
            - the passed in `values` argument
        - notes:
            - EPO patents and published applications must have seven digits, 
            so add lead zeros for older documents! 
            For example, EP11234 needs to be entered as EP0011234.
        """
        cc: str = values.get("country_code")    # 'country_code' is an attribute
        num: str = values.get("patent_number")  # 'patent_number' is an attribute
        
        if cc == "EP":
            
            # https://www.familyizer.com/index.html
            # EPO patents and published applications must have seven digits, 
            # so add lead zeros for older documents! 
            # For example, EP11234 needs to be entered as EP0011234.

            formatted_num: str = "{:0>7}".format(num)
            values.update({"patent_number": formatted_num})
            msg: str = "formatted EPO patent number from '{}' to '{}'".format(
                num, formatted_num
            )
            logger.warning(msg)

        return values
    

    pass # end of PatentNumber
