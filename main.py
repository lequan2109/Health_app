# main.py
import tkinter as tk
from tkinter import messagebox
import logging
from database.db_manager import DatabaseManager
from gui.login_window import LoginWindow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('health_app.log'),
        logging.StreamHandler()
    ]
)

def main():
    """Hàm chính khởi chạy ứng dụng"""
    try:
        logging.info("Khởi động ứng dụng Theo dõi Sức khỏe")
        
        # Khởi tạo database
        db_manager = DatabaseManager()
        db_manager.init_database()
        
        # Hiển thị màn hình đăng nhập
        login_window = LoginWindow(db_manager)
        login_window.run()
        
    except Exception as e:
        logging.error(f"Lỗi khởi chạy ứng dụng: {e}")
        messagebox.showerror("Lỗi", f"Không thể khởi chạy ứng dụng: {e}")

if __name__ == "__main__":
    main()