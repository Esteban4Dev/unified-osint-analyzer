const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

async function handle(res) {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Error ${res.status}: ${text}`);
  }
  return res.json();
}

export const api = {
  getSources: () => fetch(`${API_BASE}/osint/sources`).then(handle),

  search: (query, lang = "es") =>
    fetch(`${API_BASE}/osint/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, lang }),
    }).then(handle),

  getHistory: (limit = 20) =>
    fetch(`${API_BASE}/osint/history?limit=${limit}`).then(handle),

  reportUrl: (id, fmt) => `${API_BASE}/reports/${id}/${fmt}`,
};
