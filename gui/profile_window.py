# gui/profile_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import logging
from datetime import datetime
from database.db_manager import DatabaseManager
from utils.validators import HealthDataValidator
from .theme import AppTheme

class ProfileWindow:
    """Cửa sổ cập nhật hồ sơ người dùng"""
    
    def __init__(self, parent, db_manager: DatabaseManager, user: dict, on_update_callback=None):
        """
        Args:
            parent: Cửa sổ cha (None nếu là cửa sổ độc lập)
            db_manager: Database manager
            user: Thông tin user hiện tại
            on_update_callback: Hàm callback khi cập nhật xong
        """
        self.parent = parent
        self.db = db_manager
        self.user = user
        self.on_update_callback = on_update_callback
        self.logger = logging.getLogger(__name__)
        
        # Tạo cửa sổ
        if parent:
            self.root = tk.Toplevel(parent)
        else:
            self.root = tk.Tk()
        
        self.setup_window()
        self.setup_ui()
    
    def setup_window(self):
        """Thiết lập cửa sổ"""
        self.root.title("Cập nhật Hồ sơ")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center window
        if self.parent:
            self.root.transient(self.parent)
            self.root.grab_set()
        else:
            self.root.eval('tk::PlaceWindow . center')
        
        # Cấu hình theme
        AppTheme.configure_styles(self.root)
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Main.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title_label = ttk.Label(main_frame, text="✏️ Cập nhật Hồ sơ", style='Title.TLabel')
        title_label.pack(pady=(0, 25))
        
        # Tạo scrollable frame
        canvas = tk.Canvas(main_frame, bg=AppTheme.BG_SECONDARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Main.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, bg=AppTheme.BG_SECONDARY)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Fields
        self.entries = {}
        
        # Họ và tên
        ttk.Label(scrollable_frame, text="👤 Họ và tên:", style='Title2.TLabel').pack(anchor=tk.W, pady=(15, 5))
        self.entries['full_name'] = ttk.Entry(scrollable_frame, width=50)
        self.entries['full_name'].pack(fill=tk.X, pady=(0, 15), ipady=6)
        self.entries['full_name'].insert(0, self.user['full_name'])
        
        # Chiều cao
        ttk.Label(scrollable_frame, text="📏 Chiều cao (cm):", style='Title2.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.entries['height'] = ttk.Entry(scrollable_frame, width=50)
        self.entries['height'].pack(fill=tk.X, pady=(0, 15), ipady=6)
        self.entries['height'].insert(0, str(self.user['height']))
        
        # Ngày sinh với DateEntry
        ttk.Label(scrollable_frame, text="📅 Ngày sinh:", style='Title2.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        # Frame cho DateEntry và nút chọn lịch
        date_input_frame = ttk.Frame(scrollable_frame, style='Main.TFrame')
        date_input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Ngày sinh (hiển thị)
        birth_date_value = self.user.get('birth_date', '')
        self.entries['birth_date'] = ttk.Entry(date_input_frame, width=45)
        self.entries['birth_date'].pack(side=tk.LEFT, ipady=6, fill=tk.X, expand=True)
        self.entries['birth_date'].insert(0, birth_date_value if birth_date_value else "")
        
        # Nút chọn lịch
        calendar_btn = ttk.Button(date_input_frame, text="📅", width=3,
                                command=self.open_calendar_picker)
        calendar_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Giới tính
        ttk.Label(scrollable_frame, text="👥 Giới tính:", style='Title2.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.entries['gender'] = ttk.Combobox(scrollable_frame, values=["Nam", "Nữ", "Khác"], 
                                             width=47, state="readonly")
        self.entries['gender'].pack(fill=tk.X, pady=(0, 20), ipady=4)
        
        # Set current gender
        current_gender = self.user.get('gender', '')
        if current_gender:
            self.entries['gender'].set(current_gender)
        
        # Buttons
        button_frame = ttk.Frame(scrollable_frame, style='Main.TFrame')
        button_frame.pack(fill=tk.X, pady=(0, 0))
        
        ttk.Button(button_frame, text="💾 Lưu", command=self.save_changes,
                  style='Primary.TButton').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(button_frame, text="✕ Hủy", command=self.close_window).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
    
    def open_calendar_picker(self):
        """Mở hộp thoại chọn ngày"""
        try:
            # Tạo cửa sổ lịch
            calendar_window = tk.Toplevel(self.root)
            calendar_window.title("Chọn ngày sinh")
            calendar_window.geometry("400x350")
            calendar_window.transient(self.root)
            calendar_window.grab_set()
            
            # Frame chứa DateEntry
            cal_frame = ttk.Frame(calendar_window, padding="20")
            cal_frame.pack(fill=tk.BOTH, expand=True)
            
            # Label
            ttk.Label(cal_frame, text="Chọn ngày sinh của bạn:", 
                     font=('Arial', 12, 'bold')).pack(pady=(0, 20))
            
            # Lấy ngày hiện tại hoặc ngày đã chọn trước đó
            current_date = self.entries['birth_date'].get()
            try:
                if current_date:
                    initial_date = datetime.strptime(current_date, "%Y-%m-%d").date()
                else:
                    initial_date = datetime.now().date()
            except:
                initial_date = datetime.now().date()
            
            # DateEntry
            date_entry = DateEntry(cal_frame, 
                                  width=30,
                                  borderwidth=2,
                                  year=initial_date.year,
                                  month=initial_date.month,
                                  day=initial_date.day,
                                  dateformat='%Y-%m-%d')
            date_entry.pack(pady=20)
            
            # Button frame
            btn_frame = ttk.Frame(cal_frame)
            btn_frame.pack(fill=tk.X, pady=(20, 0))
            
            def select_date():
                selected_date = date_entry.get_date().strftime('%Y-%m-%d')
                self.entries['birth_date'].delete(0, tk.END)
                self.entries['birth_date'].insert(0, selected_date)
                calendar_window.destroy()
            
            ttk.Button(btn_frame, text="✓ Chọn", command=select_date,
                      style='Accent.TButton').pack(side=tk.RIGHT, padx=5)
            
            ttk.Button(btn_frame, text="✕ Hủy", command=calendar_window.destroy).pack(side=tk.RIGHT)
        
        except ImportError:
            messagebox.showwarning("Cảnh báo", 
                "Thư viện tkcalendar chưa được cài đặt.\n"
                "Vui lòng nhập ngày sinh dưới dạng YYYY-MM-DD")
        except Exception as e:
            self.logger.error(f"Error opening calendar: {e}")
            messagebox.showerror("Lỗi", f"Lỗi mở lịch: {e}")
    
    def save_changes(self):
        """Lưu thay đổi"""
        try:
            # Lấy dữ liệu
            full_name = self.entries['full_name'].get().strip()
            height_str = self.entries['height'].get().strip()
            birth_date = self.entries['birth_date'].get().strip()
            gender = self.entries['gender'].get().strip()
            
            # Validate required fields
            if not full_name:
                messagebox.showerror("Lỗi", "Họ và tên không được để trống")
                return
            
            # Validate height
            if height_str:
                try:
                    height = float(height_str)
                    is_valid, message = HealthDataValidator.validate_height(height)
                    if not is_valid:
                        messagebox.showerror("Lỗi", f"Chiều cao: {message}")
                        return
                except ValueError:
                    messagebox.showerror("Lỗi", "Chiều cao phải là số")
                    return
            else:
                height = self.user['height']
            
            # Validate birth date
            if birth_date:
                is_valid, message = HealthDataValidator.validate_birth_date(birth_date)
                if not is_valid:
                    messagebox.showerror("Lỗi", f"Ngày sinh: {message}")
                    return
            
            # Validate gender
            if gender:
                is_valid, message = HealthDataValidator.validate_gender(gender)
                if not is_valid:
                    messagebox.showerror("Lỗi", f"Giới tính: {message}")
                    return
            
            # Cập nhật trong database
            success = self.db.update_user(
                user_id=self.user['user_id'],
                full_name=full_name,
                height=height,
                birth_date=birth_date if birth_date else None,
                gender=gender if gender else None
            )
            
            if success:
                # Cập nhật user dict
                self.user['full_name'] = full_name
                self.user['height'] = height
                self.user['birth_date'] = birth_date
                self.user['gender'] = gender
                
                messagebox.showinfo("Thành công", "Cập nhật hồ sơ thành công!")
                
                # Gọi callback nếu có
                if self.on_update_callback:
                    self.on_update_callback(self.user)
                
                self.close_window()
            else:
                messagebox.showerror("Lỗi", "Cập nhật hồ sơ thất bại")
        
        except Exception as e:
            self.logger.error(f"Error saving changes: {e}")
            messagebox.showerror("Lỗi", f"Lỗi khi lưu thay đổi: {e}")
    
    def close_window(self):
        """Đóng cửa sổ"""
        self.root.destroy()
    
    def run(self):
        """Chạy cửa sổ (dùng nếu là cửa sổ độc lập)"""
        self.root.mainloop()
