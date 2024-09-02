"""Integration test cases for the ready route."""

from typing import Any

from aiohttp.test_utils import TestClient as _TestClient
import pytest

SERVER_ROOT = "/srv/www/static-rdf-server"


@pytest.mark.integration
async def test_ready(client: _TestClient, fs: Any) -> None:
    """Should return OK."""
    fs.create_dir(SERVER_ROOT)
    resp = await client.get("/ready")
    assert resp.status == 200
    body = await resp.text()
    assert "OK" in body


@pytest.mark.integration
async def test_ready_when_data_root_does_not_exist(
    client: _TestClient, fs: Any
) -> None:
    """Should return 500 Internal Server Error."""
    resp = await client.get("/ready")
    assert resp.status == 500
    body = await resp.json()
    assert f'Ready fails: SERVER_ROOT "{SERVER_ROOT}" does not exist.' in body["detail"]
