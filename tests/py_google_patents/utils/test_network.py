r""" tests.py_google_patents.utils.test_network module """


# importing third-party modules ===============================================
import pytest
from aiohttp import ClientSession
from requests import Session


# importing custom modules ====================================================
from py_google_patents.utils.network import (
    get_result_response,
    get_parse_response,
    get_result_response_async,
    get_parse_response_async
)


# test definitions ============================================================
@pytest.mark.parametrize("sample_id", ["patent/US9145048B2/en"])
def test_get_result_response(sample_id: str, sync_client_session: Session) -> None:
    resp = get_result_response(sample_id, sync_client_session)
    assert resp.status_code == 200
    return None


@pytest.mark.parametrize(
    "sample_text",
    ["hybrid engine", "US91450", "213123xvds325341", "US9567832 hybrid"]
)
def test_get_parse_response(
    sample_text: str, sync_client_session: Session
) -> None:
    resp = get_parse_response(sample_text, sync_client_session)
    assert resp.status_code == 200
    return None


@pytest.mark.parametrize("sample_id", ["patent/US9145048B2/en"])
@pytest.mark.asyncio
async def test_get_result_response_async(
    sample_id: str, async_client_session: ClientSession
) -> None:
    resp = await get_result_response_async(sample_id, async_client_session)
    assert resp.status == 200
    return None


@pytest.mark.parametrize("sample_text", ["hybrid engine", "US91450"])
@pytest.mark.asyncio
async def test_get_parse_response_async(
    sample_text: str, async_client_session: ClientSession
) -> None:
    resp = await get_parse_response_async(sample_text, async_client_session)
    assert resp.status == 200
    return None
