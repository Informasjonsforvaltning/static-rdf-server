"""Test cases for the server module."""
import os
from typing import Any

from aiohttp import hdrs
import pytest


@pytest.mark.integration
async def test_put_ontology_type_when_type_does_exist(client: Any, fs: Any) -> None:
    """Should return status 204 Created and location header."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"

    fs.create_dir(f"{data_root}/{ontology_type}")

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(f"/{ontology_type}", headers=headers)

    assert response.status == 204
    assert f"{ontology_type}" in response.headers[hdrs.LOCATION]


@pytest.mark.integration
async def test_put_ontology_type_when_type_does_not_exist(client: Any, fs: Any) -> None:
    """Should return status 201 Created and location header."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"

    fs.create_dir(f"{data_root}")

    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    response = await client.put(f"/{ontology_type}", headers=headers)

    assert response.status == 201
    assert f"{ontology_type}" in response.headers[hdrs.LOCATION]


@pytest.mark.integration
async def test_put_ontology_type_no_api_key(client: Any, fs: Any) -> None:
    """Should return status 403 Forbidden."""
    data_root = "/srv/www/static-rdf-server/data"
    ontology_type = "examples"

    fs.create_dir(f"{data_root}/{ontology_type}")

    response = await client.put(f"/{ontology_type}")

    assert response.status == 403
