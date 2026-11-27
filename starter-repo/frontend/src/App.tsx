import { useEffect, useState } from "react";
import { ScheduleSidebar } from "./components/ScheduleSidebar";
import { ScheduleTable } from "./components/ScheduleTable";
import { scheduleApi } from "./features/schedule/api";
import { shortDate } from "./features/schedule/types";
import type { AssignmentField, Changes, Draft, Handoff, Review } from "./features/schedule/types";

function withoutSuggestion(proposal: Changes, id: string) {
  const next = { ...proposal };
  delete next[id];
  return next;
}

function download(handoff: Handoff) {
  const rows = handoff.rows.map((row) =>
    [shortDate(row.date), row.start + "–" + row.end, row.class_name, row.topic,
      row.room || row.online_source, row.teacher, row.coach].join(" · "));
  const text = ["Bản bàn giao BTC · Tuần " + shortDate(handoff.week), ...rows, "", handoff.notice || ""];
  const url = URL.createObjectURL(new Blob([text.join("\r\n")], { type: "text/plain;charset=utf-8" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = "lich-tuan-" + handoff.week + ".txt";
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export default function App() {
  const [weeks, setWeeks] = useState<string[]>([]);
  const [mode, setMode] = useState("");
  const [draft, setDraft] = useState<Draft>({ week: "", update: "", changes: {} });
  const [review, setReview] = useState<Review>();
  const [proposal, setProposal] = useState<Changes>({});
  const [approved, setApproved] = useState<Handoff>();
  const [busy, setBusy] = useState(true);
  const [pending, setPending] = useState(true);
  const [status, setStatus] = useState("Đang tải lịch mẫu…");

  async function run(task: () => Promise<void>) {
    setBusy(true);
    try {
      await task();
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Đã xảy ra lỗi.");
    } finally {
      setBusy(false);
    }
  }

  async function refresh(next: Draft, message: string) {
    setDraft(next);
    setApproved(undefined);
    setPending(true);
    setReview(await scheduleApi.review(next));
    setPending(false);
    setStatus(message);
  }

  async function load(week: string) {
    setReview(undefined);
    setProposal({});
    await refresh({ week, update: "", changes: {} }, "Chọn Tạo đề xuất lịch hoặc sửa từng buổi.");
  }

  useEffect(() => {
    void run(async () => {
      const metadata = await scheduleApi.weeks();
      setMode(metadata.mode);
      setWeeks(metadata.weeks);
      if (metadata.weeks.length) await load(metadata.weeks[0]);
      else setStatus("Chưa có tuần để lập lịch.");
    });
  }, []);

  function apply(ids: string[]) {
    const changes = { ...draft.changes };
    let remaining = { ...proposal };
    for (const id of ids) {
      changes[id] = { ...changes[id], ...proposal[id] };
      remaining = withoutSuggestion(remaining, id);
    }
    setProposal(remaining);
    void run(() => refresh({ ...draft, changes }, "Đã áp dụng đề xuất và rà lại bản nháp."));
  }

  function selectUpdate(update: string) {
    const changes = { ...draft.changes };
    const affected = [review?.impact?.session, review?.updates.find((item) => item.id === update)?.session];
    for (const id of affected) {
      if (id && changes[id]) {
        changes[id] = { ...changes[id] };
        delete changes[id].room;
      }
    }
    setProposal({});
    void run(() => refresh({ ...draft, update, changes }, "Đã đối chiếu với bản lịch được thông báo."));
  }

  async function propose() {
    const result = await scheduleApi.propose(draft);
    const changes: Changes = {};
    for (const row of result.rows) {
      const suggestion = result.proposal?.[row.id];
      if (suggestion && (["room", "teacher", "coach"] as const)
        .some((field) => suggestion[field] !== undefined && suggestion[field] !== row[field])) {
        changes[row.id] = suggestion;
      }
    }
    setReview(result);
    setPending(false);
    setProposal(changes);
    setApproved(undefined);
    if (!result.proposal) setStatus("Không tìm được phương án không trùng. Kiểm tra lại đăng ký và phòng.");
    else if (!Object.keys(changes).length) setStatus("Đề xuất trùng với bản nháp hiện tại.");
    else setStatus(result.method === "model" ? "Model đã chọn phương án. Kiểm tra nguồn trước khi áp dụng." :
      "Đã tạo đề xuất theo quy tắc. Kiểm tra nguồn trước khi áp dụng.");
  }

  function edit(id: string, field: AssignmentField, value: string) {
    const changes = { ...draft.changes, [id]: { ...draft.changes[id], [field]: value } };
    setProposal(withoutSuggestion(proposal, id));
    void run(() => refresh({ ...draft, changes }, "Đã rà lại sau khi sửa."));
  }

  const proposalIds = Object.keys(proposal);
  const canApprove = !busy && !pending && review && review.issues.length === 0 && !approved;

  return <>
    <header><div className="shell brand"><span className="mark" aria-hidden="true">B</span>
      <strong>Bèo dạt mây trôi</strong><span id="mode" className="environment">
        {!mode ? "Dữ liệu giả lập" : mode === "fake" ? "Dữ liệu giả lập · offline" : "Dữ liệu giả lập · có model"}
      </span></div></header>
    <main className="shell">
      <section className="intro">
        <div><p className="eyebrow">VẬN HÀNH ĐÀO TẠO</p><h1>Lịch giảng dạy tuần</h1>
          <p>Lập bản nháp phân công và đối chiếu thay đổi phòng trước khi bàn giao BTC.</p></div>
        <label>Tuần bắt đầu
          <select id="week" value={draft.week} disabled={busy || !weeks.length}
            onChange={(event) => void run(() => load(event.target.value))}>
            {weeks.map((week) => <option key={week} value={week}>{shortDate(week)}</option>)}
          </select>
        </label>
      </section>
      <div className="actions">
        <button id="propose" disabled={busy || pending || !review} onClick={() => void run(propose)}>Tạo đề xuất lịch</button>
        <button id="apply" className="secondary" hidden={!proposalIds.length} disabled={busy}
          onClick={() => apply(proposalIds)}>Áp dụng đề xuất</button>
        <button id="dismiss" className="secondary" hidden={!proposalIds.length} disabled={busy}
          onClick={() => { setProposal({}); setStatus("Đã bỏ các đề xuất chưa áp dụng."); }}>Bỏ đề xuất còn lại</button>
        <button id="retry" className="secondary" hidden={!pending || !draft.week} disabled={busy}
          onClick={() => void run(() => refresh(draft, "Đã rà lại bản nháp."))}>Rà lại bản nháp</button>
        <button id="reset" className="secondary" disabled={busy || !draft.week} onClick={() => void run(() => load(draft.week))}>Khôi phục</button>
        <button id="approve" className="secondary" disabled={!canApprove} onClick={() => void run(async () => {
          setApproved(await scheduleApi.approve(draft));
          setProposal({});
          setStatus("Đã duyệt bản bàn giao trong phiên này.");
        })}>Duyệt bản bàn giao</button>
        <button id="export" className="secondary" hidden={!approved} disabled={busy || !approved}
          onClick={() => approved && download(approved)}>Tải bản bàn giao</button>
      </div>
      <p id="status" role="status">{status}</p>
      <div className="workspace" aria-busy={busy}>
        <ScheduleTable review={review} proposal={proposal} changes={draft.changes} busy={busy} pending={pending}
          onEdit={edit} onApply={(id) => apply([id])} onSkip={(id) => setProposal(withoutSuggestion(proposal, id))} />
        <ScheduleSidebar review={review} update={draft.update} busy={busy} pending={pending} approved={!!approved}
          onUpdate={selectUpdate} onCopy={() => void run(async () => {
            if (!review?.notice) return;
            await navigator.clipboard.writeText(review.notice);
            setStatus("Đã sao chép nháp thông báo.");
          })} />
      </div>
    </main>
  </>;
}
