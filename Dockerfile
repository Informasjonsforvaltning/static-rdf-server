FROM ghcr.io/astral-sh/uv:python3.10-alpine

RUN mkdir -p /app
WORKDIR /app

RUN pip install --upgrade pip
COPY pyproject.toml /app/

# uv Project initialization:
RUN uv pip compile pyproject.toml -o uv.lock && \
    uv pip install --system -r uv.lock

ADD static_rdf_server /app/static_rdf_server

# Setting PYTHONUNBUFFERED to a non empty value ensures that
# the python output is sent straight to terminal (e.g. your container log)
# without being first buffered and that you can see the output
# of your application (e.g. django logs) in real time.
# This also ensures that no partial output is held in a buffer
# somewhere and never written in case the python application crashes.
ENV PYTHONUNBUFFERED 1

EXPOSE 5000


CMD gunicorn "static_rdf_server:create_app"  --config=static_rdf_server/gunicorn_config.py --worker-class aiohttp.GunicornWebWorker
