r""" test.core.test_network module """


# importing standard module ===================================================
from typing import List, Dict
import sys, os, asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest, pprint as pp


# importing to test modules ===================================================
from py_google_patents.core.network import http_get_parse_endpoint_response,\
    http_get_result_endpoint_response


# TEST definition =============================================================
class TestCoreNetwork(unittest.IsolatedAsyncioTestCase):
    r""" class to test methods defined in 'py_google_patents.core.network' module """

    parse_cases: List[str] = [
        "US9145048B2", "hybrid engine", "jet engine", "US914 tytbgh", "WO2004",
        "JP6712254B2", "US2020267996A1", "JP7038889B2", "WO2019204461A1",
        "AT387462B", "EP3182827A4"
    ]

    async def test_http_get_parse_endpoint_response(self) -> None:
        
        for result in await asyncio.gather(
            *[http_get_parse_endpoint_response(item) for item in self.parse_cases]
        ):
            pp.pprint(result, width=150)
        
        return None

    
    async def test_http_get_result_endpoint_response(self) -> None:
        item: str = "patent/{}/en".format(self.parse_cases[0])
        result = await http_get_result_endpoint_response(item)
        pp.pprint(result, width=150)

        return None

    
    pass # end of TestCoreNetwork


# main ========================================================================
if __name__ == "__main__":
    unittest.main()
