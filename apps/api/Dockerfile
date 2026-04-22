FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /workspace
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

COPY pyproject.toml uv.lock .python-version ./
COPY apps/api/pyproject.toml apps/api/pyproject.toml
COPY libs/common/pyproject.toml libs/common/pyproject.toml
RUN uv sync --frozen --no-dev --package api --no-install-workspace

COPY libs/ libs/
RUN uv sync --frozen --no-dev --package api --no-editable

FROM python:3.12-slim AS runtime
COPY --from=builder /opt/venv /opt/venv
COPY apps/api/src /app
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8888"]
