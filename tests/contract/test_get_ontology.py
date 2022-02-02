"""Contract test cases for ping."""
from typing import Any

from aiohttp import ClientSession, hdrs
import pytest


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_types(http_service: Any) -> None:
    """Should return 200 OK and a html-document."""
    url = f"{http_service}/examples"

    async with ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert text


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_default(http_service: Any) -> None:
    """Should return 200 OK and a html-document."""
    url = f"{http_service}/examples/hello-world"

    async with ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert '<p>Server says "Hello world!"</p>' in text


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_html(http_service: Any) -> None:
    """Should return 200 OK and a html-document."""
    url = f"{http_service}/examples/hello-world"
    headers = {
        hdrs.ACCEPT: "text/html",
    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            text = await response.text()

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert '<p>Server says "Hello world!"</p>' in text


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_turtle(http_service: Any) -> None:
    """Should return 200 OK and a turtle-document."""
    url = f"{http_service}/examples/hello-world"
    headers = {
        hdrs.ACCEPT: "text/turtle",
    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            text = await response.text()

    assert response.status == 200
    assert "text/turtle" in response.headers[hdrs.CONTENT_TYPE]
    assert (
        '<http://example.com/server> <http://example.com/says> "Hello World" .' in text
    )
