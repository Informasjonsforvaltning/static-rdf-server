"""Contract test cases for ping."""
from typing import Any

from aiohttp import ClientSession, hdrs
import pytest


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_slash(http_service: Any) -> None:
    """Should return 200 OK and a html-document."""
    url = f"{http_service}/"

    expected_body = (
        "<!doctype html>"
        '<html lang="nb">'
        "<title>Ontologi-typer</title>"
        "<body>"
        "<p>Typer</p>"
        '<p> - <a href="contract-test">contract-test</a></p>'
        '<p> - <a href="examples">examples</a></p>'
    )

    async with ClientSession() as session:
        async with session.get(url) as response:
            body = await response.text()

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "nb" in response.headers[hdrs.CONTENT_LANGUAGE]
    assert body == expected_body


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_slash_turtle(http_service: Any) -> None:
    """Should return 406 Not Acceptable."""
    url = f"{http_service}/"
    headers = {
        hdrs.ACCEPT: "text/turtle",
    }

    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            pass

    assert response.status == 406
