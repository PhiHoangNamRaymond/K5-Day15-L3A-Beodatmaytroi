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
  get("reset").disabled = busy || !result;
  get("approve").disabled = busy || !result || result.issues.length > 0 || !!approved;
  get("export").hidden = !approved;
  get("copy").disabled = busy;
  const rows = result?.rows || [];
  get("count").textContent = rows.length ? rows.length + " buổi" : "";
  get("rows").replaceChildren(...rows.map(renderRow));

  const issues = result?.issues || [];
  get("issue-count").textContent = result ? issues.length + " lỗi chặn" : "";
  get("issues").replaceChildren(...(issues.length ? issues.map((issue) => {
    const card = element("article");
    card.className = "issue";
    card.append(element("small", issue.sessions.join(", ")), element("p", issue.message));
    return card;
  }) : [element("p", result ? "Có thể duyệt bản bàn giao." : "Đang tải bản nháp.")] ));

  get("impact").hidden = !result?.impact;
  if (result?.impact) {
    const change = result.impact;
    get("impact").replaceChildren(
      element("strong", change.class_name + " · " + change.session),
      element("p", shortDate(change.date) + " · " + change.start + "–" + change.end),
      element("p", change.old_room + " → " + (change.room || "Chờ phòng thay thế")),
      element("small", "Nguồn " + change.source)
    );
  }
  get("notice").hidden = !result?.notice;
  get("notice-text").textContent = result?.notice || "";
}

function renderRow(row) {
  const tr = element("tr");
  const label = element("td", row.topic);
  label.append(element("small", shortDate(row.date) + " · " + row.start + "–" + row.end),
    element("small", row.class_name + " · " + row.id));
  if (result.issues.some((issue) => issue.sessions.includes(row.id))) label.classList.add("has-alert");
  const details = element("details");
  details.className = "source";
  const sources = element("ul");
  sources.append(
    element("li", "Lịch mẫu / " + row.id + " · " + (row.published_room || "chưa có bản đã thông báo")),
    element("li", (row.update_source || "Bảng phòng mẫu / " + row.id) + " · " + (row.room_options.join(", ") || "chưa có phòng xác nhận")),
    element("li", "Đăng ký mẫu / " + row.id + " · " + [...row.teachers, ...row.coaches].join(", "))
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
        proposal = undefined;
        approved = undefined;
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
  return tr;
}

async function run(task) {
  // Keep the current controls in place while a select change is being handled.
  busy = true;
  document.querySelectorAll("button,select").forEach((control) => { control.disabled = true; });
  try {
    await task();
  } catch (error) {
    status.textContent = error.message;
  } finally {
    busy = false;
    render();
  }
}

async function review(message) {
  result = await api("/api/review", payload());
  status.textContent = message;
}

async function load() {
  changes = {};
  proposal = approved = result = undefined;
  update.replaceChildren(option("", "Lập lịch từ nguồn của tuần"));
  await review("Chọn Tạo đề xuất lịch hoặc sửa từng buổi.");
  update.append(...result.updates.map((item) => option(item.id, item.label)));
}

week.addEventListener("change", () => run(load));
update.addEventListener("change", () => run(async () => {
  changes = {};
  proposal = approved = result = undefined;
  await review("Đã đối chiếu với bản lịch được thông báo.");
}));
get("reset").addEventListener("click", () => run(load));
get("propose").addEventListener("click", () => run(async () => {
  const response = await api("/api/propose", payload());
  result = response;
  proposal = response.proposal;
  approved = undefined;
  status.textContent = proposal ? (response.method === "model"
    ? "Model đã chọn phương án. Kiểm tra nguồn trước khi áp dụng."
    : "Đã tạo đề xuất theo quy tắc. Kiểm tra nguồn trước khi áp dụng.")
    : "Không tìm được phương án không trùng. Kiểm tra lại đăng ký và phòng.";
}));
get("apply").addEventListener("click", () => run(async () => {
  for (const [id, fields] of Object.entries(proposal)) changes[id] = {...changes[id], ...fields};
  proposal = approved = undefined;
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
