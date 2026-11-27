# WORKLOAD · Nguyễn Vũ Hoàng

## Phần đã bàn giao

- Chuyển giao diện lịch tuần sang React, TypeScript và Vite. Mã giao diện nằm ở `starter-repo/frontend/src`.
- Dựng ba tab dùng chung bản nháp: Lịch tuần, Cập nhật phòng, Rà soát & bàn giao. Cảnh báo mở đúng buổi và nguồn trong bảng lịch.
- Hoàn thiện thao tác áp dụng hoặc bỏ qua đề xuất từng buổi, sửa phân công và rà lại. Luồng đổi phòng hiển thị phòng cũ, phòng mới và nháp thông báo khi có căn cứ.
- Chặn duyệt khi trùng ca hoặc thiếu nguồn. Sau khi duyệt có thể tải bản bàn giao cho BTC.
- [Bố cục ba tab trên Figma](https://www.figma.com/design/qoG5PzrsWyG59PHbFZ8zCm?node-id=15-2) phản ánh bản FE hiện tại. Sơ đồ CP2 nằm bên dưới để đối chiếu.

## Chạy và thử

Từ thư mục gốc, chạy:

```powershell
npm --prefix starter-repo/frontend ci
npm --prefix starter-repo/frontend run build
python starter-repo/codebase/web_app.py
```

Mở http://127.0.0.1:8765, chọn tuần 26/04/2027. Thử tạo đề xuất ở **Lịch tuần**, đổi H209 sang C403 hoặc chọn ca thu hồi C402 ở **Cập nhật phòng**, rồi dùng **Rà soát & bàn giao** để kiểm duyệt và tải. Ca thiếu lịch đã thông báo phải chặn duyệt. Dữ liệu demo là giả lập.

## Điểm nối cho team

| Phần | Vị trí và việc tiếp theo |
|---|---|
| API lịch tuần | `starter-repo/frontend/src/features/schedule/` mô tả kiểu dữ liệu và gọi `/api/weeks`, `/api/review`, `/api/propose`, `/api/approve`. Khi nối backend mới, giữ hợp đồng hoặc cập nhật API client cùng kiểu dữ liệu. |
| AI và dữ liệu | Xác nhận nguồn lịch, đăng ký và phòng. Cấu hình model bằng `.env` của nhóm, kiểm lại đề xuất với dữ liệu phù hợp. |
| Đánh giá và chi phí | Chạy hai lượt benchmark chính thức, chấm và mô phỏng từ token đo thật. Kết quả kiểm giao diện chỉ phản ánh luồng chạy bằng fixture. |

Nhánh bàn giao là `hoang/weekly-demo`.
