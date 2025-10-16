# gui/login_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from database.db_manager import DatabaseManager
from utils.validators import HealthDataValidator

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
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
    
    def setup_login_tab(self):
        """Thiết lập tab đăng nhập"""
        # Title
        title_label = ttk.Label(self.main_frame, text="🔐 Đăng nhập", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Username
        username_frame = ttk.Frame(self.main_frame)
        username_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(username_frame, text="Tên đăng nhập:").pack(side=tk.LEFT)
        self.username_entry = ttk.Entry(username_frame, width=30, font=('Arial', 10))
        self.username_entry.pack(side=tk.RIGHT, padx=(10, 0))
        self.username_entry.bind('<Return>', lambda e: self.login())
        
        # Password
        password_frame = ttk.Frame(self.main_frame)
        password_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(password_frame, text="Mật khẩu:").pack(side=tk.LEFT)
        self.password_entry = ttk.Entry(password_frame, width=30, show="•", font=('Arial', 10))
        self.password_entry.pack(side=tk.RIGHT, padx=(10, 0))
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_button = ttk.Button(self.main_frame, text="Đăng nhập", 
                                command=self.login, style='Accent.TButton')
        login_button.pack(pady=20)
        
        # Register link
        register_frame = ttk.Frame(self.main_frame)
        register_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(register_frame, text="Chưa có tài khoản?").pack(side=tk.LEFT)
        register_link = ttk.Button(register_frame, text="Đăng ký ngay", 
                                 command=self.show_register, style='Link.TButton')
        register_link.pack(side=tk.RIGHT)
        
        # Focus on username field
        self.username_entry.focus()
    
    def show_register(self):
        """Hiển thị form đăng ký"""
        # Clear current widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_label = ttk.Label(self.main_frame, text="📝 Đăng ký tài khoản", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Registration form
        fields = [
            ("Tên đăng nhập:", "username"),
            ("Mật khẩu:", "password"), 
            ("Họ và tên:", "full_name"),
            ("Chiều cao (cm):", "height"),
            ("Ngày sinh (YYYY-MM-DD):", "birth_date"),
            ("Giới tính:", "gender")
        ]
        
        self.register_entries = {}
        
        for label_text, field_name in fields:
            frame = ttk.Frame(self.main_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=label_text).pack(side=tk.LEFT)
            
            if field_name == "gender":
                entry = ttk.Combobox(frame, values=["Nam", "Nữ", "Khác"], width=27)
            elif field_name == "password":
                entry = ttk.Entry(frame, width=30, show="•")
            else:
                entry = ttk.Entry(frame, width=30)
            
            entry.pack(side=tk.RIGHT, padx=(10, 0))
            self.register_entries[field_name] = entry
            
            # Bind Enter key to register
            if field_name == "gender":
                entry.bind('<Return>', lambda e: self.register())
            else:
                entry.bind('<Return>', lambda e: self.register())
        
        # Set default values
        self.register_entries['height'].insert(0, "170")
        
        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Đăng ký", 
                  command=self.register).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(button_frame, text="← Quay lại", 
                  command=self.show_login).pack(side=tk.RIGHT)
        
        # Focus on first field
        self.register_entries['username'].focus()
    
    def show_login(self):
        """Quay lại màn hình đăng nhập"""
        # Clear current widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        self.setup_login_tab()
    
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