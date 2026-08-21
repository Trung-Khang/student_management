"""
Database helper for the student management system.

Mặc định dùng SQLite để chạy được ngay lập tức mà không cần cài đặt
SQL Server. Schema bảng ``SinhVien`` được thiết kế tương thích với
script ``database/database.sql`` (MaSo, HoTen, DiaChi).
"""
import sqlite3
from pathlib import Path

# Đường dẫn file database nằm ngay cạnh file này
DB_PATH = Path(__file__).parent / "students.db"


def get_connection() -> sqlite3.Connection:
    """Trả về một connection tới SQLite (row factory đã bật)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Tạo bảng (nếu chưa tồn tại) và nạp dữ liệu mẫu ban đầu."""
    conn = get_connection()
    cur = conn.cursor()

    # Schema tương đương database/database.sql
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS SinhVien (
            MaSo   TEXT PRIMARY KEY,
            HoTen  TEXT NOT NULL,
            DiaChi TEXT
        )
        """
    )

    # Nạp dữ liệu mẫu nếu bảng còn trống (khớp với các câu INSERT trong script)
    cur.execute("SELECT COUNT(*) FROM SinhVien")
    count = cur.fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO SinhVien (MaSo, HoTen, DiaChi) VALUES (?, ?, ?)",
            [
                ("24133023", "Hoàng Ngọc Huy", "Đồng Tháp"),
                ("24133049", "Hồ Trọng Sơn", "Đồng Tháp"),
                ("24133036", "Trần Duy Luân", "Phú Yên"),
                ("24133028", "Nguyễn Quỳnh Chi", "Thành phố Hồ Chí Minh"),
                ("24133012", "Huỳnh Qy Đức", "Đồng Tháp"),
            ],
        )

    conn.commit()
    conn.close()
