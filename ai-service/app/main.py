from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.face_engine import InsightFaceBuffaloEngine
from app.recognition import register_student_face, verify_attendance_image

app = FastAPI(title="AI Attendance Face Service", version="1.0.0")
face_engine = InsightFaceBuffaloEngine()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "running"}


@app.post("/register-face")
async def register_face(
    student_id: str = Form(...), image: UploadFile = File(...), scope: str | None = Form(default=None)
) -> dict[str, str]:
    try:
        return register_student_face(face_engine, student_id, await image.read(), scope=scope)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/verify-attendance")
async def verify_attendance(image: UploadFile = File(...), scope: str | None = Form(default=None)) -> dict[str, object]:
    try:
        return verify_attendance_image(face_engine, await image.read(), scope=scope)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
