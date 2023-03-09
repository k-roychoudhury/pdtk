r""" py_google_patents.config module """

import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, root_validator
import orjson


# module variables ============================================================
module_logger: logging.Logger | None = None


# method definitions ==========================================================
def orjson_dumps(v, *, default) -> str:
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


def configure_module_logger() -> None:
    r""" configures the root logger for the whole module """
    formatter: logging.Formatter = logging.Formatter(
        # "%(levelname):[%(asctime)s]:%(filename):%(module):%(funcName):Line %(lineno): %(message)s"
    )
    stream_handler: logging.StreamHandler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    global module_logger
    module_logger = logging.getLogger("py_google_patents")
    module_logger.addHandler(stream_handler)
    module_logger.setLevel(logging.DEBUG)

    module_logger.debug("configured '{}' logger".format(module_logger.name))

    return None


def get_module_logger() -> logging.Logger:
    r""" returns the global `module_logger` """
    global module_logger
    if module_logger is None:
        configure_module_logger()
        # this makes sure that the global `module_logger` is initialized
    return module_logger


# class definitions ===========================================================
class OrjsonModel(BaseModel):
    r"""
    py_google_patents global pydantic `BaseModel`. utilizes `orjson` for JSON
    serialization
    """

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {datetime: convert_datetime_to_gmt}  # method for customer JSON encoding of datetime fields

    @root_validator()
    def set_null_microseconds(cls, data: dict) -> dict:
        r""" Drops microseconds in all the datetime field values. """
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }

        return {**data, **datetime_fields}

    pass  # end of OrjsonModel
