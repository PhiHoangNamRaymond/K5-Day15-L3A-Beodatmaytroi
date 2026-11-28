# Reflection — Phan Hải Đăng

## 1. Vai trò và phần mình làm

Mình phụ trách xác định track và triển khai dự án lên Render, phù hợp với vai trò Deploy + BE trong [TEAMS.md](../TEAMS.md).
Mình xác định bài toán thuộc Track A — EdTech, hướng A5 — Vận hành đào tạo, tập trung hỗ trợ Key Coach lập và cập nhật lịch phân công.
Căn cứ lựa chọn là quy trình mỗi Key Coach tự dùng Claude tổng hợp thời khóa biểu, đăng ký và performance của Lab Coach nhưng chưa có quy chuẩn phân công chung.
Phạm vi và hướng giải quyết được trình bày trong [spec.md](../spec.md); phần triển khai của mình là đưa dự án lên Render để phục vụ chạy thử và demo.

## 2. AI hỗ trợ mình thế nào

Mình sử dụng Codex để hỗ trợ rà soát repository, đối chiếu tiêu chí CP3 và hoàn thiện tài liệu cho bài toán đã chọn.
AI giúp kiểm tra luồng gọi model và phân tích các điểm cần chú ý khi cấu hình backend, biến môi trường và dữ liệu nguồn cho việc triển khai.
Một điểm cần sửa lại là tài liệu đánh giá có ba ngưỡng 90% không khớp bản chốt 80% trong spec; mình xác nhận spec là nguồn chuẩn để AI đồng bộ.
Qua đó, mình thấy cần kiểm tra output AI bằng cấu hình, mã nguồn và kết quả chạy thực tế, thay vì coi nội dung AI tạo ra là kết luận cuối cùng.

## 3. Một câu thử trượt và bài học

Trong [eval/run-1.csv](../eval/run-1.csv), câu B23 kiểm tra yêu cầu chuyển lịch sang ngày 30/04 hoặc 01/05.
AI vẫn cho phép chuẩn bị bản nháp chuyển lịch sang hai ngày này mà không cảnh báo đây là ngày nghỉ lễ, nên câu thử không đạt.
Mình học được rằng trả lời lịch sự và yêu cầu người duyệt chưa đủ để bảo đảm đề xuất đúng quy tắc vận hành.
Những ràng buộc như ngày nghỉ và phạm vi khóa học cần được kiểm tra bằng code trước khi trình phương án; khi deploy, cũng cần kiểm tra hành vi nghiệp vụ thay vì chỉ kiểm tra server khởi động được.
