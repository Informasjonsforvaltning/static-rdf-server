"""Contract test cases the upload ontology."""
import os
from typing import Any

from aiohttp import ClientSession, hdrs, MultipartWriter
import pytest


@pytest.fixture
@pytest.mark.asyncio
async def ontology_to_be_deleted(http_service: Any) -> None:
    """Fixture to create the test-case."""
    # ARRANGE:
    ontology_rdf_file = "tests/files/examples/hello-world/hello-world.ttl"
    ontology_en_html_file = "tests/files/examples/hello-world/hello-world-en.html"
    ontology_nb_html_file = "tests/files/examples/hello-world/hello-world-nb.html"
    ontology_nn_html_file = "tests/files/examples/hello-world/hello-world-nn.html"

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(open(ontology_rdf_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-rdf-file", filename="hello-world.ttl"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"

        # add the HTML-representations: en
        p = mpwriter.append(open(ontology_en_html_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-html-file", filename="hello-world-en.html"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"

        # add the HTML-representations: nb
        p = mpwriter.append(open(ontology_nb_html_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-html-file", filename="hello-world-nb.html"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"
        p.headers[hdrs.CONTENT_LANGUAGE] = "nb"

        # add the HTML-representations: nn
        p = mpwriter.append(open(ontology_nn_html_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-html-file", filename="hello-world-nn.html"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"
        p.headers[hdrs.CONTENT_LANGUAGE] = "nn"

    ontology_type = "contract-test"
    ontology = "hello-world-to-be-deleted"

    url = f"{http_service}/{ontology_type}/{ontology}"
    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    async with ClientSession() as session:
        async with session.put(url, headers=headers, data=mpwriter) as response:
            if response.status != 204:
                body = await response.json()
            pass

        # ASSERT
        assert response.status == 204, body


@pytest.mark.contract
@pytest.mark.asyncio
async def test_delete_ontology(http_service: Any, ontology_to_be_deleted: Any) -> None:
    """Should return 204 No Content."""
    ontology_type = "contract-test"
    ontology = "hello-world-to-be-deleted"

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    url = f"{http_service}/{ontology_type}/{ontology}"
    async with ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            if response.status != 204:
                body = await response.json()
            pass
        assert response.status == 204, body

        # Get turtle-representation:
        headers = {hdrs.ACCEPT: "text/turtle"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 404

        # Get html-representations: en
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "en"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 404

        # Get html-representations: nb
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nb"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 404

        # Get html-representations: nn
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nn"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 404

        # Get html-representations: unknown language
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "xx"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 404

        # Get html-representations: default language
        headers = {hdrs.ACCEPT: "text/html"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 404


@pytest.mark.contract
@pytest.mark.asyncio
async def test_delete_ontology_no_api_key(
    http_service: Any, ontology_to_be_deleted: Any
) -> None:
    """Should return 403 Forbidden."""
    ontology_type = "contract-test"
    ontology = "hello-world-to-be-deleted"

    url = f"{http_service}/{ontology_type}/{ontology}"
    async with ClientSession() as session:
        async with session.delete(url) as response:
            pass

    assert response.status == 403
