from pydantic import ValidationError
from types import FunctionType
from falcon import HTTPBadRequest, HTTPInternalServerError
from loguru import logger


def httperr_on_validate(func: FunctionType):
    async def wrapper(self, req, resp, *args, **kwargs):
        try:
            return await func(self, req, resp, *args, **kwargs)
        except ValidationError as e:
            raise HTTPBadRequest(
                title='Validation error',
                description=repr(e)
            )
    wrapper.__annotations__ = func.__annotations__
    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


def httperr_on_error(func: FunctionType):
    async def wrapper(self, req, resp, *args, **kwargs):
        try:
            return await func(self, req, resp, *args, **kwargs)
        except Exception as e:
            logger.exception(e)
            raise HTTPBadRequest(
                title='Internal error',
                description=repr(e)
            )
    wrapper.__annotations__ = func.__annotations__ # noqa
    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper
