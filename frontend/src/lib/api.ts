import { env } from "@/lib/env";

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const token = typeof window !== "undefined" ? localStorage.getItem("ace_token") : null;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${env.apiUrl}/api/v1${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: "API Error" }));
    throw new Error(errorData.detail || `Request failed with status ${response.status}`);
  }

  return response.json();
}

