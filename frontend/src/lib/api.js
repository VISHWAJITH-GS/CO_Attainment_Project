const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const errorPayload = await response.json();
      if (errorPayload?.detail) {
        message = errorPayload.detail;
      }
    } catch {
      // Preserve default message when backend response is not JSON.
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export function devLogin(email, password) {
  return request("/api/auth/dev-login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function getSubjects() {
  return request("/api/subjects");
}

export function getWorkspaceProgress(subjectCode, email) {
  const params = new URLSearchParams({ email });
  return request(`/api/workspaces/${subjectCode}?${params.toString()}`);
}

export function saveWorkspaceProgress(subjectCode, payload) {
  return request(`/api/workspaces/${subjectCode}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export async function uploadWorkspaceFile(subjectCode, fileKey, email, file) {
  const formData = new FormData();
  formData.append("email", email);
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/api/workspaces/${subjectCode}/files/${fileKey}`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    let message = `Upload failed (${response.status})`;
    try {
      const errorPayload = await response.json();
      if (errorPayload?.detail) {
        message = errorPayload.detail;
      }
    } catch {
      // Keep default when response is not JSON.
    }
    throw new Error(message);
  }

  return response.json();
}

export function getReports(email) {
  const params = new URLSearchParams({ email });
  return request(`/api/reports?${params.toString()}`);
}

export function generateReport(subjectCode, payload) {
  return request(`/api/reports/${subjectCode}/generate`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function downloadReportFile(subjectCode, email) {
  const params = new URLSearchParams({ email });
  const response = await fetch(`${API_BASE_URL}/api/reports/${subjectCode}/download?${params.toString()}`);

  if (!response.ok) {
    let message = `Download failed (${response.status})`;
    try {
      const errorPayload = await response.json();
      if (errorPayload?.detail) {
        message = errorPayload.detail;
      }
    } catch {
      // Keep default when response is not JSON.
    }
    throw new Error(message);
  }

  return response.blob();
}

export function getProfile(email) {
  return request(`/api/profile/${encodeURIComponent(email)}`);
}

export function updatePassword(payload) {
  return request("/api/auth/change-password", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getApiBaseUrl() {
  return API_BASE_URL;
}
