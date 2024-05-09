FROM python:3.8-slim-buster as base

WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# TODO(bdettmer): Run db migrations somewhere else

FROM base as build

RUN ./update_version.sh

RUN python update_display.py

CMD ./gunicorn.sh
