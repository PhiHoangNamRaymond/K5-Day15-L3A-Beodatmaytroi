# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử (bài mẫu, thông báo mẫu, đoạn transcript…) để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Dataset 1 · [tên]

| | |
|---|---|
| Dùng để làm gì | Nguồn chuẩn (*source of truth*) cho công cụ tra cứu lịch lớp, phòng học, giảng viên, chuyên đề và cảnh báo trùng lịch; đối chiếu dựng các câu `data_that` trong `eval/benchmark.csv`. |
| Từ đâu | Data BTC cấp (`data/training-ops/teaching-schedule.xlsx` trong repo đề — 7 sheet: `Khoá 9 (GĐ1)`, `Tong_hop`, `Canh_bao`, `Nhan_su`, `Dang_ky_chi_tiet`, `Lịch sử chỉnh sửa`, `Khoá 8 (GĐ2)`). |
| Xử lý những bước gì | |
| Số dòng / số đoạn | 108 buổi học hoạt động trên `Khoá 9 (GĐ1)` (50 LEC, 58 LAB/Hackathon trong 21 ngày học `15/04–08/05/2027`; tính tách lớp gộp là 111 buổi) · 204 dòng `Dang_ky_chi_tiet` (32 người) · 35 dòng `Tong_hop` · 46 dòng `Canh_bao` (11 trùng GV, 14 trùng Lab Coach, 21 đăng ký lặp) · 44 dòng `Lịch sử chỉnh sửa`. |
| Phiên bản / ngày lấy | Bản xuất giả lập lúc `21:00 ngày 27/04/2027` (ô `D1` sheet `Khoá 9 (GĐ1)`). |
| Nhãn | Data vận hành giả lập do BTC cấp (cấu trúc bảng tính thật, thực thể và ngày giả lập; không tính làm bằng chứng pain R1). |
| Giới hạn | 20 buổi vẫn ở trạng thái phòng `chờ xác nhận`; 3 buổi trong `Tong_hop` có 0 giảng viên đăng ký (`20/04`, `21/04`, `23/04` Sáng); không có cột khu vực hay ca tối cho giảng viên; không có mã buổi định danh duy nhất nối sẵn sang file lab coach. |

## Dataset 2 · Bảng vận hành & đổi ca đội Lab Coach (`lab-coach-schedule.xlsx`)

| | |
|---|---|
| Dùng để làm gì | Nguồn cho công cụ kiểm tra định biên Lab Coach / Key Coach theo phòng, tải công việc (`Workload`), cờ trùng ca (`L!`), hàng đợi đổi buổi và kiểm tra độ lệch đồng bộ với bảng giảng dạy. |
| Từ đâu | Data BTC cấp (`data/training-ops/lab-coach-schedule.xlsx` trong repo đề — 6 sheet: `Master Plan`, `Lịch lớp K9 (bản chép)`, `Lịch lab 1504-2404`, `Lịch lab 2604-0805`, `Đổi buổi (form)`, `Workload - Lab coach`). |
| Xử lý những bước gì | |
| Số dòng / số đoạn | 62 Lab Coach trên `Workload - Lab coach` (tải 0–10 ca; 2 cờ trùng `L!` ở `Lab Coach BH`, `Lab Coach BI`) · 279 lượt phân công coach-ca trên 2 sheet `Lịch lab` (98 `Rảnh`, 125 `Chưa bắt đầu`, 33 `Chưa cập nhật`, 18 `Đang thực hiện`, 4 `Chưa phân công`, 1 `Không phân công`) · 22 yêu cầu `Đổi buổi (form)` (8 chưa xử lý, 5 ghi `chưa cập nhật sheet`, 4 gửi khẩn ≤24h trước giờ học). |
| Phiên bản / ngày lấy | Bản chụp vận hành Khoá 9; riêng `Lịch lớp K9 (bản chép)` chép ngày `12/04/2027` (ô `D1`). |
| Nhãn | Data vận hành giả lập do BTC cấp (không tính làm bằng chứng pain R1). |
| Giới hạn | Bản chép lịch lớp cũ hơn bảng giảng dạy 15 ngày (lệch 44 ô phòng, 12 ô giảng viên); 19 buổi ở `Lịch lab 2604-0805` lệch trạng thái phòng so với `Khoá 9 (GĐ1)`; 12 buổi có số coach ít hơn số phòng (vd `28/04 Chiều L3B LAB 10`: 4 coach / 6 phòng); 11/22 đơn đổi buổi ghi mục tiêu tự do (`buổi nào cũng được`, `nhờ BTC xếp giúp`); sheet đợt 1 (`1504-2404`) không có cột `Phòng` từng dòng như đợt 2. |

## Dataset 3 · Bộ câu thử đánh giá (`eval/benchmark.csv`)

| | |
|---|---|
| Dùng để làm gì | Đánh giá tự động & bán tự động hành vi xếp lại lịch và bảo vệ vận hành lớp qua `python run.py eval` theo 9 metric trong `eval/metric_spec.yaml`. |
| Từ đâu | 21/30 câu (`data_that`, 70%) rút từ các ca và điểm lệch thực tế khi đối chiếu 2 file lịch BTC cấp + 9/30 câu (`tu_viet`, 30%) cho tình huống biên, thiếu thông tin, quyền riêng tư và tấn công vượt quyền / prompt injection. |
| Xử lý những bước gì | Kiểm toán chéo 2 file để khớp đúng mã buổi, phòng và khung ngày `15/04–08/05/2027`; chia theo 3 nhóm (`12 thuong` · `13 kho` · `5 tu_choi`); kiểm tra hợp lệ bằng `python run.py check`. |
| Số dòng / số đoạn | 30 câu thử (21 `data_that`, 9 `tu_viet`). |
| Phiên bản / ngày lấy | Chốt ngày `27/11/2026` (trước mốc CP2). |
| Nhãn | Kết hợp `data_that` (21 dòng từ bộ lịch giả lập BTC cấp) + `synthetic` / `tu_viet` (9 dòng viết tay theo kịch bản 4 lớp chỗ khó ở `spec.md` §5, không dùng LLM sinh ngẫu nhiên nên không có random seed; đã kiểm tay 9/9 dòng). |
| Giới hạn | Chưa có câu `nguoi_dung` trích từ phỏng vấn người thật (sẽ bổ sung nếu có thêm log phỏng vấn trước CP3). |
