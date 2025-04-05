FROM python:3.12.7-alpine

RUN apk add --no-cache make build-base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /backend

COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv && \
    uv pip install -e ".[dev]" --system

COPY . .

ENTRYPOINT ["make", "run"]