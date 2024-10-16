# Potiguar API

Potiguar API is a service designed to facilitate the consultation of vehicle infractions, subsidies, and fines in Rio Grande do Norte. It provides a robust and efficient way to access and manage this information through a well-structured API.

## Features

- **FastAPI**: Utilizes FastAPI for building the API, ensuring high performance and easy-to-use interfaces.
- **Celery**: Integrates Celery for handling asynchronous tasks, making it suitable for background processing.
- **Uvicorn**: Uses Uvicorn as the ASGI server for serving the FastAPI application.
- **Poetry**: Manages dependencies and virtual environments with Poetry, ensuring a consistent and reproducible environment.

## Requirements

- Python 3.12+
- Poetry
- Redis (for Celery backend)
- FastAPI
- Uvicorn
- Celery

## Installation

Follow the steps below to set up and run the Potiguar API on your local machine .

## Start Service

## Step 1 - Create environment

- Install dependencies using Poetry:

```bash
poetry install
```

## Step 2 - Start service locally

1. Run the service with Uvicorn:

```bash
uvicorn "src.app_module:http_server" --host "0.0.0.0" --port "8000" --reload
```

2. Start Celery worker and Flower for monitoring:

```bash
poetry run celery -A src.apps.tasks.tasks_service worker --loglevel=INFO
```

```bash
poetry run celery -A src.apps.tasks.tasks_service flower
```



## Step 3 - Send requests

Go to the fastapi docs and use your api endpoints - http://127.0.0.1/api/docs


```
