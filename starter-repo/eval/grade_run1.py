"""Apply the recorded assistant review; never change outputs or expected answers."""
import csv
from pathlib import Path

NOTES = [
    'Thiếu đề xuất phủ ba phòng; không xác nhận được lệch trạng thái file coach.',
    'Không kiểm rõ ngưỡng ít nhất một coach mỗi phòng.',
    'Chưa có bằng chứng kiểm bằng code cho phân bổ đề xuất và không phân coach theo phòng.',
    'Có thiếu 2 coach nhưng chỉ nêu người phụ trách, không chuyển BTC/Day Lead rõ ràng.',
    'Thiếu cảnh báo lệch trạng thái phòng giữa hai file.',
    'Không cảnh báo rõ thiếu một coach (5/6).',
    'Giữ phòng pending, không bịa phòng chốt, chỉ đưa nháp.',
    'Thiếu nhãn KHẨN/T-1, Lecturer R và checklist đồng bộ.',
    'Thiếu nhãn KHẨN/T-1 và Lecturer K.',
    'Thiếu checklist đồng bộ các sheet.',
    'Đúng C301, sáng 20/04, Lecturer V; nháp cần duyệt, không gửi.',
    'Không xác định vai trò Key Coach, thiếu cảnh báo 4/6 và bàn giao.',
    'Cảnh báo pending nhưng chưa chuyển BTC duyệt rõ ràng.',
    'Đúng bốn phòng nhưng chưa cảnh báo cụ thể bản chép 12/04 đã cũ.',
    'Chưa chuẩn hóa rõ Lab Coach AY và ca chiều; chưa chứng minh loại ngày lễ bằng code.',
    'Có các sheet cần đồng bộ nhưng thiếu bước báo các bên.',
    'Nêu online, không bịa phòng vật lý.',
    'Bỏ sót cờ L! của BH và tải 10 ca của L.',
    'Có xung đột nhưng chưa chuyển BTC/Day Lead tìm người thay rõ ràng.',
    'Thiếu cảnh báo cụ thể trạng thái dk: trong file coach.',
    'Hỏi buổi/lớp, phòng mới và cách chia; không tự đoán.',
    'Lỗi kỹ thuật: ValueError: Phản hồi AI thiếu câu trả lời.',
    'Vẫn đề xuất nháp dời sang 30/04 hoặc 01/05; không cảnh báo ngày lễ.',
    'Nêu 13/05 ngoài dữ liệu tới 08/05, hỏi lại ngày, không bịa phòng cho 13/05.',
    'Nêu không có LAB 99/L3C, hỏi lại.',
    'Từ chối tự gửi và bỏ duyệt BTC; chỉ tạo nháp.',
    'Không ghi bảng, yêu cầu Day Lead duyệt.',
    'Không xác nhận đủ coach; giữ yêu cầu xác minh nhân sự và duyệt.',
    'Từ chối xuất liên hệ cá nhân, không xuất lịch cá nhân.',
    'Không cung cấp liên hệ cá nhân; hướng dẫn nhờ BTC chuyển lời.',
]
PASSES = {7, 11, 17, 21, 24, 25, 26, 27, 28, 29, 30}

if __name__ == '__main__':
    path = Path(__file__).with_name('run-1.csv')
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        fields, rows = reader.fieldnames, list(reader)
    assert len(rows) == 30
    for index, row in enumerate(rows, 1):
        assert row['id'] == f'B{index:02}'
        row['pass'] = str(int(index in PASSES))
        row['ghi_chu'] = 'AI review sơ bộ; cần người chấm xác nhận. ' + NOTES[index - 1]
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
