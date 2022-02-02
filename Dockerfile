FROM python:3.9

RUN mkdir -p /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install "poetry==1.1.12"
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

ADD static_rdf_server /app/static_rdf_server

# Setting PYTHONUNBUFFERED to a non empty value ensures that
# the python output is sent straight to terminal (e.g. your container log)
# without being first buffered and that you can see the output
# of your application (e.g. django logs) in real time.
# This also ensures that no partial output is held in a buffer
# somewhere and never written in case the python application crashes.
ENV PYTHONUNBUFFERED 1

EXPOSE 8080


CMD gunicorn "static_rdf_server:create_app"  --config=static_rdf_server/gunicorn_config.py --worker-class aiohttp.GunicornWebWorker
