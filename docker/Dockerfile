FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.6.8 /uv /bin/uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_PROJECT_ENVIRONMENT="/opt/.venv" \
    PATH="/opt/.venv/bin:$PATH"

WORKDIR /app
COPY . ./

RUN uv sync --frozen --no-cache

EXPOSE 8000
ENTRYPOINT ["/app/docker/entrypoint.sh"]
