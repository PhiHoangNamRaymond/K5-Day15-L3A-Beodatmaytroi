# Reflection — Nguyễn Vũ Hoàng

1. **Vai trò và phần mình làm**<br>
   Mình phụ trách frontend cho luồng lập lịch giảng dạy tuần và dựng wireframe trên Figma.<br>
   Mình chuyển giao diện sang React và TypeScript, rồi tách thành ba tab Lịch tuần, Cập nhật phòng, Rà soát & bàn giao (`3e7599a`, `b77ccbf`).<br>
   Sau phản hồi của nhóm, mình đưa đề xuất vào ô chọn, thêm chọn nhiều lab coach và rà trùng theo từng người (`3aec76c`). Mình ghi cách chạy thử và hợp đồng API trong [WORKLOAD.md](../../WORKLOAD.md).

2. **AI hỗ trợ mình thế nào**<br>
   Mình dùng Codex trong VS Code để đọc spec, chuyển cấu trúc frontend, dựng các màn hình và kiểm thử luồng với dữ liệu giả lập. Mình dùng Figma để đối chiếu bố cục và luồng thao tác với nhóm.<br>
   Bản giao diện AI dựng ban đầu dồn nhiều chữ và thao tác vào cùng một màn. Mình yêu cầu tách ba tab, giữ chung bản nháp giữa các tab và rút gọn phần chữ.<br>
   Khi nhóm góp ý về ô chọn, mình yêu cầu đưa đề xuất vào ngay trong ô với nhãn rõ ràng và kiểm lại thao tác chọn hai coach cho cùng một buổi.

3. **Một câu thử trượt của nhóm và bài học**<br>
   Ở câu **B06**, lượt đánh giá đầu liệt kê 5 lab coach cho 6 phòng nhưng bỏ sót cảnh báo thiếu một người. Lượt 2 đạt sau khi nhóm đưa kết quả kiểm định biên vào dữ liệu cho model ([báo cáo đánh giá](../eval/report.md)).<br>
   Mình rút ra rằng ô chọn nhiều người chỉ hỗ trợ nhập phân công. Hệ thống vẫn phải kiểm riêng phòng nào đã đủ coach và người nào bị trùng ca.<br>
   Cảnh báo trên màn rà soát cần chỉ ra phòng còn thiếu hoặc tên người bị trùng để Key Coach biết sửa ở đâu trước khi duyệt.
