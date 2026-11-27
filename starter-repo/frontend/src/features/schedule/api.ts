import type { Draft, Handoff, Review } from "./types";

async function request<T>(path: string, data?: Draft): Promise<T> {
  const response = await fetch(path, data && {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(typeof body?.error === "string" ? body.error : "Không kết nối được với máy chủ.");
  }
  return response.json() as Promise<T>;
}

export const scheduleApi = {
  weeks: () => request<{ weeks: string[]; mode: string }>("/api/weeks"),
  review: (draft: Draft) => request<Review>("/api/review", draft),
  propose: (draft: Draft) => request<Review>("/api/propose", draft),
  approve: (draft: Draft) => request<Handoff>("/api/approve", draft),
};
