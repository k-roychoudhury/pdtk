r""" tests.conftest module """


# importing third-party modules ===============================================
import pytest
from requests import Session


# importing custom modules ====================================================
from pdtk.google_patents.client import GooglePatentsClient


# test fixtures ===============================================================
@pytest.fixture(scope='session')
def sync_client_session() -> Session:
    with Session() as session:
        yield session


@pytest.fixture(scope='session')
def gp_client() -> GooglePatentsClient:
    with GooglePatentsClient() as sync_client:
        yield sync_client
