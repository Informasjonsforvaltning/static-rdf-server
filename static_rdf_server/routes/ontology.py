"""Module for ontology route."""
import logging
import os
import shutil
from typing import List
from urllib.parse import unquote

from aiohttp import hdrs, web
from multidict import MultiDict

from static_rdf_server.utils import (
    ContentTypeNotSupportedException,
    decide_content_and_extension,
    NotValidFileContentException,
    rewrite_links,
    valid_content_type,
    valid_file_content,
    valid_file_extension,
)


async def put_ontology(request: web.Request) -> web.Response:  # noqa: C901
    """Process and store files."""
    data_root = request.app["DATA_ROOT"]
    static_root = request.app["STATIC_ROOT"]
    api_key = request.headers.get("X-API-KEY", None)
    if not api_key or os.getenv("API_KEY", None) != api_key:
        raise web.HTTPForbidden()

    ontology_type = request.match_info["ontology_type"]
    # Check if ontology-type exist. Otherwise return 404:
    ontology_type_folder = os.path.join(data_root, ontology_type)
    if not os.path.exists(ontology_type_folder):
        raise web.HTTPNotFound(
            reason=f"Ontology-type {ontology_type} does not exist."
        ) from None

    ontology = request.match_info["ontology"]
    extension: str
    logging.debug(f"Got put request{ontology_type}/{ontology}.")

    # Decide status_code:
    destination = os.path.join(data_root, ontology_type, ontology)
    if os.path.exists(destination):
        status_code = 204
    else:
        status_code = 201

    # Processing parts:
    async for part in (await request.multipart()):
        logging.debug(f"part.name {part.name}.")
        content_language: str = ""

        # Validate headers:
        try:
            content_type = part.headers[hdrs.CONTENT_TYPE]
            if not (await valid_content_type(content_type)):
                raise web.HTTPUnsupportedMediaType(
                    reason=f"Not supported content-type {content_type}."
                )
        except KeyError:
            raise web.HTTPBadRequest(
                reason="Content-Type header must be given."
            ) from None

        # For html we check that the content-language header is set:
        if "text/html" in part.headers[hdrs.CONTENT_TYPE]:
            if not part.headers.get(hdrs.CONTENT_LANGUAGE):
                raise web.HTTPBadRequest(
                    reason="For html-content, Content-Language header must be given."
                )
            content_language = part.headers[hdrs.CONTENT_LANGUAGE]

        # Validate filename extension:
        if part.filename:
            extension = part.filename.split(".")[-1]
            if not (await valid_file_extension(extension)):
                raise web.HTTPBadRequest(
                    reason=f"Not supported file-extension {extension}."
                )

        # Read the file:
        try:
            ontology_file = await part.read(decode=False)
        except ValueError:  # pragma: no cover
            raise web.HTTPBadRequest(
                reason=f'Ontology file "{part.filename}" could not be read.'
            ) from None

        # Check the content of the file:
        ontology_file_decoded: bytes
        try:
            ontology_file_decoded = part.decode(ontology_file)
            await valid_file_content(extension, ontology_file_decoded)
        except NotValidFileContentException as e:
            raise web.HTTPBadRequest(
                reason=f'Ontology file "{part.filename}" has not valid content: {str(e)}.'
            ) from e

        # For html-files We need to rewrite links to sub-folders:
        if "text/html" in part.headers[hdrs.CONTENT_TYPE]:
            ontology_file_decoded = await rewrite_links(
                ontology_file_decoded, data_root, ontology_type, ontology
            )

        # Decide and create destination folder:
        if extension in ["html", "ttl"]:
            destination = os.path.join(data_root, ontology_type, ontology)
        else:
            destination = os.path.join(static_root, ontology_type, ontology)
        if not os.path.exists(destination):
            os.makedirs(destination)

        # Decide sub-folders:
        sub_folders: List[str]
        if part.filename:
            _filename = unquote(part.filename)
            sub_folders = _filename.split(os.sep)
            for folder in sub_folders[:-1]:
                destination = os.path.join(destination, folder)

        # Create sub-folders:
        if not os.path.exists(destination):
            os.makedirs(destination)

        # For html and RDF create filename:
        filename: str
        if part.filename and extension not in ["html", "ttl"]:
            _filename = unquote(part.filename)
            filename = _filename.split(os.sep)[-1]
        else:
            if len(content_language) > 0:
                filename = f"{ontology}-{content_language}.{extension}"
            else:
                filename = f"{ontology}.{extension}"

        # Write file to path:
        path = os.path.join(destination, filename)
        logging.debug(f"Writing to path: {path}.")
        with open(path, "wb") as file:
            file.write(ontology_file_decoded)
    if status_code == 201:
        headers = MultiDict([(hdrs.LOCATION, f"{ontology_type}/{ontology}")])
    else:
        headers = None
    return web.Response(status=status_code, headers=headers)


async def get_ontology(request: web.Request) -> web.Response:
    """Return default response."""
    data_root = request.app["DATA_ROOT"]
    default_language = request.app["DEFAULT_LANGUAGE"]
    ontology_type = request.match_info["ontology_type"]
    ontology = request.match_info["ontology"]

    logging.debug(f"Got request for type/folder/file {ontology_type}/{ontology}")

    # First we check if the ontology exist:
    ontology_path = os.path.join(data_root, ontology_type, ontology)
    logging.debug(f"Looking for ontology_path: {ontology_path}")
    if not os.path.exists(ontology_path):
        raise web.HTTPNotFound()

    # Then we check headers to decide what representation to look for:
    try:
        content_type, content_language, extension = await decide_content_and_extension(
            request.headers.get(hdrs.ACCEPT),
            request.headers.get(hdrs.ACCEPT_LANGUAGE),
        )
    except ContentTypeNotSupportedException as e:
        raise web.HTTPNotAcceptable(reason=str(e)) from e

    # We finally try to get the corresponding representation:
    filename: str
    if len(content_language) > 0:
        filename = f"{ontology}-{content_language}.{extension}"
    else:
        filename = f"{ontology}.{extension}"

    # Try to get exact match on language:
    full_path = os.path.join(data_root, ontology_type, ontology, filename)
    logging.debug(f"Looking for full_path: {full_path}")
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            body = f.read()
        headers = MultiDict([(hdrs.CONTENT_LANGUAGE, content_language)])
        return web.Response(text=body, headers=headers, content_type=content_type)

    # For html-requests, if not found, we return the representation in the default langauge:
    if content_type == "text/html":
        filename = f"{ontology}-{default_language}.{extension}"
        full_path = os.path.join(data_root, ontology_type, ontology, filename)
        if os.path.exists(full_path):
            with open(full_path, "r") as f:
                body = f.read()
                logging.debug(f"Is about to return body: {body}")
            headers = MultiDict([(hdrs.CONTENT_LANGUAGE, default_language)])
            return web.Response(text=body, headers=headers, content_type=content_type)

    # If we are here, the ontology does exist, but there is no suitable representation:
    raise web.HTTPNotAcceptable() from None


async def delete_ontology(request: web.Request) -> web.Response:
    """Return default response."""
    api_key = request.headers.get("X-API-KEY", None)
    if not api_key or os.getenv("API_KEY", None) != api_key:
        raise web.HTTPForbidden()

    data_root = request.app["DATA_ROOT"]
    static_root = request.app["STATIC_ROOT"]

    ontology_type = request.match_info["ontology_type"]
    ontology = request.match_info["ontology"]

    logging.debug(f"Got request for folder/file {ontology_type}/{ontology}")
    logging.debug(f"Got request-headers: {request.headers}")

    # First we check if the ontology exist:
    ontology_path = os.path.join(data_root, ontology_type, ontology)
    logging.debug(f"Trying to delete ontology with path: {ontology_path}")
    if not os.path.exists(ontology_path):
        raise web.HTTPNotFound()

    shutil.rmtree(ontology_path)

    # We also need to remove static files, if they exist:
    static_path = os.path.join(static_root, ontology_type, ontology)
    if os.path.exists(static_path):
        shutil.rmtree(static_path)

    return web.Response(status=204)
