-- Tạo và sử dụng Cơ sở dữ liệu
CREATE DATABASE ThucHanhSQL;
USE ThucHanhSQL;

-- Tạo bảng SinhVien
CREATE TABLE SinhVien (
    MaSo VARCHAR(20) PRIMARY KEY,
    HoTen NVARCHAR(100) NOT NULL,
    DiaChi NVARCHAR(255)
);

-- INSERT
INSERT INTO SinhVien (MaSo, HoTen, DiaChi)
VALUES
    ('24133023', N'Hoàng Ngọc Huy', N'Đồng Tháp'),
    ('24133049', N'Hồ Trọng Sơn', N'Đồng Tháp'),
    ('24133036', N'Trần Duy Luân', N'Phú Yên'),
    ('24133028', N'Nguyễn Quỳnh Chi', N'Thành phố Hồ Chí Minh'),
    ('24133012', N'Huỳnh Qy Đức', N'Đồng Tháp');

-- SELECT: Xem danh sách sinh viên
SELECT * FROM SinhVien;

-- UPDATE: Cập nhật địa chỉ
UPDATE SinhVien
SET DiaChi = N'Đà Nẵng'
WHERE MaSo = '24133023';

-- Kiểm tra sau UPDATE
SELECT * FROM SinhVien;

-- DELETE: Xóa sinh viên
DELETE FROM SinhVien
WHERE MaSo = '24133049';

-- Kiểm tra sau DELETE
SELECT * FROM SinhVien;