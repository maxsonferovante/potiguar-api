# Use a imagem base do Python
FROM python:3.12 as builder

# Instala o Poetry
RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
POETRY_VIRTUALENVS_IN_PROJECT=1 \
POETRY_VIRTUALENVS_CREATE=1 \
POETRY_CACHE_DIR=/tmp/poetry_cache

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de definição de dependências (pyproject.toml) e o arquivo de bloqueio de dependências (poetry.lock) para o diretório de trabalho
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# Instala as dependências do projeto usando o Poetry
RUN poetry install --without dev
# Copia o restante do código fonte para o diretório de trabalho

FROM python:3.12-slim as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . .

EXPOSE 8000
# Define o comando padrão para executar a aplicação

ENTRYPOINT ["poetry", "run", "python", "main.py"]