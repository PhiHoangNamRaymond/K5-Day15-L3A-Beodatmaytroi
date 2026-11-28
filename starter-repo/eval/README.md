# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2) và 4.1 (mục 5–6, trước CP4). Ôn lại: ngày 9, ngày 14 · lab ngày 9. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

Dataset nào, xử lý gì: tóm 2–3 dòng từ `data/DATA_CARD.md`.

## 2. Bộ câu thử dựng ra sao

- `eval/benchmark.csv`: __ câu (thuong __ · kho __ · tu_choi __, trong đó __ câu tấn công)
- Nguồn (`python run.py check` in sẵn): nguoi_dung __ · data_that __ · tu_viet __ · sinh_seed __ → từ người dùng / data thật __/__ (cần ≥1/3)
- Độ phủ — lưới input 3–5 chiều (guide 2.4 bước 5): __
- Câu `kho` trỏ về 4 lớp chỗ khó (`spec.md` §5): lớp 1: __ · lớp 2: __ · lớp 3: __ · lớp 4: __

## 3. Metric và cách chấm

| Metric (`eval/metric_spec.yaml`) | Cách chấm | Ngưỡng |
|---|---|---|
| | code / llm / nguoi | |
| | | |
| | | |

- **Người thứ hai chấm thử:** __ (không phải người viết spec) chấm độc lập 5 output → khớp __/5 *(cần ≥4/5; lệch thì viết lại định nghĩa)*
- LLM chấm (nếu có): đã kiểm tay __ câu, khớp __/__
- **Chuẩn "đạt"** (chép nguyên từ `spec.md` §7, chốt trước 19:30 Thứ Sáu 27/11): "__"

## 4. Lệnh

`python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · điền cột `pass` · `python run.py score eval/run-N.csv`

## 5. Đã chạy gì

Người dùng đã xác nhận điểm lượt 1 **11/30 (37%)** ngày 28/11/2026 qua cuộc trao đổi hoàn thiện CP3. Chưa có tên người xác nhận hoặc kết quả chấm độc lập của người thứ hai; xem `report.md`.

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | run-1@20261128-092000 | gpt-6-luna | Câu hỏi tự nhiên, ngữ cảnh workbook toàn khóa, kiểm xung đột bằng code; OpenAI max_completion_tokens=4096 | 11/30 | 37% | Chưa; chấm AI sơ bộ, cần người xác nhận |
| 2 | | | | __/__ | | |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

Tóm 2–3 dòng từ `eval/report.md`: nhóm lỗi lớn nhất · đã sửa gì · còn lại gì.

Lượt 1 đã gọi model thật; B22 lỗi phản hồi thiếu trường answer. Các lỗi nổi bật: thiếu cảnh báo định biên, thiếu nhãn khẩn/checklist đồng bộ và chưa loại ngày lễ. Chưa thực hiện lượt cải tiến CP4. Bộ câu thử có 30 câu: 12 thường, 13 khó, 5 từ chối. Nhãn nguồn trong CSV là 23 data_that, 7 tu_viet; workbook thực tế là dữ liệu giả lập BTC, không phải bằng chứng pain ngoài đời.

Điểm do trợ lý đọc từng output theo pass_criterion, chưa thay thế người chấm hoặc LLM judge đã hiệu chuẩn. Chưa có người thứ hai chấm độc lập. Không thay chuẩn đã chốt sau CP2.
