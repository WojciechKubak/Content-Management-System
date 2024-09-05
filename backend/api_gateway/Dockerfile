FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /api-gateway

COPY Pipfile Pipfile.lock /api-gateway/

RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

COPY . /api-gateway
