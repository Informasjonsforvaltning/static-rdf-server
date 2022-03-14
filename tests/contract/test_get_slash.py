"""Contract test cases for ping."""
from typing import Any

from aiohttp import ClientSession, hdrs
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_slash(http_service: Any, chrome_service: Any) -> None:
    """Should return 200 OK and a html-document."""
    url = f"{http_service}/"

    options = ChromeOptions()
    options.headless = True

    driver = webdriver.Chrome(
        service=chrome_service, options=options
    )  # pytype: disable=wrong-keyword-args

    driver.get(url)

    assert driver.title == "Ontologi-typer"
    elements = driver.find_elements(By.TAG_NAME, "p")
    assert len(elements) == 2
    assert elements[0].text == "Typer"
    assert elements[1].text == "- contract-test"
    href = elements[1].find_element(By.CSS_SELECTOR, "a[href=contract-test]")
    assert href.text == "contract-test"

    driver.quit()


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
