"""Nox sessions."""
import sys

import nox
from nox_poetry import Session, session

package = "app"
locations = "static_rdf_server", "tests", "noxfile.py"
nox.options.envdir = ".cache"
nox.options.reuse_existing_virtualenvs = True
nox.options.stop_on_first_error = False
nox.options.sessions = (
    "lint",
    "mypy",
    "pytype",
    "unit_tests",
    "integration_tests",
    "contract_tests",
)


@session(python="3.9")
def unit_tests(session: Session) -> None:
    """Run the unit test suite."""
    args = session.posargs
    session.install(".")
    session.install(
        "pytest",
        "pytest-asyncio",
        "requests",
        "selenium",
        "webdriver-manager",
    )
    session.run(
        "pytest",
        "-m unit",
        "-ra",
        *args,
    )


@session(python="3.9")
def integration_tests(session: Session) -> None:
    """Run the integration test suite."""
    args = session.posargs or ["--cov"]
    session.install(".")
    session.install(
        "coverage[toml]",
        "pytest",
        "pytest-cov",
        "pytest-aiohttp",
        "pyfakefs",
        "requests",
        "selenium",
        "webdriver-manager",
    )
    session.run(
        "pytest",
        "-m integration",
        "-ra",
        *args,
        env={
            "LOGGING_LEVEL": "DEBUG",
            "SERVER_ROOT": "/srv/www/static-rdf-server",
            "DATA_ROOT": "/srv/www/static-rdf-server/data",
            "STATIC_ROOT": "/srv/www/static-rdf-server/static",
        },
    )


@session(python="3.9")
def contract_tests(session: Session) -> None:
    """Run the contract test suite."""
    args = session.posargs
    session.install(".")
    session.install(
        "pytest",
        "pytest-docker",
        "pytest-aiohttp",
        "requests",
        "selenium",
        "webdriver-manager",
    )
    session.run(
        "pytest",
        "-m contract",
        "-ra",
        *args,
        env={
            "LOGGING_LEVEL": "DEBUG",
        },
    )


@session(python="3.9")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python="3.9")
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
        "flake8-assertive",
        "flake8-eradicate",
    )
    session.run("flake8", *args)


@session(python="3.9")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    requirements = session.poetry.export_requirements()
    session.install("safety")
    session.run("safety", "check", f"--file={requirements}", "--output", "text")


@session(python="3.9")
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or [
        "--install-types",
        "--non-interactive",
        "static_rdf_server",
        "tests",
    ]
    session.install(".")
    session.install("mypy", "pytest")
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@session(python="3.9")
def pytype(session: Session) -> None:
    """Run the static type checker using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.install("pytype")
    session.run("pytype", *args)


@session(python="3.9")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
