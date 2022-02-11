"""Contract test cases the upload ontology."""
import os
from typing import Any

from aiohttp import ClientSession, hdrs
import pytest


@pytest.mark.contract
@pytest.mark.asyncio
async def test_create_ontology_type(http_service: Any) -> None:
    """Should return 204 No content."""
    ontology_type = "contract-test"

    url = f"{http_service}/{ontology_type}"
    headers = {
        "X-API-KEY": os.getenv("API_KEY", None),
    }
    async with ClientSession() as session:
        async with session.put(url, headers=headers) as response:
            if response.status != 204:
                body = await response.json()
            pass

        # ASSERT
        assert response.status == 204, body
        assert f"{ontology_type}" in response.headers[hdrs.LOCATION]

        # Get turtle-representation:
        headers = {hdrs.ACCEPT: "text/turtle"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 406

        # Get html-representations: en
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "en"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
        assert "en" in response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: nb
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nb"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
        assert "en" in response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: nn
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nn"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
        assert "en" in response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: unknown language
        headers = {hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "xx"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
        assert "en" in response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: default language
        headers = {hdrs.ACCEPT: "text/html"}
        async with session.get(url, headers=headers) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html" in response.headers[hdrs.CONTENT_TYPE]
        assert "en" in response.headers[hdrs.CONTENT_LANGUAGE]
        assert body


@pytest.mark.contract
@pytest.mark.asyncio
async def test_put_ontology_no_api_key(http_service: Any) -> None:
    """Should return 403 Forbidden."""
    ontology_type = "contract-test"

    url = f"{http_service}/{ontology_type}"
    async with ClientSession() as session:
        async with session.put(url) as response:
            pass
        assert response.status == 403
