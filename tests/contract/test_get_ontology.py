"""Contract test cases for ping."""
from typing import Any

from aiohttp import ClientSession, hdrs
import pytest
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_ontology_vocabulary_audience_type_turtle(http_service: Any) -> None:
    """Should return 200 OK and a turtle-document."""
    url = f"{http_service}/vocabularies/audience-type"
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
