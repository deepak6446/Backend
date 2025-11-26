# Python Recommendation Service

A production-ready recommendation microservice built with FastAPI, following SOLID principles and clean architecture.

## Features

*   **Recommendation Engine**: Configurable strategy pattern (Dummy, Rule-based, ML).
*   **API**: RESTful API with header-based versioning.
*   **Architecture**: Clean architecture with separation of concerns.
*   **DevOps**: Dockerized, CI/CD with GitHub Actions, Pre-push hooks.
*   **Quality**: Comprehensive testing (Pytest), Linting (Ruff), Formatting (Black), Type Checking (Mypy).

## Quick Start (Docker)

### Prerequisites

*   Docker & Docker Compose

### Running the Service

1.  **Start the service**:
    ```bash
    docker-compose up --build
    ```

2.  **Access the API**:
    *   API: `http://localhost:8000`
    *   Swagger UI: `http://localhost:8000/docs`
    *   Health Check: `http://localhost:8000/health`

3.  **Stop the service**:
    ```bash
    docker-compose down
    ```

### Testing in Docker

Run tests inside Docker:
```bash
make test
# or
docker-compose --profile test run --rm test
```

## Available Make Commands

All commands run in Docker - no local installation needed:

```bash
make help      # Show all available commands
make up        # Start the service (builds if needed)
make down      # Stop the service
make build     # Build Docker images
make test      # Run all tests
make lint      # Run linting checks (ruff, black, mypy)
make format    # Auto-format code
make logs      # View service logs
make shell     # Open bash shell in container
make clean     # Remove containers and volumes
make install   # Rebuild images with fresh dependencies
```

## API Documentation

### POST /recommendations

Get recommendations for a user based on their recent actions.

**Headers**:
*   `X-API-Version`: `v1` (Required)

**Request Body**:
```json
{
  "userId": "string",
  "actions": ["string", "string", "string"]
}
```

**Response**:
```json
{
  "recommendations": [
    {
      "action": "string",
      "score": 0.95
    }
  ],
  "modelVersion": "dummy",
  "requestId": "uuid"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/recommendations \
  -H "Content-Type: application/json" \
  -H "X-API-Version: v1" \
  -d '{
    "userId": "user-123",
    "actions": ["gmail", "calendar", "drive"]
  }'
```

## Development

### Local Development (without Docker)

If you prefer to run locally without Docker:

1.  **Install Poetry**:
    ```bash
    pip install poetry
    ```

2.  **Install dependencies**:
    ```bash
    poetry install
    ```

3.  **Run the service**:
    ```bash
    poetry run uvicorn app.main:app --reload
    ```

### Testing

```bash
poetry run pytest
```

### Linting & Formatting

```bash
poetry run ruff check .
poetry run black .
poetry run mypy .
```

## Project Structure

*   `app/`: Application source code.
    *   `api/`: API route handlers.
    *   `core/`: Configuration and core utilities.
    *   `models/`: Pydantic data models.
    *   `services/`: Business logic and strategies.
*   `tests/`: Test suite (Unit and Integration).
