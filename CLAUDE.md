# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run the server (must run from project root; flows load from config/flows.json)
uv run uvicorn main:app --reload --app-dir app

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/unit/test_flow_engine.py

# Run a single test by name
uv run pytest tests/unit/test_flow_engine.py::test_name
```

> Note: `mypy_path = "app"` is set in `pyproject.toml`, so mypy resolves imports from `app/` directly (no package prefix needed).

## Architecture

The app is a FastAPI service that executes named flows — sequences of async tasks with conditional routing.

**Layers:**

- `app/main.py` — FastAPI app entry point; mounts the v1 router
- `app/api/api_v1/` — route handlers for `/v1/flows` and `/v1/tasks`
- `app/core/` — execution engine, flow config loader, task registry, condition evaluator
- `app/tasks/` — concrete task implementations (subclass `BaseTask`)
- `app/models/flow.py` — all Pydantic schemas used throughout the app
- `config/flows.json` — static flow definitions (loaded at startup via `FlowLoader`)

**Execution model:**

1. `FlowLoader` parses `config/flows.json` into `FlowConfigSchema` objects (validated by Pydantic, including referential integrity checks).
2. `FlowEngine.run()` walks the flow: starting at `start_task`, executing each task via `BaseTask.execute()`, then calling `ConditionEvaluator.next_task()` to determine the next step based on `success`/`failure` outcome.
3. Tasks share a `FlowContextSchema` — results from previous tasks are accessible via `context.results[task_name]`.
4. A visited-set detects cycles; duplicate execution raises `FlowCycleError` (→ HTTP 409).
5. The task registry (`core/registry.py`) instantiates and registers all concrete tasks at import time; `FlowEngine` resolves tasks by name from it.

**Adding a new task:**

1. Subclass `BaseTask` in `app/tasks/`, set `name`, implement `async run(context)`.
2. Register the instance in `app/core/registry.py`.
3. Reference the task by name in `config/flows.json`.

## Tests

Tests use `starlette.TestClient` (sync) for API tests and plain `pytest-asyncio` for unit tests. `tests/helpers.py` provides `make_flow_config()` and `make_mock_task()` builder utilities. Fixtures live in `tests/conftest.py`.


## Commit changes

- Allow CLAUDE do to commit changes and generate commit messages based on the changes made in the code. Ensure that the commit message is descriptive and follows the conventional commit format (e.g., `feat: add new task for data processing`).
- Commit messages must be a single line — no multiline body.
