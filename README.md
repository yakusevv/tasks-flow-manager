# Tasks Flow Manager

A FastAPI-based service that executes sequences of tasks with conditional routing based on task outcomes.

---

## Task Dependencies

Tasks do not declare explicit upstream dependencies. Instead, they share a **context object** that accumulates results as tasks complete — each task can read any previous task's result from `context.results`. Execution order is determined by **conditions** in the flow config, which map each task's outcome to the next task to run.

Example chain from `config/flows.json`:

```
task1 (FetchDataTask)
  └─► on success ──► task2 (ProcessDataTask)
                        └─► on success ──► task3 (StoreDataTask)
                                              └─► (no condition) ──► end
```

---

## Success and Failure Evaluation

Each task's `run()` method is wrapped by `execute()`:

- **SUCCESS**: `run()` returns without raising an exception.
- **FAILURE**: `run()` raises any exception; the error message is captured in the result.

---

## Task Success or Failure

After each task, a `ConditionEvaluator` picks the next task based on the outcome:

- **Success** → routes to `target_task_success`
- **Failure** → routes to `target_task_failure` (can be `"end"` to stop the flow)
- **No condition defined** → flow ends normally

If routing leads to `"end"` after a failure, `final_outcome` is `ended_early` and errors are collected. A full successful chain produces `completed`.

**Cycle detection:** if a task is scheduled to run twice, a `FlowCycleError` is raised (HTTP 409).

---

## Storage

For demonstration purposes flows are currently defined in `config/flows.json`. For a production setup some NoSQL db could be used (e.g. **MongoDB**).

---

## Running the Application

```bash
# Install dependencies
uv sync

# Start the server from the app/ folder
uv run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs: `http://localhost:8000/docs`.

Run from the project root — flows are loaded from `config/flows.json` relative to the working directory.

---

## Running Tests

```bash
uv run pytest
```

---

## API Reference

| Method | Path                      | Description           |
| ------ | ------------------------- | --------------------- |
| `GET`  | `/health`                 | Health check          |
| `GET`  | `/v1/flows`               | List all flows        |
| `POST` | `/v1/flows/{flow_id}/run` | Run a flow            |
| `GET`  | `/v1/tasks`               | List registered tasks |
