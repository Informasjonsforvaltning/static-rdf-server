"""Test cases for the server module."""
import os
from typing import Any

from aiohttp import hdrs, MultipartWriter
import pytest


@pytest.mark.integration
async def test_put_ontology_when_ontology_does_not_exist(client: Any, fs: Any) -> None:
    """Should return status 204 No Content."""
    ontology_type = "examples"
    ontology = "hello-world"

    rdf_file = f"{ontology}.ttl"
    rdf_content = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        rdf_file,
        contents=rdf_content,
    )
    html_file = f"{ontology}.html"
    html_content = '<p>Server says "Hello, world!"</p>'
    fs.create_file(
        html_file,
        contents=html_content,
    )

    fs.create_dir("/srv/www/static-rdf-server")

    with open(rdf_file, "rb") as file:
        ontology_rdf = file.read()
    with open(html_file, "rb") as file:
        ontology_html = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_rdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename=rdf_file,
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"
        # add the HTML-representation
        p = mpwriter.append(ontology_html)
        p.set_content_disposition(
            "attachment",
            name="ontology-html-file",
            filename=html_file,
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )

    assert response.status == 204


@pytest.mark.integration
async def test_put_ontology_when_ontology_does_exist(client: Any, fs: Any) -> None:
    """Should return status 204 No Content."""
    ontology_type = "examples"
    ontology = "hello-world"

    rdf_file = f'/srv/www/static-rdf-server"/{ontology_type}/{ontology}/{ontology}.ttl'
    rdf_content = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        rdf_file,
        contents=rdf_content,
    )
    html_file = (
        f'/srv/www/static-rdf-server"/{ontology_type}/{ontology}/{ontology}.html'
    )
    html_content = '<p>Server says "Hello, world!"</p>'
    fs.create_file(
        html_file,
        contents=html_content,
    )

    fs.create_dir("/srv/www/static-rdf-server")

    with open(rdf_file, "rb") as file:
        ontology_rdf = file.read()
    with open(html_file, "rb") as file:
        ontology_html = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_rdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename=f"{ontology}.ttl",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"
        # add the HTML-representation
        p = mpwriter.append(ontology_html)
        p.set_content_disposition(
            "attachment",
            name="ontology-html-file",
            filename=f"{ontology}.html",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )

    assert response.status == 204


@pytest.mark.integration
async def test_put_ontology_when_when_filename_and_ontology_does_not_match(
    client: Any, fs: Any
) -> None:
    """Should return status 400 Bad Request."""
    ontology_type = "examples"
    ontology = "hello-world"

    rdf_file = "not_matching_file_name.ttl"
    rdf_content = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        rdf_file,
        contents=rdf_content,
    )

    fs.create_dir("/srv/www/static-rdf-server")

    with open(rdf_file, "rb") as file:
        ontology_rdf = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_rdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename=rdf_file,
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )

    assert response.status == 400
    body = await response.json()
    assert "Filename and ontology must match." == body["detail"]


@pytest.mark.integration
async def test_put_ontology_file_not_readable(client: Any, fs: Any) -> None:
    """Should return status 400 Bad Request."""
    ontology_type = "contract-tests"
    ontology = "hello-world"

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
            filename=f"{ontology}.ttl",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )

    assert response.status == 400
    body = await response.json()
    assert f'Ontology file "{ontology}.ttl" could not be read.' == body["detail"]


@pytest.mark.integration
async def test_put_ontology_not_valid_extension(client: Any, fs: Any) -> None:
    """Should return status 400 Bad Request."""
    ontology_type = "examples"
    ontology = "hello-world"
    not_valid_extension = "exe"

    rdf_content = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        f"{ontology}.ttl",
        contents=rdf_content,
    )

    fs.create_dir("/srv/www/static-rdf-server")

    with open(f"{ontology}.ttl", "rb") as file:
        ontology_rdf = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_rdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename=f"{ontology}.{not_valid_extension}",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )
    assert response.status == 400
    body = await response.json()
    assert f"Not valid file-extension {not_valid_extension}." == body["detail"]


@pytest.mark.integration
async def test_put_ontology_rdf_file_not_parsable(client: Any, fs: Any) -> None:
    """Should return status 400 Bad Request."""
    ontology_type = "contract-tests"
    ontology = "hello-world"

    ontology_file_not_parsable = "not_parsable_rdf_file.ttl"
    contents = "no rdf content here"

    fs.create_file(ontology_file_not_parsable, contents=contents)
    fs.create_dir("/srv/www/static-rdf-server")

    with open(ontology_file_not_parsable, "rb") as file:
        ontology_rdf = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_rdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename=f"{ontology}.ttl",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )

    assert response.status == 400
    body = await response.json()
    assert f'Ontology file "{ontology}.ttl" could not be parsed.' == body["detail"]


@pytest.mark.integration
async def test_post_ontology_no_api_key(client: Any, fs: Any) -> None:
    """Should return status 403 Forbidden."""
    ontology_type = "examples"
    ontology = "hello-world"

    rdf_content = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        f"{ontology}.ttl",
        contents=rdf_content,
    )
    html_content = '<p>Server says "Hello, world!"</p>'
    fs.create_file(
        f"{ontology}.html",
        contents=html_content,
    )

    fs.create_dir("/srv/www/static-rdf-server")

    with open(f"{ontology}.ttl", "rb") as file:
        ontology_rdf = file.read()
    with open(f"{ontology}.html", "rb") as file:
        ontology_html = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_rdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename=f"{ontology}.ttl",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"
        # add the HTML-representation
        p = mpwriter.append(ontology_html)
        p.set_content_disposition(
            "attachment",
            name="ontology-html-file",
            filename=f"{ontology}.html",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"

    response = await client.put(f"/{ontology_type}/{ontology}", data=mpwriter)

    assert response.status == 403
