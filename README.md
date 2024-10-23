# Potiguar API
A Potiguar API é um serviço projetado para facilitar a consulta de infrações de veículos, subsídios e multas no Rio Grande do Norte. Ela fornece uma maneira robusta e eficiente de acessar e gerenciar essas informações através de uma API bem estruturada.

## Funcionalidades

- **FastAPI**: Utiliza FastAPI para construir a API, garantindo alto desempenho e interfaces fáceis de usar.
- **Celery**: Integra Celery para lidar com tarefas assíncronas, tornando-o adequado para processamento em segundo plano.
- **Uvicorn**: Usa Uvicorn como o servidor ASGI para servir a aplicação FastAPI.
- **Poetry**: Gerencia dependências e ambientes virtuais com Poetry, garantindo um ambiente consistente e reproduzível.

## Requisitos

- Python 3.12+
- Poetry
- Redis (para backend do Celery)
- FastAPI
- Uvicorn
- Celery

## Instalação

Siga os passos abaixo para configurar e executar a Potiguar API em sua máquina local.

## Iniciar Serviço

## Passo 1 - Criar ambiente

- Instale as dependências usando Poetry:

```bash
poetry install
```

## Passo 2 - Iniciar serviço localmente

1. Execute o serviço com Uvicorn:

```bash
uvicorn "src.app_module:http_server" --host "0.0.0.0" --port "8000" --reload
```

2. Inicie o worker do Celery e o Flower para monitoramento:

```bash
poetry run celery -A src.apps.tasks.tasks_service worker --loglevel=INFO
```

```bash
poetry run celery -A src.apps.tasks.tasks_service flower
```

## Passo 3 - Enviar requisições

Vá para a documentação do FastAPI e use seus endpoints da API - http://127.0.0.1/api/docs
