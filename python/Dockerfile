# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

RUN pip install poetry poetry-plugin-export

COPY pyproject.toml poetry.lock* ./

# Regenerate lock file and install all dependencies (including dev)
RUN poetry lock && \
    poetry install --no-root && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes

# Download pre-trained model
COPY download_model.py ./
RUN mkdir -p /app/models && poetry run python download_model.py

# Stage 2: Runner
FROM python:3.11-slim as runner

WORKDIR /app

# Install dependencies
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Copy models from builder stage
COPY --from=builder /app/models ./models

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
