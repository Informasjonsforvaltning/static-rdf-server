"""Test cases for the server module."""

import os
from typing import Any

from aiohttp import hdrs, MultipartWriter
import pytest


@pytest.mark.integration
async def test_put_ontology_when_ontology_does_not_exist(client: Any, fs: Any) -> None:
    """Should return status 201 Created and location header."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"

    fs.create_dir(f"{data_root}/{ontology_type}")

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
    image_file = os.path.join("images", f"{ontology}.png")
    fs.create_file(
        image_file,
    )
    pdf_file = os.path.join("files", f"{ontology}.pdf")
    fs.create_file(
        pdf_file,
    )

    with open(rdf_file, "rb") as file:
        ontology_rdf = file.read()
    with open(html_file, "rb") as file:
        ontology_html = file.read()
    with open(image_file, "rb") as file:
        ontology_png = file.read()
    with open(pdf_file, "rb") as file:
        ontology_pdf = file.read()

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
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"
        # add an image:
        p = mpwriter.append(ontology_png)
        p.set_content_disposition(
            "attachment",
            name="ontology-png-file",
            filename=image_file,
        )
        p.headers[hdrs.CONTENT_TYPE] = "image/png"
        # add a pdf file
        p = mpwriter.append(ontology_pdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-pdf-file",
            filename=pdf_file,
        )
        p.headers[hdrs.CONTENT_TYPE] = "application/pdf"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )

    assert response.status == 201
    assert f"{ontology_type}/{ontology}" == response.headers[hdrs.LOCATION]


@pytest.mark.integration
async def test_put_ontology_when_ontology_does_not_exist_given_version(
    client: Any, fs: Any
) -> None:
    """Should return status 201 Created and location header."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"
    version = "v1"

    fs.create_dir(f"{data_root}/{ontology_type}/{version}")

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
    image_file = os.path.join("images", f"{ontology}.png")
    fs.create_file(
        image_file,
    )
    pdf_file = os.path.join("files", f"{ontology}.pdf")
    fs.create_file(
        pdf_file,
    )

    with open(rdf_file, "rb") as file:
        ontology_rdf = file.read()
    with open(html_file, "rb") as file:
        ontology_html = file.read()
    with open(image_file, "rb") as file:
        ontology_png = file.read()
    with open(pdf_file, "rb") as file:
        ontology_pdf = file.read()

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
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"
        # add an image:
        p = mpwriter.append(ontology_png)
        p.set_content_disposition(
            "attachment",
            name="ontology-png-file",
            filename=image_file,
        )
        p.headers[hdrs.CONTENT_TYPE] = "image/png"
        # add a pdf file
        p = mpwriter.append(ontology_pdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-pdf-file",
            filename=pdf_file,
        )
        p.headers[hdrs.CONTENT_TYPE] = "application/pdf"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}/{version}", headers=headers, data=mpwriter
    )

    assert response.status == 201
    assert f"{ontology_type}/{ontology}" == response.headers[hdrs.LOCATION]


@pytest.mark.integration
async def test_put_ontology_when_ontology_does_exist(client: Any, fs: Any) -> None:
    """Should return status 204 No Content."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"

    fs.create_dir(f"{data_root}/{ontology_type}/{ontology}")

    rdf_file = f'/srv/www/static-rdf-server"/{ontology_type}/{ontology}/{ontology}.ttl'
    rdf_content = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        rdf_file,
        contents=rdf_content,
    )
    html_file = (
        f'/srv/www/static-rdf-server"/{ontology_type}/{ontology}/{ontology}.html'
    )
    html_content = """
    <!doctype html>
    <html lang="en">
    <title>Hello world</title>

    <body>
        <p>Hello, world!</p>
        <p>This greeting was last updated 2022-02-08 14:49:40.</p>
        <img src="images/hello-world.png" alt="Hello World">
        <a href="files/hello-world-en.pdf" download="hello-world-en.pdf">Download the pdf</a>
    """

    fs.create_file(
        html_file,
        contents=html_content,
    )

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
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )

    assert response.status == 204
    assert hdrs.LOCATION != response.headers


@pytest.mark.integration
async def test_put_ontology_xml_when_ontology_does_exist(client: Any, fs: Any) -> None:
    """Should return status 204 No Content."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"

    fs.create_dir(f"{data_root}/{ontology_type}/{ontology}")

    rdf_file = f'/srv/www/static-rdf-server"/{ontology_type}/{ontology}/{ontology}.xml'
    rdf_content = """<?xml version="1.0" encoding="utf-8"?>
    <rdf:RDF
        xmlns:ns1="http://example.com/"
        xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
        <rdf:Description rdf:about="http://example.com/drewp">
            <ns1:says>Hello World</ns1:says>
        </rdf:Description>
    </rdf:RDF>
    """
    fs.create_file(
        rdf_file,
        contents=rdf_content,
    )
    html_file = (
        f'/srv/www/static-rdf-server"/{ontology_type}/{ontology}/{ontology}.html'
    )
    html_content = """
    <!doctype html>
    <html lang="en">
    <title>Hello world</title>

    <body>
        <p>Hello, world!</p>
        <p>This greeting was last updated 2022-02-08 14:49:40.</p>
        <img src="images/hello-world.png" alt="Hello World">
        <a href="files/hello-world-en.pdf" download="hello-world-en.pdf">Download the pdf</a>
    """

    fs.create_file(
        html_file,
        contents=html_content,
    )

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
            filename=f"{ontology}.xml",
        )
        p.headers[hdrs.CONTENT_TYPE] = "application/rdf+xml"
        # add the HTML-representation
        p = mpwriter.append(ontology_html)
        p.set_content_disposition(
            "attachment",
            name="ontology-html-file",
            filename=f"{ontology}.html",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )

    assert response.status == 204
    assert hdrs.LOCATION != response.headers


@pytest.mark.integration
async def test_put_ontology_when_ontology_type_does_not_exist(
    client: Any, fs: Any
) -> None:
    """Should return status 404 Not Found."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"

    fs.create_dir(f"{data_root}")

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
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )

    assert response.status == 404


@pytest.mark.integration
async def test_put_ontology_when_when_content_language_header_is_not_given(
    client: Any, fs: Any
) -> None:
    """Should return status 400 Bad Request."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"

    fs.create_dir(f"{data_root}/{ontology_type}")

    html_file = f"{data_root}/{ontology_type}/{ontology}/{ontology}.html"
    html_content = '<p>Server says "Hello, world!"</p>'
    fs.create_file(
        html_file,
        contents=html_content,
    )

    with open(html_file, "rb") as file:
        ontology_html = file.read()

    with MultipartWriter("mixed") as mpwriter:
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

    assert response.status == 400
    body = await response.json()
    assert "For html-content, Content-Language header must be given." == body["detail"]


@pytest.mark.integration
async def test_put_ontology_file_not_readable(client: Any, fs: Any) -> None:
    """Should return status 400 Bad Request."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"

    fs.create_dir(f"{data_root}/{ontology_type}")

    ontology_file_not_readable = "tests/files/not_readable_file.pdf"

    fs.add_real_file(ontology_file_not_readable)

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
    assert f'Ontology file "{ontology}.ttl" has not valid content' in body["detail"]


@pytest.mark.integration
async def test_put_ontology_not_valid_extension(client: Any, fs: Any) -> None:
    """Should return status 400 Bad Request."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"

    fs.create_dir(f"{data_root}/{ontology_type}")

    not_valid_extension = "exe"

    rdf_content = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        f"{ontology}.ttl",
        contents=rdf_content,
    )

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
    assert f"Not supported file-extension '{not_valid_extension}'." == body["detail"]


@pytest.mark.integration
async def test_put_ontology_rdf_file_not_parsable(client: Any, fs: Any) -> None:
    """Should return status 400 Bad Request."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"

    fs.create_dir(f"{data_root}/{ontology_type}")

    ontology_file_not_parsable = "not_parsable_rdf_file.ttl"
    contents = "no rdf content here"

    fs.create_file(ontology_file_not_parsable, contents=contents)

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
    assert f'Ontology file "{ontology}.ttl" has not valid content' in body["detail"]


@pytest.mark.integration
async def test_post_ontology_no_api_key(client: Any, fs: Any) -> None:
    """Should return status 403 Forbidden."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"

    fs.create_dir(f"{data_root}/{ontology_type}")

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


@pytest.mark.integration
async def test_put_ontology_when_content_type_is_not_supported(
    client: Any, fs: Any
) -> None:
    """Should return status 415 Unsupported Media Type."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"

    fs.create_dir(f"{data_root}/{ontology_type}")

    json_file = f"{ontology}.json"
    json_content = """
    "sender": "<http://example.com/drewp>",
    "action": "<http://example.com/says>",
    "message": "Hello World",
    """
    fs.create_file(
        json_file,
        contents=json_content,
    )

    with open(json_file, "rb") as file:
        ontology_json = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_json)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename=json_file,
        )
        p.headers[hdrs.CONTENT_TYPE] = "application/json"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )

    assert response.status == 415


@pytest.mark.integration
async def test_put_ontology_when_when_content_type_header_is_not_given(
    client: Any, fs: Any
) -> None:
    """Should return status 400 Bad Request."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"

    fs.create_dir(f"{data_root}/{ontology_type}")

    html_file = f"{ontology}.html"
    html_content = '<p>Server says "Hello, world!"</p>'
    fs.create_file(
        html_file,
        contents=html_content,
    )

    with open(html_file, "rb") as file:
        ontology_html = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the HTML-representation
        p = mpwriter.append(ontology_html)
        p.set_content_disposition(
            "attachment",
            name="ontology-html-file",
            filename=html_file,
        )
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"
        p.headers.pop(hdrs.CONTENT_TYPE)

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )

    assert response.status == 400
    body = await response.json()
    assert "Content-Type header must be given." == body["detail"]


@pytest.mark.integration
async def test_put_ontology_when_ontology_or_type_is_invalid(
    client: Any, fs: Any
) -> None:
    """Should return status 400 Bad Request."""
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
    image_file = os.path.join("images", f"{ontology}.png")
    fs.create_file(
        image_file,
    )
    pdf_file = os.path.join("files", f"{ontology}.pdf")
    fs.create_file(
        pdf_file,
    )

    with open(rdf_file, "rb") as file:
        ontology_rdf = file.read()
    with open(html_file, "rb") as file:
        ontology_html = file.read()
    with open(image_file, "rb") as file:
        ontology_png = file.read()
    with open(pdf_file, "rb") as file:
        ontology_pdf = file.read()

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
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"
        # add an image:
        p = mpwriter.append(ontology_png)
        p.set_content_disposition(
            "attachment",
            name="ontology-png-file",
            filename=image_file,
        )
        p.headers[hdrs.CONTENT_TYPE] = "image/png"
        # add a pdf file
        p = mpwriter.append(ontology_pdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-pdf-file",
            filename=pdf_file,
        )
        p.headers[hdrs.CONTENT_TYPE] = "application/pdf"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put("/%00/%00", headers=headers, data=mpwriter)
    assert response.status == 400
    body = await response.json()
    assert "Ontology path is not valid." == body["detail"]

    response = await client.put("/etc/passwd\0.txt", headers=headers, data=mpwriter)
    assert response.status == 400
    body = await response.json()
    assert "Ontology path is not valid." == body["detail"]


@pytest.mark.integration
async def test_put_ontology_when_filename_is_too_long(client: Any, fs: Any) -> None:
    """Should return status 400 Bad Request."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"

    fs.create_dir(f"{data_root}/{ontology_type}/{ontology}")

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
    image_file = os.path.join("images", f"{ontology}.png")
    fs.create_file(
        image_file,
    )
    pdf_file = os.path.join("files", f"{ontology}.pdf")
    fs.create_file(
        pdf_file,
    )

    with open(rdf_file, "rb") as file:
        ontology_rdf = file.read()
    with open(html_file, "rb") as file:
        ontology_html = file.read()
    with open(image_file, "rb") as file:
        ontology_png = file.read()
    with open(pdf_file, "rb") as file:
        ontology_pdf = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_rdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename="filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars.ttl",
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
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"
        # add an image:
        p = mpwriter.append(ontology_png)
        p.set_content_disposition(
            "attachment",
            name="ontology-png-file",
            filename="hello-world.png",
        )
        p.headers[hdrs.CONTENT_TYPE] = "image/png"
        # add a pdf file
        p = mpwriter.append(ontology_pdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-pdf-file",
            filename="hello-world.pdf",
        )
        p.headers[hdrs.CONTENT_TYPE] = "application/pdf"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )
    assert response.status == 400
    body = await response.json()
    assert "Ontology file is not valid." == body["detail"]


@pytest.mark.integration
async def test_put_ontology_when_filename_is_invalid(client: Any, fs: Any) -> None:
    """Should return status 400 Bad Request."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"
    ontology = "hello-world"

    fs.create_dir(f"{data_root}/{ontology_type}/{ontology}")

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
    image_file = os.path.join("images", f"{ontology}.png")
    fs.create_file(
        image_file,
    )
    pdf_file = os.path.join("files", f"{ontology}.pdf")
    fs.create_file(
        pdf_file,
    )

    with open(rdf_file, "rb") as file:
        ontology_rdf = file.read()
    with open(html_file, "rb") as file:
        ontology_html = file.read()
    with open(image_file, "rb") as file:
        ontology_png = file.read()
    with open(pdf_file, "rb") as file:
        ontology_pdf = file.read()

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(ontology_rdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-rdf-file",
            filename="filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars-filename-longer-than-256-chars.ttl",
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
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"
        # add an image:
        p = mpwriter.append(ontology_png)
        p.set_content_disposition(
            "attachment",
            name="ontology-png-file",
            filename="hello-world.png",
        )
        p.headers[hdrs.CONTENT_TYPE] = "image/png"
        # add a pdf file
        p = mpwriter.append(ontology_pdf)
        p.set_content_disposition(
            "attachment",
            name="ontology-pdf-file",
            filename="hello-world.pdf",
        )
        p.headers[hdrs.CONTENT_TYPE] = "application/pdf"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(
        f"/{ontology_type}/{ontology}", headers=headers, data=mpwriter
    )
    assert response.status == 400
    body = await response.json()
    assert "Ontology file is not valid." == body["detail"]
