"""Module for ready route."""
import os

from aiohttp import web


async def ready(request: web.Request) -> web.Response:
    """Return ready response."""
    server_root = request.app["SERVER_ROOT"]

    if not os.path.exists(server_root):
        raise web.HTTPInternalServerError(
            reason=f'Ready fails: SERVER_ROOT "{server_root}" does not exist.'
        ) from None
    return web.Response(text="OK")
