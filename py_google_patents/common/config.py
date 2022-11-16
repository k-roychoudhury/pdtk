r""" py_google_patents.common.config module """


# importing standard modules ==================================================
import logging


# module variables ============================================================
"py_google_patents_logger"
LIB_LOGGER: logging.Logger = logging.getLogger()
formatter: logging.Formatter = logging.Formatter(
    "%(levelname)-8s:[%(asctime)s]:%(filename)-20s:%(module)-15s:"
    "%(funcName)-40s:Line %(lineno)-4d: %(message)s"
)
ch: logging.StreamHandler = logging.StreamHandler()
ch.setFormatter(formatter)
LIB_LOGGER.addHandler(ch)


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


getLibraryLogger().setLevel(logging.DEBUG)
