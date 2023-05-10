r""" tests.py_google_patents.utils.test_network module """


# importing third-party modules ===============================================
import pytest
import pytest_asyncio
from aiohttp import ClientSession
from requests import Session


# test fixtures ===============================================================
@pytest_asyncio.fixture
async def async_client_session() -> ClientSession:
    async with ClientSession() as session:
        yield session


@pytest.fixture
def sync_client_session() -> Session:
    with Session() as session:
        yield session


# test definitions ============================================================
@pytest.mark.parametrize("sample_id", ["patent/US9145048B2/en"])
def test_get_result_response(sample_id: str, sync_client_session: Session) -> None:
    from py_google_patents.utils.network import get_result_response

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
    from py_google_patents.utils.network import get_parse_response

    resp = get_parse_response(sample_text, sync_client_session)
    assert resp.status_code == 200
    print(resp.text)
    return None


@pytest.mark.parametrize("sample_id", ["patent/US9145048B2/en"])
@pytest.mark.asyncio
async def test_get_result_response_async(
    sample_id: str, async_client_session: ClientSession
) -> None:
    from py_google_patents.utils.network import get_result_response_async

    resp = await get_result_response_async(sample_id, async_client_session)
    assert resp.status == 200

    return None


@pytest.mark.parametrize("sample_text", ["hybrid engine", "US91450"])
@pytest.mark.asyncio
async def test_get_parse_response_async(
    sample_text: str, async_client_session: ClientSession
) -> None:
    from py_google_patents.utils.network import get_parse_response_async

    resp = await get_parse_response_async(sample_text, async_client_session)
    assert resp.status == 200
    print(await resp.text())
    return None
