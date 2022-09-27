"""Contract test cases the upload ontology."""
import os
from typing import Any

from aiohttp import ClientSession, hdrs, MultipartWriter
import pytest


@pytest.mark.contract
@pytest.mark.asyncio
async def test_put_vocabulary(http_service: Any) -> None:
    """Should return 204 No content."""
    # ACT:
    ontology_rdf_file = "tests/files/input/vocabularies/audience-type/audience-type.ttl"
    ontology_en_html_file = (
        "tests/files/input/vocabularies/audience-type/audience-type-en.html"
    )
    ontology_nb_html_file = (
        "tests/files/input/vocabularies/audience-type/audience-type-nb.html"
    )
    ontology_nn_html_file = (
        "tests/files/input/vocabularies/audience-type/audience-type-nn.html"
    )

    with MultipartWriter("mixed") as mpwriter:
        # add the RDF-representation
        p = mpwriter.append(open(ontology_rdf_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-rdf-file", filename="audience-type.ttl"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/turtle"

        # add the HTML-representations: en
        p = mpwriter.append(open(ontology_en_html_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-html-file", filename="audience-type-en.html"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"

        # add the HTML-representations: nb
        p = mpwriter.append(open(ontology_nb_html_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-html-file", filename="audience-type-nb.html"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"
        p.headers[hdrs.CONTENT_LANGUAGE] = "nb"

        # add the HTML-representations: nn
        p = mpwriter.append(open(ontology_nn_html_file, "rb"))
        p.set_content_disposition(
            "attachment", name="ontology-html-file", filename="audience-type-nn.html"
        )
        p.headers[hdrs.CONTENT_TYPE] = "text/html"
        p.headers[hdrs.CONTENT_LANGUAGE] = "nn"

    ontology_type = "vocabularies"
    ontology = "audience-type"
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

        # Get turtle-representation:
        headers = {hdrs.ACCEPT: "text/turtle"}
        url = f"{http_service}/{ontology_type}/{ontology}"
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/turtle; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]

        # Get html-representations: en
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "en"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]

        # Get html-representations: nb
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nb"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]

        # Get html-representations: nn
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nn"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "nn" == response.headers[hdrs.CONTENT_LANGUAGE]

        # Get html-representations: unknown language
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "xx"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]

        # Get html-representations: default language
        headers = {hdrs.ACCEPT: "text/html"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]


@pytest.mark.contract
@pytest.mark.asyncio
async def test_put_specification(http_service: Any) -> None:
    """Should return 204 No content."""
    # ACT:
    specification_html_file = "tests/files/input/specifications/dcat-ap-no/index.html"
    logo_image = "tests/files/input/specifications/dcat-ap-no/images/digitaliseringsdirektoratet.png"
    model_image = (
        "tests/files/input/specifications/dcat-ap-no/images/DCAT-AP-NO2_20210903.png"
    )
    pdf_file = "tests/files/input/specifications/dcat-ap-no/files/dcat-ap-no.pdf"
    model_file = (
        "tests/files/input/specifications/dcat-ap-no/files/DCAT-AP-NO2_20210903.eap"
    )

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
            filename="images/DCAT-AP-NO2_20210903.png",
        )
        p.headers[hdrs.CONTENT_TYPE] = "image/png"

        # add an image-representations:
        p = mpwriter.append(open(logo_image, "rb"))
        p.set_content_disposition(
            "attachment",
            name="image",
            filename="images/digitaliseringsdirektoratet.png",
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

        # add an eap-file:
        p = mpwriter.append(open(model_file, "rb"))
        p.set_content_disposition(
            "attachment",
            name="specification-eap-file",
            filename="files/DCAT-AP-NO2_20210903.eap",
        )
        p.headers[hdrs.CONTENT_TYPE] = "application/octet-stream"
        p.headers[hdrs.CONTENT_LANGUAGE] = "en"

    ontology_type = "specifications"
    ontology = "dcat-ap-no"
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

        # Get html-representations: nb
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nb"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]

        # Get html-representations: unknown language
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "xx"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]

        # Get html-representations: default language
        headers = {hdrs.ACCEPT: "text/html"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]


@pytest.mark.contract
@pytest.mark.asyncio
async def test_put_ontology_no_api_key(http_service: Any) -> None:
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

    ontology_type = "contract-test"
    ontology = "audience-type"

    url = f"{http_service}/{ontology_type}/{ontology}"
    async with ClientSession() as session:
        async with session.put(url, data=mpwriter) as response:
            pass
        assert response.status == 403
