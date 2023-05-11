r""" tests.concepts.test_PatentNumber module """


# importing standard modules ==================================================


# importing third-party modules ===============================================
import pytest
from pydantic import ValidationError


# importing custom modules ====================================================
from concepts import PatentNumber


# test methods ================================================================
@pytest.mark.parametrize(
    "formatted_patent_number", 
    [
        "US-9145048-B2",
        "KR20120072372A",
        # "US12/751,612",
        "ES.2655892.T3"
    ]
)
def test_parse_string_correct(formatted_patent_number: str) -> None:
    _object: PatentNumber = PatentNumber.parse_string(formatted_patent_number)
    assert type(_object) is PatentNumber
    return None


@pytest.mark.parametrize(
    "unformatted_patent_number", 
    [
        1245676,
        "US12/751,612"
    ]
)
def test_parse_string_incorrect(unformatted_patent_number: str) -> None:
    with pytest.raises((ValidationError, TypeError)):
        _object: PatentNumber = PatentNumber.parse_string(unformatted_patent_number)
        assert type(_object) is PatentNumber
    return None


@pytest.mark.parametrize(
    ["patent_number", "format_string", "string_output"],
    [
        (
            PatentNumber.construct(
                country_code="US", patent_number="9145048", kind_code="B2"
            ),
            "{country_code}-{patent_number}-{kind_code}",
            "US-9145048-B2"
        ),
        (
            PatentNumber.construct(
                country_code="US", patent_number="9145048", kind_code="B2"
            ),
            "{country_code}-{patent_number}",
            "US-9145048"
        )
    ]
)
def test_to_string(
    patent_number: PatentNumber, 
    format_string: str, 
    string_output: str
) -> None:
    assert patent_number.to_string(format=format_string) == string_output
    return None
