r""" tests.utils.test_network module """


import pytest


# test definitions ============================================================
@pytest.mark.skip
@pytest.mark.parametrize("sample_id", ["patent/US9145048B2/en"])
def test_get_result_response(sample_id: str) -> None:
    from py_google_patents.utils.network import get_result_response

    resp = get_result_response(sample_id)
    assert resp.status_code == 200

    return None


@pytest.mark.parametrize("sample_text", ["hybrid engine", "US91450"])
def test_get_parse_response(sample_text: str) -> None:
    from py_google_patents.utils.network import get_parse_response

    resp = get_parse_response(sample_text)
    assert resp.status_code == 200
    print(resp.content)
    return None
