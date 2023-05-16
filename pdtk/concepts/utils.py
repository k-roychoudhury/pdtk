r""" pdtk.concepts.utils module """


# importing standard modules ==================================================
from typing import Union, Tuple
from re import (
    compile,
    Match,
    Pattern
)


# module variables ============================================================
patent_number_regex: str = \
    r"([A-Z]{2})[- \.]*((?:[A-Z]*)[0-9]+)[- \.]*([A-Z]{0,1}[0-9]*)"
patent_number_pattern: Pattern = compile(patent_number_regex)

# ifi_ucid_regex: str = \
# r"^([A-Z]{2})[- \.]+((?:[A-Z]*)[0-9]+)[- \.]+((?:[A-Z0-9]){1,2})$"
# ifi_ucid_pattern: Pattern = compile(ifi_ucid_regex)


# method definitions ==========================================================
def match_patent_number_pattern(__string: str) -> Union[Match[str], None]:
    return patent_number_pattern.match(__string)


def extract_patent_number_tuple(
    __string: str
    ) -> Union[Tuple[str, str, str], None]:
    string_match: Match[str] = match_patent_number_pattern(__string)
    if string_match is None:
        return None
    cc, num, kc = [string_match.group(i) for i in range(1, 4)]
    return cc, num, kc
