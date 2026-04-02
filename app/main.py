from fastapi import FastAPI

from api.api_v1.api import api as api_v1


app = FastAPI(title="Flow Manager", version="0.1.0")


@app.get("/health")
def healthcheck():
    """Simple health check endpoint."""
    return {"status": "ok"}


app.include_router(api_v1)
