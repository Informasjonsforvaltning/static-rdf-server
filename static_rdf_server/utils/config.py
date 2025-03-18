"""Module for various configs."""

from typing import Dict, List

RDF_CONTENT_TYPES: List[str] = [
    "text/turtle",  # default
    "application/rdf+xml",
    "application/ld+json",
    "text/n3",
]

STATIC_CONTENT_TYPES: List[str] = [
    "application/pdf",
    "image/png",
    "application/octet-stream",
    "image/jpeg",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/epub+zip",
    "text/xml",
]

SUPPORTED_CONTENT_TYPES: List[str] = (
    [
        "text/html",
    ]
    + RDF_CONTENT_TYPES
    + STATIC_CONTENT_TYPES
)

SUPPORTED_EXTENSIONS: List[str] = [
    "ttl",
    "html",
    "png",
    "pdf",
    "eap",
    "xsd",
    "jpg",
    "docx",
    "eapx",
    "epub",
    "uxf",
    "xml",
    "xlsx",
]

EXTENSION_MAP: Dict[str, str] = {
    "text/html": "html",
    "text/turtle": "ttl",
    "application/ld+json": "json",
    "application/rdf+xml": "xml",
    "text/n3": "n3",
}

# Default language is first in list:
SUPPORTED_LANGUAGES: List[str] = ["nb", "nb-NO", "nn", "nn-NO", "en", "en-GB"]

LANGUAGE_FILE_SUFFIX: Dict[str, str] = {
    "nb": "nb",
    "nb-NO": "nb",
    "nn": "nn",
    "nn-NO": "nn",
    "en": "en",
    "en-GB": "en",
}
