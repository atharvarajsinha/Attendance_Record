# Django Backend

Django REST Framework API for student registration, attendance verification, persistence, validation, and business workflow orchestration.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations attendance
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## APIs

- `POST /api/student/register/` multipart fields: `student_id`, `full_name`, optional `email`, `image`.
- `POST /api/attendance/verify/` multipart field: `image`.

The backend saves uploads locally, calls the AI service with `requests`, stores results, and returns JSON to React. React must not call the AI service directly.
