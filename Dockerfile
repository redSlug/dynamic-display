FROM python:3.14 as base

WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM base as build

COPY . .

RUN mkdir -p buildinfo && ./update_version.sh

CMD ./gunicorn.sh
