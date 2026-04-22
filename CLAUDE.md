# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an Nx-managed Python monorepo. **Nx** handles task orchestration and affected-project detection; **uv** manages the Python workspace and dependencies. Node/npm are present only to run Nx — there is no JavaScript application code.

## Project Structure

- `apps/` — deployable applications (not installable packages). Currently: `apps/api` (FastAPI).
- `libs/` — installable Python packages shared across apps. Currently: `libs/common`.
- `pyproject.toml` (root) — uv workspace root; declares `libs/*` and `apps/*` as workspace members.
- `uv.lock` — single lockfile for the entire workspace.

The `api` app declares `common` as a dependency via `[tool.uv.sources]` workspace reference and imports it as a regular Python package (`from common import greet`).

## Common Commands

All tasks run via Nx from the repo root. Nx caches `test`, `lint`, and `typecheck` outputs.

```sh
# Run all targets for a specific project
npx nx run api:serve        # Start FastAPI dev server on :8000
npx nx run api:test         # Run pytest for the api app
npx nx run api:lint         # Ruff check
npx nx run api:typecheck    # mypy

# Run a single test file directly
uv run pytest tests/test_main.py   # from apps/api/

# Run targets only on projects affected by current changes
npx nx affected -t lint
npx nx affected -t test
npx nx affected -t typecheck

# Install/sync all workspace packages
uv sync --all-packages
```

## Python Environment

- Python version is pinned by `.python-version` at the workspace root.
- `uv` manages the shared `.venv` at the workspace root.
- Run Python tools with `uv run <tool>` — this ensures the workspace venv is used.
- Never run `pip install` directly; use `uv add` or edit `pyproject.toml` then `uv sync`.

## Adding a New Library

1. Create `libs/<name>/` with its own `pyproject.toml` (use `uv_build` as build backend, like `libs/common`).
2. Add a `project.json` with `test`, `lint`, and `typecheck` targets (follow `libs/common/project.json`).
3. Add `<name> = { workspace = true }` under `[tool.uv.sources]` in any consuming app's `pyproject.toml`.

## CI

GitHub Actions (`.github/workflows/ci.yaml`) runs on push/PR to `main`:
1. Uses `nrwl/nx-set-shas` to determine base/head SHAs.
2. Runs `npx nx affected -t lint typecheck test --parallel=3` — only affected projects are checked.

## Docker

`apps/api/Dockerfile` uses a two-stage build:
1. **builder**: builds wheels for all workspace packages via `uv build --all-packages`, then installs them into `/opt/venv` without editable installs.
2. **runtime**: copies only the venv; starts `uvicorn api.main:app`.
