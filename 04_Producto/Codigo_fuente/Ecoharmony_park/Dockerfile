FROM python:3.13-slim

# uv con la misma versión que se usa en desarrollo.
COPY --from=ghcr.io/astral-sh/uv:0.11.17 /uv /bin/uv

# El venv vive fuera de /app para que el código montado en desarrollo no lo tape.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Primero las dependencias: esta capa solo se reconstruye si cambia el lock.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .

EXPOSE 8000
