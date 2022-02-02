"""Module for util functions."""
from typing import Any, Tuple
from xmlrpc.client import Boolean

from multidict import CIMultiDictProxy
from rdflib import Graph
from rdflib.exceptions import ParserError


class ContentTypeNotSupported(Exception):
    """Class representing the content-type not supported exception."""

    pass


async def decide_content_type_and_suffix(headers: CIMultiDictProxy) -> Tuple[str, str]:
    """Return content_type and suffix based on request."""
    # Default content-type/suffix:
    content_type: str = "text/html"
    suffix: str = ".html"

    # We inspect the accept-header:
    try:
        if "text/turtle" in headers["Accept"]:
            content_type = "text/turtle"
            suffix = ".ttl"
        elif "text/html" in headers["Accept"]:
            pass
        elif "*/*" in headers["Accept"]:
            pass
        else:
            raise ContentTypeNotSupported(
                f'None of the content-types in {headers["Accept"]} are supported.'
            )
    except KeyError:
        pass  # pragma: no cover

    return (content_type, suffix)


async def valid_file_content(file_extension: str, file_content: Any) -> Boolean:
    """Return True if file-conent is valid."""
    if "html" == file_extension:
        pass
    else:
        try:
            Graph().parse(data=file_content)
        except (ParserError, SyntaxError):
            return False

    return True


async def valid_file_extension(file_extension: str) -> Boolean:
    """Return True if valid file-extension."""
    if file_extension.lower() in ["ttl", "html"]:
        return True

    return False
