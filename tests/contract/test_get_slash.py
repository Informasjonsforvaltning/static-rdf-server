"""Contract test cases for ping."""
from typing import Any

from aiohttp import ClientSession, hdrs
import pytest


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_slash_turtle(http_service: Any) -> None:
    """Should return 406 Not Acceptable."""
    url = f"{http_service}/"
    headers = {
        hdrs.ACCEPT: "text/turtle",
    }

    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            pass

    assert response.status == 406
