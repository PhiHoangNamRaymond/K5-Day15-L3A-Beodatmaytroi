# Bèo dạt mây trôi — Rà soát lịch phân công giảng dạy

- **Lớp:** L3A
- **Track:** A — EdTech, hướng A5 — Vận hành đào tạo
- **Người dùng chính:** key coach rà soát và duyệt lịch giảng dạy cho ngày hôm sau (vai trò cần xác nhận với người trực tiếp phụ trách).
- **Thành viên và phân công:** [TEAMS.md](TEAMS.md).
- **Canvas:** [canvas.md](canvas.md).

## Bài toán

Tối trước ngày học, key coach phải đối chiếu thủ công lịch giảng dạy, đăng ký nhân sự và thông tin phòng để tìm và sửa sai lệch, khiến việc hoàn thiện lịch mất thời gian và có nguy cơ bỏ sót lỗi.

Đây là **giả thuyết cần kiểm chứng**. Nhóm sẽ xác nhận vai trò, quy trình và thời gian thực hiện với người phụ trách ngoài nhóm; hiện chưa có số liệu hay kết quả phỏng vấn để kết luận.

## Lát cắt dự kiến

Một key coach rà soát lịch giảng dạy cho ngày hôm sau, AI đối chiếu lịch với đăng ký nhân sự và thông tin phòng để quyết định cảnh báo và đề xuất chỉnh sửa khi có sai lệch hoặc thiếu dữ liệu, giúp key coach hoàn thiện và duyệt lịch nhanh hơn so với kiểm tra thủ công.

## Phạm vi website

Website chỉ dành cho key coach. Luồng dự kiến: chọn ngày → xem bảng phân công → yêu cầu agent rà soát → xem vấn đề và nguồn đối chiếu → sửa hoặc chấp nhận đề xuất → duyệt lịch.

Agent chỉ cảnh báo và đề xuất, không tự chốt phòng, đổi phân công hay gửi thông báo. Key coach quyết định thay đổi và duyệt lịch cuối cùng. Kiểm tra ràng buộc rõ ràng như trùng người, trùng phòng thực hiện bằng code; AI hỗ trợ diễn giải dữ liệu chữ tự do và đề xuất xử lý.

Các tình huống cần mô phỏng:

- Phòng chưa được xác nhận.
- Hai bảng ghi hai phòng khác nhau.
- Phòng thay đổi sau khi đã thông báo.
- Buổi học chuyển sang online.
- Tên người được nhập lệch danh sách chuẩn.

## Dữ liệu và bằng chứng

Nguồn chạy thử là bộ dữ liệu **giả lập** `teaching-schedule.xlsx` do BTC cung cấp, xem [mô tả dữ liệu](data/training-ops/README.md). Các sheet dự kiến sử dụng: `Khoá 9 (GĐ1)`, `Dang_ky_chi_tiet`, `Nhan_su` và `Lịch sử chỉnh sửa`. Không cần tích hợp nguồn dữ liệu trực tiếp để làm bản thử.

Dữ liệu mock dùng để dựng tình huống và kiểm thử, **không phải bằng chứng pain**. Không đưa nhãn rà soát có sẵn ở sheet `Canh_bao` vào đầu vào nếu dùng chúng làm đáp án đánh giá khả năng phát hiện vấn đề. Không đăng lại nguyên bộ dữ liệu BTC trong repo nộp bài; vị trí dữ liệu làm việc và cách xử lý sẽ ghi trong [data/DATA_CARD.md](data/DATA_CARD.md).

## Đánh giá dự kiến

Chỉ số chính là thời gian từ lúc mở bộ lịch đến khi sửa xong và duyệt, bao gồm thời gian chờ agent và kiểm tra đề xuất.

**Tỷ lệ giảm thời gian (%) = (thời gian thủ công − thời gian có agent) / thời gian thủ công × 100%.**

So sánh trên các bộ tình huống có độ khó tương đương, đồng thời kiểm tra lỗi còn sót trong lịch đã duyệt. Ngưỡng đạt cụ thể sẽ chốt ở CP2 trong `spec.md` §7 và `eval/metric_spec.yaml`. Hiện chưa có kết quả đo.

## Trạng thái tại CP1

Đã chốt hướng A5 teaching và phạm vi dự kiến. Website, agent, bằng chứng pain và kết quả đánh giá chưa được xác minh hoàn thành. Phần hướng dẫn bên dưới mô tả bộ khung starter và các mốc phát triển tiếp theo, không phải xác nhận sản phẩm đã chạy thật.

---

## Nhóm làm gì, khung làm gì

| Nhóm quyết định và viết | Khung làm sẵn (không cần sửa) |
|---|---|
| Người dùng, pain, bằng chứng, impact (`evidence/`, `spec.md` §1–§2) | — |
| Hình dạng giải pháp, công cụ, prompt, luồng (`spec.md` §4, `codebase/agent.py`, `tools.py`, `ai.py`) | Ghi mọi lần gọi model / công cụ vào trace, cộng token (`codebase/tracing.py`) |
| Bộ câu thử, metric, chuẩn "đạt" (`eval/benchmark.csv`, `eval/metric_spec.yaml`, `spec.md` §7) | Kiểm đủ cột, đủ câu `kho` / `tu_choi`, đủ ≥1/3 câu từ người dùng / data thật (`run.py check`) |
| Chấm cột `pass` theo metric spec | Chạy cả bộ một lệnh, có run ID, model, token từng câu (`run.py eval`) · tính % đạt (`run.py score`) |
| Persona, số người dùng thật, giá model (`cost/personas.yaml`) | Sinh ~50 phiên, chạy thật qua bản chạy thử, tính chi phí / phiên, / task thành công, / tháng 3 kịch bản (`run.py simulate`) |

*Áp dụng cho nhóm:* công cụ đọc lịch và đăng ký nhân sự trả về vị trí nguồn; agent chỉ ra sai lệch hoặc thông tin thiếu và đề xuất cách xử lý để key coach duyệt. Bộ khung hỗ trợ ghi trace, chạy đánh giá và mô phỏng chi phí sau khi nhóm triển khai luồng này.

## Chạy trong 3 phút

Bộ khung cần **Python 3.10 trở lên** (Python 3.9 có sẵn trên macOS vẫn chạy được, chỉ in một dòng nhắc). **Không cần `pip install`.**

**Bước 1 — Mở cửa sổ lệnh ngay trong thư mục repo**

| Windows (PowerShell) | macOS |
|---|---|
| Mở thư mục repo bằng File Explorer → bấm vào thanh địa chỉ → gõ `powershell` → Enter | Mở **Terminal** (Cmd + Space, gõ "Terminal") → gõ `cd ` (có dấu cách) → kéo thả thư mục repo vào → Enter |

Gõ `dir` (Windows) hoặc `ls` (macOS / Linux): thấy `run.py` và `README.md` là đang đứng đúng chỗ.

**Bước 2 — Kiểm Python và chạy thử**

| Việc | Windows (PowerShell) | macOS / Linux |
|---|---|---|
| Kiểm Python | `python --version` (không được thì `py --version`) | `python3 --version` |
| Chạy bản chạy thử (chế độ giả, chưa gọi model) | `python run.py` | `python3 run.py` |
| Kiểm bộ câu thử | `python run.py check` | `python3 run.py check` |
| Tạo file `.env` để nối model | `copy .env.example .env` | `cp .env.example .env` |

- Windows: gõ `python` mà mở Microsoft Store hoặc báo không có lệnh → dùng `py`. Chưa có Python: cài từ python.org, **tick "Add python.exe to PATH"**, mở lại PowerShell.
- macOS: báo `command not found: python` là bình thường → dùng `python3`.
- `python run.py` in ra "[câu trả lời giả — chưa nối model] …" là khung chạy đúng. Nối model thật: [docs/connect-model.md](docs/connect-model.md).

Trong README này lệnh viết là `python …`; máy nhóm cần `python3` hay `py` thì gõ thay.

## Lệnh

| Lệnh | Làm gì |
|---|---|
| `python run.py` | Chạy bản chạy thử (gõ đầu vào, nhận kết quả, kèm số lần gọi model / token) |
| `python run.py check` | Kiểm `eval/benchmark.csv` (6 cột, số câu, `kho` / `tu_choi`, mã `source`, ô trống, dòng mẫu) `eval/metric_spec.yaml` (≥3 metric điền đủ) và `TEAMS.md` (đúng format để BTC quét). Chỉ cảnh báo, không sửa file |
| `python run.py eval --try` | **Thử nối model:** chạy 3 câu đầu (`--try 5` = 5 câu) → `eval/run-try.csv`. Thấy "Nối model được" là xong. Không tính là một lượt |
| `python run.py eval` | Chạy cả bộ qua `codebase/agent.py` → `eval/run-1.csv` (lần sau `run-2.csv`…) + `traces/run-1.jsonl`. Mỗi dòng có run ID, model, số lần gọi model / công cụ, token. Model còn giả → chỉ ghi `run-mock.csv`; mọi câu lỗi → `run-error.csv`; Ctrl+C → `run-stopped.csv` — đều **không** được đánh số |
| `python run.py eval --fake` | Thử riêng bộ chạy, không gọi agent → `eval/run-fake.csv` |
| `python run.py score eval/run-1.csv` | Sau khi điền cột `pass` (1 / 0): in % đạt tổng và theo `type`. Còn ô trống → "CHƯA CHẤM XONG", không in % |
| `python run.py simulate --try` | Thử mô phỏng chi phí 10 phiên (làm trước CP3) → `cost/simulate-try.csv` |
| `python run.py simulate` | Mô phỏng chi phí khi dùng thật theo `cost/personas.yaml` (≥50 phiên) → `cost/simulate-N.csv` + `cost/simulate-N-summary.md` |
| `python run.py simulate --rate-from eval/run-2.csv` | Như trên, lấy tỉ lệ đạt từ đúng lượt chỉ định. Không ghi thì khung lấy lượt `run-N` mới nhất đã chấm, cùng model, và ghi rõ đã lấy lượt nào trong bản tóm tắt |

Gói miễn phí báo hết lượt: thêm `--wait 4` sau `eval` hoặc `simulate` (nghỉ 4 giây giữa hai lượt gọi). Sửa CSV bằng Excel: *File → Save As → CSV UTF-8*; Google Sheets: *Tệp → Tải xuống → CSV*.

**Lượt có lỗi kỹ thuật** (cột `error` có chữ): không sửa tay file đó, chạy lại thành lượt mới và ghi vào bảng các lượt ở `eval/README.md`. Không xoá file lượt nào.

Nhóm dùng stack khác (Node, Streamlit, notebook…): sửa hàm `run_app()` trong `run.py` để `python run.py` vẫn chạy được bản chạy thử, và giữ `answer()` trong `codebase/agent.py` để `eval`, `simulate` chạy được.

## Bản chạy thử — viết ở đâu

| File | Viết gì | Bước guide |
|---|---|---|
| `codebase/agent.py` | `answer(text)` — luồng chính, đúng hình dạng ở `spec.md` §4. Khung có sẵn một workflow 2 bước *ví dụ* | 3.2 |
| `codebase/tools.py` | Công cụ của bài toán, mỗi công cụ một hàm có `@tool` | 2.2, 3.2 |
| `codebase/ai.py` | `call_model(system, user)` — chỗ duy nhất gọi model. Chưa điền `.env` thì chạy **chế độ giả** | 3.3 |

- **Trước CP2:** để chế độ giả, công cụ trả dữ liệu giả — `python run.py` đi hết luồng là đủ.
- **Trước CP3:** nối model thật theo [docs/connect-model.md](docs/connect-model.md), `eval --try` thấy token > 0 rồi mới `eval`.
- Bộ chạy gửi **nguyên ô `input`** của câu thử vào `answer(text)`. Dữ liệu nền (bài học, thông báo, lịch…) để trong `data/`, đọc qua công cụ.

## Phần nào thật, phần nào giả

| Thành phần | Thật / Giả | Ghi chú |
|---|---|---|
| Lời gọi AI ở quyết định trung tâm | Chưa xác minh nối model thật; bắt buộc thật từ CP3 | Model chưa chốt |
| Dữ liệu lịch, phòng và nhân sự | Giả lập | teaching-schedule.xlsx do BTC cung cấp |

## Dùng AI vào việc gì

Nhóm sử dụng Codex để đọc yêu cầu hackathon, góp ý canvas và biên soạn README theo hướng A5 teaching. Nhóm chịu trách nhiệm kiểm tra nội dung, xác nhận giả thuyết pain và đối chiếu với phạm vi thực tế trước khi nộp. Chi tiết quá trình dùng AI sẽ được bổ sung tại [docs/ai-usage.md](docs/ai-usage.md); hướng dẫn coding agent ở [AGENTS.md](AGENTS.md).

## File mẫu — điền ở bước nào

| File | Điền ở bước guide | Mốc |
|---|---|---|
| `TEAMS.md` | 1.0 | CP1 · **đúng format**, BTC quét khi chấm |
| `canvas.md` | 1.4 | CP1, cập nhật CP2 |
| `evidence/hypothesis.md` | 1.1 | trước khi tìm bằng chứng |
| `evidence/data-mining.md` · `evidence/interviews/TEMPLATE.md` → `P1.md`… · `evidence/survey/TEMPLATE.md` | 1.2 | bắt đầu sau Zoom, xong CP3 |
| `evidence/summary.md` | 1.2 | CP3 |
| `spec.md` | §0–§2: 1.1–1.3 · §3–§5: 2.1–2.3 · §7: 2.4 · §8: 4.2 · §10: suốt | §7 chốt CP2 · §0–§7 CP3 · đủ CP4 |
| `data/DATA_CARD.md` | 2.4 | bản đầu CP2 |
| `eval/benchmark.csv` · `eval/metric_spec.yaml` | 2.4 | ≥10 câu + metric chốt CP2 · 20–30 câu CP3 |
| `codebase/` | 3.2, 3.3 | khung CP2 · AI thật CP3 |
| `eval/report.md` · `eval/README.md` | 4.1 (README mục 1–4 từ 2.4) | CP4 |
| `cost/personas.yaml` · `cost/cost-estimate.md` | 4.2 | thử 10 phiên CP3 · đủ CP4 |
| `validation/log.md` *(bonus)* | 4.3 | CP4 |
| `slides/outline.md` → `demo-slides.pdf` | 5.1 | CP4 |
| `reflection/TEMPLATE.md` → `reflection/<ten>.md` | 5.3 | 23:59 Thứ Bảy 28/11 |
| `AGENTS.md` · `docs/ai-usage.md` | khi dùng coding agent / AI | suốt |

## Bảy hạng mục bắt buộc — nằm ở file nào

| # | Hạng mục | File |
|---|---|---|
| 1 | Bằng chứng pain | `evidence/` (tổng hợp ở `evidence/summary.md`) |
| 2 | Impact có số | `spec.md` §2 |
| 3 | Thiết kế giải pháp | `spec.md` §4 |
| 4 | Bản chạy thử làm trọn lát cắt | `codebase/` · lệnh ở mục "Lệnh" |
| 5 | Định nghĩa "tốt" + bộ câu thử | `data/DATA_CARD.md` · `eval/` |
| 6 | Mô phỏng chi phí khi dùng thật | `cost/` |
| 7 | Slide + demo + video dự phòng | `demo-slides.pdf` ở thư mục gốc · link video: chưa có, bổ sung trước CP4 |
| + | *Bonus:* người dùng thử | `validation/log.md` |
