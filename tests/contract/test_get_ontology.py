"""Contract test cases for ping."""
from typing import Any

from aiohttp import ClientSession, hdrs
import pytest


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_turtle(http_service: Any) -> None:
    """Should return 200 OK and a turtle-document."""
    url = f"{http_service}/contract-test/hello-world"
    headers = {
        hdrs.ACCEPT: "text/turtle",
    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            document = await response.text()

    assert response.status == 200
    assert "text/turtle; charset=utf-8" == response.headers[hdrs.CONTENT_TYPE]
    assert (
        '<http://example.com/server> <http://example.com/says> "Hello World" .'
        in document
    )
