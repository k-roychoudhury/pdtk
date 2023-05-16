r""" pdtk.google_patents.config module """


# importing standard modules ==================================================
from typing import Dict, Any
from datetime import datetime
from zoneinfo import ZoneInfo


# importing third-party modules ===============================================
from pydantic import (
    BaseModel, 
    root_validator
)
import orjson



# method definitions ==========================================================
def orjson_dumps(v, *, default) -> str:
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


# class definitions ===========================================================
class OrjsonModel(BaseModel):
    r"""
    py_google_patents global pydantic `BaseModel`. utilizes `orjson` for JSON
    serialization
    """


    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = { datetime: convert_datetime_to_gmt }
        # method for customer JSON encoding of datetime fields


    @root_validator()
    @classmethod
    def set_null_microseconds(cls, data: Dict[str, Any]) -> Dict[str, Any]:  # noqa
        r""" Drops microseconds in all the datetime field values. """
        datetime_fields = {
            k: v.replace(microsecond=0) \
                for k, v in data.items() if isinstance(k, datetime)
        }

        return {**data, **datetime_fields}


    pass  # end of OrjsonModel
