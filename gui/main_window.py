# gui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from database.db_manager import DatabaseManager
from utils.alert_system import AlertSystem
from utils.chart_generator import ChartGenerator
from utils.device_simulator import HealthDeviceSimulator
from .components.dashboard_tab import DashboardTab
from .components.input_tab import InputTab
from .components.charts_tab import ChartsTab
from .components.history_tab import HistoryTab

class MainWindow:
    """Cửa sổ chính của ứng dụng"""
    
    def __init__(self, db_manager: DatabaseManager, user: dict):
        self.db = db_manager
        self.user = user
        self.logger = logging.getLogger(__name__)
        
        # Initialize utilities
        self.alert_system = AlertSystem(db_manager)
        self.chart_generator = ChartGenerator()
        self.device_simulator = HealthDeviceSimulator(
            user_height=user['height'],
            initial_weight=65.0
        )
        
        self.setup_window()
        self.setup_ui()
        self.load_initial_data()
    
    def setup_window(self):
        """Thiết lập cửa sổ chính"""
        self.root = tk.Tk()
        self.root.title(f"Health Tracker - {self.user['full_name']}")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure styles
        self.setup_styles()
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
    
    def setup_styles(self):
        """Thiết lập styles cho giao diện"""
        style = ttk.Style()
        
        # Configure styles
        style.configure('Main.TFrame', background='#f5f5f5')
        style.configure('Header.TFrame', background='#2c3e50')
        style.configure('Header.TLabel', background='#2c3e50', foreground='white', font=('Arial', 12, 'bold'))
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f5f5f5')
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
        
        # Tab styles
        style.configure('Custom.TNotebook', background='#f5f5f5')
        style.configure('Custom.TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[15, 5])
    
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        # Main container
        main_container = ttk.Frame(self.root, style='Main.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.setup_header(main_container)
        
        # Tab container
        self.setup_tabs(main_container)
        
        # Status bar
        self.setup_status_bar(main_container)
    
    def setup_header(self, parent):
        """Thiết lập header"""
        header_frame = ttk.Frame(parent, style='Header.TFrame', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # User info
        user_info_frame = ttk.Frame(header_frame, style='Header.TFrame')
        user_info_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        ttk.Label(user_info_frame, text=f"👤 {self.user['full_name']}", 
                 style='Header.TLabel').pack(anchor=tk.W)
        
        ttk.Label(user_info_frame, 
                 text=f"Chiều cao: {self.user['height']} cm | {self.get_bmi_classification()}",
                 style='Header.TLabel').pack(anchor=tk.W)
        
        # Current stats
        stats_frame = ttk.Frame(header_frame, style='Header.TFrame')
        stats_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        self.current_weight_label = ttk.Label(stats_frame, text="Cân nặng: -- kg", 
                                            style='Header.TLabel')
        self.current_weight_label.pack(anchor=tk.E)
        
        self.current_bmi_label = ttk.Label(stats_frame, text="BMI: --", 
                                         style='Header.TLabel')
        self.current_bmi_label.pack(anchor=tk.E)
    
    def setup_tabs(self, parent):
        """Thiết lập hệ thống tab"""
        # Create notebook
        self.notebook = ttk.Notebook(parent, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.dashboard_tab = DashboardTab(self.notebook, self)
        self.input_tab = InputTab(self.notebook, self)
        self.charts_tab = ChartsTab(self.notebook, self)
        self.history_tab = HistoryTab(self.notebook, self)
        
        # Add tabs to notebook
        self.notebook.add(self.dashboard_tab.frame, text="🏠 Tổng quan")
        self.notebook.add(self.input_tab.frame, text="📝 Nhập liệu")
        self.notebook.add(self.charts_tab.frame, text="📊 Biểu đồ")
        self.notebook.add(self.history_tab.frame, text="📋 Lịch sử")
        
        # Bind tab change event
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
    
    def setup_status_bar(self, parent):
        """Thiết lập status bar"""
        status_frame = ttk.Frame(parent, relief=tk.SUNKEN, borderwidth=1)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Sẵn sàng", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=5, pady=2)
    
    def get_bmi_classification(self):
        """Lấy phân loại BMI hiện tại"""
        current_weight = self.db.get_current_weight(self.user['user_id'])
        if current_weight:
            from utils.bmi_calculator import BMICalculator
            height_m = self.user['height'] / 100
            bmi = BMICalculator.calculate_bmi(current_weight, height_m)
            category = BMICalculator.get_bmi_category(bmi)['category']
            return category
        return "Chưa có dữ liệu"
    
    def load_initial_data(self):
        """Tải dữ liệu ban đầu"""
        self.update_current_stats()
        self.dashboard_tab.refresh_data()
        self.set_status("Tải dữ liệu thành công")
    
    def update_current_stats(self):
        """Cập nhật thống kê hiện tại"""
        current_weight = self.db.get_current_weight(self.user['user_id'])
        
        if current_weight:
            from utils.bmi_calculator import BMICalculator
            height_m = self.user['height'] / 100
            bmi = BMICalculator.calculate_bmi(current_weight, height_m)
            
            self.current_weight_label.config(text=f"Cân nặng: {current_weight} kg")
            self.current_bmi_label.config(text=f"BMI: {bmi}")
        else:
            self.current_weight_label.config(text="Cân nặng: Chưa có dữ liệu")
            self.current_bmi_label.config(text="BMI: --")
    
    def on_tab_changed(self, event):
        """Xử lý khi chuyển tab"""
        tab_index = self.notebook.index(self.notebook.select())
        tab_names = ["Tổng quan", "Nhập liệu", "Biểu đồ", "Lịch sử"]
        
        if tab_index < len(tab_names):
            self.set_status(f"Đang xem: {tab_names[tab_index]}")
            
            # Refresh tab data when selected
            if tab_index == 0:  # Dashboard
                self.dashboard_tab.refresh_data()
            elif tab_index == 2:  # Charts
                self.charts_tab.refresh_charts()
            elif tab_index == 3:  # History
                self.history_tab.refresh_data()
    
    def set_status(self, message: str):
        """Thiết lập trạng thái"""
        self.status_label.config(text=message)
        self.logger.info(f"Status: {message}")
    
    def show_alert(self, title: str, message: str, alert_type: str = "info"):
        """Hiển thị thông báo"""
        if alert_type == "error":
            messagebox.showerror(title, message)
        elif alert_type == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)
    
    def refresh_all(self):
        """Làm mới tất cả dữ liệu"""
        self.update_current_stats()
        self.dashboard_tab.refresh_data()
        self.charts_tab.refresh_charts()
        self.history_tab.refresh_data()
        self.set_status("Đã làm mới tất cả dữ liệu")
    
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()
    
    def cleanup(self):
        """Dọn dẹp tài nguyên"""
        if hasattr(self, 'root'):
            self.root.quit()