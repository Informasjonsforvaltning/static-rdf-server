"""Module for ontology route."""
import logging
import os
from textwrap import dedent
from typing import Any, List

from aiohttp import hdrs, web
from content_negotiation import (
    decide_content_type,
    decide_language,
    NoAgreeableContentTypeError,
    NoAgreeableLanguageError,
)
from multidict import MultiDict

SUPPORTED_CONTENT_TYPES = ["text/html"]
SUPPORTED_LANGUAGES = ["nb", "nn", "en"]


async def put_ontology_type(request: web.Request) -> web.Response:
    """Process and store type."""
    data_root = request.app["DATA_ROOT"]
    api_key = request.headers.get("X-API-KEY", None)
    if not api_key or os.getenv("API_KEY", None) != api_key:
        raise web.HTTPForbidden()

    ontology_type = request.match_info["ontology_type"]
    logging.debug(f"Got put request for {ontology_type}.")

    # Decide status_code:
    destination = os.path.join(data_root, ontology_type)
    if os.path.exists(destination):
        status_code = 204
    else:
        status_code = 201

    # Create destination folders:
    destination = os.path.join(data_root, ontology_type)
    if not os.path.exists(destination):
        os.makedirs(destination)

    headers = MultiDict([(hdrs.LOCATION, f"{ontology_type}")])
    return web.Response(status=status_code, headers=headers)


async def get_ontology_type(request: web.Request) -> web.Response:
    """Should generate and return a list of ontologies in give ontology-type as a html-document."""
    data_root = request.app["DATA_ROOT"]
    ontology_type = request.match_info["ontology_type"]
    try:
        content_type = decide_content_type(
            request.headers.getall(hdrs.ACCEPT, []),
            supported_content_types=SUPPORTED_CONTENT_TYPES,
        )
    except NoAgreeableContentTypeError as e:
        raise web.HTTPNotAcceptable() from e

    try:
        content_language = decide_language(
            request.headers.getall(hdrs.ACCEPT_LANGUAGE, []),
            supported_languages=SUPPORTED_LANGUAGES,
        )
    except NoAgreeableLanguageError as e:
        raise web.HTTPNotAcceptable() from e

    data_root = request.app["DATA_ROOT"]
    ontology_type_path = os.path.join(data_root, ontology_type)

    # Read content of data-root, and map all folders to a list of ontology_types:
    ontologies: List[Any] = next(os.walk(ontology_type_path), (None, [], None))[1]
    headers = MultiDict(
        [(hdrs.CONTENT_TYPE, content_type), (hdrs.CONTENT_LANGUAGE, "en")]
    )
    if len(ontologies) == 0:
        # We have no ontologies, so we return a 404:
        body = await generate_html_not_found()
        status = 404
    else:
        # Generate html with the list as body:
        body = await generate_html_document(ontology_type, ontologies, content_language)
        status = 200

    return web.Response(text=body, headers=headers, status=status)


async def generate_html_document(
    ontology_type: str, ontologies: List[str], lang: str
) -> str:
    """Based on list of ontologies, generate a html-document."""
    html_statements: List[str] = []

    # Sort the list alphabetically:
    ontologies.sort()

    # Generate the statements:
    html_statements.append("<!doctype html>")
    html_statements.append(f'<html lang="{lang}">')
    html_statements.append(f"<title>{ontology_type.title()}</title>")
    html_statements.append("<body>")
    html_statements.append(f"<h2>{ontology_type.title()}</h2>")
    html_statements.append("<ul>")
    for ontology in ontologies:
        html_statements.append(
            f'<li><a href="{ontology_type}/{ontology}">{ontology}</a></li>'
        )
    html_statements.append("</ul>")
    html_statements.append("</body>")

    # Concatenates all the statments into a string:
    return "".join(html_statements)


async def generate_html_not_found() -> str:
    """Simple not found page."""
    # Generate and return the html:
    return dedent(
        """
        <!doctype html>
        <html lang="en">
            <head>
                <title>Not found</title>
            </head>
            <body>
                <p>The page you are looking for does not exist.</p>
            </body>
        </html>
    """
    ).strip()
