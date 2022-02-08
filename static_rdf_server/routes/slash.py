"""Module for slash route."""
import logging
import os

from aiohttp import web


async def get_slash(request: web.Request) -> web.Response:
    """Return slash response."""
    data_root = request.app["DATA_ROOT"]
    full_path = os.path.join(os.sep, data_root, "index.html")
    logging.debug(f"Looking for full_path: {full_path}")
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            body = f.read()
        return web.Response(text=body, content_type="text/html")

    else:
        raise web.HTTPNotFound() from None
