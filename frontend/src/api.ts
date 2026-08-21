const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8080";

function authHeaders(): Record<string, string> {
  const token = localStorage.getItem("sf_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request(path: string, options: RequestInit = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...(options.headers || {}),
    },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  signup: (data: { email: string; password: string; full_name: string; role: string }) =>
    request("/auth/signup", { method: "POST", body: JSON.stringify(data) }),
  login: (data: { email: string; password: string }) =>
    request("/auth/login", { method: "POST", body: JSON.stringify(data) }),
  me: () => request("/auth/me"),

  getProfile: () => request("/core/profile/me"),
  updateProfile: (data: object) => request("/core/profile/me", { method: "PUT", body: JSON.stringify(data) }),
  addSkill: (data: { name: string; proficiency: number }) =>
    request("/core/skills", { method: "POST", body: JSON.stringify(data) }),
  deleteSkill: (id: string) => request(`/core/skills/${id}`, { method: "DELETE" }),
  addProject: (data: object) => request("/core/projects", { method: "POST", body: JSON.stringify(data) }),
  deleteProject: (id: string) => request(`/core/projects/${id}`, { method: "DELETE" }),
  addCertification: (data: object) => request("/core/certifications", { method: "POST", body: JSON.stringify(data) }),
  listStudents: () => request("/core/students"),
  getStudent: (id: string) => request(`/core/students/${id}`),

  getQuestions: (area: string, count = 5) => request(`/analyzer/assessment/questions?area=${area}&count=${count}`),
  submitAssessment: (data: object) => request("/analyzer/assessment/submit", { method: "POST", body: JSON.stringify(data) }),
  getScores: () => request("/analyzer/assessment/scores"),
  generateRoadmap: (target_role: string) =>
    request("/analyzer/roadmap/generate", { method: "POST", body: JSON.stringify({ target_role }) }),
  getLatestRoadmap: () => request("/analyzer/roadmap/latest"),

  chat: (message: string) => request("/ai/chat", { method: "POST", body: JSON.stringify({ message }) }),
  runAgent: (message: string) => request("/ai/agent", { method: "POST", body: JSON.stringify({ message }) }),
};
