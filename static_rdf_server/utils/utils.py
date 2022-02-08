"""Module for util functions."""
from typing import Any, Optional, Tuple

from rdflib import Graph
from rdflib.exceptions import ParserError


class ContentTypeNotSupported(Exception):
    """Class representing the content-type not supported exception."""

    pass


async def decide_content_and_extension(
    accept_header: Optional[str] = None, accept_language_header: Optional[str] = None
) -> Tuple[str, str, str]:
    """Return content_language, content_type and extension based on request."""
    # Default content-type/content-language/extension:
    content_language = ""
    content_type: str = "text/html"
    extension: str = "html"

    # We inspect the accept-header:
    if accept_header:
        if "text/turtle" in accept_header:
            content_type = "text/turtle"
            content_language = ""
            extension = "ttl"
        elif "text/html" in accept_header:
            pass
        elif "*/*" in accept_header:
            pass
        else:
            raise ContentTypeNotSupported(
                f"None of the content-types in {accept_header} are supported."
            )
    else:
        pass  # pragma: no cover

    # for text/html, we inspect the accept-language-header:
    if content_type == "text/html":
        if accept_language_header:
            content_language = accept_language_header
        else:
            pass

    return (content_type, content_language, extension)


async def valid_file_content(file_extension: str, file_content: Any) -> bool:
    """Return True if file-conent is valid."""
    if "html" == file_extension:
        pass
    else:
        try:
            Graph().parse(data=file_content)
        except (ParserError, SyntaxError):
            return False

    return True


async def valid_file_extension(file_extension: str) -> bool:
    """Return True if valid file-extension."""
    if file_extension.lower() in ["ttl", "html"]:
        return True

    return False


async def valid_content_type(content_type: str) -> bool:
    """Return True if supported content-type."""
    if content_type.lower() in ["text/turtle", "text/html"]:
        return True

    return False
