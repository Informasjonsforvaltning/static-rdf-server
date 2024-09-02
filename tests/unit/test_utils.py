"""Unit test cases for the event-service module."""

from typing import Dict, List

import pytest

from static_rdf_server.utils import (
    ContentTypeNotSupportedException,
    decide_content_and_extension,
)

# Default is the first in the list:
SUPPORTED_CONTENT_TYPES: List[str] = [
    "text/html",
    "text/turtle",
]

# Default is the first in the list:
SUPPORTED_LANGUAGES: List[str] = ["en", "nb", "nn", "en-GB", "nb-NO", "nn-NO"]

EXTENSION_MAP: Dict[str, str] = {
    "text/html": "html",
    "text/turtle": "ttl",
}


@pytest.mark.unit
async def test_decide_content_type_and_extension_default() -> None:
    """Should return defaults."""
    accept_header: List[str] = []
    accept_language_header: List[str] = []

    content_type, content_language, extension = await decide_content_and_extension(
        accept_header,
        SUPPORTED_CONTENT_TYPES,
        accept_language_header,
        SUPPORTED_LANGUAGES,
    )

    assert content_type == SUPPORTED_CONTENT_TYPES[0]
    assert extension == EXTENSION_MAP[SUPPORTED_CONTENT_TYPES[0]]
    assert content_language == SUPPORTED_LANGUAGES[0]


@pytest.mark.unit
async def test_decide_content_type_and_extension_star() -> None:
    """Should return text/html, html and default language."""
    accept_header: List[str] = ["*/*"]
    accept_language_header: List[str] = []

    content_type, content_language, extension = await decide_content_and_extension(
        accept_header,
        SUPPORTED_CONTENT_TYPES,
        accept_language_header,
        SUPPORTED_LANGUAGES,
    )

    assert content_type == SUPPORTED_CONTENT_TYPES[0]
    assert extension == EXTENSION_MAP[SUPPORTED_CONTENT_TYPES[0]]
    assert content_language == SUPPORTED_LANGUAGES[0]


@pytest.mark.unit
async def test_decide_content_type_and_extension_turtle_plus_star() -> None:
    """Should return text/turtle, ttl and default language."""
    accept_header: List[str] = ["text/turtle,*/*"]
    accept_language_header: List[str] = []

    content_type, content_language, extension = await decide_content_and_extension(
        accept_header,
        SUPPORTED_CONTENT_TYPES,
        accept_language_header,
        SUPPORTED_LANGUAGES,
    )

    assert content_type == "text/turtle"
    assert content_language == SUPPORTED_LANGUAGES[0]
    assert extension == EXTENSION_MAP["text/turtle"]


@pytest.mark.unit
async def test_decide_content_type_and_extension_html_plus_star() -> None:
    """Should return text/html, html and default language."""
    accept_header: List[str] = ["text/html,*/*"]
    accept_language_header: List[str] = []

    content_type, content_language, extension = await decide_content_and_extension(
        accept_header,
        SUPPORTED_CONTENT_TYPES,
        accept_language_header,
        SUPPORTED_LANGUAGES,
    )

    assert content_type == "text/html"
    assert content_language == SUPPORTED_LANGUAGES[0]
    assert extension == EXTENSION_MAP["text/html"]


@pytest.mark.unit
async def test_decide_content_type_and_extension_html() -> None:
    """Should return text/html, html and default_language."""
    accept_header: List[str] = ["text/html"]
    accept_language_header: List[str] = []

    content_type, content_language, extension = await decide_content_and_extension(
        accept_header,
        SUPPORTED_CONTENT_TYPES,
        accept_language_header,
        SUPPORTED_LANGUAGES,
    )

    assert content_type == "text/html"
    assert content_language == SUPPORTED_LANGUAGES[0]
    assert extension == EXTENSION_MAP["text/html"]


@pytest.mark.unit
async def test_decide_content_type_and_extension_RDF_turtle() -> None:
    """Should return text/turtle, ttl."""
    accept_header: List[str] = ["text/turtle"]
    accept_language_header: List[str] = []

    content_type, content_language, extension = await decide_content_and_extension(
        accept_header,
        SUPPORTED_CONTENT_TYPES,
        accept_language_header,
        SUPPORTED_LANGUAGES,
    )

    assert content_type == "text/turtle"
    assert content_language == SUPPORTED_LANGUAGES[0]
    assert extension == EXTENSION_MAP["text/turtle"]


@pytest.mark.unit
async def test_decide_content_type_and_extension_not_supported() -> None:
    """Should raise ContentTypeNotSupported exception."""
    accept_header: List[str] = ["not/supported"]
    accept_language_header: List[str] = []

    with pytest.raises(ContentTypeNotSupportedException):
        await decide_content_and_extension(
            accept_header,
            SUPPORTED_CONTENT_TYPES,
            accept_language_header,
            SUPPORTED_LANGUAGES,
        )
