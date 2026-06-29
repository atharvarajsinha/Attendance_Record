from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    embeddings_dir: Path = Path("../media/embeddings")
    similarity_threshold: float = 0.70
    device: str = "cpu"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
settings.embeddings_dir.mkdir(parents=True, exist_ok=True)
