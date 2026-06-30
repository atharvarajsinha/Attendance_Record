from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.model_loader import get_face_engine, load_face_engine
from app.recognition import register_student_face, verify_attendance_image


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Load the face model once before serving register/verify requests."""
    load_face_engine()
    yield


app = FastAPI(title="AI Attendance Face Service", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "running"}


@app.post("/register-face")
async def register_face(
    student_id: str = Form(...), image: UploadFile = File(...), scope: str | None = Form(default=None)
) -> dict[str, str]:
    try:
        return register_student_face(get_face_engine(), student_id, await image.read(), scope=scope)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/verify-attendance")
async def verify_attendance(image: UploadFile = File(...), scope: str | None = Form(default=None)) -> dict[str, object]:
    try:
        return verify_attendance_image(get_face_engine(), await image.read(), scope=scope)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
