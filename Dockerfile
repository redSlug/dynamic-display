FROM python:3.8-slim-buster as base

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# TODO(bdettmer): Run db migrations somewhere else

FROM base as build

RUN ./update_version.sh

CMD ./gunicorn.sh
