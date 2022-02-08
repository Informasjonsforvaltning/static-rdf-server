"""Test cases for the server module."""
from typing import Any

from aiohttp import hdrs
import pytest


@pytest.mark.integration
async def test_get_rdf_turtle(client: Any, fs: Any) -> None:
    """Should return status 200 OK and RDF as turtle."""
    contents = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1.ttl",
        contents=contents,
    )

    headers = {hdrs.ACCEPT: "text/turtle"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/turtle" in response.headers[hdrs.CONTENT_TYPE]
    text = await response.text()
    assert text == contents


@pytest.mark.integration
async def test_get_html_default_language(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html in language nb."""
    contents = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents,
    )

    headers = {hdrs.ACCEPT: "text/html"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "nb" in response.headers[hdrs.CONTENT_LANGUAGE]

    document = await response.text()
    assert '<html lang="nb">' in document
    text = await response.text()
    assert text == contents


@pytest.mark.integration
async def test_get_default(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html."""
    contents = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents,
    )

    response = await client.get("/ontology-type-1/ontology-1")

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "nb" in response.headers[hdrs.CONTENT_LANGUAGE]
    document = await response.text()
    assert '<html lang="nb">' in document
    assert document == contents


@pytest.mark.integration
async def test_get_html_nb_language(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html in language nb."""
    contents = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents,
    )

    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nb"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "nb" in response.headers[hdrs.CONTENT_LANGUAGE]

    document = await response.text()
    assert '<html lang="nb">' in document
    assert document == contents


@pytest.mark.integration
async def test_get_html_nn_language(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html in language nb."""
    contents = """
    <!doctype html>
    <html lang="nn">
    <title>Hallo verda</title>

    <body>
        <p>Hallo, verda!</p>
        <p>Denne helsinga vart sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1-nn.html",
        contents=contents,
    )

    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nn"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "nn" in response.headers[hdrs.CONTENT_LANGUAGE]

    document = await response.text()
    assert '<html lang="nn">' in document
    assert document == contents


@pytest.mark.integration
async def test_get_html_en_language(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html in language en."""
    contents = """
    <!doctype html>
    <html lang="en">
    <title>Hello world</title>

    <body>
        <p>Hello, world!</p>
        <p>This greeting was last updated 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1-en.html",
        contents=contents,
    )

    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "en"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "en" in response.headers[hdrs.CONTENT_LANGUAGE]

    document = await response.text()
    assert '<html lang="en">' in document
    assert document == contents


@pytest.mark.integration
async def test_get_accept_not_acceptable(client: Any, fs: Any) -> None:
    """Should return status 406 Not Acceptable."""
    contents = '<p>Server says "Hello, world!"</p>'
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1.html",
        contents=contents,
    )

    headers = {hdrs.ACCEPT: "not/acceptable"}
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

    headers = {hdrs.ACCEPT: "text/turtle"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 406


@pytest.mark.integration
async def test_get_ontology_not_found(client: Any, fs: Any) -> None:
    """Should return status 404 Not Found."""
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1.ttl"
    )

    headers = {hdrs.ACCEPT: "text/turtle"}
    response = await client.get("/ontology/not_found", headers=headers)

    assert response.status == 404


@pytest.mark.integration
async def test_get_html_en_language_when_en_does_not_exist(
    client: Any, fs: Any
) -> None:
    """Should return status 200 OK and body as html in language nb."""
    contents = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents,
    )

    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "en"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "nb" in response.headers[hdrs.CONTENT_LANGUAGE]

    document = await response.text()
    assert '<html lang="nb">' in document
    assert document == contents


@pytest.mark.integration
async def test_get_html_nn_language_when_nn_does_not_exist(
    client: Any, fs: Any
) -> None:
    """Should return status 200 OK and body as html in language nb."""
    contents = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents,
    )

    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nn"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
    assert "nb" in response.headers[hdrs.CONTENT_LANGUAGE]

    document = await response.text()
    assert '<html lang="nb">' in document
    assert document == contents
