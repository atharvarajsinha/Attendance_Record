# React Frontend

Vite + React + TypeScript UI for student face registration and attendance verification.

## Run

```bash
npm install
cp .env.example .env
npm run dev -- --host 0.0.0.0
```

The frontend calls only the Django backend configured by `VITE_BACKEND_URL` and never calls the AI service directly.
