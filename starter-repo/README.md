# Bèo dạt mây trôi — Hỗ trợ lập và cập nhật lịch giảng dạy theo tuần

- **Lớp:** L3A
- **Track:** A — EdTech, hướng A5 — Vận hành đào tạo
- **Người dùng chính:** key coach phụ trách chuẩn bị, rà soát và duyệt bản lịch tuần trước khi chuyển BTC thông báo; vai trò và quyền duyệt thực tế cần xác nhận với người phụ trách.
- **Thành viên và phân công:** [TEAMS.md](TEAMS.md).
- **Canvas:** [canvas.md](canvas.md).

## Bài toán

Khi chuẩn bị lịch giảng dạy cho tuần sau, key coach phải tổng hợp đăng ký nhân sự và tình trạng phòng đang chờ nhà trường duyệt, sau đó cập nhật lịch nếu phòng bị thu hồi hoặc thay đổi sau khi đã thông báo. Việc đối chiếu thủ công giữa các nguồn làm mất thời gian và có nguy cơ bỏ sót lớp bị ảnh hưởng hoặc thông báo sai địa điểm.

Spec CP2 ghi 3 người ngoài nhóm xác nhận thiếu công cụ quản lý chung. Hồ sơ phỏng vấn và trích dẫn trong `evidence/` vẫn chưa được điền, nên kết quả này đang chờ đối chiếu với ghi chép gốc của nhóm.

## Lát cắt dự kiến

Một key coach chuẩn bị lịch giảng dạy cho tuần sau, AI đề xuất bản nháp lịch từ đăng ký nhân sự và thông tin phòng được cung cấp, đồng thời chỉ ra dữ liệu thiếu hoặc mâu thuẫn và đề xuất chỉnh sửa khi phòng thay đổi, giúp key coach hoàn thiện và duyệt lịch nhanh hơn so với làm thủ công.

## Phạm vi website

Website dành cho key coach, hỗ trợ lập và cập nhật lịch giảng dạy cho một tuần được chọn.

Luồng dự kiến: chọn tuần → xem đăng ký nhân sự và tình trạng phòng → yêu cầu tạo bản nháp lịch → xem cảnh báo và nguồn đối chiếu → key coach sửa hoặc chấp nhận đề xuất → duyệt bản lịch để BTC thông báo.

Khi có cập nhật phòng sau lần thông báo trước: người dùng cung cấp thông tin xác nhận mới → hệ thống đối chiếu với bản lịch đã thông báo → chỉ ra buổi học, lớp và địa điểm bị ảnh hưởng → đề xuất cập nhật lịch và tạo bản nháp thông báo thay đổi → key coach kiểm tra và duyệt.

- AI đề xuất bản nháp lịch trên các buổi học, đăng ký nhân sự và thông tin phòng đã có; phần chưa đủ căn cứ phải được đánh dấu để xác nhận.
- Code kiểm tra ràng buộc rõ ràng như trùng người, trùng phòng và thời gian; AI hỗ trợ diễn giải nội dung chữ tự do, giải thích vấn đề và đề xuất xử lý.
- Key coach sửa và duyệt trên website; thay đổi không tự ghi vào bảng lịch chính thức hoặc tự gửi thông báo.
- Bản thử chưa tự tìm phòng trống, đặt phòng, xin nhà trường duyệt hoặc tối ưu lịch toàn khóa.

Các tình huống cần mô phỏng:

| Tình huống | Hành vi mong muốn |
|---|---|
| Phòng chưa được xác nhận | Đánh dấu chờ xác nhận; không trình bày phòng dự kiến như địa điểm đã chốt |
| Hai nguồn ghi hai phòng khác nhau | Hiển thị nguồn mâu thuẫn và yêu cầu xác minh trước khi duyệt phần bị ảnh hưởng |
| Phòng bị thu hồi, chưa có phòng mới | Chỉ ra buổi/lớp bị ảnh hưởng; báo chưa có địa điểm thay thế được xác nhận |
| Phòng đổi sau khi đã thông báo | So sánh phòng cũ và mới, nêu rõ tòa nhà nếu nguồn có; tạo nháp thông báo cập nhật |
| Buổi học chuyển sang online | Cảnh báo thông tin phòng trực tiếp còn sót và kiểm tra thông tin học online được cung cấp |
| Tên người gõ lệch danh sách chuẩn | Đề xuất tên có thể khớp; trường hợp mơ hồ cần người dùng xác nhận |
| Nhân sự hoặc phòng bị trùng giờ | Code phát hiện xung đột; mọi chỉnh sửa phải được kiểm tra lại trước khi duyệt |

## Dữ liệu và bằng chứng

Nguồn chạy thử là bộ dữ liệu **giả lập** `teaching-schedule.xlsx` do BTC cung cấp, xem [mô tả dữ liệu](data/training-ops/README.md). Các sheet dự kiến sử dụng: `Khoá 9 (GĐ1)`, `Dang_ky_chi_tiet`, `Nhan_su` và `Lịch sử chỉnh sửa`. Chỉ đề xuất nhân sự và phòng khi dữ liệu cung cấp đủ căn cứ; việc đăng ký một buổi không có nghĩa người đó rảnh ở mọi buổi khác.

Bản thử không tích hợp dữ liệu trực tiếp từ nhà trường. Cập nhật phòng được người dùng cung cấp hoặc mô phỏng có nhãn; hệ thống không tự phát hiện việc phòng vật lý bị thu hồi. Lịch sử sửa bảng không chứng minh một thông báo đã được gửi: bản lịch đã thông báo và trạng thái thông báo phải được ghi nhận riêng trong tình huống mock.

Dữ liệu mock dùng để dựng tình huống và kiểm thử, **không phải bằng chứng pain**. Không đưa nhãn rà soát có sẵn ở sheet `Canh_bao` vào đầu vào nếu dùng chúng làm đáp án đánh giá khả năng phát hiện vấn đề. Không đăng lại nguyên bộ dữ liệu BTC trong repo nộp bài; phiên bản, phần trích dùng và cách xử lý cần được ghi tại [data/DATA_CARD.md](data/DATA_CARD.md).

## Đánh giá dự kiến

Chỉ số chính là thời gian từ lúc mở bộ dữ liệu của tuần đến khi hoàn thiện và duyệt bản lịch, bao gồm thời gian chờ AI, kiểm tra căn cứ và sửa đề xuất. Với tình huống đổi phòng sau thông báo, đo thêm thời gian từ khi nhận cập nhật đến khi duyệt xong bản lịch và nháp thông báo thay đổi.

**Tỷ lệ giảm thời gian (%) = (thời gian thủ công − thời gian có AI) / thời gian thủ công × 100%.**

So sánh trên các bộ tình huống có độ khó tương đương và đổi thứ tự thử để giảm ảnh hưởng do nhớ đáp án. Chỉ tính hoàn thành khi lịch đáp ứng điều kiện đúng đã định nghĩa; đồng thời đo lỗi còn sót, cảnh báo sai, lớp bị bỏ sót và việc dùng phòng chưa xác nhận như phòng đã chốt. Không gộp hai tác vụ lập lịch tuần và cập nhật phòng thành một số thời gian nếu chưa định nghĩa cách tổng hợp.

Ngưỡng đạt cần thống nhất trong `spec.md` §7 và `eval/metric_spec.yaml` trước khi khóa CP2; README này không tự thay đổi các ngưỡng đã chốt. Hiện chưa có kết quả đo.

## Trạng thái tại CP1

Bản CP1 tập trung rà soát lịch giảng dạy cho ngày hôm sau. Định hướng đang cập nhật cho CP2 là đề xuất bản nháp lịch tuần và hỗ trợ cập nhật khi phòng thay đổi; cần đồng bộ canvas, kiến trúc, công cụ, benchmark và metric trước khi nộp.

Website, agent, bằng chứng pain và kết quả đánh giá chưa được xác minh hoàn thành. Các mục chức năng phía trên là thiết kế dự kiến; hướng dẫn bên dưới mô tả bộ khung starter và cách phát triển tiếp.

---

## Nhóm làm gì, khung làm gì

| Nhóm quyết định và viết | Khung làm sẵn (không cần sửa) |
|---|---|
| Người dùng, pain, bằng chứng, impact (`evidence/`, `spec.md` §1–§2) | — |
| Hình dạng giải pháp, công cụ, prompt, luồng (`spec.md` §4, `codebase/agent.py`, `tools.py`, `ai.py`) | Ghi mọi lần gọi model / công cụ vào trace, cộng token (`codebase/tracing.py`) |
| Bộ câu thử, metric, chuẩn "đạt" (`eval/benchmark.csv`, `eval/metric_spec.yaml`, `spec.md` §7) | Kiểm đủ cột, đủ câu `kho` / `tu_choi`, đủ ≥1/3 câu từ người dùng / data thật (`run.py check`) |
| Chấm cột `pass` theo metric spec | Chạy cả bộ một lệnh, có run ID, model, token từng câu (`run.py eval`) · tính % đạt (`run.py score`) |
| Persona, số người dùng thật, giá model (`cost/personas.yaml`) | Sinh ~50 phiên, chạy thật qua bản chạy thử, tính chi phí / phiên, / task thành công, / tháng 3 kịch bản (`run.py simulate`) |

*Áp dụng cho nhóm:* công cụ đọc lịch tuần, đăng ký nhân sự, trạng thái phòng và lịch sử thay đổi phải trả về nguồn đối chiếu. Code kiểm tra ràng buộc; AI đề xuất bản nháp lịch và cách xử lý các vấn đề để key coach duyệt. Bộ khung hỗ trợ ghi trace, đánh giá và mô phỏng chi phí sau khi luồng được triển khai.

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

Nhóm sử dụng Codex để đọc yêu cầu hackathon, góp ý canvas và biên soạn README theo hướng A5 teaching, gồm cập nhật phạm vi lịch tuần và xử lý thay đổi phòng. Nhóm chịu trách nhiệm kiểm tra nội dung, xác nhận giả thuyết pain và đối chiếu với phạm vi thực tế trước khi nộp. Chi tiết quá trình dùng AI sẽ được bổ sung tại [docs/ai-usage.md](docs/ai-usage.md); hướng dẫn coding agent ở [AGENTS.md](AGENTS.md).

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

## Chạy website lịch tuần

Web dùng React, TypeScript và Vite. Dùng Node.js 22.12 trở lên và Python 3.10 trở lên. Chạy từ thư mục `starter-repo`, sau đó mở http://127.0.0.1:8765.

```powershell
npm --prefix frontend ci --include=dev
npm --prefix frontend run build
python codebase/web_app.py
```

Khi sửa giao diện, giữ server Python chạy trên cổng 8765, rồi chạy `npm --prefix frontend run dev` ở terminal khác và mở địa chỉ Vite in ra. Vite chuyển tiếp `/api` về Python. Mã UI ở `frontend/src`, kiểu dữ liệu và API lịch tuần ở `frontend/src/features/schedule`.

Nếu đang ở `starter-repo/frontend` và gặp lỗi `'vite' is not recognized`, chạy `npm ci --include=dev` rồi chạy lại `npm run dev`. Vite đã có trong `devDependencies`. Cờ `--include=dev` cài cả Vite khi npm đang được cấu hình chỉ cài dependency production.

Chọn tuần 26/04/2027 để thử đầy đủ hai luồng hoặc tuần 03/05/2027 để thử lịch ít buổi.

1. Trong **Lịch tuần**, chọn **Tạo đề xuất lịch** để xem phòng, giảng viên và lab coach được gợi ý theo nguồn. Mở **Xem nguồn**, áp dụng đề xuất hoặc chọn từng giá trị. Mỗi lần sửa đều được kiểm lại.
2. Trong **Cập nhật phòng**, chọn ca đổi H209 sang C403. Xem lớp bị ảnh hưởng, nguồn đối chiếu và nháp thông báo cho BTC. Nếu đủ căn cứ, mở **Rà soát & bàn giao** để duyệt và tải bản bàn giao.
3. Chọn ca thu hồi C402 để kiểm trạng thái chờ phòng mới. Có thể sao chép nháp thông báo tình trạng. Hồ sơ còn phòng chưa xác nhận sẽ bị chặn duyệt.
4. Chọn cập nhật GD-04 thiếu lịch đã thông báo để kiểm trạng thái chưa xác định lớp cần báo lại. Khi muốn thử trùng ca, chọn GV An ở cả GD-01 và GD-02 rồi mở hai liên kết trong cảnh báo để đối chiếu nguồn.

Có thể áp dụng hoặc bỏ qua đề xuất theo từng buổi. Web giữ các chỉnh sửa nhân sự khi chuyển kịch bản đổi phòng và kiểm lại bản nháp trước khi cho duyệt.

Website đọc hai tuần giả lập trong `data/weekly-demo.json`. Bản bàn giao được tải thành tệp văn bản. Phiên local dùng dữ liệu mẫu và chưa ghi lịch lên hệ thống của nhóm. Nếu cấu hình `.env` với `MODEL_PROVIDER=openai`, model có thể chọn giữa các phương án hợp lệ. Ngoại tuyến, code chọn phương án theo quy tắc và giao diện ghi rõ chế độ. Bộ benchmark CP2 hiện mô tả nhiều ca điều phối trong dữ liệu BTC. Website này mới được kiểm với hai tuần giả lập bên trên.

## Bàn giao và điểm cần đối chiếu

- [WORKLOAD.md](../WORKLOAD.md) ghi phần FE đã hoàn thành, cách demo và các hợp đồng cần giữ khi tích hợp.
- [Bố cục ba tab trên Figma](https://www.figma.com/design/qoG5PzrsWyG59PHbFZ8zCm?node-id=15-2) là bản giao diện hiện tại.
- [Wireframe Figma](https://www.figma.com/design/qoG5PzrsWyG59PHbFZ8zCm?node-id=1-318) mô tả luồng lập lịch tuần và nhánh xử lý khi phòng đổi hoặc bị thu hồi.
- [Trạng thái bổ sung CP2](https://www.figma.com/design/qoG5PzrsWyG59PHbFZ8zCm?node-id=7-3) minh họa đề xuất theo từng buổi, lỗi trùng ca và ca thiếu bản lịch đã thông báo.
- Spec CP2 và `eval/metric_spec.yaml` đang lệch ngưỡng ở `hoi_lai_khi_thieu`, `ban_nhap_thong_bao_va_checklist_dong_bo` và `dung_y_yeu_cau`. Spec trên `main` ghi 80%, file metric ghi 90%. Đối chiếu bản nhóm đã nộp CP2 trước khi chấm hoặc báo điểm.
- Nhánh demo đã có workflow chạy trên fixture hai tuần. Chưa có kết quả lượt chính thức cho bộ 30 câu CP2 và chưa kiểm model qua API thật.
