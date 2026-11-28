import { useState } from "react";
import type { Review } from "../features/schedule/types";
import { scheduleApi } from "../features/schedule/api";

export function RoomUpdateForm({ review, week, busy, onCreated }: { review?: Review; week: string; busy: boolean; onCreated: (id: string) => Promise<void> }) {
  const [session, setSession] = useState("");
  const [room, setRoom] = useState("");
  const [source, setSource] = useState("");
  const [confirmed, setConfirmed] = useState(false);
  const [waiting, setWaiting] = useState(false);
  const [error, setError] = useState("");
  return <form className="room-update-form" onSubmit={e => { e.preventDefault(); setWaiting(true); setError("");
    void scheduleApi.createUpdate({week, session, room, source, confirmed}).then(async result => {await onCreated(result.id); setRoom(""); setSource(""); setConfirmed(false);}).catch(e => setError(e instanceof Error ? e.message : "Không lưu được cập nhật.")).finally(() => setWaiting(false));
  }}><h3>Ghi nhận cập nhật phòng mới</h3><p>Nhập thông tin nhận từ người phụ trách; hệ thống không tự xác nhận phòng vật lý.</p>
    <label>Buổi học<select value={session} required disabled={busy || waiting} onChange={e => setSession(e.target.value)}><option value="">Chọn buổi cần cập nhật</option>{review?.rows.map(row => <option value={row.id} key={row.id}>{row.date} / {row.class_name} / {row.session} / {row.room || "Chưa có phòng"}</option>)}</select></label>
    <label>Phòng cập nhật<input value={room} onChange={e => setRoom(e.target.value)} placeholder="H209 hoặc C401, E403; để trống nếu thu hồi" maxLength={100} /></label>
    <label>Nguồn xác nhận hoặc cập nhật<input value={source} onChange={e => setSource(e.target.value)} placeholder="Mã văn bản, thời điểm xác nhận và người/bộ phận cung cấp" minLength={8} maxLength={300} required /></label>
    <label className="checkbox-label"><input type="checkbox" checked={confirmed} onChange={e => setConfirmed(e.target.checked)} />Phòng mới đã được xác nhận theo nguồn trên</label>
    <button className="primary" disabled={busy || waiting || !week}>{waiting ? "Đang lưu…" : "Lưu cập nhật để đối chiếu"}</button>
    {error && <p role="alert" className="inline-error">{error}</p>}
  </form>;
}
