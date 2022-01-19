"""Module for server."""
import logging
import os

from aiohttp import hdrs, web
from aiohttp_middlewares import cors_middleware, error_middleware
from dotenv import load_dotenv
from multidict import MultiDict

from .utils import (
    ContentTypeNotSupported,
    decide_content_type_and_suffix,
    valid_file_content,
    valid_file_extension,
)

load_dotenv()
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
DATA_ROOT = "/srv/www/static-rdf-server"


async def upload_files(request: web.Request) -> web.Response:
    """Process and store files."""
    api_key = request.headers.get("X-API-KEY", None)
    if not api_key or os.getenv("API_KEY", None) != api_key:
        raise web.HTTPForbidden()

    ontology_type = request.match_info["ontology_type"]
    logging.debug(f"Got request post file of type {ontology_type}.")
    async for part in (await request.multipart()):
        logging.debug(f"part.name {part.name}.")
        try:
            if part.filename:
                filename: str = part.filename
                folder = filename.split(".")[0]
                extension = filename.split(".")[-1]
                if not (await valid_file_extension(extension)):
                    raise web.HTTPBadRequest(
                        reason=f"Not valid file-extension {extension}."
                    )
            ontology_file = (await part.read()).decode()
            logging.debug(f"Got ontology-file: {ontology_file}.")
            if not (await valid_file_content(extension, ontology_file)):
                raise web.HTTPBadRequest(reason="Not valid file-content.")

            # Create destination folders:
            destination = os.path.join(DATA_ROOT, ontology_type, folder)
            if not os.path.exists(destination):
                os.makedirs(destination)
            path = os.path.join(destination, filename)
            # Write file to folders:
            logging.debug(f"Writing to path: {path}.")
            with open(path, "w") as file:
                file.write(ontology_file)
        except ValueError:
            raise web.HTTPBadRequest(
                reason=f'Ontology file "{part.filename}" is not readable.'
            ) from None

    headers = MultiDict([(hdrs.LOCATION, f"{ontology_type}/{folder}")])
    return web.Response(status=201, headers=headers)


async def ready(request: web.Request) -> web.Response:
    """Return ready response."""
    if not os.path.exists(DATA_ROOT):
        raise web.HTTPInternalServerError(
            reason=f'Ready fails: DATA_ROOT "{DATA_ROOT}" does not exist.'
        ) from None
    return web.Response(text="OK")


async def ping(request: web.Request) -> web.Response:
    """Return ping response."""
    return web.Response(text="OK")


async def get_slash(request: web.Request) -> web.Response:
    """Return slash response."""
    full_path = os.path.join(os.sep, DATA_ROOT, "index.html")
    logging.debug(f"Looking for full_path: {full_path}")
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            body = f.read()
        return web.Response(text=body, content_type="text/html")

    else:
        raise web.HTTPNotFound() from None


async def get_ontology_type(request: web.Request) -> web.Response:
    """Return slash response."""
    ontology_type = request.match_info["ontology_type"]

    full_path = os.path.join(os.sep, DATA_ROOT, ontology_type, "index.html")
    logging.debug(f"Looking for full_path: {full_path}")
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            body = f.read()
        return web.Response(text=body, content_type="text/html")

    else:
        raise web.HTTPNotFound() from None


async def get_ontology(request: web.Request) -> web.Response:
    """Return default response."""
    ontology_type = request.match_info["ontology_type"]
    ontology = request.match_info["ontology"]
    logging.debug(f"Got request for folder/file {ontology_type}/{ontology}")

    logging.debug(f"Got request-headers: {request.headers}")
    # First we check if the ontology exist:
    ontology_path = os.path.join(os.sep, DATA_ROOT, ontology_type, ontology)
    logging.debug(f"Looking for ontology_path: {ontology_path}")
    if not os.path.exists(ontology_path):
        raise web.HTTPNotFound()

    # Then we check Accept-header to see decide what representation to look for:
    try:
        content_type, suffix = await decide_content_type_and_suffix(request.headers)
    except ContentTypeNotSupported as e:
        raise web.HTTPNotAcceptable(reason=str(e)) from e

    # We finally try to get the corresponding representation.
    full_path = os.path.join(
        os.sep, DATA_ROOT, ontology_type, ontology, ontology + suffix
    )
    logging.debug(f"Looking for full_path: {full_path}")
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            body = f.read()
            logging.debug(f"Is about to return body: {body}")
        return web.Response(text=body, content_type=content_type)

    else:  # Return not acceptable if representation is not found
        raise web.HTTPNotAcceptable() from None


async def create_app() -> web.Application:
    """Create an web application."""
    app = web.Application(
        middlewares=[
            cors_middleware(allow_all=True),
            error_middleware(),  # default error handler for whole application
        ],
    )
    # Set up logging
    logging.basicConfig(level=LOGGING_LEVEL)
    logging.getLogger("chardet.charsetprober").setLevel(LOGGING_LEVEL)

    # Set up routes:
    app.router.add_get("/ready", ready)
    app.router.add_get("/ping", ping)
    app.router.add_get("/", get_slash)
    app.router.add_get("/{ontology_type}", get_ontology_type)
    app.router.add_get("/{ontology_type}/{ontology}", get_ontology)
    app.router.add_post("/{ontology_type}/upload-files", upload_files)

    return app
