"""Test cases for the server module."""

from typing import Any

from aiohttp import hdrs
import pytest
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic


@pytest.mark.integration
async def test_get_rdf_turtle(client: Any, fs: Any) -> None:
    """Should return status 200 OK and RDF as turtle."""
    contents_en = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1.ttl",
        contents=contents_en,
    )

    headers = {hdrs.ACCEPT: "text/turtle"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/turtle; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    text = await response.text()

    g1 = Graph().parse(data=text, format="turtle")
    g2 = Graph().parse(data=contents_en, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic, "graphs are not isomorphic"


@pytest.mark.integration
async def test_get_rdf_json_ld(client: Any, fs: Any) -> None:
    """Should return status 200 OK and RDF as turtle."""
    contents_en = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1.ttl",
        contents=contents_en,
    )

    headers = {hdrs.ACCEPT: "application/ld+json"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "application/ld+json; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]


@pytest.mark.integration
async def test_get_html_default_language(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html in language nb."""
    contents_nb = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents_nb,
    )

    headers = {hdrs.ACCEPT: "text/html"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]

    document = await response.text()
    assert '<html lang="nb">' in document
    text = await response.text()
    assert text == contents_nb


@pytest.mark.integration
async def test_get_default(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html."""
    contents_nb = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents_nb,
    )

    response = await client.get("/ontology-type-1/ontology-1")

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]
    document = await response.text()
    assert '<html lang="nb">' in document
    assert document == contents_nb


@pytest.mark.integration
async def test_get_html_nb_language(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html in language nb."""
    contents_nb = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents_nb,
    )

    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nb"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]

    document = await response.text()
    assert '<html lang="nb">' in document
    assert document == contents_nb


@pytest.mark.integration
async def test_get_html_nn_language(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html in language nb."""
    contents_nn = """
    <!doctype html>
    <html lang="nn">
    <title>Hallo verda</title>

    <body>
        <p>Hallo, verda!</p>
        <p>Denne helsinga vart sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-nn.html",
        contents=contents_nn,
    )

    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nn"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "nn" == response.headers[hdrs.CONTENT_LANGUAGE]

    document = await response.text()
    assert '<html lang="nn">' in document
    assert document == contents_nn


@pytest.mark.integration
async def test_get_html_en_language(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html in language en."""
    contents_en = """
    <!doctype html>
    <html lang="en">
    <title>Hello world</title>

    <body>
        <p>Hello, world!</p>
        <p>This greeting was last updated 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-en.html",
        contents=contents_en,
    )

    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "en"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]

    document = await response.text()
    assert '<html lang="en">' in document
    assert document == contents_en


@pytest.mark.integration
async def test_get_default_given_version(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html."""
    contents_nb = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/v1/ontology-1-nb.html",
        contents=contents_nb,
    )

    response = await client.get("/ontology-type-1/ontology-1/v1")

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]
    document = await response.text()
    assert '<html lang="nb">' in document
    assert document == contents_nb


@pytest.mark.integration
async def test_get_accept_not_acceptable(client: Any, fs: Any) -> None:
    """Should return status 406 Not Acceptable."""
    contents_en = '<p>Server says "Hello, world!"</p>'
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1.html",
        contents=contents_en,
    )

    headers = {hdrs.ACCEPT: "not/acceptable"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 406


@pytest.mark.integration
async def test_representation_not_found(client: Any, fs: Any) -> None:
    """Should return status 406 Not Acceptable."""
    contents_en = '<p>Server says "Hello, world!"</p>'
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1.json",
        contents=contents_en,
    )

    headers = {hdrs.ACCEPT: "text/turtle"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 406


@pytest.mark.integration
async def test_get_ontology_not_found(client: Any, fs: Any) -> None:
    """Should return status 404 Not Found."""
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1.ttl"
    )

    headers = {hdrs.ACCEPT: "text/turtle"}
    response = await client.get("/ontology/not_found", headers=headers)

    assert response.status == 404


@pytest.mark.integration
async def test_get_html_en_language_when_en_does_not_exist(
    client: Any, fs: Any
) -> None:
    """Should return status 200 OK and body as html in language nb."""
    contents_nb = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents_nb,
    )

    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "en"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]

    document = await response.text()
    assert '<html lang="nb">' in document
    assert document == contents_nb


@pytest.mark.integration
async def test_get_html_nn_language_when_nn_does_not_exist(
    client: Any, fs: Any
) -> None:
    """Should return status 200 OK and body as html in language nb."""
    contents_nb = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents_nb,
    )

    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nn"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]

    document = await response.text()
    assert '<html lang="nb">' in document
    assert document == contents_nb


@pytest.mark.integration
async def test_get_html_with_preferred_language_nb(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html in preferred language."""
    contents_nb = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    contents_en = """
    <!doctype html>
    <html lang="en">
    <title>Hello world</title>

    <body>
        <p>Hello, world!</p>
        <p>This greeting was last updated 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents_nb,
    )
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-en.html",
        contents=contents_en,
    )

    headers = {
        hdrs.ACCEPT: "text/html",
        hdrs.ACCEPT_LANGUAGE: "nb-NO;q=0.9,nb,no;q=0.8,nn;q=0.7,en-US;q=0.6,en;q=0.5",
    }
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]
    document = await response.text()
    assert '<html lang="nb">' in document
    assert document == contents_nb


@pytest.mark.integration
async def test_get_html_with_preferred_language_en(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html in preferred language."""
    contents_nb = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    contents_en = """
    <!doctype html>
    <html lang="en">
    <title>Hello world</title>

    <body>
        <p>Hello, world!</p>
        <p>This greeting was last updated 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents_nb,
    )
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-en.html",
        contents=contents_en,
    )

    headers = {
        hdrs.ACCEPT: "text/html",
        hdrs.ACCEPT_LANGUAGE: "en-GB;q=0.9,en,nb-NO;q=0.8,nb;q=0.7,en-US;q=0.6,da;q=0.5,no;q=0.4",
    }
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]
    document = await response.text()
    assert '<html lang="en">' in document
    assert document == contents_en


@pytest.mark.integration
async def test_get_html_with_preferred_language_nb_NO(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html in preferred language."""
    contents_nb = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    contents_en = """
    <!doctype html>
    <html lang="en">
    <title>Hello world</title>

    <body>
        <p>Hello, world!</p>
        <p>This greeting was last updated 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents_nb,
    )
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-en.html",
        contents=contents_en,
    )

    headers = {
        hdrs.ACCEPT: "text/html",
        hdrs.ACCEPT_LANGUAGE: "nb-NO,nb;q=0.9,no;q=0.8,nn;q=0.7,en-US;q=0.6,en;q=0.5",
    }
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "nb-NO" == response.headers[hdrs.CONTENT_LANGUAGE]
    document = await response.text()
    assert '<html lang="nb">' in document
    assert document == contents_nb


@pytest.mark.integration
async def test_get_html_with_preferred_language_en_GB(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html in preferred language."""
    contents_nb = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    contents_en = """
    <!doctype html>
    <html lang="en">
    <title>Hello world</title>

    <body>
        <p>Hello, world!</p>
        <p>This greeting was last updated 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents_nb,
    )
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-en.html",
        contents=contents_en,
    )

    headers = {
        hdrs.ACCEPT: "text/html",
        hdrs.ACCEPT_LANGUAGE: "en-GB,en;q=0.9,nb-NO;q=0.8,nb;q=0.7,en-US;q=0.6,da;q=0.5,no;q=0.4",
    }
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "en-GB" == response.headers[hdrs.CONTENT_LANGUAGE]
    document = await response.text()
    assert '<html lang="en">' in document
    assert document == contents_en


@pytest.mark.integration
async def test_get_html_no_agreeable_language_en(client: Any, fs: Any) -> None:
    """Should return status 200 OK and body as html in default language (nb)."""
    contents_nb = """
    <!doctype html>
    <html lang="nb">
    <title>Hallo verden</title>

    <body>
        <p>Hallo, verden!</p>
        <p>Denne hilsen ble sist oppdatert 2022-02-04 14:20:00.</p>
    """
    contents_en = """
    <!doctype html>
    <html lang="en">
    <title>Hello world</title>

    <body>
        <p>Hello, world!</p>
        <p>This greeting was last updated 2022-02-04 14:20:00.</p>
    """
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-nb.html",
        contents=contents_nb,
    )
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1-en.html",
        contents=contents_en,
    )

    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "da"}
    response = await client.get("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 200
    assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]
    document = await response.text()
    assert '<html lang="nb">' in document
    assert document == contents_nb


@pytest.mark.integration
async def test_get_ontology_with_invalid_path(client: Any, fs: Any) -> None:
    """Should return status 400 when path is invalid."""
    headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "da"}
    response = await client.get("/ontology-type-1/%00", headers=headers)

    assert response.status == 400
    body = await response.json()
    assert "Ontology path is not valid." == body["detail"]


# ---------------------------------------------------------------------- #


# Utils for displaying debug information


def _dump_diff(g1: Graph, g2: Graph) -> None:
    in_both, in_first, in_second = graph_diff(g1, g2)
    print("\nin both:")
    _dump_turtle(in_both)
    print("\nin first:")
    _dump_turtle(in_first)
    print("\nin second:")
    _dump_turtle(in_second)


def _dump_turtle(g: Graph) -> None:
    for _l in g.serialize(format="turtle").splitlines():
        if _l:
            print(_l)
