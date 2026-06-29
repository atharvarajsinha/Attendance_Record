from abc import ABC, abstractmethod
from io import BytesIO
from typing import Iterable

import numpy as np
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings


class FaceEngine(ABC):
    @abstractmethod
    def image_to_embeddings(self, image_bytes: bytes) -> list[np.ndarray]:
        """Return one embedding per detected face."""

    @staticmethod
    def best_similarity(query: np.ndarray, candidates: Iterable[np.ndarray]) -> float:
        scores = [float(cosine_similarity([query], [candidate])[0][0]) for candidate in candidates]
        return max(scores) if scores else 0.0


class FaceNetEngine(FaceEngine):
    def __init__(self) -> None:
        self.mtcnn = MTCNN(image_size=160, margin=20, keep_all=True, device=settings.device)
        self.model = InceptionResnetV1(pretrained="vggface2").eval().to(settings.device)

    def image_to_embeddings(self, image_bytes: bytes) -> list[np.ndarray]:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        faces = self.mtcnn(image)
        if faces is None:
            return []
        if faces.ndim == 3:
            faces = faces.unsqueeze(0)
        with torch.no_grad():
            embeddings = self.model(faces.to(settings.device)).cpu().numpy()
        return [embedding.astype(np.float32) for embedding in embeddings]
