ifeq ($(OS),Windows_NT)
    OS := windows
else
    OS := $(shell uname -s | tr A-Z a-z)
endif

# Цели
.PHONY: all mypy-check

# Основная цель
all: mypy-check migration

check_docker:
ifeq ($(OS),windows)
	@docker ps > NUL 2>&1 || (echo "Docker is not running. Please start Docker and try again." && exit 1)
else
	@docker ps > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker and try again." && exit 1)
endif

migrate:
	alembic upgrade head

mypy-check:
	mypy src --config-file pyproject.toml --explicit-package-bases

server-prod:
	cd src && \
	python3 -m presentation.web_api.main

migration:
	alembic revision --autogenerate
	alembic upgrade head

build:
	docker build -t backend_service.auth_service:latest .
