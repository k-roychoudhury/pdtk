r""" tests.conftest module """


# importing standard modules ==================================================
import sys
from os.path import dirname, join
# adding the 'src' directory to path - HACK
sys.path.append(
    join(dirname(dirname(__file__)), "src")
)


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


@pytest.fixture(scope='session')
def sync_client_session() -> Session:
    with Session() as session:
        yield session
