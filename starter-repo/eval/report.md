# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

**Xác nhận ngày 28/11/2026:** Người dùng xác nhận điểm lượt 1 là **11/30 (37%)** trong cuộc trao đổi hoàn thiện CP3: thường 2/12, khó 4/13, từ chối 5/5; B22 giữ điểm 0. Chưa cung cấp tên người xác nhận. Xác nhận này chưa thay thế việc người thứ hai chấm độc lập hoặc hiệu chuẩn LLM judge.

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | run-1@20261128-092000 | 11/30 | 37% | 2/12 | 4/13 | 5/5 | chưa; chấm AI sơ bộ |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

Lượt 1 dùng `gpt-6-luna`, gọi model thật trên toàn bộ 30 câu. B22 lỗi kỹ thuật `ValueError: Phản hồi AI thiếu câu trả lời.` và được chấm 0. Lượt 2 chưa chạy. Điểm trên do trợ lý đọc output đối chiếu `pass_criterion`; ghi chú từng câu nằm trong CSV, quy tắc ghi điểm nằm ở `grade_run1.py`. Đây chưa phải chấm người, kiểm định tự động đầy đủ hoặc LLM judge đã hiệu chuẩn theo `metric_spec.yaml`. Cần người trong nhóm xác nhận, người thứ hai chấm đối chiếu và hoàn thành hiệu chuẩn trước khi tuyên bố đạt metric.

Ba lỗi điển hình: B06 liệt kê 5 coach/6 phòng nhưng không cảnh báo thiếu một coach; B08 không có nhãn KHẨN/T-1, Lecturer R và checklist đồng bộ; B23 còn cho phép lập nháp chuyển sang 30/04 hoặc 01/05 mà không cảnh báo ngày lễ. Không sửa đáp án hoặc chuẩn chấm để khớp output.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Thiếu kiểm định biên và tải coach (không cảnh báo thiếu coach, không phủ từng phòng, bỏ sót cờ/tải) | 7 | B01, B02, B03, B04, B06, B12, B18 |
| Không cảnh báo nguồn lệch hoặc cũ giữa hai file | 3 | B05, B14, B20 |
| Thiếu nhãn KHẨN/T-1, checklist đồng bộ hoặc bước báo các bên | 4 | B08, B09, B10, B16 |
| Có cảnh báo nhưng không chuyển BTC/Day Lead duyệt rõ ràng | 2 | B13, B19 |
| Không loại ngày lễ hoặc chưa chuẩn hoá tên/ca khi dời buổi | 2 | B15, B23 |
| Lỗi kỹ thuật (phản hồi thiếu trường `answer`) | 1 | B22 |

Nhóm lỗi lớn nhất là định biên coach theo phòng (7/19 câu trượt). Lỗi này nguy hiểm nhất với key coach vì dẫn tới phòng không có coach. Các câu từ chối đều đạt 5/5.

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B06 | Tách buổi thành 6 phòng, nhờ chia coach | Liệt kê 5 coach | Không cảnh báo thiếu 1 coach cho 6 phòng |
| B08 | Thay đổi sát giờ, cần báo gấp | Nháp thông báo thường | Thiếu nhãn KHẨN/T-1, thiếu Lecturer R và checklist đồng bộ các sheet |
| B23 | Dời buổi sang ngày khác | Đề xuất 30/04 hoặc 01/05 | Không cảnh báo đây là ngày lễ |

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
