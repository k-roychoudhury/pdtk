r""" pdtk.globals module """



# importing third-party modules ===============================================
from requests import (
    Session,
)


# module variables ============================================================
module_http_session: Session | None = None


# method definitions ==========================================================
def get_http_session() -> Session:
    r""" Module Method: Get Http Session 
    - returns:
        - an object of type `requests.Session`
    """
    global module_http_session
    if module_http_session is None:
        module_http_session = Session()
    return module_http_session
