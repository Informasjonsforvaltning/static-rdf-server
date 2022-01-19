"""Unit test cases for the event-service module."""
from multidict import CIMultiDict, CIMultiDictProxy
import pytest

from static_rdf_server.utils import (
    ContentTypeNotSupported,
    decide_content_type_and_suffix,
)


@pytest.mark.unit
async def test_decide_content_type_and_suffix_default() -> None:
    """Should return text/html, .html."""
    headers = CIMultiDictProxy(CIMultiDict(noAcceptheader=""))

    content_type, suffix = await decide_content_type_and_suffix(headers)

    assert content_type == "text/html"
    assert suffix == ".html"


@pytest.mark.unit
async def test_decide_content_type_and_suffix_star() -> None:
    """Should return text/html, .html."""
    headers = CIMultiDictProxy(CIMultiDict(accept="*/*"))

    content_type, suffix = await decide_content_type_and_suffix(headers)

    assert content_type == "text/html"
    assert suffix == ".html"


@pytest.mark.unit
async def test_decide_content_type_and_suffix_turtle_plus_star() -> None:
    """Should return text/turtle, .ttl."""
    headers = CIMultiDictProxy(CIMultiDict(accept="text/turtle,*/*"))

    content_type, suffix = await decide_content_type_and_suffix(headers)

    assert content_type == "text/turtle"
    assert suffix == ".ttl"


@pytest.mark.unit
async def test_decide_content_type_and_suffix_html_plus_star() -> None:
    """Should return text/turtle, .ttl."""
    headers = CIMultiDictProxy(CIMultiDict(accept="text/html,*/*"))

    content_type, suffix = await decide_content_type_and_suffix(headers)

    assert content_type == "text/html"
    assert suffix == ".html"


@pytest.mark.unit
async def test_decide_content_type_and_suffix_html() -> None:
    """Should return text/html, .html."""
    headers = CIMultiDictProxy(CIMultiDict(accept="text/html"))

    content_type, suffix = await decide_content_type_and_suffix(headers)

    assert content_type == "text/html"
    assert suffix == ".html"


@pytest.mark.unit
async def test_decide_content_type_and_suffix_RDF_turtle() -> None:
    """Should return text/turtle, .ttl."""
    headers = CIMultiDictProxy(CIMultiDict(accept="text/turtle"))

    content_type, suffix = await decide_content_type_and_suffix(headers)

    assert content_type == "text/turtle"
    assert suffix == ".ttl"


@pytest.mark.unit
async def test_decide_content_type_and_suffix_not_supported() -> None:
    """Should raise ContentTypeNotSupported exception."""
    headers = CIMultiDictProxy(CIMultiDict(accept="not/supported"))

    with pytest.raises(ContentTypeNotSupported):
        await decide_content_type_and_suffix(headers)
