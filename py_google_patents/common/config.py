r""" py_google_patents.common.config module """


# importing standard modules ==================================================
import logging


# module variables ============================================================
LIB_LOGGER: logging.Logger = logging.getLogger()


# method definitions ==========================================================
def getLibraryLogger() -> logging.Logger:
    r""" Function - Get Library Logger 
    - arguments:
    - returns:
        - a 'logging.Logger' object; the reference contained within module
        variable 'LIB_LOGGER'
    """
    global LIB_LOGGER
    return LIB_LOGGER


