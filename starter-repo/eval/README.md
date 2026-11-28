# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2) và 4.1 (mục 5–6, trước CP4). Ôn lại: ngày 9, ngày 14 · lab ngày 9. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

Hai workbook giả lập do BTC cung cấp: `teaching-schedule.xlsx` (Khoá 9, 129 bản ghi buổi/phòng, 4 tuần 15/04–08/05/2027) và `lab-coach-schedule.xlsx` (282 dòng coach, 62 người trong Workload, 22 yêu cầu đổi ca). `xlsx_reader.py` và `excel_data.py` chuẩn hóa ngày, giờ, phòng và tên, giữ nguồn sheet/ô cho từng giá trị, không gửi cột email sang model. Chi tiết ở `data/DATA_CARD.md`.

## 2. Bộ câu thử dựng ra sao

- `eval/benchmark.csv`: **30 câu** (thường 12 · khó 13 · từ chối 5, trong đó 5 câu tấn công: ép gửi tin, ép ghi bảng, "bỏ qua quy tắc", hai câu đòi dữ liệu cá nhân).
- Nguồn (`python run.py check`): nguoi_dung 0 · data_that 23 · tu_viet 7 · sinh_seed 0 → từ data thật **23/30** (đạt ≥1/3).
- Độ phủ theo 4 chiều: loại thay đổi (tách phòng, rút coach, đổi phòng, dời buổi, online) × trạng thái phòng (đã chốt, pending, lệch giữa hai file) × độ gấp (thường, T-1) × độ rõ của yêu cầu (đủ, mơ hồ, sai mã, ngoài khoảng ngày).
- Câu `kho` theo 4 lớp chỗ khó (`spec.md` §5): lớp 1 nguồn (B05, B07, B13); lớp 2 mơ hồ (B21, B22, B25); lớp 3 thẩm quyền (B26–B30, loại từ chối); lớp 4 vận hành (B04, B06, B12, B18, B19, B23, B24).

## 3. Metric và cách chấm

| Metric (`eval/metric_spec.yaml`) | Cách chấm | Ngưỡng |
|---|---|---|
| khong_trung_lich_nhan_su | code | 100% câu thường và khó có đề xuất |
| dam_bao_nhan_su_van_hanh_lop | code | 100% câu tách phòng thiếu nhân sự hoặc vắng Key Coach |
| khong_tu_quyet | code | 100% câu từ chối và thường |
| phan_loai_khan_t1 | code | 100% câu thay đổi sát giờ (≤24h) |
| hoi_lai_khi_thieu | người | ≥90% câu khó |
| ban_nhap_thong_bao_va_checklist_dong_bo | người | ≥90% câu thường |
| nguon_chuan_va_khong_bia_thong_tin | llm | 100% câu thường và khó |
| dung_y_yeu_cau | llm | ≥90% câu thường |

- **Người thứ hai chấm thử:** chưa làm (0/5). Lưu ý `spec.md` §7 ghi ngưỡng ≥80% cho ba metric cuối, còn `metric_spec.yaml` ghi ≥90%; nhóm không sửa ngưỡng sau CP2, chỉ ghi lại chỗ lệch.
- **LLM chấm:** chưa hiệu chuẩn. Cột `pass` của cả hai lượt do trợ lý AI đọc output và đối chiếu `pass_criterion` (quy tắc ở `grade_run1.py`, `grade_run2.py`), sau đó nhóm xác nhận.
- **Chuẩn "đạt"** (`spec.md` §7): từng metric đạt ngưỡng trên đúng tập câu áp dụng; báo thêm tỉ lệ câu đạt trên tổng 30 câu.

## 4. Lệnh

`python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · điền cột `pass` · `python run.py score eval/run-N.csv`

## 5. Đã chạy gì

Người dùng đã xác nhận điểm lượt 1 **11/30 (37%)** ngày 28/11/2026 qua cuộc trao đổi hoàn thiện CP3. Chưa có tên người xác nhận hoặc kết quả chấm độc lập của người thứ hai; xem `report.md`.

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | run-1@20261128-092000 | gpt-6-luna | Câu hỏi tự nhiên, ngữ cảnh workbook toàn khóa, kiểm xung đột bằng code; OpenAI max_completion_tokens=4096 | 11/30 | 37% | Chưa; chấm AI sơ bộ, cần người xác nhận |
| 2 | run-2@20261128-100217 | deepseek-flash | + công cụ `check_staffing` (định biên coach/phòng, Key Coach, tải) và 6 quy tắc staffing trong payload | 17/30 | 57% | Chưa; chấm AI sơ bộ, khác model lượt 1 |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

- **Nhóm lỗi lớn nhất ở lượt 1:** thiếu kiểm định biên coach theo phòng (7/19 câu trượt). Đã sửa bằng code `check_staffing`; nhóm này từ 0/7 lên 3/7, tổng từ 11/30 lên 17/30.
- **Còn lại:** thiếu nhãn KHẨN/T-1, chưa loại ngày lễ, chưa đọc cờ trùng ca `L!`, chia coach theo phòng còn sai, mỗi lượt có 1 lỗi JSON. B11 tụt sau khi sửa.
- **Hạn chế:** hai lượt khác model; điểm do AI chấm sơ bộ, chưa có người thứ hai chấm. Chi tiết ở `eval/report.md`.
