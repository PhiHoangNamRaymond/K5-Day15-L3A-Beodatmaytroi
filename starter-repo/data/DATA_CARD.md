# Data card — dữ liệu lập lịch và cập nhật phòng

## Dataset 1 · teaching-schedule.xlsx

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | Lịch lớp, phòng, giảng viên, đăng ký nhân sự và lịch sử sửa để lập/rà soát lịch tuần |
| Từ đâu | File người dùng cung cấp; bản local tại data-btc/ ở gốc repo, không commit |
| Xử lý | codebase/xlsx_reader.py đọc XML/cached values và ô gộp; codebase/excel_data.py chuẩn hóa ngày/giờ, lớp, buổi, phòng và tên; giữ nguồn sheet/ô |
| Quy mô nhập | 129 bản ghi buổi/phòng; 108 nhóm buổi; 204 đăng ký nhân sự; 4 tuần, 2027-04-15–2027-05-08 |
| Phiên bản | SHA-256 6618f114bdfd4c10d0c149fc45152c740eb80bc7a1d08768be147bae69934068 |
| Nhãn | Giả lập do BTC cung cấp; không phải bằng chứng pain |
| Giới hạn | Hai ô dạy song song giữ hai bản ghi; lớp online gộp giữ một bản ghi; số nhóm buổi không tự nhân theo số lớp trong ô gộp; phòng dự kiến không được coi là đã xác nhận |

Không dùng Canh_bao làm đáp án đầu vào của AI. Không trộn lịch Khoá 8 sang Khoá 9. Công thức chỉ đọc cached values, không tính lại workbook. Nếu chưa có xác nhận giờ riêng thì dùng khung giờ của buổi trong cùng sheet, không tự tạo giờ.

## Dataset 2 · lab-coach-schedule.xlsx

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | Nối phân công lab/key coach, đối chiếu bản chép lịch, đọc yêu cầu đổi ca và workload |
| Từ đâu | File người dùng cung cấp; bản local tại data-btc/ ở gốc repo, không commit |
| Xử lý | Điền giá trị ô gộp theo nguồn; nối ngày + lớp + loại/số buổi + sáng/chiều; chỉ lấy tên coach đúng nhãn; không gửi cột email sang model |
| Quy mô | 282 dòng coach có nhãn hợp lệ, 62 người trong workload, 22 yêu cầu đổi ca |
| Phiên bản | SHA-256 24ee52f50d0a3bc1b2b84b77f4e81c67d2976ee91135e339ecf4d6e760669795 |
| Nhãn | Giả lập do BTC cung cấp; không phải bằng chứng pain |
| Giới hạn | Phân công ở cấp nhóm buổi không chứng minh coach đứng ở phòng cụ thể; workload trống không chứng minh rảnh; form đã xử lý không chứng minh bảng lịch đã đồng bộ |

## Dữ liệu ứng dụng tạo

Bản nháp, cập nhật phòng do người nhập, bản duyệt, bản ghi đã thông báo và trace được lưu SQLite ở .local/schedule.sqlite3. Gắn fingerprint hai file nguồn để không áp bản nháp cũ vào workbook mới. Không có dữ liệu synthetic bổ sung được trình bày như dữ liệu nguồn; test dùng SQLite tạm và mock model riêng, không phải bằng chứng pain.

Lịch sử sửa ô không chứng minh thông báo đã gửi. Chỉ dùng bản đã được người dùng ghi nhận đã thông báo để đối chiếu lịch đã phát. Số liệu tự động trên đây có thể chạy lại qua tools.dataset(); nhóm chưa ghi nhận kiểm tay toàn bộ dữ liệu hoặc kết quả đo người dùng.
