"""Module for server."""
import logging
import os
from typing import Any

from aiohttp import web
from aiohttp_middlewares import cors_middleware, error_middleware
from dotenv import load_dotenv

from .routes import (
    get_ontology,
    get_ontology_type,
    get_slash,
    ping,
    put_ontology,
    ready,
)

load_dotenv()
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
DATA_ROOT = "/srv/www/static-rdf-server"
DEFAULT_LANGUAGE = "nb"


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
    app.router.add_put("/{ontology_type}/{ontology}", put_ontology)

    async def app_context(app: Any) -> Any:
        # Set up context:
        app["DATA_ROOT"] = DATA_ROOT
        app["DEFAULT_LANGUAGE"] = DEFAULT_LANGUAGE

        yield

        pass

    app.cleanup_ctx.append(app_context)

    return app
