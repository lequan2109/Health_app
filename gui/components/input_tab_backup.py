# gui/components/input_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
from utils.validators import HealthDataValidator
from utils.bmi_calculator import BMICalculator

class InputTab:
    """Tab nhập liệu"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.db = main_window.db
        self.user = main_window.user
        self.device_simulator = main_window.device_simulator
        self.logger = logging.getLogger(__name__)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        self.frame = ttk.Frame(self.parent)
        
        # Create notebook for different input types
        self.input_notebook = ttk.Notebook(self.frame)
        self.input_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Setup tabs
        self.setup_weight_tab()
        self.setup_activity_tab()
        self.setup_sleep_tab()
        self.setup_heart_rate_tab()
        self.setup_device_tab()
    
    def setup_weight_tab(self):
        """Thiết lập tab nhập cân nặng"""
        weight_tab = ttk.Frame(self.input_notebook)
        self.input_notebook.add(weight_tab, text="⚖️ Cân nặng")
        
        # Input form
        form_frame = ttk.LabelFrame(weight_tab, text="Nhập thông tin cân nặng", padding="15")
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Weight input
        weight_frame = ttk.Frame(form_frame)
        weight_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(weight_frame, text="Cân nặng (kg):", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.weight_entry = ttk.Entry(weight_frame, width=10, font=('Arial', 11))
        self.weight_entry.pack(side=tk.LEFT, padx=10)
        ttk.Label(weight_frame, text="kg").pack(side=tk.LEFT)
        
        # Date input
        date_frame = ttk.Frame(form_frame)
        date_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(date_frame, text="Ngày:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.date_entry = ttk.Entry(date_frame, width=12, font=('Arial', 11))
        self.date_entry.pack(side=tk.LEFT, padx=10)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        ttk.Button(date_frame, text="Hôm nay", 
                  command=self.set_today_date).pack(side=tk.LEFT, padx=5)
        
        # Notes input
        notes_frame = ttk.Frame(form_frame)
        notes_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(notes_frame, text="Ghi chú:", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        self.notes_entry = tk.Text(notes_frame, height=3, width=50, font=('Arial', 10))
        self.notes_entry.pack(fill=tk.X, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="📥 Lưu cân nặng", 
                  command=self.save_weight, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Làm mới", 
                  command=self.clear_weight_form).pack(side=tk.LEFT, padx=5)
        
        # Recent entries
        recent_frame = ttk.LabelFrame(weight_tab, text="Cân nặng gần đây", padding="10")
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for recent entries
        columns = ('date', 'weight', 'bmi', 'category')
        self.weight_tree = ttk.Treeview(recent_frame, columns=columns, show='headings', height=8)
        
        # Define headings
        self.weight_tree.heading('date', text='Ngày')
        self.weight_tree.heading('weight', text='Cân nặng (kg)')
        self.weight_tree.heading('bmi', text='BMI')
        self.weight_tree.heading('category', text='Phân loại')
        
        # Define columns
        self.weight_tree.column('date', width=100)
        self.weight_tree.column('weight', width=100)
        self.weight_tree.column('bmi', width=80)
        self.weight_tree.column('category', width=150)
        
        self.weight_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load recent data
        self.load_recent_weights()
    
    def setup_activity_tab(self):
        """Thiết lập tab nhập hoạt động"""
        activity_tab = ttk.Frame(self.input_notebook)
        self.input_notebook.add(activity_tab, text="🏃 Hoạt động")
        
        # Input form
        form_frame = ttk.LabelFrame(activity_tab, text="Nhập thông tin hoạt động", padding="15")
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Activity type
        type_frame = ttk.Frame(form_frame)
        type_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(type_frame, text="Loại hoạt động:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.activity_combo = ttk.Combobox(type_frame, 
                                          values=["Đi bộ", "Chạy bộ", "Đạp xe", "Bơi lội", 
                                                 "Gym", "Yoga", "Nhảy dây", "Leo cầu thang"],
                                          width=15, font=('Arial', 11))
        self.activity_combo.pack(side=tk.LEFT, padx=10)
        self.activity_combo.set("Đi bộ")
        
        # Duration
        duration_frame = ttk.Frame(form_frame)
        duration_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(duration_frame, text="Thời gian (phút):", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.duration_entry = ttk.Entry(duration_frame, width=10, font=('Arial', 11))
        self.duration_entry.pack(side=tk.LEFT, padx=10)
        self.duration_entry.insert(0, "30")
        
        # Intensity
        intensity_frame = ttk.Frame(form_frame)
        intensity_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(intensity_frame, text="Cường độ:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.intensity_combo = ttk.Combobox(intensity_frame, 
                                           values=["low", "medium", "high"],
                                           width=10, font=('Arial', 11))
        self.intensity_combo.pack(side=tk.LEFT, padx=10)
        self.intensity_combo.set("medium")
        
        # Activity date
        activity_date_frame = ttk.Frame(form_frame)
        activity_date_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(activity_date_frame, text="Ngày:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.activity_date_entry = ttk.Entry(activity_date_frame, width=12, font=('Arial', 11))
        self.activity_date_entry.pack(side=tk.LEFT, padx=10)
        self.activity_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        ttk.Button(activity_date_frame, text="Hôm nay", 
                  command=lambda: self.activity_date_entry.delete(0, tk.END) or 
                  self.activity_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))).pack(side=tk.LEFT, padx=5)
        
        # Activity notes
        activity_notes_frame = ttk.Frame(form_frame)
        activity_notes_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(activity_notes_frame, text="Ghi chú:", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        self.activity_notes_entry = tk.Text(activity_notes_frame, height=2, width=50, font=('Arial', 10))
        self.activity_notes_entry.pack(fill=tk.X, pady=5)
        
        # Buttons
        activity_button_frame = ttk.Frame(form_frame)
        activity_button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(activity_button_frame, text="💾 Lưu hoạt động", 
                  command=self.save_activity).pack(side=tk.LEFT, padx=5)
        ttk.Button(activity_button_frame, text="🔄 Làm mới", 
                  command=self.clear_activity_form).pack(side=tk.LEFT, padx=5)
        
        # Recent activities
        recent_activity_frame = ttk.LabelFrame(activity_tab, text="Hoạt động gần đây", padding="10")
        recent_activity_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for recent activities
        activity_columns = ('date', 'type', 'duration', 'calories', 'intensity')
        self.activity_tree = ttk.Treeview(recent_activity_frame, columns=activity_columns, show='headings', height=8)
        
        # Define headings
        self.activity_tree.heading('date', text='Ngày')
        self.activity_tree.heading('type', text='Loại')
        self.activity_tree.heading('duration', text='Thời gian (phút)')
        self.activity_tree.heading('calories', text='Calories')
        self.activity_tree.heading('intensity', text='Cường độ')
        
        # Define columns
        self.activity_tree.column('date', width=100)
        self.activity_tree.column('type', width=100)
        self.activity_tree.column('duration', width=100)
        self.activity_tree.column('calories', width=80)
        self.activity_tree.column('intensity', width=80)
        
        self.activity_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load recent activities
        self.load_recent_activities()
    
    def setup_sleep_tab(self):
        """Thiết lập tab nhập dữ liệu giấc ngủ"""
        sleep_tab = ttk.Frame(self.input_notebook)
        self.input_notebook.add(sleep_tab, text="😴 Giấc ngủ")
        
        # Input form
        form_frame = ttk.LabelFrame(sleep_tab, text="Nhập thông tin giấc ngủ", padding="15")
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Date input
        date_frame = ttk.Frame(form_frame)
        date_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(date_frame, text="Ngày:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.sleep_date_entry = ttk.Entry(date_frame, width=12, font=('Arial', 11))
        self.sleep_date_entry.pack(side=tk.LEFT, padx=10)
        self.sleep_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        ttk.Button(date_frame, text="Hôm nay", 
                  command=lambda: self.sleep_date_entry.delete(0, tk.END) or 
                                  self.sleep_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))).pack(side=tk.LEFT, padx=5)
        
        # Sleep hours input
        hours_frame = ttk.Frame(form_frame)
        hours_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(hours_frame, text="Số giờ ngủ:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.sleep_hours_entry = ttk.Entry(hours_frame, width=10, font=('Arial', 11))
        self.sleep_hours_entry.pack(side=tk.LEFT, padx=10)
        ttk.Label(hours_frame, text="giờ").pack(side=tk.LEFT)
        
        # Sleep quality dropdown
        quality_frame = ttk.Frame(form_frame)
        quality_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(quality_frame, text="Chất lượng giấc ngủ:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.sleep_quality_combo = ttk.Combobox(quality_frame, 
                                               values=["Rất tốt", "Tốt", "Trung bình", "Không tốt", "Rất không tốt"],
                                               width=15, font=('Arial', 10))
        self.sleep_quality_combo.pack(side=tk.LEFT, padx=10)
        self.sleep_quality_combo.set("Trung bình")
        
        # Notes input
        notes_frame = ttk.Frame(form_frame)
        notes_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(notes_frame, text="Ghi chú:", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        self.sleep_notes_entry = tk.Text(notes_frame, height=3, width=50, font=('Arial', 10))
        self.sleep_notes_entry.pack(fill=tk.X, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="📥 Lưu giấc ngủ", 
                  command=self.save_sleep, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Làm mới", 
                  command=self.clear_sleep_form).pack(side=tk.LEFT, padx=5)
        
        # Recent entries
        recent_frame = ttk.LabelFrame(sleep_tab, text="Giấc ngủ gần đây", padding="10")
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for recent sleep entries
        columns = ('date', 'hours', 'quality', 'status')
        self.sleep_tree = ttk.Treeview(recent_frame, columns=columns, show='headings', height=8)
        
        # Define headings
        self.sleep_tree.heading('date', text='Ngày')
        self.sleep_tree.heading('hours', text='Giờ ngủ')
        self.sleep_tree.heading('quality', text='Chất lượng')
        self.sleep_tree.heading('status', text='Trạng thái')
        
        # Define columns
        self.sleep_tree.column('date', width=100)
        self.sleep_tree.column('hours', width=80)
        self.sleep_tree.column('quality', width=100)
        self.sleep_tree.column('status', width=150)
        
        self.sleep_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load recent sleep records
        self.load_recent_sleep()
    
    def setup_heart_rate_tab(self):
        """Thiết lập tab nhập dữ liệu nhịp tim"""
        hr_tab = ttk.Frame(self.input_notebook)
        self.input_notebook.add(hr_tab, text="❤️ Nhịp tim")
        
        # Input form
        form_frame = ttk.LabelFrame(hr_tab, text="Nhập thông tin nhịp tim", padding="15")
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Date input
        date_frame = ttk.Frame(form_frame)
        date_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(date_frame, text="Ngày:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.hr_date_entry = ttk.Entry(date_frame, width=12, font=('Arial', 11))
        self.hr_date_entry.pack(side=tk.LEFT, padx=10)
        self.hr_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        ttk.Button(date_frame, text="Hôm nay", 
                  command=lambda: self.hr_date_entry.delete(0, tk.END) or 
                                  self.hr_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))).pack(side=tk.LEFT, padx=5)
        
        # Time input
        time_frame = ttk.Frame(form_frame)
        time_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(time_frame, text="Thời gian:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.hr_time_entry = ttk.Entry(time_frame, width=10, font=('Arial', 11))
        self.hr_time_entry.pack(side=tk.LEFT, padx=10)
        self.hr_time_entry.insert(0, datetime.now().strftime("%H:%M"))
        ttk.Button(time_frame, text="Bây giờ", 
                  command=lambda: self.hr_time_entry.delete(0, tk.END) or 
                                  self.hr_time_entry.insert(0, datetime.now().strftime("%H:%M"))).pack(side=tk.LEFT, padx=5)
        
        # Heart rate (BPM) input
        bpm_frame = ttk.Frame(form_frame)
        bpm_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(bpm_frame, text="Nhịp tim (BPM):", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.hr_bpm_entry = ttk.Entry(bpm_frame, width=10, font=('Arial', 11))
        self.hr_bpm_entry.pack(side=tk.LEFT, padx=10)
        ttk.Label(bpm_frame, text="BPM").pack(side=tk.LEFT)
        
        # Activity type dropdown
        activity_frame = ttk.Frame(form_frame)
        activity_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(activity_frame, text="Loại hoạt động:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.hr_activity_combo = ttk.Combobox(activity_frame, 
                                             values=["Nghỉ ngơi", "Nhẹ", "Vừa", "Mạnh", "Tập luyện"],
                                             width=15, font=('Arial', 10))
        self.hr_activity_combo.pack(side=tk.LEFT, padx=10)
        self.hr_activity_combo.set("Nghỉ ngơi")
        
        # Notes input
        notes_frame = ttk.Frame(form_frame)
        notes_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(notes_frame, text="Ghi chú:", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        self.hr_notes_entry = tk.Text(notes_frame, height=3, width=50, font=('Arial', 10))
        self.hr_notes_entry.pack(fill=tk.X, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="❤️ Lưu nhịp tim", 
                  command=self.save_heart_rate, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Làm mới", 
                  command=self.clear_heart_rate_form).pack(side=tk.LEFT, padx=5)
        
        # Recent entries
        recent_frame = ttk.LabelFrame(hr_tab, text="Nhịp tim gần đây", padding="10")
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for recent heart rate entries
        columns = ('date', 'time', 'bpm', 'activity', 'status')
        self.hr_tree = ttk.Treeview(recent_frame, columns=columns, show='headings', height=8)
        
        # Define headings
        self.hr_tree.heading('date', text='Ngày')
        self.hr_tree.heading('time', text='Thời gian')
        self.hr_tree.heading('bpm', text='Nhịp tim (BPM)')
        self.hr_tree.heading('activity', text='Hoạt động')
        self.hr_tree.heading('status', text='Trạng thái')
        
        # Define columns
        self.hr_tree.column('date', width=80)
        self.hr_tree.column('time', width=80)
        self.hr_tree.column('bpm', width=80)
        self.hr_tree.column('activity', width=80)
        self.hr_tree.column('status', width=120)
        
        self.hr_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load recent heart rate records
        self.load_recent_heart_rate()
    
    def setup_device_tab(self):
        """Thiết lập tab đồng bộ thiết bị"""
        device_tab = ttk.Frame(self.input_notebook)
        self.input_notebook.add(device_tab, text="📱 Thiết bị")
        
        # Device simulation section
        sim_frame = ttk.LabelFrame(device_tab, text="Giả lập Thiết bị Đo", padding="15")
        sim_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Description
        ttk.Label(sim_frame, text="Tính năng giả lập thiết bị đo sức khỏe thông minh",
                 font=('Arial', 11)).pack(anchor=tk.W, pady=5)
        
        ttk.Label(sim_frame, text="Tạo dữ liệu ngẫu nhiên để thử nghiệm ứng dụng",
                 font=('Arial', 9), foreground='gray').pack(anchor=tk.W, pady=(0, 10))
        
        # Controls
        controls_frame = ttk.Frame(sim_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(controls_frame, text="Xu hướng:", font=('Arial', 10)).pack(side=tk.LEFT)
        self.trend_combo = ttk.Combobox(controls_frame, 
                                       values=["stable", "loss", "gain"],
                                       width=10)
        self.trend_combo.pack(side=tk.LEFT, padx=10)
        self.trend_combo.set("stable")
        
        ttk.Label(controls_frame, text="Cường độ:", font=('Arial', 10)).pack(side=tk.LEFT, padx=(20, 0))
        self.sim_intensity_combo = ttk.Combobox(controls_frame, 
                                              values=["low", "medium", "high"],
                                              width=10)
        self.sim_intensity_combo.pack(side=tk.LEFT, padx=10)
        self.sim_intensity_combo.set("medium")
        
        # Buttons
        device_button_frame = ttk.Frame(sim_frame)
        device_button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(device_button_frame, text="⚖️ Tạo cân nặng", 
                  command=self.simulate_weight).pack(side=tk.LEFT, padx=5)
        ttk.Button(device_button_frame, text="🏃 Tạo hoạt động", 
                  command=self.simulate_activity).pack(side=tk.LEFT, padx=5)
        ttk.Button(device_button_frame, text="😴 Tạo giấc ngủ", 
                  command=self.simulate_sleep).pack(side=tk.LEFT, padx=5)
        ttk.Button(device_button_frame, text="❤️ Tạo nhịp tim", 
                  command=self.simulate_heart_rate).pack(side=tk.LEFT, padx=5)
        ttk.Button(device_button_frame, text="🔄 Tạo tất cả", 
                  command=self.simulate_all).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.device_status = ttk.Label(sim_frame, text="Sẵn sàng giả lập", 
                                      font=('Arial', 10), foreground='gray')
        self.device_status.pack(anchor=tk.W, pady=5)
        
        # Historical data generation
        hist_frame = ttk.LabelFrame(device_tab, text="Tạo dữ liệu Lịch sử", padding="15")
        hist_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(hist_frame, text="Tạo dữ liệu mẫu cho 30 ngày qua:",
                 font=('Arial', 10)).pack(anchor=tk.W, pady=5)
        
        hist_button_frame = ttk.Frame(hist_frame)
        hist_button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(hist_button_frame, text="📊 Tạo dữ liệu mẫu", 
                  command=self.generate_sample_data).pack(side=tk.LEFT, padx=5)
        
        self.hist_status = ttk.Label(hist_frame, text="", font=('Arial', 9))
        self.hist_status.pack(anchor=tk.W, pady=5)
    
    def set_today_date(self):
        """Đặt ngày hôm nay cho trường ngày"""
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
    
    def save_weight(self):
        """Lưu thông tin cân nặng"""
        try:
            # Get data from form
            weight_str = self.weight_entry.get().strip()
            date = self.date_entry.get().strip()
            notes = self.notes_entry.get("1.0", tk.END).strip()
            
            # Validation
            if not weight_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập cân nặng")
                return
            
            try:
                weight = float(weight_str)
            except ValueError:
                messagebox.showerror("Lỗi", "Cân nặng phải là số")
                return
            
            # Validate data
            is_valid, message = HealthDataValidator.validate_weight(weight)
            if not is_valid:
                messagebox.showerror("Lỗi", message)
                return
            
            if date:
                is_valid, message = HealthDataValidator.validate_date(date)
                if not is_valid:
                    messagebox.showerror("Lỗi", message)
                    return
            
            # Save to database
            bmi = self.db.add_weight_record(
                user_id=self.user['user_id'],
                weight=weight,
                date=date if date else None,
                notes=notes if notes else None
            )
            
            if bmi is not None:
                # Show BMI result
                from utils.bmi_calculator import BMICalculator
                category = BMICalculator.get_bmi_category(bmi)
                
                messagebox.showinfo("Thành công", 
                                  f"Đã lưu cân nặng: {weight} kg\n"
                                  f"BMI: {bmi} - {category['category']}")
                
                # Clear form
                self.weight_entry.delete(0, tk.END)
                self.notes_entry.delete("1.0", tk.END)
                
                # Refresh data
                self.load_recent_weights()
                self.main_window.refresh_all()
                self.main_window.set_status(f"Đã lưu cân nặng: {weight} kg")
                
            else:
                messagebox.showerror("Lỗi", "Không thể lưu cân nặng")
                
        except Exception as e:
            self.logger.error(f"Error saving weight: {e}")
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")
    
    def save_activity(self):
        """Lưu thông tin hoạt động"""
        try:
            # Get data from form
            activity_type = self.activity_combo.get().strip()
            duration_str = self.duration_entry.get().strip()
            intensity = self.intensity_combo.get().strip()
            date = self.activity_date_entry.get().strip()
            notes = self.activity_notes_entry.get("1.0", tk.END).strip()
            
            # Validation
            if not activity_type:
                messagebox.showerror("Lỗi", "Vui lòng chọn loại hoạt động")
                return
            
            if not duration_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập thời gian")
                return
            
            try:
                duration = int(duration_str)
            except ValueError:
                messagebox.showerror("Lỗi", "Thời gian phải là số nguyên")
                return
            
            # Validate data
            is_valid, message = HealthDataValidator.validate_activity_type(activity_type)
            if not is_valid:
                messagebox.showerror("Lỗi", message)
                return
            
            is_valid, message = HealthDataValidator.validate_activity_duration(duration)
            if not is_valid:
                messagebox.showerror("Lỗi", message)
                return
            
            if date:
                is_valid, message = HealthDataValidator.validate_date(date)
                if not is_valid:
                    messagebox.showerror("Lỗi", message)
                    return
            
            # Calculate calories (rough estimate)
            calorie_rates = {
                "Đi bộ": 5, "Chạy bộ": 10, "Đạp xe": 8, 
                "Bơi lội": 9, "Gym": 7, "Yoga": 4, 
                "Nhảy dây": 11, "Leo cầu thang": 9
            }
            base_rate = calorie_rates.get(activity_type, 5)
            
            # Adjust for intensity
            intensity_multiplier = {"low": 0.8, "medium": 1.0, "high": 1.2}
            calories_burned = round(base_rate * duration * intensity_multiplier.get(intensity, 1.0))
            
            # Save to database
            success = self.db.add_activity(
                user_id=self.user['user_id'],
                activity_type=activity_type,
                duration=duration,
                calories_burned=calories_burned,
                intensity=intensity,
                date=date if date else None,
                notes=notes if notes else None
            )
            
            if success:
                messagebox.showinfo("Thành công", 
                                  f"Đã lưu hoạt động: {activity_type}\n"
                                  f"Thời gian: {duration} phút\n"
                                  f"Calories: {calories_burned}")
                
                # Clear form
                self.duration_entry.delete(0, tk.END)
                self.duration_entry.insert(0, "30")
                self.activity_notes_entry.delete("1.0", tk.END)
                
                # Refresh data
                self.load_recent_activities()
                self.main_window.refresh_all()
                self.main_window.set_status(f"Đã lưu hoạt động: {activity_type}")
                
            else:
                messagebox.showerror("Lỗi", "Không thể lưu hoạt động")
                
        except Exception as e:
            self.logger.error(f"Error saving activity: {e}")
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")
    
    def clear_weight_form(self):
        """Xóa form nhập cân nặng"""
        self.weight_entry.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)
        self.set_today_date()
    
    def clear_activity_form(self):
        """Xóa form nhập hoạt động"""
        self.duration_entry.delete(0, tk.END)
        self.duration_entry.insert(0, "30")
        self.activity_notes_entry.delete("1.0", tk.END)
        self.activity_date_entry.delete(0, tk.END)
        self.activity_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
    
    def load_recent_weights(self):
        """Tải cân nặng gần đây"""
        # Clear existing data
        for item in self.weight_tree.get_children():
            self.weight_tree.delete(item)
        
        # Get recent weights
        weights = self.db.get_weight_records(self.user['user_id'], days=30)
        
        from utils.bmi_calculator import BMICalculator
        
        for weight_data in weights[:10]:  # Show last 10 entries
            category = BMICalculator.get_bmi_category(weight_data['bmi'])
            self.weight_tree.insert('', 'end', values=(
                weight_data['date'],
                weight_data['weight'],
                weight_data['bmi'],
                category['category']
            ))
    
    def load_recent_activities(self):
        """Tải hoạt động gần đây"""
        # Clear existing data
        for item in self.activity_tree.get_children():
            self.activity_tree.delete(item)
        
        # Get recent activities
        activities = self.db.get_activities(self.user['user_id'], days=30)
        
        for activity in activities[:10]:  # Show last 10 entries
            self.activity_tree.insert('', 'end', values=(
                activity['date'],
                activity['activity_type'],
                activity['duration'],
                activity['calories_burned'] or '--',
                activity['intensity'] or 'medium'
            ))
    
    def simulate_weight(self):
        """Giả lập dữ liệu cân nặng"""
        try:
            trend = self.trend_combo.get()
            measurement = self.device_simulator.generate_weight_measurement(trend)
            
            # Save to database
            bmi = self.db.add_weight_record(
                user_id=self.user['user_id'],
                weight=measurement['weight']
            )
            
            if bmi:
                self.device_status.config(
                    text=f"Đã tạo cân nặng: {measurement['weight']} kg {measurement['trend']}",
                    foreground='green'
                )
                self.load_recent_weights()
                self.main_window.refresh_all()
            else:
                self.device_status.config(text="Lỗi khi lưu cân nặng", foreground='red')
                
        except Exception as e:
            self.logger.error(f"Error simulating weight: {e}")
            self.device_status.config(text=f"Lỗi: {e}", foreground='red')
    
    def simulate_activity(self):
        """Giả lập dữ liệu hoạt động"""
        try:
            self.device_simulator.set_activity_intensity(self.sim_intensity_combo.get())
            activity_data = self.device_simulator.generate_activity_data()
            
            # Save to database
            success = self.db.add_activity(
                user_id=self.user['user_id'],
                activity_type=activity_data['activity_type'],
                duration=activity_data['duration'],
                calories_burned=activity_data['calories_burned'],
                intensity=activity_data['intensity']
            )
            
            if success:
                self.device_status.config(
                    text=f"Đã tạo hoạt động: {activity_data['activity_type']} - {activity_data['duration']} phút",
                    foreground='green'
                )
                self.load_recent_activities()
                self.main_window.refresh_all()
            else:
                self.device_status.config(text="Lỗi khi lưu hoạt động", foreground='red')
                
        except Exception as e:
            self.logger.error(f"Error simulating activity: {e}")
            self.device_status.config(text=f"Lỗi: {e}", foreground='red')
    
    def simulate_sleep(self):
        """Giả lập dữ liệu giấc ngủ"""
        try:
            sleep_data = self.device_simulator.generate_sleep_data()
            
            # Map quality to Vietnamese
            quality_map = {
                'poor': 'Rất không tốt',
                'fair': 'Không tốt',
                'good': 'Tốt',
                'excellent': 'Rất tốt'
            }
            sleep_quality = quality_map.get(sleep_data['sleep_quality'], 'Trung bình')
            
            # Save to database
            success = self.db.add_sleep_record(
                user_id=self.user['user_id'],
                record_date=datetime.now().strftime("%Y-%m-%d"),
                sleep_hours=sleep_data['sleep_hours'],
                sleep_quality=sleep_quality,
                notes=f"Giả lập - Ngủ sâu: {sleep_data['deep_sleep_hours']}h, REM: {sleep_data['rem_sleep_hours']}h"
            )
            
            if success:
                self.device_status.config(
                    text=f"Đã tạo giấc ngủ: {sleep_data['sleep_hours']:.1f} giờ - {sleep_quality}",
                    foreground='green'
                )
                self.load_recent_sleep()
                self.main_window.refresh_all()
            else:
                self.device_status.config(text="Lỗi khi lưu giấc ngủ", foreground='red')
                
        except Exception as e:
            self.logger.error(f"Error simulating sleep: {e}")
            self.device_status.config(text=f"Lỗi: {e}", foreground='red')
    
    def simulate_heart_rate(self):
        """Giả lập dữ liệu nhịp tim"""
        try:
            hr_data = self.device_simulator.generate_heart_rate_data()
            
            # Save to database
            success = self.db.add_heart_rate_record(
                user_id=self.user['user_id'],
                record_date=datetime.now().strftime("%Y-%m-%d"),
                record_time=datetime.now().strftime("%H:%M"),
                bpm=hr_data['resting_heart_rate'],
                activity_type='Nghỉ ngơi',
                notes=f"Giả lập - BPM tối đa: {hr_data['max_heart_rate']}, Bình thường: {hr_data['average_heart_rate']}"
            )
            
            if success:
                self.device_status.config(
                    text=f"Đã tạo nhịp tim: {hr_data['resting_heart_rate']} BPM",
                    foreground='green'
                )
                self.load_recent_heart_rate()
                self.main_window.refresh_all()
            else:
                self.device_status.config(text="Lỗi khi lưu nhịp tim", foreground='red')
                
        except Exception as e:
            self.logger.error(f"Error simulating heart rate: {e}")
            self.device_status.config(text=f"Lỗi: {e}", foreground='red')
    
    def simulate_all(self):
        """Giả lập cả cân nặng và hoạt động"""
        self.simulate_weight()
        self.simulate_activity()
        self.simulate_sleep()
        self.simulate_heart_rate()
    
    def generate_sample_data(self):
        """Tạo dữ liệu mẫu"""
        try:
            historical_data = self.device_simulator.generate_historical_data(days=30)
            
            saved_count = 0
            for day_data in historical_data:
                # Save weight
                weight_bmi = self.db.add_weight_record(
                    user_id=self.user['user_id'],
                    weight=day_data['weight_data']['weight'],
                    date=day_data['date']
                )
                
                # Save activity if exists
                if day_data['activity_data']:
                    activity_success = self.db.add_activity(
                        user_id=self.user['user_id'],
                        activity_type=day_data['activity_data']['activity_type'],
                        duration=day_data['activity_data']['duration'],
                        calories_burned=day_data['activity_data']['calories_burned'],
                        intensity=day_data['activity_data']['intensity'],
                        date=day_data['date']
                    )
                    if activity_success:
                        saved_count += 1
                
                if weight_bmi:
                    saved_count += 1
            
            self.hist_status.config(
                text=f"Đã tạo {saved_count} bản ghi dữ liệu mẫu cho 30 ngày",
                foreground='green'
            )
            
            # Refresh data
            self.load_recent_weights()
            self.load_recent_activities()
            self.main_window.refresh_all()
            
        except Exception as e:
            self.logger.error(f"Error generating sample data: {e}")
            self.hist_status.config(text=f"Lỗi: {e}", foreground='red')
    
    def save_sleep(self):
        """Lưu thông tin giấc ngủ"""
        try:
            # Get data from form
            sleep_hours_str = self.sleep_hours_entry.get().strip()
            quality = self.sleep_quality_combo.get().strip()
            date = self.sleep_date_entry.get().strip()
            notes = self.sleep_notes_entry.get("1.0", tk.END).strip()
            
            # Validation
            if not sleep_hours_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập số giờ ngủ")
                return
            
            try:
                sleep_hours = float(sleep_hours_str)
            except ValueError:
                messagebox.showerror("Lỗi", "Số giờ ngủ phải là số")
                return
            
            if sleep_hours < 0 or sleep_hours > 24:
                messagebox.showerror("Lỗi", "Số giờ ngủ phải từ 0 đến 24")
                return
            
            if not quality:
                messagebox.showerror("Lỗi", "Vui lòng chọn chất lượng giấc ngủ")
                return
            
            # Save to database
            success = self.db.add_sleep_record(
                user_id=self.user['user_id'],
                record_date=date if date else datetime.now().strftime("%Y-%m-%d"),
                sleep_hours=sleep_hours,
                sleep_quality=quality,
                notes=notes
            )
            
            if success:
                messagebox.showinfo("Thành công", 
                                  f"Đã lưu giấc ngủ: {sleep_hours} giờ\n"
                                  f"Chất lượng: {quality}")
                
                # Clear form
                self.clear_sleep_form()
                
                # Refresh data
                self.load_recent_sleep()
                self.main_window.refresh_all()
                self.main_window.set_status(f"Đã lưu giấc ngủ: {sleep_hours} giờ")
                
            else:
                messagebox.showerror("Lỗi", "Không thể lưu giấc ngủ")
                
        except Exception as e:
            self.logger.error(f"Error saving sleep: {e}")
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")
    
    def save_heart_rate(self):
        """Lưu thông tin nhịp tim"""
        try:
            # Get data from form
            bpm_str = self.hr_bpm_entry.get().strip()
            activity = self.hr_activity_combo.get().strip()
            date = self.hr_date_entry.get().strip()
            time = self.hr_time_entry.get().strip()
            notes = self.hr_notes_entry.get("1.0", tk.END).strip()
            
            # Validation
            if not bpm_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập nhịp tim")
                return
            
            try:
                bpm = int(bpm_str)
            except ValueError:
                messagebox.showerror("Lỗi", "Nhịp tim phải là số nguyên")
                return
            
            if bpm < 30 or bpm > 200:
                messagebox.showerror("Lỗi", "Nhịp tim phải từ 30 đến 200 BPM")
                return
            
            if not activity:
                messagebox.showerror("Lỗi", "Vui lòng chọn loại hoạt động")
                return
            
            # Save to database
            success = self.db.add_heart_rate_record(
                user_id=self.user['user_id'],
                record_date=date if date else datetime.now().strftime("%Y-%m-%d"),
                record_time=time if time else datetime.now().strftime("%H:%M"),
                bpm=bpm,
                activity_type=activity,
                notes=notes
            )
            
            if success:
                messagebox.showinfo("Thành công", 
                                  f"Đã lưu nhịp tim: {bpm} BPM\n"
                                  f"Hoạt động: {activity}")
                
                # Clear form
                self.clear_heart_rate_form()
                
                # Refresh data
                self.load_recent_heart_rate()
                self.main_window.refresh_all()
                self.main_window.set_status(f"Đã lưu nhịp tim: {bpm} BPM")
                
            else:
                messagebox.showerror("Lỗi", "Không thể lưu nhịp tim")
                
        except Exception as e:
            self.logger.error(f"Error saving heart rate: {e}")
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")
    
    def clear_sleep_form(self):
        """Xóa dữ liệu form giấc ngủ"""
        self.sleep_hours_entry.delete(0, tk.END)
        self.sleep_notes_entry.delete("1.0", tk.END)
        self.sleep_date_entry.delete(0, tk.END)
        self.sleep_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.sleep_quality_combo.set("Trung bình")
    
    def clear_heart_rate_form(self):
        """Xóa dữ liệu form nhịp tim"""
        self.hr_bpm_entry.delete(0, tk.END)
        self.hr_notes_entry.delete("1.0", tk.END)
        self.hr_date_entry.delete(0, tk.END)
        self.hr_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.hr_time_entry.delete(0, tk.END)
        self.hr_time_entry.insert(0, datetime.now().strftime("%H:%M"))
        self.hr_activity_combo.set("Nghỉ ngơi")
    
    def load_recent_sleep(self):
        """Tải danh sách giấc ngủ gần đây"""
        try:
            # Clear treeview
            for item in self.sleep_tree.get_children():
                self.sleep_tree.delete(item)
            
            # Load records from database
            records = self.db.get_sleep_records(self.user['user_id'], days=30)
            
            for record in records:
                from models.sleep import SleepRecord
                
                # Get health status
                sleep_rec = SleepRecord(
                    user_id=record['user_id'],
                    record_date=record['record_date'],
                    sleep_hours=record['sleep_hours'],
                    sleep_quality=record['sleep_quality']
                )
                status = sleep_rec.get_health_status()
                
                self.sleep_tree.insert('', 'end', values=(
                    record['record_date'],
                    f"{record['sleep_hours']:.1f}h",
                    record['sleep_quality'],
                    status
                ))
                
        except Exception as e:
            self.logger.error(f"Error loading recent sleep: {e}")
    
    def load_recent_heart_rate(self):
        """Tải danh sách nhịp tim gần đây"""
        try:
            # Clear treeview
            for item in self.hr_tree.get_children():
                self.hr_tree.delete(item)
            
            # Load records from database
            records = self.db.get_heart_rate_records(self.user['user_id'], days=30)
            
            for record in records:
                from models.heart_rate import HeartRateRecord
                
                # Get health status
                hr_rec = HeartRateRecord(
                    user_id=record['user_id'],
                    record_date=record['record_date'],
                    record_time=record['record_time'],
                    bpm=record['bpm'],
                    activity_type=record['activity_type']
                )
                status = hr_rec.get_health_status()
                
                self.hr_tree.insert('', 'end', values=(
                    record['record_date'],
                    record['record_time'],
                    f"{record['bpm']} BPM",
                    record['activity_type'],
                    status
                ))
                
        except Exception as e:
            self.logger.error(f"Error loading recent heart rate: {e}")

            self.hist_status.config(text=f"Lỗi: {e}", foreground='red')