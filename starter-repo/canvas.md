# Canvas — Bèo dạt mây trôi · Track A

> Điền ở guide bước 1.4. CP1 17:00 Thứ Sáu 27/11: nộp bản đầu, đủ 7 dòng (dòng 4 được ghi giả thuyết + nguồn sẽ kiểm).
> CP2 19:30 Thứ Sáu 27/11: cập nhật (số bằng chứng đầu, lát cắt đã chốt) và điền dòng "Đã đổi gì so với CP1".
> Track F: chép thêm thẻ đề của nhóm (khung trong file track F) xuống dưới bảng này.

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt dự kiến | Track A — hướng A5: hỗ trợ key coach lập bản nháp lịch giảng dạy theo tuần và cập nhật lịch khi thông tin phòng thay đổi. |
| 2 | Người dùng chính (một vai cụ thể — không phải "học viên nói chung") | Key coach phụ trách chuẩn bị, rà soát và duyệt bản lịch tuần trước khi chuyển BTC thông báo; vai trò và quyền duyệt thực tế cần xác nhận với người trực tiếp phụ trách ngoài nhóm. |
| 3 | Pain một câu: ai — đang làm gì — vướng đâu — hậu quả | Khi chuẩn bị lịch giảng dạy cho tuần sau, key coach phải tổng hợp đăng ký nhân sự và tình trạng phòng đang chờ nhà trường duyệt rồi cập nhật khi phòng bị thu hồi hoặc đổi sau thông báo, khiến việc đối chiếu thủ công mất thời gian và có nguy cơ bỏ sót lớp bị ảnh hưởng hoặc thông báo sai địa điểm. |
| 4 | Bằng chứng đầu — CP1: giả thuyết + nguồn sẽ kiểm · CP2: số đầu tiên + 1 trích dẫn | Giả thuyết cần kiểm chứng: việc tổng hợp lịch tuần và xử lý thay đổi phòng bằng tay gây chậm trễ hoặc sai lệch. Bối cảnh do nhóm mô tả; chưa có số đo thời gian hoặc trích dẫn phỏng vấn được ghi nhận trong repo. Nhóm dự kiến xác nhận quy trình, vai trò, quyền duyệt và thời gian thực hiện với key coach hoặc cán bộ BTC trực tiếp phụ trách ngoài nhóm; cần bổ sung tiến độ liên hệ và bằng chứng thật cho CP2. Dữ liệu giả lập chỉ dùng chạy thử, không phải bằng chứng pain. |
| 5 | **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả) | Một key coach chuẩn bị lịch giảng dạy cho tuần sau, AI đề xuất bản nháp lịch từ đăng ký nhân sự và thông tin phòng được cung cấp, đồng thời chỉ ra dữ liệu thiếu hoặc mâu thuẫn và đề xuất chỉnh sửa khi phòng thay đổi, giúp key coach hoàn thiện và duyệt lịch nhanh hơn so với làm thủ công. |
| 6 | AI tự làm đến đâu + 1 dòng lý do: sai thì ai chịu gì | AI chỉ tạo bản nháp lịch, cảnh báo, đề xuất chỉnh sửa và nháp thông báo kèm nguồn; phòng chưa xác nhận thì đánh dấu chờ xác nhận, không tự tìm hay chốt phòng, ghi vào lịch chính thức hoặc gửi thông báo; code kiểm tra trùng người, trùng phòng, còn key coach sửa và duyệt vì lịch sai có thể khiến giảng viên hoặc lớp đến sai phòng, sai tòa nhà hoặc sai giờ. |
| 7 | Phân công có tên | Phí Hoàng Nam: yêu cầu, tài liệu, UI/UX và hỗ trợ tích hợp; Trần Thanh Long: luồng AI đề xuất lịch tuần, giải thích cảnh báo và xử lý thay đổi phòng; Phan Hải Đăng: BE, kiểm tra ràng buộc và triển khai; Nguyễn Vũ Hoàng: FE bảng lịch tuần, nguồn đối chiếu, chỉnh sửa và duyệt. |
| — | *(CP2)* Đã đổi gì so với CP1 | Chuyển từ rà soát lịch ngày hôm sau sang đề xuất bản nháp lịch tuần; bổ sung xử lý phòng chưa xác nhận, bị thu hồi hoặc đổi sau thông báo, xác định lớp bị ảnh hưởng và tạo nháp thông báo thay đổi; giữ key coach là người sửa và duyệt. Điều chỉnh dựa trên phạm vi và bối cảnh nhóm mô tả, chưa có kết quả kiểm chứng pain. |
