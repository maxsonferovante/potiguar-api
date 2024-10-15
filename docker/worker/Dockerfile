#Use a imagem base do Python
FROM python:3.12 AS builder

WORKDIR /app

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
POETRY_VIRTUALENVS_IN_PROJECT=1 \
POETRY_VIRTUALENVS_CREATE=1 \
POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./

RUN poetry install

FROM python:3.12-slim AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . .

CMD ["celery", "-A", "src.apps.tasks.tasks_service", "worker", "--loglevel=INFO"]