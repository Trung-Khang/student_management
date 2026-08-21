"""
Student Management System - Backend + Frontend (Flask)

Chỉ cần MỘT lệnh duy nhất:  py app.py

Flask đồng thời phục vụ:
  - REST API tại  /api/students  (SELECT, INSERT, UPDATE, DELETE)
  - Frontend tĩnh tại  /         (file frontend/index.html)

Mở trình duyệt: http://localhost:5000
"""
import sqlite3

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from db import get_connection, init_db

app = Flask(__name__)
# Cho phép frontend gọi API từ nguồn khác (localhost:5500, file://, ...)
CORS(app)

# Khởi tạo database khi app load
init_db()

# Thư mục chứa frontend (cấp trên của backend, trong thư mục gốc dự án)
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


# ---------------------------------------------------------------------------
# Frontend (phục vụ index.html ở trang chủ)
# ---------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def serve_index():
    """Trả về file frontend/index.html."""
    return send_from_directory(FRONTEND_DIR, "index.html")


# ---------------------------------------------------------------------------
# Helpers chuyển đổi dữ liệu
# ---------------------------------------------------------------------------
def row_to_dict(row):
    """Chuyển một sqlite3.Row thành dict với key là tên cột."""
    return {key: row[key] for key in row.keys()}


# ---------------------------------------------------------------------------
# API - SELECT (danh sách / tìm kiếm)
# ---------------------------------------------------------------------------
@app.route("/api/students", methods=["GET"])
def list_students():
    maso = request.args.get("maso", "").strip()
    hoten = request.args.get("hoten", "").strip()

    queries, params = ["SELECT * FROM SinhVien WHERE 1=1"], []

    if maso:
        queries.append("AND MaSo = ?")
        params.append(maso)
    if hoten:
        queries.append("AND HoTen LIKE ?")
        params.append(f"%{hoten}%")

    conn = get_connection()
    rows = conn.execute(" ".join(queries), params).fetchall()
    conn.close()

    return jsonify([row_to_dict(r) for r in rows]), 200


# ---------------------------------------------------------------------------
# API - INSERT (thêm mới)
# ---------------------------------------------------------------------------
@app.route("/api/students", methods=["POST"])
def create_student():
    data = request.get_json(silent=True) or {}
    maso = (data.get("maso") or "").strip()
    hoten = (data.get("hoten") or "").strip()
    diachi = (data.get("diachi") or "").strip()

    if not maso or not hoten:
        return jsonify({"error": "MaSo và HoTen là bắt buộc."}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO SinhVien (MaSo, HoTen, DiaChi) VALUES (?, ?, ?)",
            (maso, hoten, diachi),
        )
        conn.commit()
        cur.execute("SELECT * FROM SinhVien WHERE MaSo = ?", (maso,))
        created = cur.fetchone()
        conn.close()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": f"Mã số {maso} đã tồn tại."}), 409

    return jsonify(row_to_dict(created)), 201


# ---------------------------------------------------------------------------
# API - UPDATE
# ---------------------------------------------------------------------------
@app.route("/api/students/<maso>", methods=["PUT"])
def update_student(maso):
    data = request.get_json(silent=True) or {}
    hoten = (data.get("hoten") or "").strip()
    diachi = (data.get("diachi") or "").strip()

    if not hoten and not diachi:
        return jsonify({"error": "Không có dữ liệu nào để cập nhật."}), 400

    conn = get_connection()
    cur = conn.cursor()

    # Kiểm tra tồn tại
    existing = cur.execute(
        "SELECT * FROM SinhVien WHERE MaSo = ?", (maso,)
    ).fetchone()
    if existing is None:
        conn.close()
        return jsonify({"error": f"Không tìm thấy Mã số {maso}."}), 404

    # Cập nhật các trường được gửi lên
    new_hoten = hoten if hoten else existing["HoTen"]
    new_diachi = diachi if diachi else existing["DiaChi"]

    cur.execute(
        "UPDATE SinhVien SET HoTen = ?, DiaChi = ? WHERE MaSo = ?",
        (new_hoten, new_diachi, maso),
    )
    conn.commit()
    cur.execute("SELECT * FROM SinhVien WHERE MaSo = ?", (maso,))
    updated = cur.fetchone()
    conn.close()

    return jsonify(row_to_dict(updated)), 200


# ---------------------------------------------------------------------------
# API - DELETE
# ---------------------------------------------------------------------------
@app.route("/api/students/<maso>", methods=["DELETE"])
def delete_student(maso):
    conn = get_connection()
    cur = conn.cursor()

    existing = cur.execute(
        "SELECT * FROM SinhVien WHERE MaSo = ?", (maso,)
    ).fetchone()
    if existing is None:
        conn.close()
        return jsonify({"error": f"Không tìm thấy Mã số {maso}."}), 404

    cur.execute("DELETE FROM SinhVien WHERE MaSo = ?", (maso,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Đã xóa Mã số {maso}."}), 200


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # host=0.0.0.0 để có thể truy cập từ máy khác trong mạng LAN nếu cần
    app.run(host="0.0.0.0", port=5000, debug=True)
