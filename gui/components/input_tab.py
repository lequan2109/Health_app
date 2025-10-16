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
    
    def simulate_all(self):
        """Giả lập cả cân nặng và hoạt động"""
        self.simulate_weight()
        self.simulate_activity()
    
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