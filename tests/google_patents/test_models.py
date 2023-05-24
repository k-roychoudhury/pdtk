r""" tests.google_patents.test_models module """


# importing standard modules ==================================================
from typing import List
from os import walk
from os.path import (
    join, 
    dirname
)
import pprint as pp


# importing third-party modules ===============================================
import pytest


# importing custom modules ====================================================
from pdtk.google_patents.models import GoogleRawPatent


# test methods ================================================================
def patent_data_file_paths() -> List[str]:
    patent_data_directory_path: str = join(
        dirname(dirname(__file__)), "data", "google_api_patent_data_responses"
    )
    __filenames: List[str] = list()
    for dirpath, _, filenames in walk(patent_data_directory_path):
        __filenames.extend(
            map(lambda x: join(dirpath, x), filenames)
        )
    
    return __filenames


@pytest.mark.parametrize(
    "raw_content_filepath", patent_data_file_paths()
)
def test_GoogleRawPatent_parse_bytes_content(
    raw_content_filepath: str
) -> None:
    with open(raw_content_filepath, "rb") as raw_file:
        bytes_data: bytes = raw_file.read()

    _object: GoogleRawPatent = GoogleRawPatent.parse_bytes_content(bytes_data)
    print("")
    pp.pprint(_object.dict(), width=150, compact=True)

    return None
