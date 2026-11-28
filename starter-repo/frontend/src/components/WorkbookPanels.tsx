import { useState } from "react";
import { scheduleApi } from "../features/schedule/api";
import type { AIStatus, DatasetMetadata, Draft, AssistantReply, SourceData } from "../features/schedule/types";
import { Icon } from "./Icon";

export function AIAssistant({ draft, ai, busy }: { draft: Draft; ai?: AIStatus; busy: boolean }) {
  const [question, setQuestion] = useState("");
  const [reply, setReply] = useState<AssistantReply>();
  const [waiting, setWaiting] = useState(false);
  const [error, setError] = useState("");
  async function ask() {
    setWaiting(true); setError(""); setReply(undefined);
    try { setReply(await scheduleApi.assistant(draft, question)); }
    catch (e) { setError(e instanceof Error ? e.message : "Không gọi được AI."); }
    finally { setWaiting(false); }
  }
  return <section className="panel ai-panel" aria-labelledby="ai-heading">
    <div className="panel-title"><div><h2 id="ai-heading"><Icon name="spark" /> Trợ lý DeepSeek</h2><p>Hỏi về lịch đang chọn, căn cứ và các điểm cần xử lý.</p></div><span>{ai?.ready ? "Đã cấu hình" : "Chưa có API key"}</span></div>
    <form className="assistant-form" onSubmit={event => { event.preventDefault(); void ask(); }}>
      <label htmlFor="ai-question">Câu hỏi về tuần này</label>
      <textarea id="ai-question" value={question} maxLength={1500} onChange={e => setQuestion(e.target.value)} placeholder="Những buổi nào có nguy cơ trùng phòng và cần xác minh nguồn nào?" rows={3} />
      <button className="primary" disabled={!ai?.ready || busy || waiting || question.trim().length < 3}>{waiting ? "DeepSeek đang phân tích…" : "Hỏi DeepSeek"}</button>
      {!ai?.ready && <p role="note">Cần cấu hình API key DeepSeek ở máy chủ để sử dụng AI. Rà soát bằng quy tắc vẫn hoạt động.</p>}
      {error && <p className="inline-error" role="alert">{error}</p>}
      {reply && <div className="assistant-reply" role="status"><p>{reply.answer}</p><details><summary>Nguồn đối chiếu ({reply.references.length})</summary><ul>{reply.references.map(ref => <li key={ref}>{ref}</li>)}</ul></details><small>{reply.usage.model} / {reply.usage.tokens_in} token vào / {reply.usage.tokens_out} token ra</small></div>}
    </form>
  </section>;
}

export function DataPanel({ metadata, ai, data, onReload, busy }: { metadata?: DatasetMetadata; ai?: AIStatus; data?: SourceData; onReload: () => void; busy: boolean }) {
  return <section className="panel" aria-labelledby="data-heading"><div className="panel-title"><div><h2 id="data-heading">Nguồn dữ liệu và kết nối AI</h2><p>Đọc trực tiếp hai workbook, giữ vị trí nguồn cho từng bản ghi.</p></div><button className="secondary" onClick={onReload} disabled={busy}>Đọc lại Excel</button></div>
    <div className="data-content"><div className="dataset-summary"><strong>{metadata?.course || "Đang đọc workbook"}</strong><p>{metadata?.sessions ?? 0} bản ghi buổi/phòng · {metadata?.registrations ?? 0} đăng ký nhân sự · {metadata?.coach_assignments ?? 0} phân công coach</p><p>{metadata?.date_start} đến {metadata?.date_end}</p></div>
      {metadata?.files.map(file => <details className="source-file" key={file.name}><summary>{file.name}</summary><p>Sheet: {file.sheets.join(", ")}</p><small>SHA-256: {file.sha256}</small></details>)}
      <h3>DeepSeek</h3><p>{ai?.model} — {ai?.message}</p><p>AI chỉ đề xuất và giải thích. Dữ liệu Excel được coi là dữ liệu, không phải chỉ dẫn; hệ thống kiểm tra lại các lựa chọn bằng code.</p>
      <h3>Yêu cầu đổi ca từ workbook ({data?.requests.length ?? 0})</h3><p>Yêu cầu được giữ nguyên trạng thái nguồn để người phụ trách xác minh; không tự đổi ca hoặc suy ra người đó rảnh.</p>
      <div className="request-list">{data?.requests.map(item => <article key={item.id}><strong>{item.name}</strong><p>{item.from} → {item.to}</p><p>{item.reason} / {item.status || "Chưa ghi nhận xử lý"}</p>{item.note && <p>{item.note}</p>}<small>{item.source}</small></article>)}</div>
      <details><summary>Tải phân công coach ({data?.workload.length ?? 0} người)</summary><ul>{data?.workload.map(person => <li key={person.name}>{person.name}: {person.total || "0"} ca (key: {person.key || "0"}, lab: {person.lab || "0"})</li>)}</ul></details>
      <ul>{metadata?.notes.map(note => <li key={note}>{note}</li>)}</ul>
    </div>
  </section>;
}
