"""Module for ontology route."""
import logging
import os
from typing import Any, List

from aiohttp import hdrs, web
from multidict import MultiDict


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
    accept_header = request.headers.get(hdrs.ACCEPT, None)
    if not accept_header or "*" in accept_header or "text/html" in accept_header:
        pass
    else:
        raise web.HTTPNotAcceptable()

    data_root = request.app["DATA_ROOT"]
    ontology_type_path = os.path.join(data_root, ontology_type)

    # Read content of data-root, and map all folders to a list of ontology_types:
    ontologies: List[Any] = next(os.walk(ontology_type_path), (None, [], None))[1]

    # Generate html with the list as body:
    body = await generate_html_document(ontology_type, ontologies)
    headers = MultiDict([(hdrs.CONTENT_LANGUAGE, "en")])

    return web.Response(text=body, headers=headers, content_type="text/html")


async def generate_html_document(ontology_type: str, ontologies: List[str]) -> str:
    """Based on list of ontologies, generate a html-document."""
    html_statements: List[str] = []

    # Sort the list alphabetically:
    ontologies.sort()

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
