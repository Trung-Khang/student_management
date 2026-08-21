# Student Management System

Bài tập nhỏ môn Công nghệ phần mềm.

## Công nghệ sử dụng

| Thành phần | Công nghệ |
|-----------|-----------|
| Frontend   | HTML / CSS / JavaScript (Vanilla) |
| Backend    | Python + Flask (REST API) |
| Database   | SQLite (mục đích chạy ngay, không cần cài đặt) |

> Ghi chú: `database/database.sql` chứa script gốc dùng cho **SQL Server**.
> Bản chạy này dùng **SQLite** với cùng schema (`SinhVien`, `MaSo`, `HoTen`, `DiaChi`)
> để có thể khởi chạy nhanh mà không cần cài SQL Server.

## Cài đặt & Chạy

> **Trên Windows, dùng `py` thay vì `python`** vì lệnh `python` có thể bị
> trỏ nhầm tới Windows Store (gây lỗi "Python was not found").

### Chạy chỉ với MỘT lệnh duy nhất

Backend Flask **tự phục vụ luôn cả frontend** tại trang chủ, nên bạn không cần
chạy server riêng cho frontend:

```bash
cd backend
py -m pip install -r requirements.txt
py app.py
```

Sau đó mở trình duyệt truy cập: **http://localhost:5000**

Cả giao diện (frontend) lẫn API (backend) đều chạy trên cùng một cổng 5000.

> (Không bắt buộc) Nếu muốn tách riêng frontend ra, chạy thêm:
> ```bash
> cd frontend
> py -m http.server 5500
> ```
> rồi truy cập `http://localhost:5500`. CORS đã được bật để hỗ trợ trường hợp này.

## API Endpoints

| Method | Endpoint                  | Mô tả                              |
|--------|---------------------------|------------------------------------|
| GET    | `/api/students`           | Lấy danh sách sinh viên            |
| GET    | `/api/students?maso=...`   | Lọc theo mã số (chính xác)         |
| GET    | `/api/students?hoten=...`  | Lọc theo tên (chứa chuỗi, không phân biệt hoa thường) |
| POST   | `/api/students`           | Thêm mới `{maso, hoten, diachi}`   |
| PUT    | `/api/students/<maso>`    | Cập nhật `{hoten, diachi}`         |
| DELETE | `/api/students/<maso>`    | Xóa theo mã số                     |
| GET    | `/api/health`             | Kiểm tra trạng thái server         |

### Ví dụ với curl

```bash
# Lấy tất cả
curl http://localhost:5000/api/students

# Thêm mới
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"maso":"24133099","hoten":"Nguyễn Test","diachi":"Cần Thơ"}'

# Cập nhật
curl -X PUT http://localhost:5000/api/students/24133099 \
  -H "Content-Type: application/json" \
  -d '{"diachi":"Đà Lạt"}'

# Xóa
curl -X DELETE http://localhost:5000/api/students/24133099
```

## Cấu trúc thư mục

```
student_management/
├── backend/
│   ├── app.py              # Flask app + REST API
│   ├── db.py               # Kết nối & khởi tạo SQLite
│   ├── requirements.txt    # Dependencies
│   └── students.db         # (tự tạo khi chạy)
├── database/
│   └── database.sql        # Script SQL Server gốc
└── frontend/
    └── index.html          # Giao diện quản lý (gọi API backend)
``` 
