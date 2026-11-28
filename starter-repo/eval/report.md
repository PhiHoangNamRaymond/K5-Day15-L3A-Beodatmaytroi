# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

**Xác nhận ngày 28/11/2026:** Người dùng xác nhận điểm lượt 1 là **11/30 (37%)** trong cuộc trao đổi hoàn thiện CP3: thường 2/12, khó 4/13, từ chối 5/5; B22 giữ điểm 0. Chưa cung cấp tên người xác nhận. Xác nhận này chưa thay thế việc người thứ hai chấm độc lập hoặc hiệu chuẩn LLM judge.

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | run-1@20261128-092000 | 11/30 | 37% | 2/12 | 4/13 | 5/5 | chưa; chấm AI sơ bộ |
| 2 | run-2@20261128-100217 | 17/30 | 57% | 4/12 | 8/13 | 5/5 | chưa; chấm AI sơ bộ |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

Lượt 1 dùng `gpt-6-luna`, gọi model thật trên toàn bộ 30 câu. B22 lỗi kỹ thuật `ValueError: Phản hồi AI thiếu câu trả lời.` và được chấm 0. Lượt 2 (`deepseek-flash`) chạy đủ 30 câu; B16 lỗi kỹ thuật `Model trả JSON không hợp lệ` và được chấm 0, quy tắc ghi điểm ở `grade_run2.py`. **Lượt 1 và lượt 2 khác model** (`gpt-6-luna` → `deepseek-flash`, vì máy chạy lượt 2 chỉ có key DeepSeek), nên mức tăng điểm có thể một phần do đổi model, không chỉ do cải tiến. Điểm trên do trợ lý đọc output đối chiếu `pass_criterion`; ghi chú từng câu nằm trong CSV, quy tắc ghi điểm nằm ở `grade_run1.py`. Đây chưa phải chấm người, kiểm định tự động đầy đủ hoặc LLM judge đã hiệu chuẩn theo `metric_spec.yaml`. Cần người trong nhóm xác nhận, người thứ hai chấm đối chiếu và hoàn thành hiệu chuẩn trước khi tuyên bố đạt metric.

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

- **Nhắm vào nhóm lỗi:** thiếu kiểm định biên và tải coach theo phòng (7 câu: B01, B02, B03, B04, B06, B12, B18). Đây là nhóm **đau nhất với người dùng** vì key coach lo nhất chuyện phòng không có coach khi tách lớp. Khảo sát R2 cũng kể: *"phải tách ra các phòng nhỏ hơn, phải tìm và sắp xếp thêm người rất là khó khăn"*. Ở lượt 1, model phải tự đếm coach trong ngữ cảnh khoảng 70k token nên đếm sai hoặc bỏ qua.
- **Đã sửa gì:**
  1. Thêm công cụ `check_staffing` (`codebase/tools.py`). Code tính cho từng nhóm buổi: số phòng, số coach đã phân, số coach thiếu, Key Coach, coach đã ở mức tải cao nhất, ứng viên tải thấp không trùng giờ, kèm nguồn.
  2. Đưa kết quả đó vào payload kèm 6 quy tắc trả lời (`STAFFING_RULES` trong `codebase/agent.py`): nêu x coach / y phòng, nêu Key Coach, cảnh báo quá tải, không bịa coach, chia theo từng phòng, chuyển BTC/Day Lead duyệt.
- **Kết quả:** nhóm lỗi định biên từ **0/7 → 3/7** (B02, B04, B06 đạt). Tổng điểm từ **37% → 57%** (11/30 → 17/30). Thường 2/12 → 4/12, khó 4/13 → 8/13, từ chối giữ 5/5. Ngoài nhóm mục tiêu còn đạt thêm B05, B10, B13, B14. Phần tăng này nhiều khả năng đến từ đổi model và từ dữ liệu staffing có số phòng rõ ràng.
- **Câu tệ đi sau khi sửa:** B11. Lượt 1 đạt; lượt 2 từ chối soạn nháp vì không thấy phòng cũ H210 trong nguồn, dù đề yêu cầu một bản nháp chờ duyệt. Ngoài ra B16 bị lỗi JSON (lượt 1 không lỗi nhưng chấm 0), còn B22 lượt 1 lỗi thì lượt 2 chạy được nhưng vẫn trượt.
- **Chi phí:** token vào trung bình tăng từ khoảng 70k lên **85k/câu** vì payload có thêm staffing.

## 4. Còn lại

- **Lỗi chưa sửa và mức nguy hiểm:**
  - Không có nhãn KHẨN/T-1 cho thay đổi sát giờ (B08, B09). Thông báo gấp có thể bị đọc như tin thường.
  - Không loại ngày lễ 30/04, 01/05 (B15, B23). Có thể dời buổi sang ngày nghỉ.
  - Chưa đọc được cờ `L!` trong Workload (B18). Có thể gán coach đang trùng ca.
  - Chia coach theo phòng còn sai khi coach chỉ được phân ở cấp nhóm buổi (B01 ghi mọi phòng "chưa có coach").
  - Hai câu lỗi JSON (B22 ở lượt 1, B16 ở lượt 2).
- **Chưa xác minh:** cả hai lượt đều do trợ lý AI chấm sơ bộ. Chưa có người thứ hai chấm 5 output; chưa hiệu chuẩn LLM judge; mỗi câu mới chạy 1 lần; chưa có tập giữ riêng (held-out).
- **Nếu có thêm 1 tuần:** thêm code gắn nhãn T-1 và lịch ngày lễ; parse cờ trong Workload; cắt ngữ cảnh theo ngày được hỏi để giảm token; chạy lại cả hai lượt trên cùng một model; nhờ người thứ hai chấm.
