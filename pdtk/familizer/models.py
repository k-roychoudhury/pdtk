r""" pdtk.familizer.models module """


# importing standard modules ==================================================
from typing import List, Union, Dict, Tuple


# importing third-party modules ===============================================
from pydantic import (
    BaseModel,
    Field
)
from bs4 import (
    Tag,
    ResultSet,
    BeautifulSoup
)


# importing custom modules ====================================================
from concepts.utils import extract_patent_number_tuple
from concepts.patent_number import PatentNumber


# model definitions ===========================================================
class FamilizerApiResponse(BaseModel):
    r""" model defining data elements of the response received from the 
    Familizer API """

    payload: Dict[PatentNumber, Union[List[PatentNumber], None]] = Field(...)


    @classmethod
    def parse_familizer_response_content(
        cls,
        response_content: bytes
    ) -> 'FamilizerApiResponse':
        r""" Class Method: Parse Familizer Response Content 
        - arguments:
            - `response_content`: an object of type `bytes`; from the response 
            content
        - returns:
            - an object of type `FamilizerApiResponse`
        - raises:
            - `TypeError`
        """
        soup: BeautifulSoup = BeautifulSoup(response_content, "lxml")
        container_table: Union[Tag, None] = soup.find("table")
        if container_table is None:
            container_table_type_error: str = "type of 'container_table' is None"
            raise TypeError(container_table_type_error)
        
        inner_table_tags: ResultSet[Tag] = container_table\
            .find_all("table", recursive=False)

        result_dict: Dict[str, Union[List[str], None]] = dict()
        for table in inner_table_tags:
            table_data_tags: Tuple[str, str, str, str] = \
                tuple((item.text for item in table.find_all("td")))
            
            input_patent_number: str = table_data_tags[0]
            table_data_row: str = table_data_tags[1]

            if table_data_row == "Not found":
                result_dict[input_patent_number] = None
                continue
            elif "A member of the same family as" in table_data_row:
                family_patent_number: str = table_data_row\
                    .replace("A member of the same family as", "").strip()
                result_dict[input_patent_number] = \
                    result_dict[family_patent_number]
                continue
            else:
                result_dict[input_patent_number] = \
                    table_data_row.strip().split(" ")
                
        del soup
        # ---------------------------------------------------------------------
        new_result_map: Dict[PatentNumber, Union[List[str], None]] = dict()
        for key, value in result_dict.items():
            
            if value is None:
                continue

            else:
                patent_number_object_list: List[PatentNumber] = [
                    PatentNumber.parse_string(item) for item in value
                ]
                cc, num, kc = extract_patent_number_tuple(key)
                new_key: Union[PatentNumber, None] = None
                for item in patent_number_object_list:
                    if item.patent_number == num:
                        new_key = item
                        break

                patent_number_object_list.remove(new_key)
                new_result_map[new_key] = patent_number_object_list

        return FamilizerApiResponse.construct(payload=new_result_map)
    

    def get_request_inputs(self) -> List[PatentNumber]:
        r""" Instance Method: Get Request Inputs
        - arguments:
        - returns:
            - a list of objects of type `PatentNumber`; 
                - that were input to the API
        """
        return [item for item in self.payload.keys()]


    pass # end of FamilizerApiResponse
