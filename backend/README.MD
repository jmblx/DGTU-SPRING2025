---

## Установка зависимостей 

### uv:
```shell
pip install uv
```

### Рабочие зависимости:

#### Windows:
```shell
cd backend
uv venv .venv
.venv\Scripts\activate
uv pip install -e .
```

#### Linux/macOS:
```shell
cd backend
uv venv .venv
source .venv/bin/activate
uv pip install -e .
```

### Для разработки backend:
```shell
uv pip install -e ".[dev]"
```

---

## Запуск для локальной разработки

В корне проекта можно использовать:

```bash
make run
```

Эта команда запускает Gunicorn с `uvicorn.workers.UvicornWorker` и считывает параметры из конфигурационного файла (`config.toml`).  
Используется `main:app` из FastAPI.

> ⚠️ Для Windows вместо `make` можно запускать эквивалентную команду вручную:
> ```bash
> uvicorn main:app --reload
> ```

---

## Конфигурация `config.toml`

```toml
[global]
debug = false  # Влияет на поведение Gunicorn/Uvicorn (например, отключает авто-перезапуск и логгирование в dev-режиме)

[gunicorn]
bind = "0.0.0.0:8080"
workers = 2
timeout = 30
worker_class = "uvicorn.workers.UvicornWorker"

[database]
host = "109.120.178.67"
port = "5432"
name = "race_simulation"
user = "postgres"
password = "postgres"

[redis]
host = "109.120.178.67"
port = 6379
```

---

## ERD (Entity Relationship Diagram)

![erd](erd.jpg)

---
