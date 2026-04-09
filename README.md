# CO Attainment Project

This project is a full-stack CO Attainment application with:

- a FastAPI backend with local runtime persistence
- a React frontend (Vite)
- Python data-processing scripts in the backend folder

## Project Structure

- `backend/`: FastAPI API server and Python processing scripts.
- `frontend/`: React application for login, dashboard, subject workspace, reports, profile, and settings.

## Getting Started

To run the project end-to-end, start backend and frontend separately.

## 1) Backend Setup

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
    - Set `ALLOWED_ORIGINS`
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

- Demo login uses local SQLite auth in `backend/runtime/users.db`.
- Use `faculty1@tce.edu` or `faculty2@tce.edu` with password `tce123`.

## Notes

- Backend state is persisted in `backend/runtime/local_state.json`.
- Uploaded workspace files are stored under `backend/runtime/workspace_uploads/`.
