"""Contract test cases for ping."""
from typing import Any

from aiohttp import ClientSession, hdrs
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By


@pytest.mark.skip(reason="Setting lang in headless mode does not work")
@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_norwegian_bokmaal(
    http_service: Any, chrome_service: Any
) -> None:
    """Should return 200 OK and a html-document in Norwegian bokmål."""
    url = f"{http_service}/contract-test/hello-world"

    options = ChromeOptions()
    options.headless = True
    options.add_experimental_option("prefs", {"intl.accept_languages": "nb,nb_NO"})

    driver = webdriver.Chrome(
        service=chrome_service, options=options
    )  # pytype: disable=wrong-keyword-args

    driver.get(url)

    # html_lang = driver.find_element(By.TAG_NAME, "html").get_attribute("lang")
    # assert html_lang == "nb"

    assert driver.title == "Hallo verden"
    elements = driver.find_elements(By.TAG_NAME, "p")
    assert len(elements) == 2
    assert elements[0].text == "Hallo, verden!"
    assert elements[1].text == "Denne hilsen ble sist oppdatert 2022-02-04 14:20:00."

    driver.quit()


@pytest.mark.skip(reason="Setting lang in headless mode does not work")
@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_html_norwegian_nynorsk(
    http_service: Any, chrome_service: Any
) -> None:
    """Should return 200 OK and a html-document in Norwegian nynorsk."""
    url = f"{http_service}/contract-test/hello-world"

    options = ChromeOptions()
    options.headless = True
    options.add_experimental_option("prefs", {"intl.accept_languages": "nn,nn_NO"})

    driver = webdriver.Chrome(
        service=chrome_service, options=options
    )  # pytype: disable=wrong-keyword-args

    driver.get(url)

    # html_lang = driver.find_element(By.TAG_NAME, "html").get_attribute("lang")
    # assert html_lang == "nn"

    assert driver.title == "Hallo verda"
    elements = driver.find_elements(By.TAG_NAME, "p")
    assert len(elements) == 2
    assert elements[0].text == "Hallo, verda!"
    assert elements[1].text == "Denne helsinga vart sist oppdatert 2022-02-04 14:20:00."

    driver.quit()


@pytest.mark.skip(reason="Setting lang in headless mode does not work")
@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_html_english(
    http_service: Any, chrome_service: Any
) -> None:
    """Should return 200 OK and a html-document in English."""
    url = f"{http_service}/contract-test/hello-world"
    url = f"{http_service}/contract-test/hello-world"

    options = ChromeOptions()
    options.headless = True
    options.add_experimental_option("prefs", {"intl.accept_languages": "en,en_GB"})

    driver = webdriver.Chrome(
        service=chrome_service, options=options
    )  # pytype: disable=wrong-keyword-args

    driver.get(url)

    # html_lang = driver.find_element(By.TAG_NAME, "html").get_attribute("lang")
    # assert html_lang == "en"

    assert driver.title == "Hello world"
    elements = driver.find_elements(By.TAG_NAME, "p")
    assert len(elements) == 2
    assert elements[0].text == "Hello, world!"
    assert elements[1].text == "This greeting was last updated 2022-02-08 14:49:40."

    # Check that image src is correct:
    img = driver.find_element_by_tag_name(("img"))
    img_src = img.get_attribute("src")
    assert img_src == f"{http_service}/contract-test/hello-world/images/hello-world.png"
    # Assert that images is downloadable:
    r = requests.get(img_src)
    assert r.status_code == 200

    # Check that pdf href is correct:
    pdf_href_value = "hello-world/files/hello-world-en.pdf"
    pdf = driver.find_element(By.CSS_SELECTOR, f'a[href="{pdf_href_value}"]')
    assert pdf.get_attribute("download") == "hello-world-en.pdf"
    assert pdf.text == "Download the pdf"
    # Assert that pdf is downloadable:
    url_to_pdf = f"{http_service}/contract-test/{pdf_href_value}"
    r = requests.get(url_to_pdf)
    assert r.status_code == 200, f"Not found: {url_to_pdf}"

    driver.quit()


@pytest.mark.skip(reason="Setting lang in headless mode does not work")
@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_example_hello_world_html_german(
    http_service: Any, chrome_service: Any
) -> None:
    """Should return 200 OK and a html-document in Norwegian bokmål."""
    url = f"{http_service}/contract-test/hello-world"
    url = f"{http_service}/contract-test/hello-world"

    options = ChromeOptions()
    options.headless = True
    options.add_experimental_option("prefs", {"intl.accept_languages": "ge,ge_DE"})

    driver = webdriver.Chrome(
        service=chrome_service, options=options
    )  # pytype: disable=wrong-keyword-args

    driver.get(url)

    # html_lang = driver.find_element(By.TAG_NAME, "html").get_attribute("lang")
    # assert html_lang == "nb"

    assert driver.title == "Hallo verden"
    elements = driver.find_elements(By.TAG_NAME, "p")
    assert len(elements) == 2
    assert elements[0].text == "Hallo, verden!"
    assert elements[1].text == "Denne hilsen ble sist oppdatert 2022-02-04 14:20:00."

    driver.quit()


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
