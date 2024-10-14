#Use a imagem base do Python
FROM python:3.12 as builder

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala o Poetry
RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
POETRY_VIRTUALENVS_IN_PROJECT=1 \
POETRY_VIRTUALENVS_CREATE=1 \
POETRY_CACHE_DIR=/tmp/poetry_cache

COPY . .

# Instala as dependências do projeto usando o Poetry
RUN poetry install


FROM python:3.12-slim as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}


EXPOSE 8000

ENTRYPOINT ["poetry", "run","uvicorn", "src.app_module:http_server", "--port", "8000", "--reload"]