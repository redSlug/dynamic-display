FROM python:3.10-bookworm as base

WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# TODO(bdettmer): Run db migrations somewhere else

FROM base as build

RUN ./update_version.sh

CMD ./gunicorn.sh
