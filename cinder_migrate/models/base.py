import functools
import pydantic


class BaseModel(pydantic.BaseModel):
    class Config:
        keep_untouched = (functools.cached_property,)
