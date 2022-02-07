"""Unit test cases for the event-service module."""
import pytest

from static_rdf_server.utils import (
    ContentTypeNotSupported,
    decide_content_and_extension,
)


@pytest.mark.unit
async def test_decide_content_type_and_extension_default() -> None:
    """Should return text/html, html."""
    content_type, content_language, extension = await decide_content_and_extension()

    assert content_type == "text/html"
    assert content_language == ""
    assert extension == "html"


@pytest.mark.unit
async def test_decide_content_type_and_extension_star() -> None:
    """Should return text/html, html."""
    accept_header = "*/*"
    accept_language_header = ""

    content_type, content_language, extension = await decide_content_and_extension(
        accept_header, accept_language_header
    )

    assert content_type == "text/html"
    assert content_language == ""
    assert extension == "html"


@pytest.mark.unit
async def test_decide_content_type_and_extension_turtle_plus_star() -> None:
    """Should return text/turtle, ttl."""
    accept_header = "text/turtle,*/*"
    accept_language_header = ""

    content_type, content_language, extension = await decide_content_and_extension(
        accept_header, accept_language_header
    )

    assert content_type == "text/turtle"
    assert content_language == ""
    assert extension == "ttl"


@pytest.mark.unit
async def test_decide_content_type_and_extension_html_plus_star() -> None:
    """Should return text/turtle, ttl."""
    accept_header = "text/html,*/*"
    accept_language_header = ""

    content_type, content_language, extension = await decide_content_and_extension(
        accept_header, accept_language_header
    )

    assert content_type == "text/html"
    assert content_language == ""
    assert extension == "html"


@pytest.mark.unit
async def test_decide_content_type_and_extension_html() -> None:
    """Should return text/html, html."""
    accept_header = "text/html"
    accept_language_header = ""

    content_type, content_language, extension = await decide_content_and_extension(
        accept_header, accept_language_header
    )

    assert content_type == "text/html"
    assert content_language == ""
    assert extension == "html"


@pytest.mark.unit
async def test_decide_content_type_and_extension_RDF_turtle() -> None:
    """Should return text/turtle, ttl."""
    accept_header = "text/turtle"
    accept_language_header = ""

    content_type, content_language, extension = await decide_content_and_extension(
        accept_header, accept_language_header
    )

    assert content_type == "text/turtle"
    assert content_language == ""
    assert extension == "ttl"


@pytest.mark.unit
async def test_decide_content_type_and_extension_not_supported() -> None:
    """Should raise ContentTypeNotSupported exception."""
    accept_header = "not/supported"
    accept_language_header = ""

    with pytest.raises(ContentTypeNotSupported):
        await decide_content_and_extension(accept_header, accept_language_header)
