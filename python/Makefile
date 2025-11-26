.PHONY: help up down build test lint format logs shell clean install

# Default target - show help
help:
	@echo "Available commands:"
	@echo "  make up        - Start the service in Docker"
	@echo "  make down      - Stop the service"
	@echo "  make build     - Build Docker images"
	@echo "  make test      - Run tests in Docker"
	@echo "  make lint      - Run linting checks in Docker"
	@echo "  make format    - Auto-format code in Docker"
	@echo "  make logs      - View service logs"
	@echo "  make shell     - Open bash shell in container"
	@echo "  make clean     - Remove containers and volumes"
	@echo "  make install   - Install dependencies in Docker"

# Start the recommendation service
up:
	docker-compose up --build

# Stop all services
down:
	docker-compose down

# Build Docker images
build:
	docker-compose build

# View logs from running containers
logs:
	docker-compose logs -f

# Open a bash shell in the service container
shell:
	docker-compose run --rm recommendation-service /bin/bash

# Run all tests in Docker
test:
	docker-compose --profile test run --rm test

# Clean up containers, volumes, and images
clean:
	docker-compose down -v
	docker system prune -f

# Install/update dependencies in Docker (rebuilds the image)
install:
	docker-compose build --no-cache

# Run linting checks (ruff, black, mypy) in Docker
lint:
	@echo "Running Ruff..."
	docker-compose --profile test run --rm test poetry run ruff check .
	@echo "Running Black..."
	docker-compose --profile test run --rm test poetry run black --check .
	@echo "Running Mypy..."
	docker-compose --profile test run --rm test poetry run mypy .

# Auto-format code with ruff and black in Docker
format:
	@echo "Formatting with Ruff..."
	docker-compose --profile test run --rm test poetry run ruff check --fix .
	@echo "Formatting with Black..."
	docker-compose --profile test run --rm test poetry run black .
