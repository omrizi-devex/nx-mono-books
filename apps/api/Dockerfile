FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/
WORKDIR /workspace

# Copy everything, build wheels for workspace members
COPY . .
RUN uv build --all-packages --out-dir /wheels

# Install third-party deps + your workspace wheels into a clean venv
RUN uv venv /opt/venv
RUN uv pip install --python /opt/venv/bin/python --no-editable \
    -r <(uv export --all-packages --no-dev --no-emit-project) \
    /wheels/*.whl

FROM python:3.12-slim AS runtime
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
