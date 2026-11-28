import type { Draft, Handoff, Review, AIStatus, DatasetMetadata, SourceData, AssistantReply } from "./types";

async function request<T>(path: string, data?: object): Promise<T> {
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
  data: () => request<SourceData>("/api/data"),
  savedDraft: (week: string) => request<{draft: Draft | null}>("/api/draft?week=" + encodeURIComponent(week)),
  reset: (week: string) => request<Draft>("/api/reset", {week}),
  reload: () => request<{metadata: DatasetMetadata}>("/api/reload", {}),
  createUpdate: (body: {week: string; session: string; room: string; source: string; confirmed: boolean}) => request<{id: string}>("/api/updates", body),
  assistant: (draft: Draft, question: string) => request<AssistantReply>("/api/assistant", {...draft, question}),
  publish: (week: string, approved_at: string) => request<{published_at: string}>("/api/publish", {week, approved_at}),
  weeks: () => request<{ weeks: string[]; mode: string; ai: AIStatus; dataset: DatasetMetadata }>("/api/weeks"),
  review: (draft: Draft) => request<Review>("/api/review", draft),
  propose: (draft: Draft) => request<Review>("/api/propose", draft),
  approve: (draft: Draft) => request<Handoff>("/api/approve", draft),
};
