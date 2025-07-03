FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
#
# 1. Install _only_ the third-party deps first so we keep the Docker cache
#    even when the source code changes.  --no-root skips installing our
#    own package, which would otherwise fail because /app hasn't been
#    copied yet.
RUN poetry install --only main --no-root --no-interaction --no-ansi

# Copy application code (everything else in the repo)
COPY . .

# 2. Now that /app/* exists, install the project itself
RUN poetry install --only main --no-interaction --no-ansi

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# default launch
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 