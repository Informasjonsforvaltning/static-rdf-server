# static-rdf-server

Simple server that will serve ontologies in either html or RDF based on accept-header

The server supports all of the "standard" serializations of RDF:

- turtle (text/turtle)
- TBD

## Usage

### To upload content to the server

Say you want to upload two files to your ontology of ontology-type "vocabulary".

```shell
% curl -i \ 
 -H "X-API-KEY: supersecretapikey" \
 -F "ontology-rdf-file=@tests/files/examples/hello-world/hello-world.ttl;type=text/turtle" \
 -F "ontology-html-file=@tests/files/examples/hello-world/hello-world-en.html;type=text/html;headers=\"content-language: en\"" \
 -X PUT http://localhost:8080/examples/hello-world
```

If the ontology exists, it will be updated. Otherwise it will be created.

### To get content from the server

```shell
% curl -H "Accept: text/turtle" http://localhost:8080/examples/hello-world  # will return a hello-world RDF document
% curl -H  http://localhost:8080/examples/hello-world  # will return a hello-world HTML document
```

### To delete an ontology from the server

```shell
% curl -i -H "X-API-KEY: supersecretapikey" -X DELETE http://localhost:8080/examples/hello-world
```

## Location of ontology files

Ontolgies are grouped by types, e.g.

- specifications
- vocabularies
- ...

This directory on the server will be structured as follows:

```Shell
static-rdf-server
├── ontology-type-1
│  ├── ontology-1
│  │   ├── ontology-1.ttl 
│  │   ├── ontology-1-en.html 
│  │   ├── ontology-1-nb.html 
│  │   └── ontology-1-nn.html
│  ├── ontology_2
│  │   └── ontology-2.ttl 
│  │   ├── ontology-2-en.html 
│  │   ├── ontology-2-nb.html 
│  │   └── ontology-2-nn.html
│  └── index.html
├── ontology-type-2
|  ├── ontology-3
|  │   ├── ontology-3.ttl 
|  │   ├── ontology-3-en.html 
|  │   ├── ontology-3-nb.html 
|  │   └── ontology-3-nn.html
|  ├── ontology-4
|  │   ├── ontology-4.ttl 
|  │   ├── ontology-4-en.html 
|  │   ├── ontology-4-nb.html 
|  │   └── ontology-4-nn.html
|  └── index.html
└── index.html
```

The static files to be served should be store under `/srv/www/static-rdf-server`.

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
```
