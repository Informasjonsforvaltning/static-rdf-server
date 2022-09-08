"""Contract test cases for ontology-type."""
from typing import Any

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_ontology_type(http_service: Any, chrome_service: Any) -> None:
    """Should return 200 OK and a html-document with a list of ontologies for the given type."""
    url = f"{http_service}/contract-test"

    options = ChromeOptions()
    options.headless = True

    driver = webdriver.Chrome(
        service=chrome_service, options=options
    )  # pytype: disable=wrong-keyword-args

    driver.get(url)

    assert driver.title == "Contract-Test"
    elements = driver.find_elements(By.TAG_NAME, "p")
    assert len(elements) == 3
    assert elements[0].text == "Contract-Test"
    assert elements[1].text == "- hello-world"
    href = elements[1].find_element(
        By.CSS_SELECTOR, 'a[href="contract-test/hello-world"]'
    )
    assert href.text == "hello-world"
    assert elements[2].text == "- hello-world-to-be-deleted"
    href = elements[2].find_element(
        By.CSS_SELECTOR, 'a[href="contract-test/hello-world-to-be-deleted"]'
    )
    assert href.text == "hello-world-to-be-deleted"

    driver.quit()


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_ontology_type_that_does_not_exist(
    http_service: Any, chrome_service: Any
) -> None:
    """Should return 404 Not found."""
    url = f"{http_service}/does-not-exist"

    options = ChromeOptions()
    options.headless = True

    driver = webdriver.Chrome(
        service=chrome_service, options=options
    )  # pytype: disable=wrong-keyword-args

    driver.get(url)

    assert driver.title == "Not found"
    elements = driver.find_elements(By.TAG_NAME, "p")
    assert len(elements) == 1
    assert elements[0].text == "The page you are looking for does not exist."

    driver.quit()
