"""Test cases for the server module."""
from typing import Any

from aiohttp import hdrs
import pytest


@pytest.mark.integration
async def test_get_ontology_type(client: Any, fs: Any) -> None:
    """Should return status 200 OK and html document."""
    expected = (
        "<!doctype html>"
        '<html lang="en">'
        "<title>Examples</title>"
        "<body>"
        "<p><b>Examples</b></p>"
        '<p> - <a href="examples/hello-world">hello-world</a></p>'
        "</body>"
    )

    ontology_type = "examples"
    ontology = "hello-world"
    fs.create_dir(f"/srv/www/static-rdf-server/data/{ontology_type}")
    contents = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        f"/srv/www/static-rdf-server/data/{ontology_type}/{ontology}/hello-world-nb.html",
        contents=contents,
    )

    headers = {hdrs.ACCEPT: "text/html"}
    response = await client.get(f"/{ontology_type}", headers=headers)

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "en" in response.headers[hdrs.CONTENT_LANGUAGE]

    text = await response.text()
    assert text == expected


@pytest.mark.integration
async def test_get_ontology_type_ask_for_turtle(client: Any, fs: Any) -> None:
    """Should return status 406 Not Acceptable."""
    ontology_type = "ontology-type-1"
    ontology = "hello-world"
    fs.create_dir(f"/srv/www/static-rdf-server/data/{ontology_type}")
    contents = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        f"/srv/www/static-rdf-server/data/{ontology_type}/{ontology}/hello-world-nb.html",
        contents=contents,
    )

    headers = {hdrs.ACCEPT: "text/turtle"}
    response = await client.get(f"/{ontology_type}", headers=headers)

    assert response.status == 406
