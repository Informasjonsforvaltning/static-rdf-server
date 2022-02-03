"""Test cases for the server module."""
from typing import Any

from aiohttp import hdrs
import pytest


@pytest.mark.integration
async def test_get_slash(client: Any, fs: Any) -> None:
    """Should return status 200 OK and html document."""
    contents = ""
    fs.create_file(
        "/srv/www/static-rdf-server/index.html",
        contents=contents,
    )

    response = await client.get("/")

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    text = await response.text()
    assert text == contents


@pytest.mark.integration
async def test_get_slash_not_found(client: Any, fs: Any) -> None:
    """Should return status 404 Not found."""
    fs.create_dir("/srv/www/static-rdf-server")

    response = await client.get("/")

    assert response.status == 404


@pytest.mark.integration
async def test_get_type_slash(client: Any, fs: Any) -> None:
    """Should return status 200 OK and html document."""
    contents = ""
    fs.create_file(
        "/srv/www/static-rdf-server/examples/index.html",
        contents=contents,
    )

    response = await client.get("/examples")

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    text = await response.text()
    assert text == contents


@pytest.mark.integration
async def test_get_type_slash_not_found(client: Any, fs: Any) -> None:
    """Should return status 404 Not found."""
    fs.create_dir("/srv/www/static-rdf-server/examples")

    response = await client.get("/examples")

    assert response.status == 404


@pytest.mark.integration
async def test_get_rdf_turtle(client: Any, fs: Any) -> None:
    """Should return status 200 OK and RDF as turtle."""
    contents = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1.ttl",
        contents=contents,
    )

    headers = {"accept": "text/turtle"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/turtle" in response.headers[hdrs.CONTENT_TYPE]
    text = await response.text()
    assert text == contents


@pytest.mark.integration
async def test_get_html(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html."""
    contents = '<p>Server says "Hello, world!"</p>'
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1.html",
        contents=contents,
    )

    headers = {"accept": "text/html"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    text = await response.text()
    assert text == contents


@pytest.mark.integration
async def test_get_default(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html."""
    contents = '<p>Server says "Hello, world!"</p>'
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1.html",
        contents=contents,
    )

    response = await client.get("/ontology-type-1/ontology-1")

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    text = await response.text()
    assert text == contents


@pytest.mark.integration
async def test_get_not_acceptable(client: Any, fs: Any) -> None:
    """Should return status 406 Not Acceptable."""
    contents = '<p>Server says "Hello, world!"</p>'
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1.html",
        contents=contents,
    )

    headers = {"accept": "not/acceptable"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 406


@pytest.mark.integration
async def test_representation_not_found(client: Any, fs: Any) -> None:
    """Should return status 406 Not Acceptable."""
    contents = '<p>Server says "Hello, world!"</p>'
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1.json",
        contents=contents,
    )

    headers = {"accept": "text/turtle"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 406


@pytest.mark.integration
async def test_get_ontology_not_found(client: Any, fs: Any) -> None:
    """Should return status 404 Not Found."""
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1.ttl"
    )

    headers = {"accept": "text/turtle"}
    response = await client.get("/ontology/not_found", headers=headers)

    assert response.status == 404
