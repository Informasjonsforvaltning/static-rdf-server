"""Test cases for the server module."""
from typing import Any

from aiohttp import hdrs
import pytest


@pytest.mark.integration
async def test_get_slash(client: Any, fs: Any) -> None:
    """Should return status 200 OK and html document."""
    contents = ""
    fs.create_file(
        "/srv/www/static-rdf-server/index.html",
        contents=contents,
    )

    response = await client.get("/")

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    text = await response.text()
    assert text == contents


@pytest.mark.integration
async def test_get_slash_not_found(client: Any, fs: Any) -> None:
    """Should return status 404 Not found."""
    fs.create_dir("/srv/www/static-rdf-server")

    response = await client.get("/")

    assert response.status == 404
