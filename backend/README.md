# Backend

This folder now includes:

- FastAPI server (`app.py`) with local runtime persistence
- Local SQLite auth database under `runtime/users.db`
- Existing Python scripts for CO processing
- Runtime-generated artifacts under `runtime/` (workspace uploads and local state)

## Demo Accounts

- `faculty1@tce.edu` / `tce123`
- `faculty2@tce.edu` / `tce123`

Uploaded files are stored by account and subject under:

- `runtime/workspace_uploads/<email>/<subject_code>/`

## Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Configure environment:
    - create `.env` from `.env.example`
    - set `ALLOWED_ORIGINS` (usually `http://localhost:5173,http://127.0.0.1:5173`)

## Run API

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

## Main Routes

- `GET /health`
- `POST /api/auth/dev-login`
- `GET /api/subjects`
- `GET /api/profile/{email}`
- `GET /api/workspaces/{subject_code}?email=...`
- `PUT /api/workspaces/{subject_code}`
- `GET /api/reports?email=...`
- `POST /api/reports/{subject_code}/generate`
