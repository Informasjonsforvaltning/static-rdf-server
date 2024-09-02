"""Test cases for the server module."""

from textwrap import dedent
from typing import Any

from aiohttp import hdrs
import pytest


@pytest.mark.integration
async def test_get_ontology_type_language_en(client: Any, fs: Any) -> None:
    """Should return status 200 OK and html document."""
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

    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "en"}
    response = await client.get(f"/{ontology_type}", headers=headers)

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]


@pytest.mark.integration
async def test_get_ontology_type_unsupported_language(client: Any, fs: Any) -> None:
    """Should return status 406."""
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

    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "not-supported"}
    response = await client.get(f"/{ontology_type}", headers=headers)

    assert response.status == 406


@pytest.mark.integration
async def test_get_ontology_type_that_does_not_exist(client: Any, fs: Any) -> None:
    """Should return status 404 OK and html document."""
    expected = dedent(
        """
        <!doctype html>
        <html lang="en">
            <head>
                <title>Not found</title>
            </head>
            <body>
                <p>The page you are looking for does not exist.</p>
            </body>
        </html>
    """
    ).strip()

    ontology_type = "does_not_exist"

    headers = {hdrs.ACCEPT: "text/html"}
    response = await client.get(f"/{ontology_type}", headers=headers)

    assert response.status == 404
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]

    text = await response.text()
    assert text == expected


@pytest.mark.integration
async def test_get_ontology_type_with_no_ontologies(client: Any, fs: Any) -> None:
    """Should return status 200 OK and html document."""
    expected = (
        "<!doctype html>"
        '<html lang="nb">'
        "<title>Is_Empty</title>"
        "<body>"
        "<h2>Is_Empty</h2>"
        "<table></table>"
        "</body>"
    )

    ontology_type = "is_empty"
    fs.create_file(
        f"/srv/www/static-rdf-server/data/{ontology_type}/",
    )

    headers = {hdrs.ACCEPT: "text/html"}
    response = await client.get(f"/{ontology_type}", headers=headers)

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]

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


@pytest.mark.integration
async def test_get_ontology_type_with_invalid_path(client: Any, fs: Any) -> None:
    """Should return status 400 when path is invalid."""
    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "en"}
    response = await client.get("/%00", headers=headers)

    assert response.status == 400
    body = await response.json()
    assert "Ontology-type path is not valid." == body["detail"]
