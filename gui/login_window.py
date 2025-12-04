# gui/login_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import logging
from datetime import datetime
from database.db_manager import DatabaseManager
from utils.validators import HealthDataValidator
from .theme import AppTheme

class LoginWindow:
    """Cửa sổ đăng nhập và đăng ký"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.logger = logging.getLogger(__name__)
        self.root = tk.Tk()
        self.setup_window()
        self.setup_login_tab()
    
    def setup_window(self):
        """Thiết lập cửa sổ chính"""
        self.root.title("Health Tracker - Theo dõi Sức khỏe")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        # Cấu hình theme
        AppTheme.configure_styles(self.root)
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
    
    def setup_login_tab(self):
        """Thiết lập tab đăng nhập"""
        # Container chính
        container = ttk.Frame(self.main_frame, style='Main.TFrame')
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Logo/Title
        title_frame = ttk.Frame(container, style='Main.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = ttk.Label(title_frame, text="🏥 Health Tracker", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Theo dõi Sức khỏe của bạn", 
                                  style='Secondary.TLabel')
        subtitle_label.pack()
        
        # Form frame
        form_frame = ttk.Frame(container, style='Main.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username
        ttk.Label(form_frame, text="📧 Tên đăng nhập:", style='Title2.TLabel').pack(anchor=tk.W, pady=(15, 5))
        self.username_entry = ttk.Entry(form_frame, width=40)
        self.username_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        self.username_entry.bind('<Return>', lambda e: self.login())
        
        # Password
        ttk.Label(form_frame, text="🔐 Mật khẩu:", style='Title2.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.password_entry = ttk.Entry(form_frame, width=40, show="•")
        self.password_entry.pack(fill=tk.X, pady=(0, 25), ipady=8)
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_button = ttk.Button(form_frame, text="✓ Đăng nhập", 
                                command=self.login, style='Primary.TButton')
        login_button.pack(fill=tk.X, ipady=10)
        
        # Register link
        register_frame = ttk.Frame(form_frame, style='Main.TFrame')
        register_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Label(register_frame, text="Chưa có tài khoản?", 
                 style='Secondary.TLabel').pack(side=tk.LEFT)
        register_link = ttk.Button(register_frame, text="Đăng ký ngay →", 
                                 command=self.show_register, style='Accent.TButton')
        register_link.pack(side=tk.RIGHT)
        
        # Focus on username field
        self.username_entry.focus()
    
    def show_register(self):
        """Hiển thị form đăng ký"""
        # Clear current widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        title_frame.pack(fill=tk.X, padx=40, pady=20)
        
        title_label = ttk.Label(title_frame, text="📝 Đăng ký tài khoản", style='Title.TLabel')
        title_label.pack()
        
        # Tạo scrollable frame
        canvas = tk.Canvas(self.main_frame, bg=AppTheme.BG_SECONDARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Main.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, bg=AppTheme.BG_SECONDARY)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Padding frame
        padding_frame = ttk.Frame(scrollable_frame, style='Main.TFrame')
        padding_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Registration form
        fields = [
            ("📧 Tên đăng nhập:", "username"),
            ("🔐 Mật khẩu:", "password"), 
            ("👤 Họ và tên:", "full_name"),
            ("📏 Chiều cao (cm):", "height"),
            ("👥 Giới tính:", "gender")
        ]
        
        self.register_entries = {}
        
        for label_text, field_name in fields:
            ttk.Label(padding_frame, text=label_text, style='Title2.TLabel').pack(anchor=tk.W, pady=(10, 5))
            
            if field_name == "gender":
                entry = ttk.Combobox(padding_frame, values=["Nam", "Nữ", "Khác"], width=40, state="readonly")
            elif field_name == "password":
                entry = ttk.Entry(padding_frame, width=40, show="•")
            else:
                entry = ttk.Entry(padding_frame, width=40)
            
            entry.pack(fill=tk.X, pady=(0, 0), ipady=6)
            self.register_entries[field_name] = entry
            
            # Bind Enter key to register
            entry.bind('<Return>', lambda e: self.register())
        
        # Ngày sinh với DateEntry
        ttk.Label(padding_frame, text="📅 Ngày sinh:", style='Title2.TLabel').pack(anchor=tk.W, pady=(10, 5))
        
        # Frame cho input và nút chọn lịch
        date_input_frame = ttk.Frame(padding_frame, style='Main.TFrame')
        date_input_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.register_entries['birth_date'] = ttk.Entry(date_input_frame, width=34)
        self.register_entries['birth_date'].pack(side=tk.LEFT, ipady=6, fill=tk.X, expand=True)
        self.register_entries['birth_date'].bind('<Return>', lambda e: self.register())
        
        # Nút chọn lịch
        calendar_btn = ttk.Button(date_input_frame, text="📅", width=3,
                                 command=self.open_calendar_picker)
        calendar_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Set default values
        self.register_entries['height'].insert(0, "170")
        
        # Buttons
        button_frame = ttk.Frame(padding_frame, style='Main.TFrame')
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="✓ Đăng ký", 
                  command=self.register, style='Primary.TButton').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(button_frame, text="← Quay lại", 
                  command=self.show_login).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Focus on first field
        self.register_entries['username'].focus()
    
    def show_login(self):
        """Quay lại màn hình đăng nhập"""
        # Clear current widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        self.setup_login_tab()
    
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
            
            # DateEntry
            date_entry = DateEntry(cal_frame, 
                                  width=30,
                                  borderwidth=2,
                                  year=datetime.now().year - 20,
                                  month=datetime.now().month,
                                  day=1,
                                  dateformat='%Y-%m-%d')
            date_entry.pack(pady=20)
            
            # Button frame
            btn_frame = ttk.Frame(cal_frame)
            btn_frame.pack(fill=tk.X, pady=(20, 0))
            
            def select_date():
                selected_date = date_entry.get_date().strftime('%Y-%m-%d')
                self.register_entries['birth_date'].delete(0, tk.END)
                self.register_entries['birth_date'].insert(0, selected_date)
                calendar_window.destroy()
            
            ttk.Button(btn_frame, text="✓ Chọn", command=select_date,
                      style='Accent.TButton').pack(side=tk.RIGHT, padx=5)
            
            ttk.Button(btn_frame, text="✕ Hủy", command=calendar_window.destroy).pack(side=tk.RIGHT)
        
        except ImportError:
            messagebox.showwarning("Cảnh báo", 
                "Thư viện tkcalendar chưa được cài đặt.\n"
                "Chạy lệnh: pip install tkcalendar\n"
                "Bạn có thể nhập ngày sinh dưới dạng YYYY-MM-DD")
        except Exception as e:
            self.logger.error(f"Error opening calendar: {e}")
            messagebox.showerror("Lỗi", f"Lỗi mở lịch: {e}")
    
    def login(self):
        """Xử lý đăng nhập"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Validation
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin đăng nhập")
            return
        
        # Authenticate user
        user = self.db.authenticate_user(username, password)
        
        if user:
            self.logger.info(f"User logged in: {username}")
            self.root.destroy()
            
            # Import here to avoid circular imports
            from .main_window import MainWindow
            main_window = MainWindow(self.db, user)
            main_window.run()
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def register(self):
        """Xử lý đăng ký"""
        try:
            # Get data from entries
            username = self.register_entries['username'].get().strip()
            password = self.register_entries['password'].get()
            full_name = self.register_entries['full_name'].get().strip()
            height_str = self.register_entries['height'].get().strip()
            birth_date = self.register_entries['birth_date'].get().strip()
            gender = self.register_entries['gender'].get().strip()
            
            # Validate required fields
            if not username or not password or not full_name:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin bắt buộc")
                return
            
            # Validate data
            validation_results = HealthDataValidator.validate_user_registration(
                username, password, full_name
            )
            
            # Check for validation errors
            errors = []
            for field, (is_valid, message) in validation_results.items():
                if not is_valid:
                    errors.append(f"{field}: {message}")
            
            # Validate height
            if height_str:
                try:
                    height = float(height_str)
                    is_valid, message = HealthDataValidator.validate_height(height)
                    if not is_valid:
                        errors.append(f"Chiều cao: {message}")
                except ValueError:
                    errors.append("Chiều cao phải là số")
            else:
                height = 170.0  # Default height
            
            # Validate birth date
            if birth_date:
                is_valid, message = HealthDataValidator.validate_birth_date(birth_date)
                if not is_valid:
                    errors.append(f"Ngày sinh: {message}")
            
            # Validate gender
            if gender:
                is_valid, message = HealthDataValidator.validate_gender(gender)
                if not is_valid:
                    errors.append(f"Giới tính: {message}")
            
            if errors:
                messagebox.showerror("Lỗi đăng ký", "\n".join(errors))
                return
            
            # Create user
            success = self.db.create_user(
                username=username,
                password=password,
                full_name=full_name,
                height=height,
                birth_date=birth_date if birth_date else None,
                gender=gender if gender else None
            )
            
            if success:
                messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
                self.show_login()
            else:
                messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại")
                
        except Exception as e:
            self.logger.error(f"Error during registration: {e}")
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi đăng ký: {e}")
    
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()