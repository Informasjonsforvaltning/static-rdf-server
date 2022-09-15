"""Module for slash route."""
import os
from typing import Any, List

from aiohttp import hdrs, web
from content_negotiation import decide_content_type, NoAgreeableContentTypeError
from multidict import MultiDict


async def get_slash(request: web.Request) -> web.Response:
    """Should generate and return a list of ontology-types as a html-document."""
    try:
        content_type = decide_content_type(
            request.headers.getall(hdrs.ACCEPT, []),
            supported_content_types=["text/html"],
        )
    except NoAgreeableContentTypeError as e:
        raise web.HTTPNotAcceptable() from e

    data_root = request.app["DATA_ROOT"]
    default_language = request.app["DEFAULT_LANGUAGE"]

    # Read content of data-root, and map all folders to a list of ontology_types:
    ontology_types: List[Any] = next(os.walk(data_root), (None, [], None))[1]

    # Generate html with the list as body:
    body = await generate_html_document(ontology_types)
    headers = MultiDict(
        [(hdrs.CONTENT_TYPE, content_type), (hdrs.CONTENT_LANGUAGE, default_language)]
    )

    return web.Response(text=body, headers=headers)


async def generate_html_document(ontology_types: List[str]) -> str:
    """Based on list of ontologies, generate a html-document."""
    html_statements: List[str] = []

    # Sort the list alphabetically:
    ontology_types.sort()

    # Generate the statements:
    html_statements.append("<!doctype html>")
    html_statements.append('<html lang="nb">')
    html_statements.append("<title>Ontologi-typer</title>")
    html_statements.append("<body>")
    html_statements.append("<h2>Typer</h2>")
    html_statements.append("<ul>")
    for ontology_type in ontology_types:
        html_statements.append(
            f'<li><a href="{ontology_type}">{ontology_type}</a></li>'
        )
    html_statements.append("</ul>")
    html_statements.append("</body>")

    # Concatenates all the statments into a string:
    return "".join(html_statements)
