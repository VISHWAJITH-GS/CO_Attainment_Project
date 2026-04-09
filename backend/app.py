import os
import re
import shutil
import subprocess
import sys
import json
import base64
import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field

load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
ALLOWED_ORIGIN_REGEX = os.getenv(
    "ALLOWED_ORIGIN_REGEX",
    r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
)

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
REPORT_FILE_KEY = "official_report"

BACKEND_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = BACKEND_DIR / "runtime"
UPLOADS_ROOT = RUNTIME_DIR / "workspace_uploads"
DEFAULT_TEMPLATE_FILE = BACKEND_DIR / "data" / "CO ATTAINMENT TEMPLATE (1).xlsx"
LOCAL_STATE_FILE = RUNTIME_DIR / "local_state.json"
USER_DB_FILE = RUNTIME_DIR / "users.db"

RUNTIME_DIR.mkdir(parents=True, exist_ok=True)


def password_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def init_user_db() -> None:
    USER_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(USER_DB_FILE)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL,
                department TEXT NOT NULL,
                employee_id TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        now = datetime.now(timezone.utc).isoformat()
        seed_rows = [
            (
                "faculty.test1@tce.edu",
                password_hash("tce123"),
                "Faculty Test User",
                "Staff",
                "Computer Science and Engineering",
                "TCE-CSE-TEST1",
                1,
                now,
                now,
            ),
            # Computer Science and Engineering (CSE)
            (
                "shalinie@tce.edu",
                password_hash("tce123"),
                "Dr. S. Mercy Shalinie",
                "Staff",
                "Computer Science and Engineering",
                "TCE-CSE-1001",
                1,
                now,
                now,
            ),
            (
                "mviji@tce.edu",
                password_hash("tce123"),
                "Dr. M. Vijayalakshmi",
                "Staff",
                "Computer Science and Engineering",
                "TCE-CSE-1002",
                1,
                now,
                now,
            ),
            (
                "mkkdit@tce.edu",
                password_hash("tce123"),
                "Dr. M. K. Kavitha Devi",
                "Staff",
                "Computer Science and Engineering",
                "TCE-CSE-1003",
                1,
                now,
                now,
            ),
            # Mathematics
            (
                "bvkmat@tce.edu",
                password_hash("tce123"),
                "Dr. B. Vellaikannan",
                "Staff",
                "Mathematics",
                "TCE-MATH-1001",
                1,
                now,
                now,
            ),
            (
                "kumarstays@tce.edu",
                password_hash("tce123"),
                "Dr. C. S. Senthilkumar",
                "Staff",
                "Mathematics",
                "TCE-MATH-1002",
                1,
                now,
                now,
            ),
            (
                "suriyaprabha@tce.edu",
                password_hash("tce123"),
                "Dr. S. P. Suriya Prabha",
                "Staff",
                "Mathematics",
                "TCE-MATH-1003",
                1,
                now,
                now,
            ),
            # Physics
            (
                "manickam-mahendran@tce.edu",
                password_hash("tce123"),
                "Dr. M. Mahendran",
                "Staff",
                "Physics",
                "TCE-PHY-1001",
                1,
                now,
                now,
            ),
            (
                "nssphy@tce.edu",
                password_hash("tce123"),
                "Dr. N. Sankara Subramanian",
                "Staff",
                "Physics",
                "TCE-PHY-1002",
                1,
                now,
                now,
            ),
            (
                "alsphy@tce.edu",
                password_hash("tce123"),
                "Dr. AL. Subramaniyan",
                "Staff",
                "Physics",
                "TCE-PHY-1003",
                1,
                now,
                now,
            ),
            # Chemistry
            (
                "hodchem@tce.edu",
                password_hash("tce123"),
                "Dr. M. Kottaisamy",
                "Staff",
                "Chemistry",
                "TCE-CHEM-1001",
                1,
                now,
                now,
            ),
            (
                "velkannan@tce.edu",
                password_hash("tce123"),
                "Dr. V. Velkannan",
                "Staff",
                "Chemistry",
                "TCE-CHEM-1002",
                1,
                now,
                now,
            ),
            (
                "drssilango@tce.edu",
                password_hash("tce123"),
                "Dr. S. Sivailango",
                "Staff",
                "Chemistry",
                "TCE-CHEM-1003",
                1,
                now,
                now,
            ),
            # English
            (
                "tamilselvi@tce.edu",
                password_hash("tce123"),
                "Dr. A. Tamilselvi",
                "Staff",
                "English",
                "TCE-ENG-1001",
                1,
                now,
                now,
            ),
            (
                "sreng@tce.edu",
                password_hash("tce123"),
                "Dr. S. Rajaram",
                "Staff",
                "English",
                "TCE-ENG-1002",
                1,
                now,
                now,
            ),
            (
                "jeyajeevakani@tce.edu",
                password_hash("tce123"),
                "Dr. G. Jeya Jeevakani",
                "Staff",
                "English",
                "TCE-ENG-1003",
                1,
                now,
                now,
            ),
        ]
        conn.executemany(
            """
            INSERT OR IGNORE INTO users (
                email,
                password_hash,
                full_name,
                role,
                department,
                employee_id,
                is_active,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            seed_rows,
        )
        conn.commit()
    finally:
        conn.close()


def fetch_auth_user(email: str) -> dict[str, Any] | None:
    conn = sqlite3.connect(USER_DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute(
            """
            SELECT email, password_hash, full_name, role, department, employee_id, is_active
            FROM users
            WHERE email = ?
            LIMIT 1
            """,
            (email,),
        ).fetchone()
    finally:
        conn.close()

    return dict(row) if row else None


def update_auth_password(email: str, new_password: str) -> None:
    conn = sqlite3.connect(USER_DB_FILE)
    try:
        conn.execute(
            """
            UPDATE users
            SET password_hash = ?, updated_at = ?
            WHERE email = ?
            """,
            (password_hash(new_password), datetime.now(timezone.utc).isoformat(), email),
        )
        conn.commit()
    finally:
        conn.close()


init_user_db()


def _state_defaults() -> dict[str, Any]:
    return {
        "profiles": {},
        "users": {},
        "workspace_progress": {},
        "reports": {},
        "workspace_files": {},
    }


def _read_state_raw() -> dict[str, Any]:
    if not LOCAL_STATE_FILE.exists():
        return _state_defaults()

    try:
        data = json.loads(LOCAL_STATE_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return _state_defaults()
        defaults = _state_defaults()
        for key, default_value in defaults.items():
            data.setdefault(key, default_value)
        return data
    except Exception:
        return _state_defaults()


def _write_state_raw(state: dict[str, Any]) -> None:
    LOCAL_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


class LocalResult:
    def __init__(self, data: list[dict[str, Any]]):
        self.data = data


class LocalTableQuery:
    def __init__(self, client: "LocalClient", table_name: str):
        self.client = client
        self.table_name = table_name
        self.mode = "select"
        self.payload: dict[str, Any] | None = None
        self.on_conflict: str | None = None
        self.filters: list[tuple[str, Any]] = []
        self._limit: int | None = None
        self.order_field: str | None = None
        self.order_desc = False

    def upsert(self, payload: dict[str, Any], on_conflict: str | None = None) -> "LocalTableQuery":
        self.mode = "upsert"
        self.payload = payload
        self.on_conflict = on_conflict
        return self

    def select(self, _columns: str = "*") -> "LocalTableQuery":
        self.mode = "select"
        return self

    def eq(self, field: str, value: Any) -> "LocalTableQuery":
        self.filters.append((field, value))
        return self

    def limit(self, count: int) -> "LocalTableQuery":
        self._limit = count
        return self

    def order(self, field: str, desc: bool = False) -> "LocalTableQuery":
        self.order_field = field
        self.order_desc = desc
        return self

    def execute(self) -> LocalResult:
        if self.mode == "upsert":
            return self.client._execute_upsert(self.table_name, self.payload or {}, self.on_conflict)
        return self.client._execute_select(
            self.table_name,
            filters=self.filters,
            limit=self._limit,
            order_field=self.order_field,
            order_desc=self.order_desc,
        )


class LocalClient:
    table_key_map = {
        "user_profiles": "profiles",
        "users": "users",
        "workspace_progress": "workspace_progress",
        "reports": "reports",
        "workspace_files": "workspace_files",
    }

    def table(self, table_name: str) -> LocalTableQuery:
        if table_name not in self.table_key_map:
            raise ValueError(f"Unsupported table: {table_name}")
        return LocalTableQuery(self, table_name)

    def _table_bucket(self, state: dict[str, Any], table_name: str) -> dict[str, dict[str, Any]]:
        key = self.table_key_map[table_name]
        bucket = state.get(key)
        if not isinstance(bucket, dict):
            bucket = {}
            state[key] = bucket
        return bucket

    def _build_row_key(self, table_name: str, payload: dict[str, Any], on_conflict: str | None) -> str:
        if on_conflict:
            cols = [part.strip() for part in on_conflict.split(",") if part.strip()]
        elif table_name in ("user_profiles", "users"):
            cols = ["email"]
        else:
            cols = ["id"]

        values = [str(payload.get(col, "")) for col in cols]
        key = "::".join(values).strip(":")
        if key:
            return key
        return str(payload.get("id", "")) or str(datetime.now(timezone.utc).timestamp())

    def _next_id(self, bucket: dict[str, dict[str, Any]]) -> int:
        ids = [int(row.get("id")) for row in bucket.values() if str(row.get("id", "")).isdigit()]
        return (max(ids) + 1) if ids else 1

    def _execute_upsert(self, table_name: str, payload: dict[str, Any], on_conflict: str | None) -> LocalResult:
        state = _read_state_raw()
        bucket = self._table_bucket(state, table_name)
        row_key = self._build_row_key(table_name, payload, on_conflict)
        existing = bucket.get(row_key, {})
        merged = {**existing, **payload}
        merged.setdefault("id", self._next_id(bucket))
        bucket[row_key] = merged
        _write_state_raw(state)
        return LocalResult([merged])

    def _execute_select(
        self,
        table_name: str,
        *,
        filters: list[tuple[str, Any]],
        limit: int | None,
        order_field: str | None,
        order_desc: bool,
    ) -> LocalResult:
        state = _read_state_raw()
        bucket = self._table_bucket(state, table_name)
        rows = list(bucket.values())

        for field, value in filters:
            rows = [row for row in rows if row.get(field) == value]

        if order_field:
            rows.sort(key=lambda row: row.get(order_field) or "", reverse=order_desc)

        if limit is not None:
            rows = rows[:limit]

        return LocalResult(rows)


Client = LocalClient


def create_client() -> Client:
    return LocalClient()


state_store: Client = create_client()


def sanitize_identifier(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]", "_", value.strip().lower())
    return cleaned or "unknown"


def workspace_dir(subject_code: str, email: str) -> Path:
    return UPLOADS_ROOT / sanitize_identifier(email) / sanitize_identifier(subject_code)


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

    if not all(manifest.get(key) and Path(manifest[key]).exists() for key in REQUIRED_UPLOAD_KEYS):
        manifest = materialize_files_from_database(subject_code, email) or manifest

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
        state_store.table("reports").upsert(payload, on_conflict="user_email,subject_code").execute()
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

    row = fetch_file_record(email, subject_code, REPORT_FILE_KEY)
    if row and row.get("file_base64"):
        try:
            report_bytes = base64.b64decode(row["file_base64"])
        except Exception as exc:
            raise FileNotFoundError("Stored report exists but is corrupted.") from exc

        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_bytes(report_bytes)
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
    return False


def read_local_state() -> dict[str, Any]:
    return _read_state_raw()


def write_local_state(state: dict[str, Any]) -> None:
    _write_state_raw(state)


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


def file_record_payload(
    *,
    normalized_email: str,
    subject_code: str,
    file_key: str,
    file_name: str,
    content_type: str,
    file_bytes: bytes,
) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "user_email": normalized_email,
        "subject_code": subject_code.upper(),
        "file_key": file_key,
        "file_name": file_name,
        "content_type": content_type,
        "file_size": len(file_bytes),
        "file_base64": base64.b64encode(file_bytes).decode("ascii"),
        "updated_at": now,
    }


def upsert_file_record(payload: dict[str, Any]) -> bool:
    try:
        state_store.table("workspace_files").upsert(
            payload,
            on_conflict="user_email,subject_code,file_key",
        ).execute()
        return True
    except Exception as exc:
        if is_missing_table_error(exc, "workspace_files"):
            return False
        raise


def fetch_file_records(normalized_email: str, subject_code: str) -> list[dict[str, Any]]:
    try:
        response = (
            state_store.table("workspace_files")
            .select("*")
            .eq("user_email", normalized_email)
            .eq("subject_code", subject_code.upper())
            .execute()
        )
        return response.data or []
    except Exception as exc:
        if is_missing_table_error(exc, "workspace_files"):
            return []
        raise


def fetch_file_record(normalized_email: str, subject_code: str, file_key: str) -> dict[str, Any] | None:
    try:
        response = (
            state_store.table("workspace_files")
            .select("*")
            .eq("user_email", normalized_email)
            .eq("subject_code", subject_code.upper())
            .eq("file_key", file_key)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return rows[0] if rows else None
    except Exception as exc:
        if is_missing_table_error(exc, "workspace_files"):
            return None
        raise


def materialize_files_from_database(subject_code: str, normalized_email: str) -> dict[str, str]:
    records = fetch_file_records(normalized_email, subject_code)
    if not records:
        return {}

    target_dir = workspace_dir(subject_code, normalized_email)
    target_dir.mkdir(parents=True, exist_ok=True)

    manifest = read_manifest(subject_code, normalized_email)
    updated = False

    for row in records:
        key = str(row.get("file_key") or "").strip()
        if not key:
            continue
        b64 = row.get("file_base64")
        if not b64:
            continue

        try:
            file_bytes = base64.b64decode(b64)
        except Exception:
            continue

        original_name = str(row.get("file_name") or f"{key}.bin")
        suffix = Path(original_name).suffix or ".bin"
        destination = target_dir / f"{key}{suffix.lower()}"

        # Skip rewriting if manifest already points to an existing file.
        existing = manifest.get(key)
        if existing and Path(existing).exists():
            continue

        destination.write_bytes(file_bytes)
        manifest[key] = str(destination)
        updated = True

    if updated:
        write_manifest(subject_code, normalized_email, manifest)

    return manifest


def persist_generated_report_file(normalized_email: str, subject_code: str, final_output_path: str) -> None:
    path = Path(final_output_path)
    if not path.exists():
        return

    payload = file_record_payload(
        normalized_email=normalized_email,
        subject_code=subject_code,
        file_key=REPORT_FILE_KEY,
        file_name=path.name,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        file_bytes=path.read_bytes(),
    )
    upsert_file_record(payload)


def upsert_profile(email: str) -> dict[str, Any]:
    row = fetch_auth_user(email)
    if not row or not row.get("is_active"):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    return {
        "email": row["email"],
        "full_name": row["full_name"],
        "role": row["role"],
        "department": row["department"],
        "employee_id": row["employee_id"],
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/subjects")
def get_subjects() -> list[dict[str, str]]:
    return SUBJECTS


@app.post("/api/auth/dev-login")
def dev_login(payload: DevLoginRequest) -> dict[str, Any]:
    email = ensure_tce_email(payload.email)

    user = fetch_auth_user(email)
    if not user or not user.get("is_active"):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    if user.get("password_hash") != password_hash(payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    try:
        profile = upsert_profile(email)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Profile setup failed: {exc}",
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
    except HTTPException:
        raise
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
            state_store.table("workspace_progress")
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
        state_store.table("workspace_progress").upsert(
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
            persist_generated_report_file(normalized_email, subject_code, pipeline["finalOutput"])
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
                state_store.table("workspace_progress").upsert(
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

    payload = file_record_payload(
        normalized_email=normalized_email,
        subject_code=subject_code,
        file_key=key,
        file_name=file.filename or destination.name,
        content_type=file.content_type or "application/octet-stream",
        file_bytes=destination.read_bytes(),
    )
    upsert_file_record(payload)

    row = {}
    try:
        existing = (
            state_store.table("workspace_progress")
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
        state_store.table("workspace_progress").upsert(
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
            persist_generated_report_file(normalized_email, subject_code, pipeline["finalOutput"])
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
                state_store.table("workspace_progress").upsert(
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
            state_store.table("reports")
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
            state_store.table("workspace_progress")
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
        persist_generated_report_file(normalized_email, subject_code, pipeline["finalOutput"])
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
            state_store.table("workspace_progress").upsert(
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
                state_store.table("reports")
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
    email = ensure_tce_email(payload.email)

    if len(payload.newPassword) < 8:
        raise HTTPException(status_code=400, detail="New password must be at least 8 characters.")

    user = fetch_auth_user(email)
    if not user or not user.get("is_active"):
        raise HTTPException(status_code=401, detail="Invalid account.")

    if user.get("password_hash") != password_hash(payload.currentPassword):
        raise HTTPException(status_code=401, detail="Current password is incorrect.")

    update_auth_password(email, payload.newPassword)

    return {"message": "Password updated successfully."}

