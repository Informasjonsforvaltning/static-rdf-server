"""Module for slash route."""

import os
from typing import Any, Dict, List

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


async def get_slash(request: web.Request) -> web.Response:
    """Should generate and return a list of ontology-types as a html-document."""
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

    # Read content of data-root, and map all folders to a list of ontology_types:
    ontology_types: List[Any] = next(os.walk(data_root), (None, [], None))[1]

    # Generate html with the list as body:
    body = await generate_html_document(ontology_types, content_language)
    headers = MultiDict(
        [(hdrs.CONTENT_TYPE, content_type), (hdrs.CONTENT_LANGUAGE, content_language)]
    )

    return web.Response(text=body, headers=headers)


async def generate_html_document(ontology_types: List[str], lang: str) -> str:
    """Based on list of ontologies, generate a html-document."""
    html_statements: List[str] = []
    title: Dict[str, str] = {
        "nb": "Ontologi-typer",
        "nn": "Ontologi-typar",
        "en": "Ontology-types",
    }
    # Sort the list alphabetically:
    ontology_types.sort()

    # Generate the statements:
    html_statements.append("<!doctype html>")
    html_statements.append(f'<html lang="{lang}">')
    html_statements.append(f"<title>{title[lang]}</title>")
    html_statements.append("<body>")
    html_statements.append(f"<h2>{title[lang]}</h2>")
    html_statements.append("<ul>")
    for ontology_type in ontology_types:
        html_statements.append(
            f'<li><a href="{ontology_type}">{ontology_type}</a></li>'
        )
    html_statements.append("</ul>")
    html_statements.append("</body>")

    # Concatenates all the statments into a string:
    return "".join(html_statements)
