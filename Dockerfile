# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    PATH="$POETRY_HOME/bin:$PATH" \
    PYTHONPATH=/app

# Additional environment variables for Poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# ✅ Ensure Poetry is available in PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# Set working directory
WORKDIR /app

# Copy only pyproject.toml and poetry.lock if they exist
COPY pyproject.toml poetry.lock* /app/

# ✅ Install dependencies using Poetry correctly
RUN poetry install --no-root --no-dev

# Copy application code
COPY app ./app

# Expose FastAPI default port
EXPOSE 8000

# Start the FastAPI server
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
