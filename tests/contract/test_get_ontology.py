"""Contract test cases for ping."""
from typing import Any

from aiohttp import ClientSession, hdrs
import pytest


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_default(http_service: Any) -> None:
    """Should return 200 OK and a html-document in Norwegian bokmål."""
    url = f"{http_service}/examples/hello-world"

    async with ClientSession() as session:
        async with session.get(url) as response:
            document = await response.text()

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "nb" in response.headers[hdrs.CONTENT_LANGUAGE]
    assert '<html lang="nb">' in document
    assert "<p>Hallo, verden!</p>" in document


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_html_norwegian_bokmaal(
    http_service: Any,
) -> None:
    """Should return 200 OK and a html-document in Norwegian bokmål."""
    url = f"{http_service}/examples/hello-world"

    headers = {
        hdrs.ACCEPT_LANGUAGE: "nb",
    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            document = await response.text()

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "nb" in response.headers[hdrs.CONTENT_LANGUAGE]
    assert '<html lang="nb">' in document
    assert "<p>Hallo, verden!</p>" in document


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_html_norwegian_nynorsk(
    http_service: Any,
) -> None:
    """Should return 200 OK and a html-document in Norwegian nynorsk."""
    url = f"{http_service}/examples/hello-world"

    headers = {
        hdrs.ACCEPT_LANGUAGE: "nn",
    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            document = await response.text()

    assert response.status == 200, document
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "nn" in response.headers[hdrs.CONTENT_LANGUAGE]
    assert '<html lang="nn">' in document
    assert "<p>Hallo, verda!</p>" in document


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_html_english(http_service: Any) -> None:
    """Should return 200 OK and a html-document in English."""
    url = f"{http_service}/examples/hello-world"

    headers = {
        hdrs.ACCEPT_LANGUAGE: "en",
    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            document = await response.text()
    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "en" in response.headers[hdrs.CONTENT_LANGUAGE]
    assert '<html lang="en">' in document
    assert "<p>Hello, world!</p>" in document


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_html_german(http_service: Any) -> None:
    """Should return 200 OK and a html-document in Norwegian bokmål."""
    url = f"{http_service}/examples/hello-world"

    headers = {
        hdrs.ACCEPT: "text/html",
        hdrs.ACCEPT_LANGUAGE: "de",
    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            document = await response.text()
    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "nb" in response.headers[hdrs.CONTENT_LANGUAGE]
    assert '<html lang="nb">' in document
    assert "<p>Hallo, verden!</p>" in document


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_html(http_service: Any) -> None:
    """Should return 200 OK and a html-document in Norwegian bokmål."""
    url = f"{http_service}/examples/hello-world"
    headers = {
        hdrs.ACCEPT: "text/html",
    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            document = await response.text()

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "nb" in response.headers[hdrs.CONTENT_LANGUAGE]
    assert '<html lang="nb">' in document
    assert "<p>Hallo, verden!</p>" in document


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
            document = await response.text()

    assert response.status == 200
    assert "text/turtle" in response.headers[hdrs.CONTENT_TYPE]
    assert (
        '<http://example.com/server> <http://example.com/says> "Hello World" .'
        in document
    )
