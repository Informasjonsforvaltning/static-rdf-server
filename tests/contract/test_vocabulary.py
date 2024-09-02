"""Contract test cases the upload ontology."""

import os
from typing import Any

from aiohttp import ClientSession, hdrs, MultipartWriter
import pytest
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

ONTOLOGY_TYPE = "vocabularies"
ONTOLOGY = "audience-type"


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

    ontology_type = ONTOLOGY_TYPE
    ontology = ONTOLOGY
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
async def test_put_vocabulary_xml(http_service: Any) -> None:
    """Should return 204 No content."""
    # ACT:
    ontology_rdf_file = "tests/files/input/vocabularies/audience-type/audience-type.xml"
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
            "attachment", name="ontology-rdf-file", filename="audience-type.xml"
        )
        p.headers[hdrs.CONTENT_TYPE] = "application/rdf+xml"

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

    ontology_type = ONTOLOGY_TYPE
    ontology = ONTOLOGY
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
async def test_get_ontology_vocabulary_audience_type_html(http_service: Any) -> None:
    """Should return 200 OK and a html-document."""
    ontology_type = ONTOLOGY_TYPE
    ontology = ONTOLOGY
    url = f"{http_service}/{ontology_type}/{ontology}"

    async with ClientSession() as session:
        # Get html-representations: en
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "en"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: nb
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nb"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "nb" == response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: nn
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nn"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "nn" == response.headers[hdrs.CONTENT_LANGUAGE]
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
async def test_get_ontology_vocabulary_audience_type_turtle(http_service: Any) -> None:
    """Should return 200 OK and a turtle-document."""
    ontology_type = ONTOLOGY_TYPE
    ontology = ONTOLOGY
    url = f"{http_service}/{ontology_type}/{ontology}"
    headers = {
        hdrs.ACCEPT: "text/turtle",
    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            document = await response.text()

    assert response.status == 200
    assert "text/turtle; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]

    g1 = Graph().parse(data=document, format="turtle")
    g2 = Graph().parse(
        location="tests/files/input/vocabularies/audience-type/audience-type.ttl",
        format="turtle",
    )

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic, "graphs are not isomorphic"


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_ontology_vocabulary_audience_type_ld_json(http_service: Any) -> None:
    """Should return 200 OK and a json-ld document."""
    content_type = "application/ld+json"
    ontology_type = ONTOLOGY_TYPE
    ontology = ONTOLOGY
    url = f"{http_service}/{ontology_type}/{ontology}"
    headers = {hdrs.ACCEPT: content_type}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            document = await response.text()

    assert response.status == 200
    assert f"{content_type}; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]

    assert Graph().parse(data=document, format=content_type)


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_ontology_vocabulary_audience_type_rdf_xml(http_service: Any) -> None:
    """Should return 200 OK and an rdf xml-document."""
    content_type = "application/rdf+xml"
    ontology_type = ONTOLOGY_TYPE
    ontology = ONTOLOGY
    url = f"{http_service}/{ontology_type}/{ontology}"
    headers = {hdrs.ACCEPT: content_type}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            document = await response.text()

    assert response.status == 200
    assert f"{content_type}; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]

    assert Graph().parse(data=document, format=content_type)


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_ontology_vocabulary_audience_type_n3(http_service: Any) -> None:
    """Should return 200 OK and a n3 document."""
    content_type = "text/n3"
    ontology_type = ONTOLOGY_TYPE
    ontology = ONTOLOGY
    url = f"{http_service}/{ontology_type}/{ontology}"
    headers = {hdrs.ACCEPT: content_type}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            document = await response.text()

    assert response.status == 200
    assert f"{content_type}; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]

    assert Graph().parse(data=document, format=content_type)


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
