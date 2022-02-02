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
% docker build -t static-rdf-server:latest .
% docker run --env-file .env -p 8080:8080 -d static-rdf-server:latest
```

The easier way would be with docker-compose:

```shell
docker-compose up --build
```

## Usage

To get content from the server:

```shell
% curl -H "Accept: text/turtle" http://localhost:8080/examples/hello-world  # will return a hello-world RDF document
% curl -H  http://localhost:8080/examples/hello-world  # will return a hello-world HTML document
```

### To post content to the server

Say you want to post two files to your ontology of ontology-type "vocabulary".

```shell
% curl -i \
 -H "X-API-KEY: <a valid api-key>" \
 -H "Content-Type: multipart/form-data" \
 -F "ontology-rdf-file=@path/to/your/files/ontology.ttl;type=text/turtle" \
 -F "ontology-html-file=@path/to/your/files/ontology.html;type=text/html" \
 -X POST http://localhost:8000/vocabulary/upload-files
```

If all goes well you should receive a 201 Created status-code and a relative URL to your content in the Location-header.

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
