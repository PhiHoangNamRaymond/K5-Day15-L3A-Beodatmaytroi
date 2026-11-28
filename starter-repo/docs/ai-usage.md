# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Codex, Claude Code | Codex: bộ đọc XLSX, kiểm ràng buộc, SQLite, API (xem mục dưới). Claude Code: `check_staffing`, retry JSON, lưới lịch tuần `WeekCalendar.tsx` | Test tự động 25/25; nhóm cần đọc hiểu phần có tên mình | |
| Thiết kế và code giao diện lịch tuần | Codex; skill frontend-design của Anthropic | Thiết kế bố cục, màu sắc, kiểu chữ và component React/CSS; kiểm tra build, TypeScript và luồng giao diện trên localhost | Kiểm tra tự động và trình duyệt đã chạy; nhóm cần xem lại giao diện và giải thích phần có tên mình trước khi nộp | Nguyễn Vũ Hoàng: FE; Phí Hoàng Nam: UI/UX và tích hợp |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào data (viết script đếm, gợi ý nhãn) | Không dùng | Nhóm không đào data làm bằng chứng pain (workbook là dữ liệu giả lập) | — | — |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | Không dùng | Không sinh dữ liệu synthetic; chỉ dùng workbook BTC | — | — |
| Chấm cột `pass` bằng LLM (nếu có) | Claude Code | Đọc output lượt 1 và lượt 2, đối chiếu `pass_criterion`, ghi điểm sơ bộ qua `eval/grade_run1.py`, `grade_run2.py` | Nhóm xác nhận điểm lượt 1; lượt 2 cần người kiểm lại; chưa có người thứ hai chấm 5 output | |
| Slide, văn bản | Claude Code | Đồng bộ `spec.md`, README, `eval/report.md`, `eval/README.md`, `cost/cost-estimate.md`; tổng hợp khảo sát thành số x/n và trích dẫn | Nhóm kiểm nội dung trước khi nộp | |
| Cải tiến lượt 2 | Claude Code | Viết `check_staffing` (`codebase/tools.py`), quy tắc staffing trong `agent.py`, test `tests/test_staffing.py` | 22/22 test qua; nhóm cần đọc hiểu code trước demo | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).


## Tích hợp workbook và DeepSeek

Codex hỗ trợ viết bộ đọc XLSX, nối dữ liệu hai workbook, kiểm ràng buộc, SQLite, API DeepSeek và UI nguồn/đổi phòng/trợ lý. Bộ test tự động dùng dữ liệu local và mock model; các lượt API thật được báo riêng, lấy token từ usage. Nhóm cần kiểm tra logic nguồn, quyền duyệt và phần việc có tên mình trước khi nộp.
