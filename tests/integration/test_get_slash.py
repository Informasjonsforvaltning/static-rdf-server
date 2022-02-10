"""Test cases for the server module."""
from typing import Any

from aiohttp import hdrs
import pytest


@pytest.mark.integration
async def test_get_slash(client: Any, fs: Any) -> None:
    """Should return status 200 OK and html document."""
    expected = (
        "<!doctype html>"
        '<html lang="nb">'
        "<title>Ontologi-typer</title>"
        "<body>"
        "<p>Typer</p>"
        '<p> - <a href="examples">examples</a></p>'
    )

    ontology_type = "examples"
    fs.create_dir(f"/srv/www/static-rdf-server/{ontology_type}")

    headers = {hdrs.ACCEPT: "text/html"}
    response = await client.get("/", headers=headers)

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "nb" in response.headers[hdrs.CONTENT_LANGUAGE]

    text = await response.text()
    assert text == expected


@pytest.mark.integration
async def test_get_slash_ask_for_turtle(client: Any, fs: Any) -> None:
    """Should return status 406 Not Acceptable."""
    fs.create_dir("/srv/www/static-rdf-server/examples")

    headers = {hdrs.ACCEPT: "text/turtle"}
    response = await client.get("/", headers=headers)

    assert response.status == 406
