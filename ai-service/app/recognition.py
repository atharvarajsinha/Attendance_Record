from pathlib import Path
import re

import numpy as np
from app.config import settings
from app.face_engine import FaceEngine


def register_student_face(
    face_engine: FaceEngine, student_id: str, image_bytes: bytes, scope: str | None = None
) -> dict[str, str]:
    embeddings = face_engine.image_to_embeddings(image_bytes)
    if len(embeddings) != 1:
        raise ValueError("Registration image must contain exactly one detectable face.")

    path = _embedding_dir(scope) / f"student_{student_id}.npy"
    np.save(path, embeddings[0])
    return {"status": "success", "student_id": student_id, "scope": _normalize_scope(scope), "embedding_path": str(path)}


def load_known_embeddings(scope: str | None = None) -> dict[str, np.ndarray]:
    return {
        path.stem.removeprefix("student_"): np.load(path)
        for path in _embedding_dir(scope).glob("student_*.npy")
    }


def verify_attendance_image(face_engine: FaceEngine, image_bytes: bytes, scope: str | None = None) -> dict[str, object]:
    known_embeddings = load_known_embeddings(scope)
    if not known_embeddings:
        raise ValueError("No registered student embeddings were found.")

    detected_embeddings = face_engine.image_to_embeddings(image_bytes)
    present_ids: set[str] = set()
    matches: list[dict[str, object]] = []

    for face_index, embedding in enumerate(detected_embeddings):
        best_student_id = None
        best_score = 0.0
        for student_id, known_embedding in known_embeddings.items():
            score = face_engine.best_similarity(embedding, [known_embedding])
            if score > best_score:
                best_score = score
                best_student_id = student_id
        if best_student_id and best_score >= settings.similarity_threshold:
            present_ids.add(best_student_id)
            matches.append({"face_index": face_index, "student_id": best_student_id, "similarity": best_score})

    students = [
        {"student_id": student_id, "status": "Present" if student_id in present_ids else "Absent"}
        for student_id in sorted(known_embeddings)
    ]
    return {
        "status": "success",
        "scope": _normalize_scope(scope),
        "detected_faces": len(detected_embeddings),
        "matches": matches,
        "students": students,
    }


def _embedding_dir(scope: str | None = None) -> Path:
    normalized_scope = _normalize_scope(scope)
    directory = settings.embeddings_dir / normalized_scope if normalized_scope else Path(settings.embeddings_dir)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _normalize_scope(scope: str | None = None) -> str | None:
    if scope is None or not scope.strip():
        return None
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", scope.strip()).strip("._-") or None
