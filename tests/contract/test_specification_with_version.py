"""Contract test cases the upload ontology."""
import os
from typing import Any

from aiohttp import ClientSession, hdrs, MultipartWriter
import pytest

ONTOLOGY_TYPE = "specifications"
ONTOLOGY = "dcat-ap-no"
VERSION = "v1.1"


@pytest.mark.contract
@pytest.mark.asyncio
async def test_put_specification_with_version(http_service: Any) -> None:
    """Should return 204 No content."""
    # ACT:
    specification_html_file = (
        "tests/files/input/specifications/dcat-ap-no_v1.1/index.html"
    )
    model_image = (
        "tests/files/input/specifications/dcat-ap-no_v1.1/images/dcat-ap-no-1.1p3.png"
    )
    pdf_file = "tests/files/input/specifications/dcat-ap-no_v1.1/files/dcat-ap-no.pdf"

    with MultipartWriter("mixed") as mpwriter:
        # add the HTML-representations: nb
        p = mpwriter.append(open(specification_html_file, "rb"))
        p.set_content_disposition(
            "attachment",
            name="specification-html-file",
            filename="dcat-ap-no-nb.html",
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"
        p.headers[hdrs.CONTENT_LANGUAGE] = "nb"

        # add an image-representations:
        p = mpwriter.append(open(model_image, "rb"))
        p.set_content_disposition(
            "attachment",
            name="image",
            filename="images/dcat-ap-no-1.1p3.png",
        )
        p.headers[hdrs.CONTENT_TYPE] = "image/png"

        # add a pdf-file:
        p = mpwriter.append(open(pdf_file, "rb"))
        p.set_content_disposition(
            "attachment",
            name="specification-pdf-file",
            filename="files/dcat-ap-no.pdf",
        )
        p.headers[hdrs.CONTENT_TYPE] = "application/pdf"
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"

    ontology_type = ONTOLOGY_TYPE
    ontology = ONTOLOGY
    version = VERSION
    url = f"{http_service}/{ontology_type}/{ontology}/{version}"
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
async def test_get_ontology_specification_with_version_html(http_service: Any) -> None:
    """Should return 200 OK and a html-document."""
    ontology_type = ONTOLOGY_TYPE
    ontology = ONTOLOGY
    version = VERSION

    url = f"{http_service}/{ontology_type}/{ontology}/{version}"
    async with ClientSession() as session:
        # Get html-representations: nb
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nb"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: unknown language
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "xx"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: default language
        headers = {hdrs.ACCEPT: "text/html"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]
        assert body


@pytest.mark.contract
@pytest.mark.asyncio
async def test_put_ontology_with_version_no_api_key(http_service: Any) -> None:
    """Should return 403 Forbidden."""
    ontology_rdf_file = "tests/files/input/vocabularies/audience-type/audience-type.ttl"
    ontology_en_html_file = (
        "tests/files/input/vocabularies/audience-type/audience-type-en.html"
    )

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(open(ontology_rdf_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-rdf-file", filename="audience-type.ttl"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"
        # add the HTML-representation
        p = mpwriter.append(open(ontology_en_html_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-html-file", filename="audience-type-en.html"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"

    ontology_type = ONTOLOGY_TYPE
    ontology = ONTOLOGY
    version = VERSION

    url = f"{http_service}/{ontology_type}/{ontology}/{version}"
    async with ClientSession() as session:
        async with session.put(url, data=mpwriter) as response:
            pass
        assert response.status == 403
