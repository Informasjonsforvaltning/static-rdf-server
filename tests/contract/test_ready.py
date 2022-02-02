"""Contract test cases for ready."""
from typing import Any

from aiohttp import ClientSession
import pytest


@pytest.mark.contract
@pytest.mark.asyncio
async def test_ready(http_service: Any) -> None:
    """Should return OK."""
    url = f"{http_service}/ready"

    async with ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()

    assert response.status == 200
    assert text == "OK"
