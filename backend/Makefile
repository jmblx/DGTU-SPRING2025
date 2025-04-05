ifeq ($(OS),Windows_NT)
    OS := windows
else
    OS := $(shell uname -s | tr A-Z a-z)
endif

check_docker:
ifeq ($(OS),windows)
	@docker ps > NUL 2>&1 || (echo "Docker is not running. Please start Docker and try again." && exit 1)
else
	@docker ps > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker and try again." && exit 1)
endif

migrate:
	alembic upgrade head

run:
	cd src && \
	uvicorn presentation.web_api.main:app --reload

run-prod:
	cd src && \
	python3 presentation/web_api/main.py

migration:
	alembic revision --autogenerate

build:
	docker build -t race_simulation.api:latest .
