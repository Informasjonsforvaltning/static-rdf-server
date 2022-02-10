"""Contract test cases for ontology-type."""
from typing import Any

from aiohttp import ClientSession, hdrs
import pytest


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_ontology_type(http_service: Any) -> None:
    """Should return 200 OK and a html-document with a list of ontologies for the given type."""
    expected_body = (
        "<!doctype html>"
        '<html lang="en">'
        "<title>Contract-Test</title>"
        "<body>"
        "<p><b>Contract-Test</b></p>"
        '<p> - <a href="contract-test/hello-world">hello-world</a></p>'
        '<p> - <a href="contract-test/hello-world-to-be-deleted">hello-world-to-be-deleted</a></p>'
    )

    url = f"{http_service}/contract-test"

    async with ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "en" in response.headers[hdrs.CONTENT_LANGUAGE]

    assert text == expected_body
