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
