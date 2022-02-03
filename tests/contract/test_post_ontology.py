"""Contract test cases for ping."""
import os
from typing import Any

from aiohttp import ClientSession, hdrs, MultipartWriter
import pytest


@pytest.mark.contract
@pytest.mark.asyncio
async def test_put_ontology(http_service: Any) -> None:
    """Should return 204 No content."""
    ontology_rdf_file = "tests/files/examples/hello-world/hello-world.ttl"
    ontology_html_file = "tests/files/examples/hello-world/hello-world.html"

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(open(ontology_rdf_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-rdf-file", filename="hello-world.ttl"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"
        # add the HTML-representation
        p = mpwriter.append(open(ontology_html_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-html-file", filename="hello-world.html"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"

    ontology_type = "contract-test"
    ontology = "hello-world"

    url = f"{http_service}/{ontology_type}/{ontology}"
    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    async with ClientSession() as session:
        async with session.put(url, headers=headers, data=mpwriter) as response:
            pass
        assert response.status == 204

        headers = {hdrs.ACCEPT: "text/turtle"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/turtle" in response.headers[hdrs.CONTENT_TYPE]
        with open(ontology_rdf_file) as expected:
            assert body == expected.read()

        headers = {hdrs.ACCEPT: "text/html"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
        with open(ontology_html_file) as expected:
            assert body == expected.read()


@pytest.mark.contract
@pytest.mark.asyncio
async def test_post_ontology_no_api_key(http_service: Any) -> None:
    """Should return 403 Forbidden."""
    ontology_rdf_file = "tests/files/examples/hello-world/hello-world.ttl"
    ontology_html_file = "tests/files/examples/hello-world/hello-world.html"

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(open(ontology_rdf_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-rdf-file", filename="hello-world.ttl"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"
        # add the HTML-representation
        p = mpwriter.append(open(ontology_html_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-html-file", filename="hello-world.html"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"

    ontology_type = "contract-test"
    ontology = "hello-world"

    url = f"{http_service}/{ontology_type}/{ontology}"
    async with ClientSession() as session:
        async with session.put(url, data=mpwriter) as response:
            pass
        assert response.status == 403
