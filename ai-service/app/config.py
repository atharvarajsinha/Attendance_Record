from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    embeddings_dir: Path = Path("../media/embeddings")
    similarity_threshold: float = 0.45
    verification_max_workers: int = 4
    device: str = "cpu"
    insightface_model_name: str = "buffalo_l"
    detection_width: int = 640
    detection_height: int = 640

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @computed_field
    @property
    def insightface_ctx_id(self) -> int:
        return -1 if self.device.lower() == "cpu" else 0

    @computed_field
    @property
    def insightface_providers(self) -> list[str]:
        if self.device.lower() == "cpu":
            return ["CPUExecutionProvider"]
        return ["CUDAExecutionProvider", "CPUExecutionProvider"]

    @computed_field
    @property
    def detection_size(self) -> tuple[int, int]:
        return (self.detection_width, self.detection_height)


settings = Settings()
settings.embeddings_dir.mkdir(parents=True, exist_ok=True)
