import re
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# ----------------------------------------------------
# 1. Khởi tạo Cơ sở dữ liệu SQLite & Bảng SinhVien
# ----------------------------------------------------
def init_db():
    conn = sqlite3.connect("QuanLySinhVien.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SinhVien (
            MaSo TEXT PRIMARY KEY,
            HoTen TEXT NOT NULL,
            DiaChi TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ----------------------------------------------------
# RÀNG BUỘC CẤU TRÚC MÃ SỐ SINH VIÊN
# ----------------------------------------------------
def validate_maso(maso):
    # Ràng buộc 1: Không được chứa khoảng trắng
    if " " in maso:
        messagebox.showwarning("Lỗi định dạng", "Mã số sinh viên không được chứa khoảng trắng!")
        return False
        
    # Ràng buộc 2: Độ dài tối thiểu/tối đa (ví dụ từ 4 đến 10 ký tự)
    if not (4 <= len(maso) <= 10):
        messagebox.showwarning("Lỗi độ dài", "Mã số sinh viên phải từ 4 đến 10 ký tự!")
        return False

    # Ràng buộc 3: Chỉ bao gồm chữ cái và chữ số (không chứa ký tự đặc biệt)
    if not maso.isalnum():
        messagebox.showwarning("Lỗi ký tự", "Mã số sinh viên chỉ được chứa chữ cái và chữ số (không gồm ký tự đặc biệt)!")
        return False

    # Ràng buộc 4 (Tùy chọn): Kiểm tra định dạng Regex cụ thể (VD: SV12345 - 2 chữ cái đầu, các chữ số sau)
    # pattern = r'^[A-Za-z]{2}\d{5}$'
    # if not re.match(pattern, maso):
    #     messagebox.showwarning("Lỗi định dạng", "Mã số phải có dạng 2 chữ cái + 5 chữ số (Ví dụ: SV12345)!")
    #     return False

    return True

# ----------------------------------------------------
# 2. Các hàm xử lý CRUD (SQL Commands)
# ----------------------------------------------------

def load_data():
    for row in tree.get_children():
        tree.delete(row)
        
    conn = sqlite3.connect("QuanLySinhVien.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MaSo, HoTen, DiaChi FROM SinhVien")
    rows = cursor.fetchall()
    
    for row in rows:
        tree.insert("", tk.END, values=row)
        
    conn.close()

def insert_sinhvien():
    maso = entry_maso.get().strip().upper() # Tự động in hoa mã số
    hoten = entry_hoten.get().strip()
    diachi = entry_diachi.get().strip()
    
    # Ràng buộc trống
    if not maso or not hoten:
        messagebox.showwarning("Cảnh báo", "Mã số và Họ tên không được để trống!")
        return
    
    # Kiểm tra ràng buộc định dạng MSSV
    if not validate_maso(maso):
        return
        
    try:
        conn = sqlite3.connect("QuanLySinhVien.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO SinhVien (MaSo, HoTen, DiaChi) VALUES (?, ?, ?)", 
                       (maso, hoten, diachi))
        conn.commit()
        conn.close()
        
        clear_entries()
        load_data()
        messagebox.showinfo("Thành công", "Thêm sinh viên thành công!")
    except sqlite3.IntegrityError:
        # Ràng buộc trùng lặp khóa chính (PRIMARY KEY)
        messagebox.showerror("Lỗi trùng lặp", f"Mã sinh viên '{maso}' đã tồn tại trong hệ thống!")

def update_sinhvien():
    maso = entry_maso.get().strip().upper()
    hoten = entry_hoten.get().strip()
    diachi = entry_diachi.get().strip()
    
    if not maso:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã số sinh viên cần sửa!")
        return

    if not validate_maso(maso):
        return

    if not hoten:
        messagebox.showwarning("Cảnh báo", "Họ tên không được để trống khi cập nhật!")
        return
        
    conn = sqlite3.connect("QuanLySinhVien.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE SinhVien SET HoTen = ?, DiaChi = ? WHERE MaSo = ?", 
                   (hoten, diachi, maso))
    conn.commit()
    
    if cursor.rowcount > 0:
        messagebox.showinfo("Thành công", "Cập nhật thông tin thành công!")
    else:
        messagebox.showerror("Lỗi", "Không tìm thấy Mã sinh viên để cập nhật!")
        
    conn.close()
    clear_entries()
    load_data()

def delete_sinhvien():
    maso = entry_maso.get().strip().upper()
    
    if not maso:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn hoặc nhập Mã số sinh viên cần xóa!")
        return
        
    if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sinh viên {maso}?"):
        conn = sqlite3.connect("QuanLySinhVien.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SinhVien WHERE MaSo = ?", (maso,))
        conn.commit()
        
        if cursor.rowcount > 0:
            messagebox.showinfo("Thành công", "Xóa sinh viên thành công!")
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy Mã sinh viên để xóa!")
            
        conn.close()
        clear_entries()
        load_data()

def on_tree_select(event):
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        values = item['values']
        
        clear_entries()
        entry_maso.insert(0, values[0])
        entry_hoten.insert(0, values[1])
        entry_diachi.insert(0, values[2])

def clear_entries():
    entry_maso.delete(0, tk.END)
    entry_hoten.delete(0, tk.END)
    entry_diachi.delete(0, tk.END)

# ----------------------------------------------------
# 3. Xây dựng giao diện UI (Tkinter Window)
# ----------------------------------------------------
init_db()

root = tk.Tk()
root.title("Chương Trình Quản Lý Sinh Viên")
root.geometry("600x450")
root.resizable(False, False)

# Tiêu đề
lbl_title = tk.Label(root, text="QUẢN LÝ SINH VIÊN", font=("Arial", 16, "bold"), fg="blue")
lbl_title.pack(pady=10)

# Khung nhập liệu (Input Frame)
frame_input = tk.Frame(root)
frame_input.pack(pady=5)

tk.Label(frame_input, text="Mã Số:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
entry_maso = tk.Entry(frame_input, width=30)
entry_maso.grid(row=0, column=1, padx=5, pady=3)

tk.Label(frame_input, text="Họ Tên:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
entry_hoten = tk.Entry(frame_input, width=30)
entry_hoten.grid(row=1, column=1, padx=5, pady=3)

tk.Label(frame_input, text="Địa Chỉ:").grid(row=2, column=0, sticky="w", padx=5, pady=3)
entry_diachi = tk.Entry(frame_input, width=30)
entry_diachi.grid(row=2, column=1, padx=5, pady=3)

# Khung nút bấm (Button Frame)
frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

btn_add = tk.Button(frame_btn, text="Thêm (INSERT)", width=13, bg="#4CAF50", fg="white", command=insert_sinhvien)
btn_add.grid(row=0, column=0, padx=5)

btn_update = tk.Button(frame_btn, text="Sửa (UPDATE)", width=13, bg="#2196F3", fg="white", command=update_sinhvien)
btn_update.grid(row=0, column=1, padx=5)

btn_delete = tk.Button(frame_btn, text="Xóa (DELETE)", width=13, bg="#f44336", fg="white", command=delete_sinhvien)
btn_delete.grid(row=0, column=2, padx=5)

btn_clear = tk.Button(frame_btn, text="Làm mới", width=10, command=clear_entries)
btn_clear.grid(row=0, column=3, padx=5)

# Bảng hiển thị danh sách (Treeview - SELECT)
frame_tree = tk.Frame(root)
frame_tree.pack(fill="both", expand=True, padx=15, pady=10)

columns = ("MaSo", "HoTen", "DiaChi")
tree = ttk.Treeview(frame_tree, columns=columns, show="headings", height=8)

tree.heading("MaSo", text="Mã Số")
tree.heading("HoTen", text="Họ và Tên")
tree.heading("DiaChi", text="Địa Chỉ")

tree.column("MaSo", width=100, anchor="center")
tree.column("HoTen", width=200, anchor="w")
tree.column("DiaChi", width=250, anchor="w")

tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Nạp dữ liệu ban đầu
load_data()

# Chạy ứng dụng
root.mainloop()