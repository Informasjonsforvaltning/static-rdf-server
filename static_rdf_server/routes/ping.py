"""Module for ping route."""
from aiohttp import web


async def ping(request: web.Request) -> web.Response:
    """Return ping response."""
    return web.Response(text="OK")
