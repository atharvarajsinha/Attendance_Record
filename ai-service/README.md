# AI Service

Independent FastAPI service for face detection, embedding generation, embedding storage, and attendance prediction.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

## APIs

- `GET /health` returns service status.
- `POST /register-face` accepts `student_id` and `image`; saves `student_<id>.npy`.
- `POST /verify-attendance` accepts `image`; compares detected faces against stored embeddings and returns present/absent records.

The model adapter is isolated in `app/face_engine.py` so FaceNet can later be replaced by another implementation without changing Django or React.


## Run without backend/frontend

Use `verify_student.py` when you want to test the AI service locally without starting Django or React. Run it from the `ai-service/` directory after installing this service's requirements.

Register a single student image and create `../media/embeddings/student_101.npy`:

```bash
python verify_student.py --register --student-id 101 --image ../media/students/student101.jpg
```

Verify a classroom image against existing local embeddings:

```bash
python verify_student.py --image ../media/attendance/2026-06-29/classroom.jpg
```

The script prints the same JSON shape as `POST /verify-attendance`, including `detected_faces`, `matches`, and each student's `Present`/`Absent` status.
