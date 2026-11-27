"use strict";

const get = (id) => document.getElementById(id);
const week = get("week");
const update = get("update");
const status = get("status");
let result;
let changes = {};
let proposal;
let approved;
let busy = false;
let needsReview = true;
const expandedSources = new Set();

function element(tag, text) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  return node;
}

function shortDate(value) {
  return value.split("-").reverse().join("/");
}

function option(value, title) {
  const node = element("option", title);
  node.value = value;
  return node;
}

async function api(path, data) {
  const response = await fetch(path, data === undefined ? undefined : {
    method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(data)
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error);
  return payload;
}

function payload() {
  return {week: week.value, update: update.value, changes};
}

function render() {
  week.disabled = busy;
  update.disabled = busy || !result?.updates.length;
  get("propose").disabled = busy || !result;
  get("apply").hidden = !proposal;
  get("apply").disabled = busy;
  get("dismiss").hidden = !proposal;
  get("dismiss").disabled = busy;
  get("retry").hidden = !needsReview || !result;
  get("retry").disabled = busy;
  get("reset").disabled = busy || !result;
  get("approve").disabled = busy || needsReview || !result || result.issues.length > 0 || !!approved;
  get("export").hidden = !approved;
  get("export").disabled = busy || !approved;
  get("copy").disabled = busy || needsReview;
  const rows = result?.rows || [];
  get("count").textContent = rows.length ? rows.length + " buổi" : "";
  get("rows").replaceChildren(...rows.map(renderRow));

  const issues = result?.issues || [];
  get("issue-count").textContent = result ? issues.length + " lỗi chặn" : "";
  get("issues").replaceChildren(...(issues.length ? issues.map((issue) => {
    const card = element("article");
    card.className = "issue";
    card.append(element("p", issue.message));
    for (const id of issue.sessions) {
      const row = rows.find((item) => item.id === id);
      const link = element("a", row.class_name + " · " + id + " · " + row.start + "–" + row.end);
      link.href = "#row-" + id;
      link.addEventListener("click", () => {
        const source = document.querySelector("#row-" + id + " details");
        source.open = true;
        source.querySelector("summary").focus({preventScroll: true});
      });
      card.append(link);
    }
    return card;
  }) : [element("p", needsReview ? "Đang chờ kiểm tra bản nháp." :
    approved ? "Bản bàn giao đã duyệt." : "Có thể duyệt bản bàn giao.")] ));

  get("impact").hidden = !result?.impact;
  if (result?.impact) {
    const change = result.impact;
    get("impact").replaceChildren(
      element("strong", change.old_room ? change.class_name + " · " + change.session : "Chưa xác định lớp cần báo lại"),
      element("p", shortDate(change.date) + " · " + change.start + "–" + change.end),
      element("p", change.old_room
        ? change.old_room + " → " + (change.room || "Chờ phòng thay thế")
        : "Cần bản lịch đã thông báo để đối chiếu."),
      element("small", "Nguồn " + change.source)
    );
  }
  get("notice").hidden = !result?.notice;
  get("notice-text").textContent = result?.notice || "";
}

function renderRow(row) {
  const tr = element("tr");
  tr.id = "row-" + row.id;
  const label = element("td", row.topic);
  label.append(element("small", shortDate(row.date) + " · " + row.start + "–" + row.end),
    element("small", row.class_name + " · " + row.id));
  const blockers = result.issues.filter((issue) => issue.sessions.includes(row.id)).length;
  if (blockers) label.classList.add("has-alert");
  const state = element("small", needsReview ? "Chờ rà lại" :
    blockers ? "Chờ xác minh · " + blockers + " lỗi" : "Đủ căn cứ");
  state.className = "row-state";
  label.append(state);
  const details = element("details");
  details.className = "source";
  details.open = expandedSources.has(row.id);
  details.addEventListener("toggle", () => {
    if (!details.isConnected) return;
    if (details.open) expandedSources.add(row.id);
    else expandedSources.delete(row.id);
  });
  const sources = element("ul");
  sources.append(
    element("li", "Lịch mẫu / " + row.id + " · " + (row.published_room || "chưa có bản đã thông báo")),
    element("li", (row.update_source || "Bảng phòng mẫu / " + row.id) + " · " + (row.room_options.join(", ") || "chưa có phòng xác nhận")),
    element("li", "Đăng ký giảng viên / " + row.id + " · " + (row.teachers.join(", ") || "chưa có")),
    element("li", "Đăng ký lab coach / " + row.id + " · " + (row.coaches.join(", ") || "chưa có"))
  );
  if (row.online_source) sources.append(element("li", "Online · " + row.online_source));
  details.append(element("summary", "Xem nguồn"), sources);
  label.append(details);
  tr.append(label);

  for (const [field, choices, title] of [
    ["room", row.room_options, "Phòng"], ["teacher", row.teachers, "Giảng viên"], ["coach", row.coaches, "Lab coach"]
  ]) {
    const td = element("td");
    td.dataset.label = title;
    if (field === "room" && row.format === "online") td.textContent = "Online";
    else {
      const select = element("select");
      select.setAttribute("aria-label", title + " " + row.id);
      select.disabled = busy;
      select.append(option("", "Chưa chọn"), ...choices.map((name) => option(name, name)));
      select.value = row[field];
      select.addEventListener("change", () => run(async () => {
        changes[row.id] = {...changes[row.id], [field]: select.value};
        removeSuggestion(row.id);
        await review("Đã rà lại sau khi sửa.");
      }));
      td.append(select);
    }
    const suggested = proposal?.[row.id]?.[field];
    if (suggested && suggested !== row[field]) {
      td.classList.add("proposal");
      td.append(element("small", "Đề xuất " + suggested));
    }
    tr.append(td);
  }
  if (proposal?.[row.id]) {
    const apply = element("button", "Áp dụng buổi này");
    const skip = element("button", "Bỏ qua");
    const controls = element("div");
    controls.className = "row-actions";
    for (const button of [apply, skip]) {
      button.className = "secondary";
      button.disabled = busy;
    }
    apply.addEventListener("click", () => run(async () => {
      applySuggestion(row.id);
      await review("Đã áp dụng và rà lại buổi " + row.id + ".");
    }));
    skip.addEventListener("click", () => {
      removeSuggestion(row.id);
      render();
      document.querySelector("#row-" + row.id + " summary").focus();
    });
    controls.append(apply, skip);
    label.append(controls);
  }
  return tr;
}

function removeSuggestion(id) {
  if (!proposal) return;
  delete proposal[id];
  if (!Object.keys(proposal).length) proposal = undefined;
}

function applySuggestion(id) {
  changes[id] = {...changes[id], ...proposal[id]};
  removeSuggestion(id);
}

async function run(task) {
  const activeLabel = document.activeElement?.getAttribute("aria-label");
  const activeId = document.activeElement?.id;
  busy = true;
  document.querySelectorAll("button,select").forEach((control) => { control.disabled = true; });
  try {
    await task();
  } catch (error) {
    status.textContent = error.message;
  } finally {
    busy = false;
    render();
    const next = activeId ? get(activeId) :
      [...get("rows").querySelectorAll("select")].find((node) => node.getAttribute("aria-label") === activeLabel);
    if (next && !next.hidden && !next.disabled) next.focus({preventScroll: true});
  }
}

async function review(message) {
  needsReview = true;
  approved = undefined;
  result = await api("/api/review", payload());
  needsReview = false;
  status.textContent = message;
}

async function load() {
  changes = {};
  expandedSources.clear();
  proposal = approved = result = undefined;
  update.replaceChildren(option("", "Lập lịch từ nguồn của tuần"));
  await review("Chọn Tạo đề xuất lịch hoặc sửa từng buổi.");
  update.append(...result.updates.map((item) => option(item.id, item.label)));
}

week.addEventListener("change", () => run(load));
update.addEventListener("change", () => run(async () => {
  const affected = [result?.impact?.session, result?.updates.find((item) => item.id === update.value)?.session];
  for (const id of affected) {
    if (id && changes[id]) delete changes[id].room;
  }
  proposal = undefined;
  await review("Đã đối chiếu với bản lịch được thông báo.");
}));
get("reset").addEventListener("click", () => run(load));
get("retry").addEventListener("click", () => run(() => review("Đã rà lại bản nháp.")));
get("dismiss").addEventListener("click", () => {
  proposal = undefined;
  status.textContent = "Đã bỏ các đề xuất chưa áp dụng.";
  render();
  get("propose").focus();
});
get("propose").addEventListener("click", () => run(async () => {
  const response = await api("/api/propose", payload());
  result = response;
  proposal = response.proposal && Object.fromEntries(Object.entries(response.proposal).filter(([id, fields]) =>
    Object.entries(fields).some(([field, value]) => response.rows.find((item) => item.id === id)[field] !== value)));
  if (proposal && !Object.keys(proposal).length) proposal = undefined;
  needsReview = false;
  approved = undefined;
  status.textContent = proposal ? (response.method === "model"
    ? "Model đã chọn phương án. Kiểm tra nguồn trước khi áp dụng."
    : "Đã tạo đề xuất theo quy tắc. Kiểm tra nguồn trước khi áp dụng.")
    : response.proposal ? "Đề xuất trùng với bản nháp hiện tại."
    : "Không tìm được phương án không trùng. Kiểm tra lại đăng ký và phòng.";
}));
get("apply").addEventListener("click", () => run(async () => {
  for (const id of Object.keys(proposal)) applySuggestion(id);
  await review("Đã áp dụng đề xuất và rà lại bản nháp.");
}));
get("approve").addEventListener("click", () => run(async () => {
  approved = await api("/api/approve", payload());
  proposal = undefined;
  status.textContent = "Đã duyệt bản bàn giao trong phiên này.";
}));
get("copy").addEventListener("click", () => run(async () => {
  await navigator.clipboard.writeText(result.notice);
  status.textContent = "Đã sao chép nháp thông báo.";
}));
get("export").addEventListener("click", () => {
  const lines = approved.rows.map((row) =>
    [shortDate(row.date), row.start + "–" + row.end, row.class_name, row.topic,
      row.room || row.online_source, row.teacher, row.coach].join(" · "));
  const text = ["Bản bàn giao BTC · Tuần " + shortDate(approved.week), ...lines, "", approved.notice || ""];
  const url = URL.createObjectURL(new Blob([text.join("\r\n")], {type: "text/plain;charset=utf-8"}));
  const link = element("a");
  link.href = url;
  link.download = "lich-tuan-" + approved.week + ".txt";
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});

run(async () => {
  const meta = await api("/api/weeks");
  get("mode").textContent = meta.mode === "fake" ? "Dữ liệu giả lập · offline" : "Dữ liệu giả lập · có model";
  week.append(...meta.weeks.map((value) => option(value, shortDate(value))));
  await load();
});
