# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`), đơn vị là 1 key coach:
  - dùng ít: 40%, 6 phiên/tháng, 1 lượt hỏi
  - dùng vừa: 40%, 12 phiên/tháng, 3 lượt hỏi
  - dùng nhiều: 20%, 20 phiên/tháng, 5 lượt hỏi

  Nguồn: tần suất ở `spec.md` §2 (ước tính của nhóm; khảo sát n = 3 chỉ xác nhận chu kỳ theo tuần/ngày). Số lượt hỏi mỗi phiên là **(tự ước tính)**.
- **Số người dùng thật** là key coach, không phải học viên: thấp 5 · cơ sở 10 · cao 20. Nguồn: mức cơ sở 10 = số Key Coach khác nhau trong `teaching-schedule.xlsx` Khoá 9 (dữ liệu giả lập BTC); thấp và cao là **(tự ước tính)** theo khối L3 và cả khoá.
- **Giá** (`further-reading/model-prices.md`, BTC tra 25/11/2026), USD / 1M token vào · ra:
  - gpt-6-luna 0.10 · 0.50 (rẻ)
  - deepseek-flash 0.30 · 1.20 (giá cao điểm)
  - deepseek-v4-pro 1.32 · 3.96 (mạnh)
- **Tỉ lệ đạt dùng để tính:** 17/30 (57%), lượt `run-2@20261128-100217` (lượt 2).
- **Đo token trên** `deepseek-flash`, **tính giá** cho cả ba model. Bộ tách token khác nhau nên token thật trên gpt-6-luna và deepseek-v4-pro có thể lệch.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · 50 phiên · seed 42 · tóm tắt ở `cost/simulate-1-summary.md` · trace `traces/simulate-1.jsonl`.

| Persona | Số phiên | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 15 | 1 | 85.123 | 611 | 1 | 2 |
| dung_vua | 17 | 3 | 255.382 | 1.822 | 3 | 6 |
| dung_nhieu | 9 | 5 | 425.661 | 3.200 | 5 | 10 |

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (5) | / tháng — cơ sở (10) | / tháng — cao (20) | / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6-luna | $0,0239 | $0,0422 | $1,62 | $3,25 | $6,50 | $0,32 (≈ 8.400 ₫) |
| deepseek-flash | $0,0712 | $0,1256 | $4,84 | $9,67 | $19,35 | $0,97 (≈ 25.200 ₫) |
| deepseek-v4-pro | $0,3109 | $0,5486 | $21,13 | $42,26 | $84,53 | $4,23 (≈ 109.900 ₫) |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ 57%, **không coi như đạt 100%**. Tỷ giá 1 USD = 26.000 ₫ là **(tự ước tính)**.

**Phiên lỗi: 9/50 (18%)**, đều do model trả JSON không hợp lệ (cùng loại lỗi với B16 ở lượt 2). 9 phiên này không được tính vào trung bình. Nếu người dùng phải hỏi lại sau mỗi lần lỗi, chi phí thật cao hơn khoảng 1/(1 − 0,18) ≈ 1,2 lần.

## 3. So với impact

- **Impact / người / tháng** (`spec.md` §2): 120 phút công lập và cập nhật lịch cho mỗi key coach (tự ước tính, chưa đo).
- **Chi phí / người / tháng** (cơ sở, deepseek-flash): **$0,97 ≈ 25.000 ₫**. Model mạnh deepseek-v4-pro là $4,23 ≈ 110.000 ₫.
- **Kết luận một dòng:** **đáng làm.** Chi phí model mỗi key coach dưới 1 USD/tháng. Chỉ cần tiết kiệm được khoảng 15 phút trong 120 phút mỗi tháng là đã hòa vốn, nếu giờ công key coach từ khoảng 100.000 ₫/giờ trở lên (tự ước tính, chưa có số thật). Rủi ro lớn hơn tiền model là chất lượng: tỉ lệ đạt mới 57% và 18% phiên lỗi JSON. Vì vậy phần đáng đầu tư tiếp là độ đúng, không phải giảm giá.

## 4. Độ nhạy (sơ bộ, chưa chạy lại)

- **Cắt ngữ cảnh:** mỗi lượt gửi khoảng 85k token vào vì có lịch cả khoá. Chỉ gửi tuần được hỏi (khoảng 13–42 nhóm buổi trên tổng 108) có thể giảm token vào khoảng 3–4 lần (ước tính theo số buổi, chưa đo).
- **Cache:** giá vào khi cache hit của deepseek-flash là 0,006 $/1M, khoảng 50 lần rẻ hơn. Phần workbook gần như không đổi giữa các lượt nên cache được.
- **Ngoài giờ cao điểm:** giá deepseek-flash chỉ bằng một nửa.
- **Chi phí ngoài model:** chưa tính hosting và giờ công key coach rà duyệt.
