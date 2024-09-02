"""Test cases for the server module."""

import os
from typing import Any

import pytest


@pytest.mark.integration
async def test_delete_ontology(client: Any, fs: Any) -> None:
    """Should return status 204."""
    contents = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1.ttl",
        contents=contents,
    )
    fs.create_file(
        "/srv/www/static-rdf-server/static/ontology-type-1/ontology-1/ontology-1.static",
        contents=contents,
    )
    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.delete("/ontology-type-1/ontology-1", headers=headers)

    assert response.status == 204


@pytest.mark.integration
async def test_delete_ontology_not_found(client: Any, fs: Any) -> None:
    """Should return status 404."""
    contents = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1.ttl",
        contents=contents,
    )

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.delete(
        "/ontology-type-1/ontology-not-found", headers=headers
    )

    assert response.status == 404


@pytest.mark.integration
async def test_delete_ontology_no_api_key(client: Any, fs: Any) -> None:
    """Should return status 403 Forbidden."""
    contents = '<http://example.com/drewp> <http://example.com/says> "Hello World" .'
    fs.create_file(
        "/srv/www/static-rdf-server/data/ontology-type-1/ontology-1/ontology-1.ttl",
        contents=contents,
    )

    response = await client.delete("/ontology-type-1/ontology-1")

    assert response.status == 403


@pytest.mark.integration
async def test_delete_ontology_not_valid(client: Any, fs: Any) -> None:
    """Should return status 400."""
    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.delete("/ontology-type-1/%00", headers=headers)

    assert response.status == 400
