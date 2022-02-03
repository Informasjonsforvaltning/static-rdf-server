"""Test cases for the server module."""
import os
from typing import Any

from aiohttp import hdrs, MultipartWriter
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


# Testing post ontology
@pytest.mark.integration
async def test_post_ontology(client: Any, fs: Any) -> None:
    """Should return status 201 Created."""
    ontology_rdf_file = "tests/files/examples/hello-world/hello-world.ttl"
    ontology_html_file = "tests/files/examples/hello-world/hello-world.html"

    fs.add_real_file(ontology_rdf_file)
    fs.add_real_file(ontology_html_file)
    fs.create_dir("/srv/www/static-rdf-server")

    with open(ontology_rdf_file, "rb") as file:
        ontology_rdf = file.read()
    with open(ontology_html_file, "rb") as file:
        ontology_html = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_rdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename="hello-world.ttl",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"
        # add the HTML-representation
        p = mpwriter.append(ontology_html)
        p.set_content_disposition(
            "attachment",
            name="ontology-html-file",
            filename="hello-world.html",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"

    ontology_type = "contract-tests"
    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.post(f"/{ontology_type}", headers=headers, data=mpwriter)

    assert response.status == 201
    assert response.headers[hdrs.LOCATION] == f"{ontology_type}/hello-world"


@pytest.mark.integration
async def test_post_ontology_file_not_readable(client: Any, fs: Any) -> None:
    """Should return status 400 Bad Request."""
    ontology_file_not_readable = "tests/files/not_readable_file.pdf"

    fs.add_real_file(ontology_file_not_readable)
    fs.create_dir("/srv/www/static-rdf-server")

    with open(ontology_file_not_readable, "rb") as file:
        ontology_rdf = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_rdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename="hello-world.ttl",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"

    ontology_type = "contract-tests"
    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.post(f"/{ontology_type}", headers=headers, data=mpwriter)

    assert response.status == 400


@pytest.mark.integration
async def test_post_ontology_not_valid_extension(client: Any, fs: Any) -> None:
    """Should return status 400 Bad Request."""
    ontology_file_not_valid_extension = "tests/files/not_valide_extension.exe"
    contents = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(ontology_file_not_valid_extension, contents=contents)
    fs.create_dir("/srv/www/static-rdf-server")

    with open(ontology_file_not_valid_extension, "rb") as file:
        ontology_rdf = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_rdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename=ontology_file_not_valid_extension,
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"

    ontology_type = "contract-tests"
    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.post(f"/{ontology_type}", headers=headers, data=mpwriter)

    assert response.status == 400


@pytest.mark.integration
async def test_post_ontology_rdf_file_not_parsable(client: Any, fs: Any) -> None:
    """Should return status 400 Bad Request."""
    ontology_file_not_readable = "tests/files/not_parsable_rdf_file.ttl"
    contents = "no rdf content here"

    fs.create_file(ontology_file_not_readable, contents=contents)
    fs.create_dir("/srv/www/static-rdf-server")

    with open(ontology_file_not_readable, "rb") as file:
        ontology_rdf = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_rdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename=ontology_file_not_readable,
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"

    ontology_type = "contract-tests"
    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.post(f"/{ontology_type}", headers=headers, data=mpwriter)

    assert response.status == 400


@pytest.mark.integration
async def test_post_ontology_no_api_key(client: Any, fs: Any) -> None:
    """Should return status 403 Forbidden."""
    ontology_rdf_file = "tests/files/examples/hello-world/hello-world.ttl"
    ontology_html_file = "tests/files/examples/hello-world/hello-world.html"

    fs.add_real_file(ontology_rdf_file)
    fs.add_real_file(ontology_html_file)
    fs.create_dir("/srv/www/static-rdf-server")

    with open(ontology_rdf_file, "rb") as file:
        ontology_rdf = file.read()
    with open(ontology_html_file, "rb") as file:
        ontology_html = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_rdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename="hello-world.ttl",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"
        # add the HTML-representation
        p = mpwriter.append(ontology_html)
        p.set_content_disposition(
            "attachment",
            name="ontology-html-file",
            filename="hello-world.html",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"

    ontology_type = "contract-tests"
    response = await client.post(f"/{ontology_type}", data=mpwriter)

    assert response.status == 403
