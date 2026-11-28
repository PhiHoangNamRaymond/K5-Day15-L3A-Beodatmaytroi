# Chạy project với hai workbook và DeepSeek

## Dữ liệu nguồn

Đặt hai file `teaching-schedule.xlsx` và `lab-coach-schedule.xlsx` trong `data-btc/` ở gốc repository, hoặc cấu hình `SCHEDULE_SOURCE_DIR` trỏ tới thư mục chứa chúng. Máy kiểm tra CP3 đang dùng `data/training-ops/` qua biến này trong `.env`. Không chỉnh sửa workbook gốc và không commit chúng.

Có thể thay đường dẫn bằng biến `TEACHING_FILE`, `COACH_FILE` hoặc `SCHEDULE_SOURCE_DIR` trong `starter-repo/.env`. Nút **Đọc lại Excel** nhập lại nội dung và kiểm tra fingerprint. Bản nháp của phiên bản dữ liệu cũ được giữ riêng, không tự áp vào nguồn mới.

Bộ nhập dùng thư viện chuẩn Python: đọc giá trị XML đã lưu và ô gộp, không chạy macro hoặc chỉ dẫn trong workbook. Công thức chỉ dùng cached value; không tính lại Excel. Lịch hoạt động từ sheet Khoá 9 được nhập, Khoá 8 chỉ là dữ liệu lịch sử và không được trộn sang lịch hiện tại. Hai ô dạy song song ở hai phòng được giữ thành hai bản ghi; lớp online gộp được giữ một bản ghi. Vì vậy số bản ghi buổi/phòng không đồng nghĩa số buổi của từng lớp.

## Cấu hình DeepSeek

Mở `starter-repo/.env`, điền `API_KEY` trực tiếp trên máy, không đưa key vào frontend hay Git:

```dotenv
MODEL_PROVIDER=deepseek
MODEL_NAME=deepseek-flash
API_BASE_URL=https://api.deepseek.com
API_KEY=
```

Sau khi sửa `.env`, khởi động lại backend. Project gửi nội dung lịch, lựa chọn nhân sự và vị trí nguồn của tuần được chọn sang DeepSeek khi bấm tạo đề xuất hoặc hỏi trợ lý. Không gửi cột email. Khi chưa có key hoặc model lỗi, lịch và kiểm tra quy tắc vẫn dùng được; UI ghi rõ fallback, không tính là AI thật.

Nhà cung cấp và JSON output: https://api-docs.deepseek.com/ và https://api-docs.deepseek.com/guides/json_mode/ . Model có thể thay đổi bằng `MODEL_NAME` theo tài khoản của nhóm.

## Phát triển trên Windows

### Cấu hình OpenAI

Đặt `MODEL_PROVIDER=openai`, `MODEL_NAME` theo model tài khoản được phép dùng và `API_KEY` trong `.env`. Bỏ dòng `API_BASE_URL` hoặc để trống để dùng `https://api.openai.com/v1`. URL có giá trị sẽ ghi đè mặc định, kể cả khi đổi provider. Biến môi trường của tiến trình được ưu tiên hơn `.env`.

Nhánh OpenAI gửi `max_completion_tokens`; nhánh DeepSeek giữ `max_tokens`. Lượt thử CP3 ngày 28/11/2026 đã gọi `gpt-6-luna` thành công, có usage thực. Đây không phải bằng chứng mọi câu benchmark đều đạt.

Lệnh eval nhận câu hỏi tự nhiên và gửi ngữ cảnh toàn khóa từ workbook, gồm lịch, yêu cầu đổi buổi, workload và lịch sử. Giao diện hỏi trợ lý vẫn dùng ngữ cảnh tuần được chọn. Chi phí và hành vi hai đường gọi có thể khác nhau.

Terminal 1 — từ thư mục gốc repo:

```powershell
cd starter-repo
python codebase/web_app.py
```

Terminal 2 — từ thư mục gốc repo:

```powershell
cd starter-repo/frontend
npm ci --include=dev
npm run dev
```

Mở http://127.0.0.1:5173 . Vite chuyển tiếp `/api` tới Python cổng 8765. Chỉ cần cài dependency một lần hoặc khi lockfile thay đổi. Không khởi động hai Vite của cùng project.

## Chạy một server sau khi build

```powershell
cd starter-repo
npm --prefix frontend run build
python codebase/web_app.py
```

Mở http://127.0.0.1:8765 . Backend mặc định chỉ bind localhost. Để chạy trong container, dùng `HOST=0.0.0.0` và mount nguồn dữ liệu chỉ đọc.

## Luồng sử dụng

1. Chọn tuần, tìm/lọc lớp trong bảng lịch; mở **Xem nguồn** để kiểm tra sheet và ô.
2. **Tạo đề xuất lịch**: code sinh phương án có giới hạn, kiểm ràng buộc rồi DeepSeek chọn và giải thích. Chỉ có thể chọn nhân sự/phòng có nguồn; đề xuất không tự ghi đè.
3. Áp dụng từng buổi hoặc cả đề xuất. Ghi kết quả xác minh với nguồn khi hai bảng khác nhau. Với buổi online, bổ sung link HTTPS.
4. Ở **Cập nhật phòng**, nhập buổi, phòng mới hoặc để trống khi thu hồi, nguồn và trạng thái xác nhận. Các cập nhật được lưu tích lũy, không thay thế cập nhật của buổi khác.
5. Rà soát tất cả vấn đề trước khi duyệt. Phòng chưa xác nhận, trùng phòng, trùng nhân sự và thiếu dữ liệu quan trọng sẽ chặn duyệt.
6. Duyệt để lưu bản bàn giao, tải bản văn bản. Hệ thống không tự gửi ra ngoài. Chỉ bấm **Ghi nhận đã thông báo** sau khi người phụ trách đã gửi thông báo thật; bản đó mới được dùng làm mốc lịch đã thông báo.

Yêu cầu đổi ca trong workbook chỉ hiển thị để rà soát. Trạng thái “đã đổi” trong form không tự chứng minh lịch nguồn đã đồng bộ. Đăng ký một buổi cũng không chứng minh người đó rảnh mọi buổi khác. Phòng phụ và sự phân công bao phủ nhiều phòng được hiển thị theo nguồn, không tự suy đoán vị trí từng coach.

## Lưu trữ và giới hạn triển khai

SQLite mặc định tại `starter-repo/.local/schedule.sqlite3`, gồm bản nháp, cập nhật phòng, bản duyệt, bản ghi đã thông báo và trace. Dữ liệu này bị Git bỏ qua. Đặt `SCHEDULE_DB` nếu muốn dùng đường dẫn khác; giữ file qua các lần chạy. Không dùng filesystem tạm thời của hosting làm lưu trữ bền vững nếu chưa gắn volume.

Ứng dụng hiện là công cụ local cho người điều phối, chưa có đăng nhập/phân quyền nhiều người dùng. Không mở public với dữ liệu thật khi chưa bổ sung xác thực. Các file nguồn BTC là giả lập, không phải bằng chứng pain. Không sửa metric/chuẩn đạt đã khóa ở CP2 để khớp triển khai.

## Kiểm tra

Tại thư mục gốc repository:

```powershell
python -B -m unittest discover -s starter-repo/tests -v
npm --prefix starter-repo/frontend run build
```

Bộ test dùng workbook local và SQLite tạm, không gọi API trả phí. Test transport/model dùng mock không được báo là đánh giá model thật. Kết quả gọi DeepSeek thật phải ghi token usage thực tế, không tự sửa báo cáo đánh giá.
