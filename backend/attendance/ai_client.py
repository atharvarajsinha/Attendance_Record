from pathlib import Path
from typing import Any

import requests
from django.conf import settings


class AIServiceError(RuntimeError):
    pass


class AIServiceClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or settings.AI_SERVICE_URL).rstrip("/")

    def register_face(self, student_id: str, image_path: str) -> dict[str, Any]:
        return self._post_image("/register-face", image_path, data={"student_id": student_id})

    def verify_attendance(self, image_path: str) -> dict[str, Any]:
        return self._post_image("/verify-attendance", image_path)

    def _post_image(self, endpoint: str, image_path: str, data: dict[str, str] | None = None) -> dict[str, Any]:
        path = Path(image_path)
        try:
            with path.open("rb") as image_file:
                response = requests.post(
                    f"{self.base_url}{endpoint}",
                    data=data or {},
                    files={"image": (path.name, image_file)},
                    timeout=60,
                )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            detail = getattr(exc.response, "text", str(exc)) if hasattr(exc, "response") else str(exc)
            raise AIServiceError(f"AI service request failed: {detail}") from exc
