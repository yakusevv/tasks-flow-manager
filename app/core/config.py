from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_uri: str | None = None
    mongodb_db: str = "flows_manager"
    mongodb_collection: str = "flows"
