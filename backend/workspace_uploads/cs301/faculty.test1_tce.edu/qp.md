# CO Attainment Project

This project is a full-stack CO Attainment application with:

- a FastAPI backend connected to Supabase
- a React frontend (Vite)
- Python data-processing scripts in the backend folder

## Project Structure

- `backend/`: FastAPI API server, Supabase schema, and Python processing scripts.
- `frontend/`: React application for login, dashboard, subject workspace, reports, profile, and settings.

## Getting Started

To run the project end-to-end, start backend and frontend separately.

## 1) Supabase Setup

1. Open your Supabase SQL editor.
2. Run the SQL from `backend/supabase_schema.sql`.
3. Keep the Supabase project URL, anon key, and service role key ready.

### Backend

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configure environment file:
    - Create `backend/.env` from `backend/.env.example`
    - Set `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, and `ALLOWED_ORIGINS`
4.  Start backend API:
    ```bash
    uvicorn app:app --reload --host 127.0.0.1 --port 8000
    ```

### Frontend

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install the required npm packages:
    ```bash
    npm install
    ```
3.  Configure environment file:
    - Create `frontend/.env` from `frontend/.env.example`
    - Set `VITE_API_BASE_URL` to `http://127.0.0.1:8000`
4.  Start the development server:
    ```bash
    npm run dev
    ```

## Login

- Dev login is enabled for TCE emails.
- Use any `@tce.edu` email and password `tce123`.

## Notes

- Supabase `service_role` key is used only in backend.
- Do not expose service key in frontend code.
