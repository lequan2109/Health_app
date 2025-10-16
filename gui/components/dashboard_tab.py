# gui/components/dashboard_tab.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import logging
from utils.bmi_calculator import BMICalculator
from utils.alert_system import AlertSystem

class DashboardTab:
    """Tab tổng quan dashboard"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.db = main_window.db
        self.user = main_window.user
        self.alert_system = main_window.alert_system
        self.logger = logging.getLogger(__name__)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        self.frame = ttk.Frame(self.parent)
        
        # Create scrollable frame
        self.canvas = tk.Canvas(self.frame, bg='#f5f5f5')
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Setup content
        self.setup_content()
    
    def _on_mousewheel(self, event):
        """Xử lý sự kiện cuộn chuột"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def setup_content(self):
        """Thiết lập nội dung dashboard"""
        # Welcome section
        self.setup_welcome_section()
        
        # Alerts section
        self.setup_alerts_section()
        
        # Current stats section
        self.setup_stats_section()
        
        # BMI info section
        self.setup_bmi_section()
        
        # Recent activity section
        self.setup_activity_section()
        
        # Goals section
        self.setup_goals_section()
    
    def setup_welcome_section(self):
        """Thiết lập phần chào mừng"""
        welcome_frame = ttk.LabelFrame(self.scrollable_frame, text="👋 Chào mừng", padding="15")
        welcome_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(welcome_frame, text=f"Xin chào {self.user['full_name']}!",
                 font=('Arial', 14, 'bold')).pack(anchor=tk.W)
        
        ttk.Label(welcome_frame, 
                 text="Theo dõi sức khỏe của bạn một cách thông minh và hiệu quả",
                 font=('Arial', 10)).pack(anchor=tk.W, pady=(5, 0))
        
        # Current date
        current_date = datetime.now().strftime("%d/%m/%Y")
        ttk.Label(welcome_frame, text=f"Hôm nay: {current_date}",
                 font=('Arial', 9), foreground='gray').pack(anchor=tk.W, pady=(10, 0))
    
    def setup_alerts_section(self):
        """Thiết lập phần cảnh báo"""
        self.alerts_frame = ttk.LabelFrame(self.scrollable_frame, text="⚠️ Cảnh báo & Đề xuất", padding="15")
        self.alerts_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.alerts_content = ttk.Frame(self.alerts_frame)
        self.alerts_content.pack(fill=tk.X)
        
        # Default message
        ttk.Label(self.alerts_content, text="Đang tải cảnh báo...",
                 font=('Arial', 10), foreground='gray').pack(pady=10)
    
    def setup_stats_section(self):
        """Thiết lập phần thống kê hiện tại"""
        self.stats_frame = ttk.LabelFrame(self.scrollable_frame, text="📈 Thống kê Hiện tại", padding="15")
        self.stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create stats grid
        stats_grid = ttk.Frame(self.stats_frame)
        stats_grid.pack(fill=tk.X)
        
        # Stats will be populated in refresh_data()
        self.stats_labels = {}
        
        # Weight stat
        weight_frame = ttk.Frame(stats_grid)
        weight_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ttk.Label(weight_frame, text="Cân nặng:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.stats_labels['weight'] = ttk.Label(weight_frame, text="-- kg", 
                                              font=('Arial', 12), foreground='#2c3e50')
        self.stats_labels['weight'].pack(anchor=tk.W)
        
        # BMI stat
        bmi_frame = ttk.Frame(stats_grid)
        bmi_frame.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ttk.Label(bmi_frame, text="Chỉ số BMI:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.stats_labels['bmi'] = ttk.Label(bmi_frame, text="--", 
                                           font=('Arial', 12), foreground='#2c3e50')
        self.stats_labels['bmi'].pack(anchor=tk.W)
        
        # Weekly activity
        activity_frame = ttk.Frame(stats_grid)
        activity_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        ttk.Label(activity_frame, text="Hoạt động tuần:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.stats_labels['activity'] = ttk.Label(activity_frame, text="-- phút", 
                                                font=('Arial', 12), foreground='#2c3e50')
        self.stats_labels['activity'].pack(anchor=tk.W)
        
        # Last update
        update_frame = ttk.Frame(stats_grid)
        update_frame.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ttk.Label(update_frame, text="Cập nhật:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.stats_labels['last_update'] = ttk.Label(update_frame, text="--", 
                                                   font=('Arial', 10), foreground='gray')
        self.stats_labels['last_update'].pack(anchor=tk.W)
    
    def setup_bmi_section(self):
        """Thiết lập phần thông tin BMI"""
        self.bmi_frame = ttk.LabelFrame(self.scrollable_frame, text="🎯 Chỉ số BMI", padding="15")
        self.bmi_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.bmi_content = ttk.Frame(self.bmi_frame)
        self.bmi_content.pack(fill=tk.X)
        
        # Default message
        ttk.Label(self.bmi_content, text="Chưa có đủ dữ liệu để tính BMI",
                 font=('Arial', 10), foreground='gray').pack(pady=10)
    
    def setup_activity_section(self):
        """Thiết lập phần hoạt động gần đây"""
        self.activity_frame = ttk.LabelFrame(self.scrollable_frame, text="🏃 Hoạt động Gần đây", padding="15")
        self.activity_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.activity_content = ttk.Frame(self.activity_frame)
        self.activity_content.pack(fill=tk.X)
        
        # Default message
        ttk.Label(self.activity_content, text="Chưa có hoạt động nào được ghi nhận",
                 font=('Arial', 10), foreground='gray').pack(pady=10)
    
    def setup_goals_section(self):
        """Thiết lập phần mục tiêu"""
        goals_frame = ttk.LabelFrame(self.scrollable_frame, text="🎯 Mục tiêu Sức khỏe", padding="15")
        goals_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Goal items
        goals = [
            ("🎯", "Theo dõi cân nặng hàng ngày"),
            ("🏃", "Hoạt động thể chất 150 phút/tuần"),
            ("📊", "Duy trì BMI trong khoảng 18.5-23"),
            ("💧", "Uống đủ nước mỗi ngày"),
            ("😴", "Ngủ đủ 7-8 tiếng mỗi đêm")
        ]
        
        for icon, goal in goals:
            goal_frame = ttk.Frame(goals_frame)
            goal_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(goal_frame, text=icon, font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Label(goal_frame, text=goal, font=('Arial', 10)).pack(side=tk.LEFT)
    
    def refresh_data(self):
        """Làm mới dữ liệu dashboard"""
        try:
            self.update_stats()
            self.update_alerts()
            self.update_bmi_info()
            self.update_recent_activity()
            self.logger.info("Dashboard data refreshed")
        except Exception as e:
            self.logger.error(f"Error refreshing dashboard: {e}")
            self.main_window.show_alert("Lỗi", f"Không thể làm mới dashboard: {e}", "error")
    
    def update_stats(self):
        """Cập nhật thống kê"""
        current_weight = self.db.get_current_weight(self.user['user_id'])
        weekly_activity = self.db.get_weekly_activity_minutes(self.user['user_id'])
        
        if current_weight:
            from utils.bmi_calculator import BMICalculator
            height_m = self.user['height'] / 100
            bmi = BMICalculator.calculate_bmi(current_weight, height_m)
            
            self.stats_labels['weight'].config(text=f"{current_weight} kg")
            self.stats_labels['bmi'].config(text=f"{bmi}")
            
            # Color code BMI
            category = BMICalculator.get_bmi_category(bmi)
            self.stats_labels['bmi'].config(foreground=category['color'])
        else:
            self.stats_labels['weight'].config(text="Chưa có dữ liệu")
            self.stats_labels['bmi'].config(text="--")
        
        self.stats_labels['activity'].config(text=f"{weekly_activity} phút")
        
        # Update last update time
        last_update = datetime.now().strftime("%H:%M %d/%m")
        self.stats_labels['last_update'].config(text=last_update)
    
    def update_alerts(self):
        """Cập nhật cảnh báo"""
        # Clear existing alerts
        for widget in self.alerts_content.winfo_children():
            widget.destroy()
        
        # Get current data for alerts
        current_weight = self.db.get_current_weight(self.user['user_id'])
        current_bmi = None
        
        if current_weight:
            from utils.bmi_calculator import BMICalculator
            height_m = self.user['height'] / 100
            current_bmi = BMICalculator.calculate_bmi(current_weight, height_m)
        
        # Get alerts
        alerts = self.alert_system.get_all_alerts(
            self.user['user_id'], current_weight, current_bmi
        )
        
        if not alerts:
            ttk.Label(self.alerts_content, text="✅ Không có cảnh báo nào",
                     font=('Arial', 10), foreground='green').pack(pady=10)
            return
        
        # Display alerts
        for alert in alerts:
            alert_frame = ttk.Frame(self.alerts_content, relief=tk.GROOVE, borderwidth=1)
            alert_frame.pack(fill=tk.X, pady=2, padx=5)
            
            # Alert icon and message
            icon_label = ttk.Label(alert_frame, text=alert.get('icon', '⚠️'), 
                                 font=('Arial', 14))
            icon_label.pack(side=tk.LEFT, padx=5, pady=5)
            
            message_label = ttk.Label(alert_frame, text=alert['message'], 
                                    font=('Arial', 10), wraplength=800, justify=tk.LEFT)
            message_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
            
            # Color code by level
            colors = {
                'critical': '#ff4444',
                'danger': '#ff6b6b', 
                'warning': '#ffa726',
                'info': '#42a5f5',
                'success': '#66bb6a'
            }
            message_label.config(foreground=colors.get(alert['level'], 'black'))
    
    def update_bmi_info(self):
        """Cập nhật thông tin BMI"""
        # Clear existing content
        for widget in self.bmi_content.winfo_children():
            widget.destroy()
        
        current_weight = self.db.get_current_weight(self.user['user_id'])
        
        if not current_weight:
            ttk.Label(self.bmi_content, text="Chưa có đủ dữ liệu để tính BMI",
                     font=('Arial', 10), foreground='gray').pack(pady=10)
            return
        
        from utils.bmi_calculator import BMICalculator
        height_m = self.user['height'] / 100
        bmi = BMICalculator.calculate_bmi(current_weight, height_m)
        category = BMICalculator.get_bmi_category(bmi)
        recommendations = BMICalculator.get_health_recommendations(bmi)
        ideal_range = BMICalculator.calculate_ideal_weight_range(height_m)
        
        # BMI value and category
        bmi_frame = ttk.Frame(self.bmi_content)
        bmi_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(bmi_frame, text=f"Chỉ số BMI: ", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        ttk.Label(bmi_frame, text=f"{bmi}", font=('Arial', 11, 'bold'),
                 foreground=category['color']).pack(side=tk.LEFT)
        ttk.Label(bmi_frame, text=f" - {category['category']}", font=('Arial', 11),
                 foreground=category['color']).pack(side=tk.LEFT)
        
        # Risk level
        ttk.Label(self.bmi_content, text=f"Mức độ nguy cơ: {category['risk']}",
                 font=('Arial', 10)).pack(anchor=tk.W, pady=2)
        
        # Ideal weight range
        ttk.Label(self.bmi_content, 
                 text=f"Cân nặng lý tưởng: {ideal_range['min']} - {ideal_range['max']} kg (BMI {ideal_range['bmi_range']})",
                 font=('Arial', 10)).pack(anchor=tk.W, pady=2)
        
        # Recommendations
        ttk.Label(self.bmi_content, text="Đề xuất:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 5))
        
        for recommendation in recommendations[:3]:  # Show first 3 recommendations
            rec_frame = ttk.Frame(self.bmi_content)
            rec_frame.pack(fill=tk.X, pady=1)
            ttk.Label(rec_frame, text="• ", font=('Arial', 9)).pack(side=tk.LEFT)
            ttk.Label(rec_frame, text=recommendation, font=('Arial', 9),
                     wraplength=800, justify=tk.LEFT).pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def update_recent_activity(self):
        """Cập nhật hoạt động gần đây"""
        # Clear existing content
        for widget in self.activity_content.winfo_children():
            widget.destroy()
        
        activities = self.db.get_activities(self.user['user_id'], days=7)
        
        if not activities:
            ttk.Label(self.activity_content, text="Chưa có hoạt động nào trong 7 ngày qua",
                     font=('Arial', 10), foreground='gray').pack(pady=10)
            return
        
        # Show last 5 activities
        for activity in activities[:5]:
            activity_frame = ttk.Frame(self.activity_content, relief=tk.GROOVE, borderwidth=1)
            activity_frame.pack(fill=tk.X, pady=2, padx=5)
            
            # Activity info
            info_text = f"{activity['activity_type']} - {activity['duration']} phút"
            if activity['calories_burned']:
                info_text += f" - {activity['calories_burned']} cal"
            
            ttk.Label(activity_frame, text=info_text, font=('Arial', 10)).pack(side=tk.LEFT, padx=5, pady=5)
            ttk.Label(activity_frame, text=activity['date'], font=('Arial', 9), 
                     foreground='gray').pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Show total for week
        total_duration = sum(act['duration'] for act in activities)
        total_frame = ttk.Frame(self.activity_content)
        total_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(total_frame, text=f"Tổng tuần: {total_duration} phút", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        # Compare to WHO recommendation
        if total_duration >= 150:
            status_text = "✅ Đạt mục tiêu WHO"
            color = "green"
        else:
            status_text = f"⚠️ Còn {150 - total_duration} phút để đạt mục tiêu"
            color = "orange"
        
        ttk.Label(total_frame, text=status_text, font=('Arial', 10),
                 foreground=color).pack(side=tk.RIGHT)