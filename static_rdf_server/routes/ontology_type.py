"""Module for ontology route."""
import os
from typing import Any, List

from aiohttp import hdrs, web
from multidict import MultiDict


async def get_ontology_type(request: web.Request) -> web.Response:
    """Should generate and return a list of ontologies in give ontology-type as a html-document."""
    data_root = request.app["DATA_ROOT"]
    ontology_type = request.match_info["ontology_type"]
    accept_header = request.headers.get(hdrs.ACCEPT, None)
    if not accept_header or "*" in accept_header or "text/html" in accept_header:
        pass
    else:
        raise web.HTTPNotAcceptable()

    data_root = request.app["DATA_ROOT"]
    ontology_type_path = os.path.join(data_root, ontology_type)
    default_language = request.app["DEFAULT_LANGUAGE"]

    # Read content of data-root, and map all folders to a list of ontology_types:
    ontologies: List[Any] = next(os.walk(ontology_type_path), (None, [], None))[1]

    # Generate html with the list as body:
    body = await generate_html_document(ontology_type, ontologies)
    headers = MultiDict([(hdrs.CONTENT_LANGUAGE, default_language)])

    return web.Response(text=body, headers=headers, content_type="text/html")


async def generate_html_document(ontology_type: str, ontologies: List[str]) -> str:
    """Based on list of ontologies, generate a html-document."""
    html_statements: List[str] = []

    # Generate the statements:
    html_statements.append("<!doctype html>")
    html_statements.append('<html lang="en">')
    html_statements.append(f"<title>{ontology_type.title()}</title>")
    html_statements.append("<body>")
    html_statements.append(f"<p><b>{ontology_type.title()}</b></p>")
    for ontology in ontologies:
        html_statements.append(
            f'<p> - <a href="{ontology_type}/{ontology}">{ontology}</a></p>'
        )

    # Concatenates all the statments into a string:
    return "".join(html_statements)
