# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | | | | |
| Thiết kế và code giao diện lịch tuần | Codex; skill frontend-design của Anthropic | Thiết kế bố cục, màu sắc, kiểu chữ và component React/CSS; kiểm tra build, TypeScript và luồng giao diện trên localhost | Kiểm tra tự động và trình duyệt đã chạy; nhóm cần xem lại giao diện và giải thích phần có tên mình trước khi nộp | Nguyễn Vũ Hoàng: FE; Phí Hoàng Nam: UI/UX và tích hợp |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào data (viết script đếm, gợi ý nhãn) | | | Kiểm tay __ dòng, khớp __ | |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, văn bản | | | | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).


## Tích hợp workbook và DeepSeek

Codex hỗ trợ viết bộ đọc XLSX, nối dữ liệu hai workbook, kiểm ràng buộc, SQLite, API DeepSeek và UI nguồn/đổi phòng/trợ lý. Bộ test tự động dùng dữ liệu local và mock model; các lượt API thật được báo riêng, lấy token từ usage. Nhóm cần kiểm tra logic nguồn, quyền duyệt và phần việc có tên mình trước khi nộp.
