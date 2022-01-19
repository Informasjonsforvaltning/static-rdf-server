# static-rdf-server

Simple server that will serve ontologies in either html or RDF based on accept-header

The server supports all of the "standard" serializations of RDF:

- turtle (text/turtle)
- TBD

## Run locally

### Environment variables

To run the service locally, you need to supply a set of environment variables. A simple way to solve this is to supply a .env file in the project root directory.

A minimal .env:

```shell
LOGGING_LEVEL=DEBUG
API_KEY=supersecret
```

### Run i development-mode

```shell
% poetry run adev runserver -p 8080 --aux-port 8089 static_rdf_server
```

### Running the API in a wsgi-server (gunicorn)

```shell
% poetry run gunicorn static_rdf_server:create_app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker
```

### Running the wsgi-server in Docker

To build and run the api in a Docker container:

```shell
% docker build -t eu.gcr.io/digdir-fdk-infra/static-rdf-server:latest .
% docker run --env-file .env -p 8080:8080 -d eu.gcr.io/digdir-fdk-infra/static-rdf-server:latest
```

The easier way would be with docker-compose:

```shell
docker-compose up --build
```

## Usage

```shell
% curl -H "Accept: text/turtle" http://localhost:8080/examples/hello-world  # will return a hello-world RDF document
% curl -H  http://localhost:8080/examples/hello-world  # will return a hello-world HTML document
```

## Testing

We use [pytest](https://docs.pytest.org/en/latest/) for contract testing.

To run linters, checkers and tests:

```shell
% nox
```

To run specific test:

```shell
% nox -s integration_tests -- -k test_static_web_server.py
```

To run tests with logging, do:

```shell
% nox -s integration_tests -- --log-cli-level=DEBUG


## Location of ontology files

The static files to be served should be store under `/srv/www/static-rdf-server`. 

Ontolgies are grouped by types, e.g. 

- specifications
- vocabularies
- ...

This directory should be structured as follows:
```Shell
static-rdf-server
├── index.html
├── ontology-type_1
│  ├── ontology_1
│  │   ├── ontology_1.ttl 
│  │   └── ontology_1.html
│  ├── ontology_1
│  │   ├── ontology_1.ttl 
│  │   └── ontology_1.html
│  └── index.html
└── ontology-type_2
   ├── ontology_3
   │   ├── ontology_3.ttl 
   │   └── ontology_3.html
   ├── ontology_4
   │   ├── ontology_4.ttl 
   │   └── ontology_4.html
   └── index.html
```
