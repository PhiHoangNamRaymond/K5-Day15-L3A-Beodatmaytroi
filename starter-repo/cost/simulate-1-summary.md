# Tóm tắt mô phỏng simulate-1@20261128-101507

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 15 | 1 | 85123 | 611 | 1.0 | 2.0 |
| dung_vua | 17 | 3 | 255382 | 1822 | 3.0 | 6.0 |
| dung_nhieu | 9 | 5 | 425661 | 3200 | 5.0 | 10.0 |

Tỉ lệ đạt dùng để tính: 17/30 (57%) — lượt run-2@20261128-100217

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (5 người) | Chi phí / tháng — cơ sở (10 người) | Chi phí / tháng — cao (20 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-luna (vào 0.1 · ra 0.5 $/1M) | $0.0239 (≈ 621 ₫) | $0.0422 (≈ 1.096 ₫) | $0.0156 (≈ 405 ₫) | $1.62 (≈ 42.222 ₫) | $3.25 (≈ 84.444 ₫) | $6.50 (≈ 168.887 ₫) | $0.3248 (≈ 8.444 ₫) |
| deepseek-flash (vào 0.3 · ra 1.2 $/1M) | $0.0712 (≈ 1.850 ₫) | $0.1256 (≈ 3.265 ₫) | $0.0464 (≈ 1.206 ₫) | $4.84 (≈ 125.768 ₫) | $9.67 (≈ 251.536 ₫) | $19.35 (≈ 503.072 ₫) | $0.9674 (≈ 25.154 ₫) |
| deepseek-v4-pro (vào 1.32 · ra 3.96 $/1M) | $0.3109 (≈ 8.083 ₫) | $0.5486 (≈ 14.264 ₫) | $0.2026 (≈ 5.269 ₫) | $21.13 (≈ 549.430 ₫) | $42.26 (≈ 1.098.860 ₫) | $84.53 (≈ 2.197.720 ₫) | $4.23 (≈ 109.886 ₫) |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.7) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: deepseek-flash. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 9/50.
- Tỷ giá: 1 USD = 26.000 ₫ ((tự ước tính) tỉ giá tham khảo, chưa tra ngày 28/11/2026).
