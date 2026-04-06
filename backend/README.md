# Backend

This folder now includes:

- FastAPI server (`app.py`) connected to Supabase
- SQL schema (`supabase_schema.sql`)
- Existing Python scripts for CO processing
- Runtime-generated artifacts under `runtime/` (workspace uploads and local state)

## Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Configure environment:
    - create `.env` from `.env.example`
    - set `SUPABASE_URL`
    - set `SUPABASE_SERVICE_KEY`
    - set `ALLOWED_ORIGINS` (usually `http://localhost:5173,http://127.0.0.1:5173`)
3. Run SQL in Supabase:
    - execute `supabase_schema.sql` in SQL editor

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
