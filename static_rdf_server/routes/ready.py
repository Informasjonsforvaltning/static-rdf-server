"""Module for ready route."""
import os

from aiohttp import web


async def ready(request: web.Request) -> web.Response:
    """Return ready response."""
    data_root = request.app["DATA_ROOT"]

    if not os.path.exists(data_root):
        raise web.HTTPInternalServerError(
            reason=f'Ready fails: DATA_ROOT "{data_root}" does not exist.'
        ) from None
    return web.Response(text="OK")
