"""Contract test cases the upload ontology."""

import os
from typing import Any

from aiohttp import ClientSession, hdrs
import pytest


def get_api_headers() -> dict[str, str]:
    """Returns a headers dictionary with the API key if set in the environment.

    This helper function reads the API_KEY environment variable and, if present,
    adds it to the headers as "X-API-KEY". This is used to authenticate requests
    to the API in contract tests.

    Returns:
        dict[str, str]: Headers dictionary for authenticated requests.
    """
    api_key = os.getenv("API_KEY")
    headers = {}
    if api_key:
        headers["X-API-KEY"] = api_key
    return headers


@pytest.mark.contract
@pytest.mark.asyncio
async def test_create_ontology_type_specifications(http_service: Any) -> None:
    """Should return 204 No content."""
    ontology_type = "specifications"

    url = f"{http_service}/{ontology_type}"
    headers = get_api_headers()
    async with ClientSession() as session:
        async with session.put(url, headers=headers) as response:
            if response.status != 204:
                body = await response.json()
            pass

        # ASSERT
        assert response.status == 204, body
        assert f"{ontology_type}" == response.headers[hdrs.LOCATION]

        # Get turtle-representation:
        async with session.get(url, headers={hdrs.ACCEPT: "text/turtle"}) as response:
            body = await response.text()
        assert response.status == 406

        # Get html-representations: en
        async with session.get(
            url, headers={hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "en"}
        ) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: nb
        async with session.get(
            url, headers={hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nb"}
        ) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: nn
        async with session.get(
            url, headers={hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nn"}
        ) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: unknown language
        async with session.get(
            url, headers={hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "xx"}
        ) as response:
            body = await response.text()
        assert response.status == 406

        # Get html-representations: default language
        async with session.get(url, headers={hdrs.ACCEPT: "text/html"}) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]
        assert body


@pytest.mark.contract
@pytest.mark.asyncio
async def test_create_ontology_type_vocabularies(http_service: Any) -> None:
    """Should return 204 No content."""
    ontology_type = "vocabularies"

    url = f"{http_service}/{ontology_type}"
    headers = get_api_headers()
    async with ClientSession() as session:
        async with session.put(url, headers=headers) as response:
            if response.status != 204:
                body = await response.json()
            pass

        # ASSERT
        assert response.status == 204, body
        assert f"{ontology_type}" == response.headers[hdrs.LOCATION]

        # Get turtle-representation:
        async with session.get(url, headers={hdrs.ACCEPT: "text/turtle"}) as response:
            body = await response.text()
        assert response.status == 406

        # Get html-representations: en
        async with session.get(
            url, headers={hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "en"}
        ) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: nb
        async with session.get(
            url, headers={hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nb"}
        ) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: nn
        async with session.get(
            url, headers={hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "nn"}
        ) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]
        assert body

        # Get html-representations: unknown language
        async with session.get(
            url, headers={hdrs.ACCEPT: "text/html", hdrs.ACCEPT_LANGUAGE: "xx"}
        ) as response:
            body = await response.text()
        assert response.status == 406

        # Get html-representations: default language
        async with session.get(url, headers={hdrs.ACCEPT: "text/html"}) as response:
            body = await response.text()
        assert response.status == 200
        assert "text/html; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
        assert "en" == response.headers[hdrs.CONTENT_LANGUAGE]
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
