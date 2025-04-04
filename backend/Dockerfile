FROM python:3.12.7-alpine

RUN apk add --no-cache make build-base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/usr/src

WORKDIR /backend-service.auth_service

COPY poetry.lock pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .

RUN chmod +x /backend-service.auth_service/docker/serve.sh && chmod +x /backend-service.auth_service/docker/migrate.sh