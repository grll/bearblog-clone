FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen

# Copy application code
COPY . .

# Create media directory
RUN mkdir -p /app/media

# Create directories and collect static files
RUN mkdir -p data static_collected
RUN uv run python manage.py collectstatic --noinput

# Run migrations and start gunicorn
CMD uv run python manage.py migrate && \
    uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2