import os
import re
import shutil
import subprocess
import sys
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
ALLOWED_ORIGIN_REGEX = os.getenv(
    "ALLOWED_ORIGIN_REGEX",
    r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
)

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in backend environment.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

app = FastAPI(title="CO Attainment API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in ALLOWED_ORIGINS.split(",") if origin.strip()],
    allow_origin_regex=ALLOWED_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUBJECTS = [
    {"code": "CS301", "name": "Database Management Systems", "semester": "Semester V"},
    {"code": "CS302", "name": "Design and Analysis of Algorithms", "semester": "Semester V"},
    {"code": "CS401", "name": "Machine Learning", "semester": "Semester VII"},
    {"code": "CS403", "name": "Compiler Design", "semester": "Semester VII"},
    {"code": "IT305", "name": "Software Engineering", "semester": "Semester V"},
    {"code": "IT407", "name": "Cloud Computing", "semester": "Semester VII"},
]

REQUIRED_UPLOAD_KEYS = (
    "qp",
    "marks",
    "cat1",
    "cat2",
    "assignment1",
    "assignment2",
    "terminal",
)

BACKEND_DIR = Path(__file__).resolve().parent
UPLOADS_ROOT = BACKEND_DIR / "workspace_uploads"
DEFAULT_TEMPLATE_FILE = BACKEND_DIR / "data" / "CO ATTAINMENT TEMPLATE (1).xlsx"
LOCAL_STATE_FILE = BACKEND_DIR / "local_state.json"


def sanitize_identifier(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]", "_", value.strip().lower())
    return cleaned or "unknown"


def workspace_dir(subject_code: str, email: str) -> Path:
    return UPLOADS_ROOT / sanitize_identifier(subject_code) / sanitize_identifier(email)


def workspace_manifest_path(subject_code: str, email: str) -> Path:
    return workspace_dir(subject_code, email) / "manifest.json"


def read_manifest(subject_code: str, email: str) -> dict[str, str]:
    path = workspace_manifest_path(subject_code, email)
    if not path.exists():
        return {}
    try:
        import json

        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {str(k): str(v) for k, v in data.items()}
    except Exception:
        return {}
    return {}


def write_manifest(subject_code: str, email: str, manifest: dict[str, str]) -> None:
    import json

    target_dir = workspace_dir(subject_code, email)
    target_dir.mkdir(parents=True, exist_ok=True)
    workspace_manifest_path(subject_code, email).write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def files_ready(uploaded_files: dict[str, Any]) -> bool:
    return all(bool(uploaded_files.get(key)) for key in REQUIRED_UPLOAD_KEYS)


def params_ready(parameters: dict[str, Any]) -> bool:
    if not parameters:
        return False

    ep = parameters.get("ep")
    constraint = parameters.get("constraint")
    ela = parameters.get("ela") if isinstance(parameters.get("ela"), dict) else {}

    if ep in (None, "") or constraint in (None, ""):
        return False

    required_cos = [f"CO{i}" for i in range(1, 7)]
    return all(ela.get(co) not in (None, "") for co in required_cos)


def run_python_script(script_name: str, extra_env: dict[str, str]) -> str:
    script_path = BACKEND_DIR / script_name
    env = os.environ.copy()
    env.update(extra_env)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(BACKEND_DIR),
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
    if result.returncode != 0:
        raise RuntimeError(f"{script_name} failed with code {result.returncode}.\n{output.strip()}")

    return output.strip()


def run_attainment_pipeline(subject_code: str, email: str, parameters: dict[str, Any]) -> dict[str, str]:
    manifest = read_manifest(subject_code, email)
    missing = [key for key in REQUIRED_UPLOAD_KEYS if not manifest.get(key) or not Path(manifest[key]).exists()]
    if missing:
        raise RuntimeError(f"Missing uploaded files: {', '.join(missing)}")

    if not DEFAULT_TEMPLATE_FILE.exists() and not manifest.get("template"):
        raise RuntimeError("Template file is missing. Place `CO ATTAINMENT TEMPLATE (1).xlsx` in backend/data or upload as key `template`.")

    output_dir = workspace_dir(subject_code, email) / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    qp_output = output_dir / "QP_FINAL.xlsx"
    agg_output = output_dir / "CO_ATTAINMENT_FINAL.xlsx"
    final_output = output_dir / "OFFICIAL_REPORT.xlsx"

    ela = parameters.get("ela") or {}
    ela_values = [str(ela.get(f"CO{i}", "")) for i in range(1, 7)]

    script1_log = run_python_script(
        "01_qp_processing.py",
        {
            "QP_DOCX_FILE": manifest["qp"],
            "STUDENT_DB_FILE": manifest["marks"],
            "QP_OUTPUT_FILE": str(qp_output),
        },
    )
    script2_log = run_python_script(
        "02_assessment_aggregator.py",
        {
            "TEMPLATE_FILE": manifest.get("template", str(DEFAULT_TEMPLATE_FILE)),
            "CAT1_FILE": manifest["cat1"],
            "CAT2_FILE": manifest["cat2"],
            "ASS1_FILE": manifest["assignment1"],
            "ASS2_FILE": manifest["assignment2"],
            "AGG_OUT_FILE": str(agg_output),
        },
    )
    script3_log = run_python_script(
        "03_final_attainment.py",
        {
            "CO_FILE": str(agg_output),
            "TERMINAL_FILE": manifest["terminal"],
            "FINAL_OUT_FILE": str(final_output),
            "EP_VALUE": str(parameters.get("ep")),
            "CONSTRAINT_VALUE": str(parameters.get("constraint")),
            "ELA_VALUES": ",".join(ela_values),
        },
    )

    return {
        "script1Log": script1_log,
        "script2Log": script2_log,
        "script3Log": script3_log,
        "qpOutput": str(qp_output),
        "aggregateOutput": str(agg_output),
        "finalOutput": str(final_output),
    }


def upsert_generated_report(
    *,
    normalized_email: str,
    subject_code: str,
    subject_name: str,
    semester: str,
    final_output_path: str,
) -> None:
    now = datetime.now(timezone.utc)
    report_text = "\n".join(
        [
            "CO Attainment Report",
            f"Subject Code: {subject_code.upper()}",
            f"Subject Name: {subject_name}",
            f"Semester: {semester}",
            "Status: Generated",
            f"Generated On (UTC): {now.isoformat()}",
            f"Final Output: {final_output_path}",
        ]
    )

    payload = {
        "user_email": normalized_email,
        "subject_code": subject_code.upper(),
        "subject_name": subject_name,
        "semester": semester,
        "status": "Generated",
        "generated_on": now.isoformat(),
        "report_text": report_text,
        "updated_at": now.isoformat(),
    }

    try:
        supabase.table("reports").upsert(payload, on_conflict="user_email,subject_code").execute()
        return
    except Exception as exc:
        if not is_missing_table_error(exc, "reports"):
            raise

    state = read_local_state()
    state["reports"][workspace_key(normalized_email, subject_code)] = payload
    write_local_state(state)


def subject_details(subject_code: str) -> tuple[str, str]:
    code = subject_code.upper()
    for item in SUBJECTS:
        if item["code"] == code:
            return item["name"], item["semester"]
    return "Unknown Subject", "Semester"


def resolve_final_report_path(subject_code: str, email: str) -> Path:
    report_path = workspace_dir(subject_code, email) / "outputs" / "OFFICIAL_REPORT.xlsx"
    if report_path.exists():
        return report_path
    raise FileNotFoundError("Final report file is not available yet.")


class DevLoginRequest(BaseModel):
    email: str
    password: str


class WorkspaceProgressRequest(BaseModel):
    email: str
    uploadedFiles: dict[str, bool] = Field(default_factory=dict)
    parameters: dict[str, Any] = Field(default_factory=dict)
    step: int = 1


class GenerateReportRequest(BaseModel):
    email: str
    subjectName: str
    semester: str


class PasswordUpdateRequest(BaseModel):
    email: str
    currentPassword: str
    newPassword: str


def ensure_tce_email(email: str) -> str:
    normalized_email = email.strip().lower()
    if not normalized_email.endswith("@tce.edu"):
        raise HTTPException(status_code=400, detail="Please use your TCE email address.")
    return normalized_email


def is_missing_table_error(exc: Exception, table_name: str) -> bool:
    text = str(exc)
    return "PGRST205" in text and f"public.{table_name}" in text


def read_local_state() -> dict[str, Any]:
    if not LOCAL_STATE_FILE.exists():
        return {"profiles": {}, "workspace_progress": {}, "reports": {}}

    try:
        data = json.loads(LOCAL_STATE_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data.setdefault("profiles", {})
            data.setdefault("workspace_progress", {})
            data.setdefault("reports", {})
            return data
    except Exception:
        pass

    return {"profiles": {}, "workspace_progress": {}, "reports": {}}


def write_local_state(state: dict[str, Any]) -> None:
    LOCAL_STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def profile_fallback(email: str) -> dict[str, Any]:
    state = read_local_state()
    profiles = state["profiles"]

    existing = profiles.get(email)
    if existing:
        return existing

    employee_id = f"TCE-FAC-{abs(hash(email)) % 9000 + 1000}"
    profile = {
        "email": email,
        "full_name": email.split("@")[0].replace(".", " ").title(),
        "role": "Staff",
        "department": "Computer Science and Engineering",
        "employee_id": employee_id,
    }
    profiles[email] = profile
    write_local_state(state)
    return profile


def workspace_key(email: str, subject_code: str) -> str:
    return f"{email}::{subject_code.upper()}"


def upsert_profile(email: str) -> dict[str, Any]:
    employee_id = f"TCE-FAC-{abs(hash(email)) % 9000 + 1000}"
    payload = {
        "email": email,
        "full_name": email.split("@")[0].replace(".", " ").title(),
        "role": "Staff",
        "department": "Computer Science and Engineering",
        "employee_id": employee_id,
    }
    try:
        response = supabase.table("user_profiles").upsert(payload, on_conflict="email").execute()
        data = response.data or []
        if isinstance(data, list) and data:
            return data[0]

        fetch = supabase.table("user_profiles").select("*").eq("email", email).limit(1).execute()
        fetch_data = fetch.data or []
        if fetch_data:
            return fetch_data[0]
    except Exception as exc:
        if not is_missing_table_error(exc, "user_profiles"):
            raise

    # Compatibility fallback for projects that still use a legacy `users` table.
    legacy_payload = {
        "email": email,
        "name": payload["full_name"],
        "role": payload["role"].lower(),
        "password_hash": "dev-login",
    }

    try:
        legacy_response = supabase.table("users").upsert(legacy_payload, on_conflict="email").execute()
        legacy_data = legacy_response.data or []
        if isinstance(legacy_data, list) and legacy_data:
            row = legacy_data[0]
            return {
                "email": row.get("email", email),
                "full_name": row.get("name") or payload["full_name"],
                "role": (row.get("role") or "Staff").title(),
                "department": payload["department"],
                "employee_id": employee_id,
            }

        legacy_fetch = supabase.table("users").select("*").eq("email", email).limit(1).execute()
        legacy_rows = legacy_fetch.data or []
        if legacy_rows:
            row = legacy_rows[0]
            return {
                "email": row.get("email", email),
                "full_name": row.get("name") or payload["full_name"],
                "role": (row.get("role") or "Staff").title(),
                "department": payload["department"],
                "employee_id": employee_id,
            }
    except Exception:
        pass

    return profile_fallback(email)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/subjects")
def get_subjects() -> list[dict[str, str]]:
    return SUBJECTS


@app.post("/api/auth/dev-login")
def dev_login(payload: DevLoginRequest) -> dict[str, Any]:
    email = ensure_tce_email(payload.email)

    if payload.password != "tce123":
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    try:
        profile = upsert_profile(email)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Supabase profile setup failed: {exc}",
        ) from exc

    return {
        "email": profile.get("email", email),
        "name": profile.get("full_name") or "Staff User",
        "role": profile.get("role") or "Staff",
        "department": profile.get("department") or "Computer Science and Engineering",
        "employeeId": profile.get("employee_id") or "TCE-FAC-0000",
    }


@app.get("/api/profile/{email}")
def get_profile(email: str) -> dict[str, Any]:
    normalized_email = ensure_tce_email(email)

    try:
        profile = upsert_profile(normalized_email)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch profile: {exc}") from exc

    return {
        "name": profile.get("full_name") or "Staff User",
        "email": profile.get("email") or normalized_email,
        "department": profile.get("department") or "Computer Science and Engineering",
        "role": profile.get("role") or "Staff",
        "employeeId": profile.get("employee_id") or "TCE-FAC-0000",
    }


@app.get("/api/workspaces/{subject_code}")
def get_workspace_progress(subject_code: str, email: str) -> dict[str, Any]:
    normalized_email = ensure_tce_email(email)
    key = workspace_key(normalized_email, subject_code)

    try:
        response = (
            supabase.table("workspace_progress")
            .select("*")
            .eq("subject_code", subject_code.upper())
            .eq("user_email", normalized_email)
            .limit(1)
            .execute()
        )
        rows = response.data or []
    except Exception as exc:
        if is_missing_table_error(exc, "workspace_progress"):
            row = read_local_state()["workspace_progress"].get(key)
            if not row:
                return {"uploadedFiles": {}, "parameters": {}, "step": 1}
            return {
                "uploadedFiles": row.get("uploaded_files") or {},
                "parameters": row.get("parameters") or {},
                "step": row.get("step") or 1,
                "updatedAt": row.get("updated_at"),
            }
        raise HTTPException(status_code=500, detail=f"Failed to fetch workspace progress: {exc}") from exc

    if not rows:
        return {"uploadedFiles": {}, "parameters": {}, "step": 1}

    row = rows[0]
    return {
        "uploadedFiles": row.get("uploaded_files") or {},
        "parameters": row.get("parameters") or {},
        "step": row.get("step") or 1,
        "updatedAt": row.get("updated_at"),
    }


@app.put("/api/workspaces/{subject_code}")
def save_workspace_progress(subject_code: str, payload: WorkspaceProgressRequest) -> dict[str, str]:
    normalized_email = ensure_tce_email(payload.email)
    key = workspace_key(normalized_email, subject_code)

    upsert_payload = {
        "user_email": normalized_email,
        "subject_code": subject_code.upper(),
        "uploaded_files": payload.uploadedFiles,
        "parameters": payload.parameters,
        "step": payload.step,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        supabase.table("workspace_progress").upsert(
            upsert_payload,
            on_conflict="user_email,subject_code",
        ).execute()
    except Exception as exc:
        if is_missing_table_error(exc, "workspace_progress"):
            state = read_local_state()
            state["workspace_progress"][key] = upsert_payload
            write_local_state(state)
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save workspace progress. Ensure table workspace_progress exists: {exc}",
            ) from exc

    auto_generated = False
    if files_ready(payload.uploadedFiles) and params_ready(payload.parameters):
        try:
            pipeline = run_attainment_pipeline(subject_code, normalized_email, payload.parameters)
            subj_name, sem = subject_details(subject_code)
            upsert_generated_report(
                normalized_email=normalized_email,
                subject_code=subject_code,
                subject_name=subj_name,
                semester=sem,
                final_output_path=pipeline["finalOutput"],
            )
            auto_generated = True
            progress_payload = {
                "user_email": normalized_email,
                "subject_code": subject_code.upper(),
                "uploaded_files": payload.uploadedFiles,
                "parameters": payload.parameters,
                "step": 4,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }

            try:
                supabase.table("workspace_progress").upsert(
                    progress_payload,
                    on_conflict="user_email,subject_code",
                ).execute()
            except Exception as exc:
                if is_missing_table_error(exc, "workspace_progress"):
                    state = read_local_state()
                    state["workspace_progress"][key] = progress_payload
                    write_local_state(state)
                else:
                    raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Automatic pipeline failed: {exc}") from exc

    if auto_generated:
        return {"message": "Workspace progress saved. Pipeline ran automatically and generated the report."}

    return {"message": "Workspace progress saved."}


@app.post("/api/workspaces/{subject_code}/files/{file_key}")
async def upload_workspace_file(
    subject_code: str,
    file_key: str,
    email: str = Form(...),
    file: UploadFile = File(...),
) -> dict[str, Any]:
    normalized_email = ensure_tce_email(email)
    state_key = workspace_key(normalized_email, subject_code)
    key = file_key.strip().lower()

    allowed_keys = set(REQUIRED_UPLOAD_KEYS) | {"template"}
    if key not in allowed_keys:
        raise HTTPException(status_code=400, detail=f"Invalid file key '{file_key}'.")

    target_dir = workspace_dir(subject_code, normalized_email)
    target_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(file.filename or "upload.bin").suffix
    if not suffix:
        suffix = ".bin"
    destination = target_dir / f"{key}{suffix.lower()}"

    with destination.open("wb") as handle:
        shutil.copyfileobj(file.file, handle)

    manifest = read_manifest(subject_code, normalized_email)
    manifest[key] = str(destination)
    write_manifest(subject_code, normalized_email, manifest)

    row = {}
    try:
        existing = (
            supabase.table("workspace_progress")
            .select("*")
            .eq("subject_code", subject_code.upper())
            .eq("user_email", normalized_email)
            .limit(1)
            .execute()
        )
        rows = existing.data or []
        row = rows[0] if rows else {}
    except Exception as exc:
        if is_missing_table_error(exc, "workspace_progress"):
            row = read_local_state()["workspace_progress"].get(state_key, {})
        else:
            raise HTTPException(status_code=500, detail=f"Failed to read workspace progress: {exc}") from exc

    uploaded_files = row.get("uploaded_files") or {}
    uploaded_files[key] = True
    parameters = row.get("parameters") or {}
    next_step = 2 if files_ready(uploaded_files) else (row.get("step") or 1)

    progress_payload = {
        "user_email": normalized_email,
        "subject_code": subject_code.upper(),
        "uploaded_files": uploaded_files,
        "parameters": parameters,
        "step": next_step,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        supabase.table("workspace_progress").upsert(
            progress_payload,
            on_conflict="user_email,subject_code",
        ).execute()
    except Exception as exc:
        if is_missing_table_error(exc, "workspace_progress"):
            state = read_local_state()
            state["workspace_progress"][state_key] = progress_payload
            write_local_state(state)
        else:
            raise HTTPException(status_code=500, detail=f"Failed to save workspace progress: {exc}") from exc

    auto_generated = False
    message = f"Uploaded {key}."

    if files_ready(uploaded_files) and params_ready(parameters):
        try:
            pipeline = run_attainment_pipeline(subject_code, normalized_email, parameters)
            subj_name, sem = subject_details(subject_code)
            upsert_generated_report(
                normalized_email=normalized_email,
                subject_code=subject_code,
                subject_name=subj_name,
                semester=sem,
                final_output_path=pipeline["finalOutput"],
            )
            auto_generated = True
            message = "All required files and parameters are present. Pipeline ran automatically."
            next_step = 4
            final_payload = {
                "user_email": normalized_email,
                "subject_code": subject_code.upper(),
                "uploaded_files": uploaded_files,
                "parameters": parameters,
                "step": next_step,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            try:
                supabase.table("workspace_progress").upsert(
                    final_payload,
                    on_conflict="user_email,subject_code",
                ).execute()
            except Exception as exc:
                if is_missing_table_error(exc, "workspace_progress"):
                    state = read_local_state()
                    state["workspace_progress"][state_key] = final_payload
                    write_local_state(state)
                else:
                    raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Uploaded file, but automatic pipeline failed: {exc}") from exc

    return {
        "uploadedFiles": uploaded_files,
        "step": next_step,
        "autoGenerated": auto_generated,
        "message": message,
    }


@app.get("/api/reports")
def get_reports(email: str) -> list[dict[str, Any]]:
    normalized_email = ensure_tce_email(email)
    subject_map = {subject["code"]: subject for subject in SUBJECTS}

    try:
        response = (
            supabase.table("reports")
            .select("*")
            .eq("user_email", normalized_email)
            .order("updated_at", desc=True)
            .execute()
        )
        rows = response.data or []
    except Exception as exc:
        if is_missing_table_error(exc, "reports"):
            state = read_local_state()
            rows = [
                row
                for row in state["reports"].values()
                if row.get("user_email") == normalized_email
            ]
            rows.sort(key=lambda r: r.get("updated_at", ""), reverse=True)
        else:
            raise HTTPException(status_code=500, detail=f"Failed to fetch reports: {exc}") from exc

    records = []
    for row in rows:
        code = row.get("subject_code")
        subject = subject_map.get(code, {})
        records.append(
            {
                "id": row.get("id") or code,
                "subjectCode": code,
                "subjectName": row.get("subject_name") or subject.get("name") or "Unknown Subject",
                "semester": row.get("semester") or subject.get("semester") or "Semester",
                "generatedOn": row.get("generated_on"),
                "status": row.get("status") or "Pending",
                "reportText": row.get("report_text") or "",
            }
        )

    if not records:
        # Return seeded rows so the reports page is usable before first generation.
        return [
            {
                "id": subject["code"],
                "subjectCode": subject["code"],
                "subjectName": subject["name"],
                "semester": subject["semester"],
                "generatedOn": None,
                "status": "Pending",
                "reportText": "",
            }
            for subject in SUBJECTS
        ]

    return records


@app.post("/api/reports/{subject_code}/generate")
def generate_report(subject_code: str, payload: GenerateReportRequest) -> dict[str, Any]:
    normalized_email = ensure_tce_email(payload.email)
    state_key = workspace_key(normalized_email, subject_code)

    progress = {}
    try:
        progress_response = (
            supabase.table("workspace_progress")
            .select("*")
            .eq("subject_code", subject_code.upper())
            .eq("user_email", normalized_email)
            .limit(1)
            .execute()
        )
        rows = progress_response.data or []
        progress = rows[0] if rows else {}
    except Exception as exc:
        if is_missing_table_error(exc, "workspace_progress"):
            progress = read_local_state()["workspace_progress"].get(state_key, {})
        else:
            raise HTTPException(status_code=500, detail=f"Failed to read workspace progress: {exc}") from exc

    uploaded_files = progress.get("uploaded_files") or {}
    parameters = progress.get("parameters") or {}

    if not files_ready(uploaded_files):
        raise HTTPException(status_code=400, detail="Please upload all required files before generating report.")
    if not params_ready(parameters):
        raise HTTPException(status_code=400, detail="Please complete all CO parameters before generating report.")

    try:
        pipeline = run_attainment_pipeline(subject_code, normalized_email, parameters)
        subject_name = payload.subjectName or subject_details(subject_code)[0]
        semester = payload.semester or subject_details(subject_code)[1]
        upsert_generated_report(
            normalized_email=normalized_email,
            subject_code=subject_code,
            subject_name=subject_name,
            semester=semester,
            final_output_path=pipeline["finalOutput"],
        )

        progress_payload = {
            "user_email": normalized_email,
            "subject_code": subject_code.upper(),
            "uploaded_files": uploaded_files,
            "parameters": parameters,
            "step": 4,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            supabase.table("workspace_progress").upsert(
                progress_payload,
                on_conflict="user_email,subject_code",
            ).execute()
        except Exception as exc:
            if is_missing_table_error(exc, "workspace_progress"):
                state = read_local_state()
                state["workspace_progress"][state_key] = progress_payload
                write_local_state(state)
            else:
                raise

        try:
            report_row = (
                supabase.table("reports")
                .select("*")
                .eq("user_email", normalized_email)
                .eq("subject_code", subject_code.upper())
                .limit(1)
                .execute()
            )
            row = (report_row.data or [{}])[0]
        except Exception as exc:
            if is_missing_table_error(exc, "reports"):
                row = read_local_state()["reports"].get(workspace_key(normalized_email, subject_code), {})
            else:
                raise
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {exc}") from exc

    return {
        "id": row.get("id") or subject_code.upper(),
        "subjectCode": subject_code.upper(),
        "subjectName": row.get("subject_name") or payload.subjectName,
        "semester": row.get("semester") or payload.semester,
        "generatedOn": row.get("generated_on"),
        "status": row.get("status") or "Generated",
        "reportText": row.get("report_text") or "CO Attainment Report generated.",
        "finalOutputPath": pipeline["finalOutput"],
    }


@app.get("/api/reports/{subject_code}/download")
def download_report(subject_code: str, email: str) -> FileResponse:
    normalized_email = ensure_tce_email(email)

    try:
        report_path = resolve_final_report_path(subject_code, normalized_email)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return FileResponse(
        path=str(report_path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"{subject_code.upper()}_OFFICIAL_REPORT.xlsx",
    )


@app.post("/api/auth/change-password")
def change_password(payload: PasswordUpdateRequest) -> dict[str, str]:
    ensure_tce_email(payload.email)

    if len(payload.newPassword) < 8:
        raise HTTPException(status_code=400, detail="New password must be at least 8 characters.")

    # This route is intentionally a placeholder when using dev-login mode.
    return {"message": "Password validation passed. Configure Supabase Auth to enable real password updates."}
