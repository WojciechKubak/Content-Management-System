FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /translations-service

COPY /Pipfile.lock /Pipfile /translations-service/

RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

COPY . /translations-service
