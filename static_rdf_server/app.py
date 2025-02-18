"""Module for server."""

import logging
import os
from typing import Any

from aiohttp import web
from aiohttp_middlewares import cors_middleware, error_middleware
from dotenv import load_dotenv

from .routes import (
    delete_ontology,
    get_ontology,
    get_ontology_type,
    get_slash,
    ping,
    put_ontology,
    put_ontology_type,
    ready,
)

load_dotenv()
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
SERVER_ROOT = os.getenv("SERVER_ROOT", "/srv/www/static-rdf-server")
DATA_ROOT = os.getenv("DATA_ROOT", os.path.join(SERVER_ROOT, "data"))
STATIC_ROOT = os.getenv("STATIC_ROOT", os.path.join(SERVER_ROOT, "static"))
DEFAULT_LANGUAGE = "nb"


async def create_app() -> web.Application:
    """Create an web application."""
    origins = os.getenv("CORS_ORIGIN_PATTERNS", "*").split(",")
    origins = [origin.strip() for origin in origins]
    allow_all = "*" in origins

    app = web.Application(
        middlewares=[
            cors_middleware(
                allow_all=allow_all,
                origins=None if allow_all else origins,
                allow_methods=["GET"],
                allow_headers=["*"],
            ),
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
    app.router.add_put("/{ontology_type}", put_ontology_type)
    app.router.add_get("/{ontology_type}/{ontology}", get_ontology)
    app.router.add_get("/{ontology_type}/{ontology}/{version}", get_ontology)
    app.router.add_put("/{ontology_type}/{ontology}", put_ontology)
    app.router.add_put("/{ontology_type}/{ontology}/{version}", put_ontology)
    app.router.add_delete("/{ontology_type}/{ontology}", delete_ontology)
    app.router.add_delete("/{ontology_type}/{ontology}/{version}", delete_ontology)

    async def app_context(app: Any) -> Any:
        # Set up context:
        app["SERVER_ROOT"] = SERVER_ROOT
        app["DATA_ROOT"] = DATA_ROOT
        app["STATIC_ROOT"] = STATIC_ROOT
        app["DEFAULT_LANGUAGE"] = DEFAULT_LANGUAGE

        yield

        pass

    app.cleanup_ctx.append(app_context)

    return app
