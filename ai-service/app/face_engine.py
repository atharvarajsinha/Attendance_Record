from abc import ABC, abstractmethod
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from io import StringIO
from typing import Iterable, Iterator
import warnings

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from app.config import settings


class FaceEngine(ABC):
    @abstractmethod
    def image_to_embeddings(self, image_bytes: bytes) -> list[np.ndarray]:
        """Return one normalized embedding per detected face."""

    @staticmethod
    def best_similarity(query: np.ndarray, candidates: Iterable[np.ndarray]) -> float:
        query_norm = _l2_normalize(query)
        scores = [float(np.dot(query_norm, _l2_normalize(candidate))) for candidate in candidates]
        return max(scores) if scores else 0.0


class InsightFaceBuffaloEngine(FaceEngine):
    """InsightFace Buffalo_L adapter used by the AI service.

    The rest of the system depends only on the FaceEngine contract, so Django,
    React, and API payloads remain unchanged if this adapter is replaced later.
    """

    def __init__(self) -> None:
        with _suppress_insightface_console_output():
            self.app = FaceAnalysis(name=settings.insightface_model_name, providers=settings.insightface_providers)
            self.app.prepare(ctx_id=settings.insightface_ctx_id, det_size=settings.detection_size)

    def image_to_embeddings(self, image_bytes: bytes) -> list[np.ndarray]:
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Unable to decode image bytes.")

        with _suppress_insightface_console_output():
            faces = self.app.get(image)
        return [_l2_normalize(face.normed_embedding).astype(np.float32) for face in faces]


def _l2_normalize(embedding: np.ndarray) -> np.ndarray:
    embedding = np.asarray(embedding, dtype=np.float32)
    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding
    return embedding / norm


@contextmanager
def _suppress_insightface_console_output() -> Iterator[None]:
    """Keep InsightFace provider/model logs and NumPy FutureWarnings out of CLI JSON output."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            yield
