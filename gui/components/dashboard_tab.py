# gui/components/dashboard_tab.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import logging

class DashboardTab:
    """Tab tổng quan dashboard (Giao diện thu gọn)"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.db = main_window.db
        self.user = main_window.user
        self.alert_system = main_window.alert_system
        self.logger = logging.getLogger(__name__)
        
        # Lưu trạng thái đóng/mở của các section
        self.sections = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        self.frame = ttk.Frame(self.parent)
        
        # Tạo frame cuộn (Scrollable frame)
        self.canvas = tk.Canvas(self.frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, padding="5")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=880)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        
        # Setup content
        self.setup_content()
    
    def _on_mousewheel(self, event):
        """Xử lý sự kiện cuộn chuột"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_collapsible_section(self, title, setup_content_func, icon="▶"):
        """
        Tạo một section có thể đóng mở
        Args:
            title: Tiêu đề nút
            setup_content_func: Hàm callback để vẽ nội dung bên trong
            icon: Icon mặc định
        """
        # Container cho cả nút và nội dung
        section_container = ttk.Frame(self.scrollable_frame)
        section_container.pack(fill=tk.X, padx=5, pady=3)
        
        # Biến lưu trạng thái (False = đang đóng)
        is_expanded = tk.BooleanVar(value=False)
        
        # Frame nội dung (Ban đầu ẩn đi)
        content_frame = ttk.Frame(section_container)
        
        # Hàm toggle
        def toggle():
            if is_expanded.get():
                # Đang mở -> Đóng lại
                content_frame.pack_forget()
                toggle_btn.configure(text=f"▶ {title}")
                is_expanded.set(False)
            else:
                # Đang đóng -> Mở ra
                content_frame.pack(fill=tk.X, expand=True, padx=(15, 5), pady=(8, 10))
                toggle_btn.configure(text=f"▼ {title}")
                is_expanded.set(True)
        
        # Tạo style cho nút section
        style = ttk.Style()
        style.configure('Section.TButton', 
                       font=('Arial', 11, 'bold'),
                       padding=(10, 8),
                       relief="flat",
                       background='#e9ecef',
                       foreground='#495057')
        
        toggle_btn = ttk.Button(
            section_container, 
            text=f"{icon} {title}", 
            command=toggle,
            style='Section.TButton',
            width=25
        )
        toggle_btn.pack(fill=tk.X)
        
        # Thêm hiệu ứng hover
        def on_enter(e):
            toggle_btn.configure(style='SectionHover.TButton')
        def on_leave(e):
            toggle_btn.configure(style='Section.TButton')
            
        toggle_btn.bind("<Enter>", on_enter)
        toggle_btn.bind("<Leave>", on_leave)
        
        # Tạo style hover
        style.configure('SectionHover.TButton', 
                       font=('Arial', 11, 'bold'),
                       padding=(10, 8),
                       relief="flat",
                       background='#dee2e6',
                       foreground='#212529')
        
        # Gọi hàm setup nội dung truyền vào frame con
        setup_content_func(content_frame)
        
        return content_frame

    def setup_content(self):
        """Thiết lập toàn bộ nội dung"""
        # 1. Phần Chào mừng (Luôn hiện)
        self.setup_welcome_section()
        
        # Separator đẹp hơn
        separator = ttk.Separator(self.scrollable_frame, orient='horizontal')
        separator.pack(fill='x', padx=20, pady=15)
        
        # 2. Các nút chức năng (Đóng/Mở)
        
        # Nút: Cảnh báo và Đề xuất
        self.create_collapsible_section("🚨 Cảnh báo và Đề xuất", self.setup_alerts_content)
        
        # Nút: Thống kê
        self.create_collapsible_section("📊 Thống kê chỉ số", self.setup_stats_content)
        
        # Nút: Chỉ số BMI
        self.create_collapsible_section("⚖️ Chỉ số BMI chi tiết", self.setup_bmi_content)
        
        # Nút: Hoạt động gần đây
        self.create_collapsible_section("🏃 Hoạt động gần đây", self.setup_activity_content)
        
        # Nút: Giấc ngủ
        self.create_collapsible_section("😴 Giấc ngủ", self.setup_sleep_content)
        
        # Nút: Nhịp tim
        self.create_collapsible_section("❤️ Nhịp tim", self.setup_heart_rate_content)
        
        # Nút: Mục tiêu sức khỏe
        self.create_collapsible_section("🎯 Mục tiêu sức khỏe", self.setup_goals_content)

    def setup_welcome_section(self):
        """Thiết lập phần chào mừng (Giữ nguyên hiển thị)"""
        welcome_frame = ttk.Frame(self.scrollable_frame, padding="20 15")
        welcome_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Background màu nhẹ
        style = ttk.Style()
        style.configure('Welcome.TFrame', background='#e3f2fd')
        welcome_frame.configure(style='Welcome.TFrame')
        
        # Avatar và thông tin
        main_info_frame = ttk.Frame(welcome_frame, style='Welcome.TFrame')
        main_info_frame.pack(fill=tk.X)
        
        # Avatar placeholder
        avatar_frame = ttk.Frame(main_info_frame, style='Welcome.TFrame')
        avatar_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        avatar_label = ttk.Label(avatar_frame, text="👤", font=('Arial', 24), 
                               background='#e3f2fd')
        avatar_label.pack()
        
        # Thông tin chính
        info_frame = ttk.Frame(main_info_frame, style='Welcome.TFrame')
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(info_frame, text=f"Xin chào {self.user['full_name']}!",
                 font=('Arial', 18, 'bold'), background='#e3f2fd',
                 foreground='#1565c0').pack(anchor=tk.W)
        
        ttk.Label(info_frame, 
                 text="Chọn các mục bên dưới để xem chi tiết sức khỏe của bạn.",
                 font=('Arial', 11), background='#e3f2fd',
                 foreground='#546e7a').pack(anchor=tk.W, pady=(2, 0))
        
        current_date = datetime.now().strftime("%A, %d/%m/%Y")
        ttk.Label(info_frame, text=f"📅 {current_date}",
                 font=('Arial', 10), background='#e3f2fd',
                 foreground='#78909c').pack(anchor=tk.W, pady=(8, 0))

    def setup_alerts_content(self, parent):
        """Nội dung phần cảnh báo"""
        # Container cho alerts
        self.alerts_content = ttk.Frame(parent)
        self.alerts_content.pack(fill=tk.X)
        
        # Default message với styling đẹp hơn
        loading_frame = ttk.Frame(self.alerts_content)
        loading_frame.pack(fill=tk.X, pady=15)
        
        ttk.Label(loading_frame, text="⏳ Đang tải cảnh báo...",
                 font=('Arial', 11), foreground='#78909c',
                 justify=tk.CENTER).pack(fill=tk.X)

    def setup_stats_content(self, parent):
        """Nội dung phần thống kê"""
        # Frame chính với border nhẹ
        stats_frame = ttk.Frame(parent, relief=tk.RAISED, borderwidth=1)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Tiêu đề
        title_frame = ttk.Frame(stats_frame)
        title_frame.pack(fill=tk.X, padx=15, pady=(12, 8))
        ttk.Label(title_frame, text="📈 Tổng quan nhanh", 
                 font=('Arial', 12, 'bold'), foreground='#2c3e50').pack(anchor=tk.W)
        
        # Lưới hiển thị thống kê
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X, padx=10, pady=(0, 12))
        
        self.stats_labels = {}
        
        # Tạo 4 ô thống kê
        stats_data = [
            ("⚖️ Cân nặng", "weight", "-- kg", 0, 0),
            ("📊 Chỉ số BMI", "bmi", "--", 0, 1),
            ("🏃 Hoạt động tuần", "activity", "-- phút", 1, 0),
            ("🕒 Cập nhật", "last_update", "--", 1, 1)
        ]
        
        for icon, key, default_value, row, col in stats_data:
            stat_frame = ttk.Frame(stats_grid, relief=tk.GROOVE, borderwidth=1)
            stat_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            stat_frame.columnconfigure(0, weight=1)
            
            # Icon và label
            ttk.Label(stat_frame, text=icon, font=('Arial', 14),
                     foreground='#5d6d7e').pack(pady=(8, 2))
            
            ttk.Label(stat_frame, text=key.replace('_', ' ').title(), 
                     font=('Arial', 9), foreground='#7f8c8d').pack()
            
            self.stats_labels[key] = ttk.Label(stat_frame, text=default_value, 
                                             font=('Arial', 13, 'bold'), 
                                             foreground='#2c3e50')
            self.stats_labels[key].pack(pady=(2, 8))
        
        # Cấu hình grid để căn đều
        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)

    def setup_bmi_content(self, parent):
        """Nội dung phần BMI"""
        self.bmi_content = ttk.Frame(parent)
        self.bmi_content.pack(fill=tk.X)
        
        # Default message với styling đẹp hơn
        empty_frame = ttk.Frame(self.bmi_content)
        empty_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(empty_frame, text="📋 Chưa có đủ dữ liệu để tính BMI",
                 font=('Arial', 11), foreground='#95a5a6',
                 justify=tk.CENTER).pack(fill=tk.X)
        
        ttk.Label(empty_frame, text="Hãy thêm thông tin cân nặng để xem phân tích BMI",
                 font=('Arial', 9), foreground='#bdc3c7',
                 justify=tk.CENTER).pack(fill=tk.X, pady=(5, 0))

    def setup_activity_content(self, parent):
        """Nội dung phần hoạt động"""
        self.activity_content = ttk.Frame(parent)
        self.activity_content.pack(fill=tk.X)
        
        # Default message với styling đẹp hơn
        empty_frame = ttk.Frame(self.activity_content)
        empty_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(empty_frame, text="🏃 Chưa có hoạt động nào được ghi nhận",
                 font=('Arial', 11), foreground='#95a5a6',
                 justify=tk.CENTER).pack(fill=tk.X)
        
        ttk.Label(empty_frame, text="Hãy thêm hoạt động thể chất để theo dõi tiến độ",
                 font=('Arial', 9), foreground='#bdc3c7',
                 justify=tk.CENTER).pack(fill=tk.X, pady=(5, 0))

    def setup_goals_content(self, parent):
        """Nội dung phần mục tiêu"""
        goals_frame = ttk.Frame(parent)
        goals_frame.pack(fill=tk.X)
        
        goals = [
            ("🎯", "Theo dõi cân nặng hàng ngày", "#e74c3c"),
            ("🏃", "Hoạt động thể chất 150 phút/tuần", "#3498db"),
            ("📊", "Duy trì BMI trong khoảng 18.5-23", "#2ecc71"),
            ("💧", "Uống đủ nước mỗi ngày", "#3498db"),
            ("😴", "Ngủ đủ 7-8 tiếng mỗi đêm", "#9b59b6")
        ]
        
        for icon, goal, color in goals:
            goal_frame = ttk.Frame(goals_frame, relief=tk.RIDGE, borderwidth=1)
            goal_frame.pack(fill=tk.X, pady=4, padx=2)
            
            # Icon với màu sắc
            icon_label = ttk.Label(goal_frame, text=icon, font=('Arial', 16))
            icon_label.pack(side=tk.LEFT, padx=(12, 10), pady=8)
            
            # Text goal
            goal_label = ttk.Label(goal_frame, text=goal, font=('Arial', 11))
            goal_label.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=8)
            
            # Progress indicator (placeholder)
            progress_frame = ttk.Frame(goal_frame)
            progress_frame.pack(side=tk.RIGHT, padx=10, pady=8)
            
            # Dot indicator
            dot_label = ttk.Label(progress_frame, text="●", font=('Arial', 8),
                                foreground='#bdc3c7')
            dot_label.pack()

    # --- CÁC HÀM LOGIC (GIỮ NGUYÊN) ---
    
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
            self.stats_labels['bmi'].config(text=f"{bmi:.1f}")
            
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
            empty_frame = ttk.Frame(self.alerts_content)
            empty_frame.pack(fill=tk.X, pady=20)
            ttk.Label(empty_frame, text="✅ Không có cảnh báo nào",
                     font=('Arial', 11), foreground='#27ae60',
                     justify=tk.CENTER).pack(fill=tk.X)
            return
        
        # Display alerts với styling đẹp hơn
        for alert in alerts:
            alert_frame = ttk.Frame(self.alerts_content, relief=tk.RAISED, borderwidth=1)
            alert_frame.pack(fill=tk.X, pady=3, padx=2)
            
            # Màu nền dựa trên mức độ cảnh báo
            bg_colors = {
                'critical': '#ffebee',
                'danger': '#fff3e0', 
                'warning': '#fff8e1',
                'info': '#e3f2fd',
                'success': '#e8f5e8'
            }
            
            # Configure style cho alert frame
            style = ttk.Style()
            style.configure(f'Alert.{alert["level"]}.TFrame', 
                          background=bg_colors.get(alert['level'], '#fafafa'))
            
            alert_frame.configure(style=f'Alert.{alert["level"]}.TFrame')
            
            # Alert icon and message
            icon_frame = ttk.Frame(alert_frame, style=f'Alert.{alert["level"]}.TFrame')
            icon_frame.pack(side=tk.LEFT, padx=12, pady=10)
            
            icon_label = ttk.Label(icon_frame, text=alert.get('icon', '⚠️'), 
                                 font=('Arial', 16),
                                 background=bg_colors.get(alert['level'], '#fafafa'))
            icon_label.pack()
            
            message_frame = ttk.Frame(alert_frame, style=f'Alert.{alert["level"]}.TFrame')
            message_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=10)
            
            message_label = ttk.Label(message_frame, text=alert['message'], 
                                    font=('Arial', 10), wraplength=700, justify=tk.LEFT,
                                    background=bg_colors.get(alert['level'], '#fafafa'))
            message_label.pack(anchor=tk.W)
            
            # Color code by level
            colors = {
                'critical': '#c62828',
                'danger': '#e65100', 
                'warning': '#f57c00',
                'info': '#1565c0',
                'success': '#2e7d32'
            }
            message_label.config(foreground=colors.get(alert['level'], 'black'))
            icon_label.config(foreground=colors.get(alert['level'], 'black'))
    
    def update_bmi_info(self):
        """Cập nhật thông tin BMI"""
        # Clear existing content
        for widget in self.bmi_content.winfo_children():
            widget.destroy()
        
        current_weight = self.db.get_current_weight(self.user['user_id'])
        
        if not current_weight:
            empty_frame = ttk.Frame(self.bmi_content)
            empty_frame.pack(fill=tk.X, pady=20)
            ttk.Label(empty_frame, text="📋 Chưa có đủ dữ liệu để tính BMI",
                     font=('Arial', 11), foreground='#95a5a6',
                     justify=tk.CENTER).pack(fill=tk.X)
            return
        
        from utils.bmi_calculator import BMICalculator
        height_m = self.user['height'] / 100
        bmi = BMICalculator.calculate_bmi(current_weight, height_m)
        category = BMICalculator.get_bmi_category(bmi)
        recommendations = BMICalculator.get_health_recommendations(bmi)
        ideal_range = BMICalculator.calculate_ideal_weight_range(height_m)
        
        # Main BMI card
        bmi_card = ttk.Frame(self.bmi_content, relief=tk.RAISED, borderwidth=1)
        bmi_card.pack(fill=tk.X, pady=5)
        
        # Header với chỉ số BMI
        header_frame = ttk.Frame(bmi_card)
        header_frame.pack(fill=tk.X, padx=15, pady=12)
        
        ttk.Label(header_frame, text="Chỉ số BMI của bạn:", 
                 font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        bmi_value_frame = ttk.Frame(header_frame)
        bmi_value_frame.pack(side=tk.RIGHT)
        
        ttk.Label(bmi_value_frame, text=f"{bmi:.1f}", 
                 font=('Arial', 16, 'bold'),
                 foreground=category['color']).pack(side=tk.LEFT)
        
        ttk.Label(bmi_value_frame, text=f" - {category['category']}", 
                 font=('Arial', 12),
                 foreground=category['color']).pack(side=tk.LEFT, padx=(5, 0))
        
        # Thông tin chi tiết
        details_frame = ttk.Frame(bmi_card)
        details_frame.pack(fill=tk.X, padx=15, pady=(0, 12))
        
        # Risk level
        risk_frame = ttk.Frame(details_frame)
        risk_frame.pack(fill=tk.X, pady=3)
        ttk.Label(risk_frame, text="Mức độ nguy cơ:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        ttk.Label(risk_frame, text=category['risk'], font=('Arial', 10),
                 foreground=category['color']).pack(side=tk.LEFT, padx=(5, 0))
        
        # Ideal weight range
        ideal_frame = ttk.Frame(details_frame)
        ideal_frame.pack(fill=tk.X, pady=3)
        ttk.Label(ideal_frame, text="Cân nặng lý tưởng:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        ttk.Label(ideal_frame, 
                 text=f"{ideal_range['min']} - {ideal_range['max']} kg (BMI {ideal_range['bmi_range']})",
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Recommendations card
        if recommendations:
            rec_card = ttk.Frame(self.bmi_content, relief=tk.RAISED, borderwidth=1)
            rec_card.pack(fill=tk.X, pady=(10, 5))
            
            ttk.Label(rec_card, text="💡 Đề xuất sức khỏe", 
                     font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=15, pady=10)
            
            for recommendation in recommendations[:3]:  # Show first 3 recommendations
                rec_frame = ttk.Frame(rec_card)
                rec_frame.pack(fill=tk.X, padx=15, pady=2)
                ttk.Label(rec_frame, text="•", font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 8))
                ttk.Label(rec_frame, text=recommendation, font=('Arial', 10),
                         wraplength=800, justify=tk.LEFT).pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def update_recent_activity(self):
        """Cập nhật hoạt động gần đây"""
        # Clear existing content
        for widget in self.activity_content.winfo_children():
            widget.destroy()
        
        activities = self.db.get_activities(self.user['user_id'], days=7)
        
        if not activities:
            empty_frame = ttk.Frame(self.activity_content)
            empty_frame.pack(fill=tk.X, pady=20)
            ttk.Label(empty_frame, text="🏃 Chưa có hoạt động nào trong 7 ngày qua",
                     font=('Arial', 11), foreground='#95a5a6',
                     justify=tk.CENTER).pack(fill=tk.X)
            return
        
        # Show last 5 activities
        for activity in activities[:5]:
            activity_frame = ttk.Frame(self.activity_content, relief=tk.RIDGE, borderwidth=1)
            activity_frame.pack(fill=tk.X, pady=2)
            
            # Activity info
            main_info_frame = ttk.Frame(activity_frame)
            main_info_frame.pack(fill=tk.X, padx=12, pady=8)
            
            # Icon và type
            icon_type_frame = ttk.Frame(main_info_frame)
            icon_type_frame.pack(side=tk.LEFT)
            
            # Icon dựa trên loại activity
            activity_icons = {
                'chạy bộ': '🏃', 'đi bộ': '🚶', 'bơi lội': '🏊',
                'xe đạp': '🚴', 'gym': '💪', 'yoga': '🧘'
            }
            icon = activity_icons.get(activity['activity_type'].lower(), '🏃')
            
            ttk.Label(icon_type_frame, text=icon, font=('Arial', 14)).pack(side=tk.LEFT)
            ttk.Label(icon_type_frame, text=activity['activity_type'], 
                     font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=(8, 15))
            
            # Thông tin chi tiết
            details_frame = ttk.Frame(main_info_frame)
            details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            info_text = f"{activity['duration']} phút"
            if activity['calories_burned']:
                info_text += f" • {activity['calories_burned']} cal"
            
            ttk.Label(details_frame, text=info_text, font=('Arial', 10)).pack(anchor=tk.W)
            
            # Ngày
            date_frame = ttk.Frame(main_info_frame)
            date_frame.pack(side=tk.RIGHT)
            ttk.Label(date_frame, text=activity['date'], font=('Arial', 9), 
                     foreground='gray').pack()
        
        # Show total for week
        total_duration = sum(act['duration'] for act in activities)
        total_frame = ttk.Frame(self.activity_content)
        total_frame.pack(fill=tk.X, pady=8)
        
        # Card tổng kết
        summary_card = ttk.Frame(total_frame, relief=tk.RAISED, borderwidth=1)
        summary_card.pack(fill=tk.X, padx=2)
        
        summary_content = ttk.Frame(summary_card)
        summary_content.pack(fill=tk.X, padx=15, pady=10)
        
        ttk.Label(summary_content, text=f"📅 Tổng tuần: {total_duration} phút", 
                 font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        
        # Compare to WHO recommendation
        if total_duration >= 150:
            status_text = "✅ Đạt mục tiêu WHO (150 phút/tuần)"
            color = "#27ae60"
        else:
            status_text = f"⏳ Còn {150 - total_duration} phút để đạt mục tiêu WHO"
            color = "#f39c12"
        
        ttk.Label(summary_content, text=status_text, font=('Arial', 10),
                 foreground=color).pack(side=tk.RIGHT)
    
    def setup_sleep_content(self, parent):
        """Thiết lập nội dung giấc ngủ"""
        try:
            sleep_records = self.db.get_sleep_records(self.user['user_id'], days=7)
            
            if not sleep_records:
                ttk.Label(parent, text="Chưa có dữ liệu giấc ngủ", 
                         font=('Arial', 10), foreground='gray').pack(pady=20)
                return
            
            sleep_hours = [r['sleep_hours'] for r in sleep_records]
            avg_sleep = sum(sleep_hours) / len(sleep_hours)
            
            stats_frame = ttk.Frame(parent)
            stats_frame.pack(fill=tk.X, pady=10)
            
            ttk.Label(stats_frame, text=f"Trung bình tuần: {avg_sleep:.1f} giờ", 
                     font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
            
            if avg_sleep < 6:
                status = "😴 Thiếu ngủ"
                color = "#e74c3c"
            elif avg_sleep < 7:
                status = "😴 Hơi thiếu ngủ"
                color = "#f39c12"
            elif avg_sleep <= 9:
                status = "✅ Bình thường (7-9h)"
                color = "#27ae60"
            else:
                status = "⚠️ Ngủ quá nhiều"
                color = "#f39c12"
            
            ttk.Label(stats_frame, text=status, font=('Arial', 11, 'bold'),
                     foreground=color).pack(side=tk.RIGHT, padx=5)
            
            quality_frame = ttk.LabelFrame(parent, text="Chất lượng giấc ngủ", padding="10")
            quality_frame.pack(fill=tk.X, pady=5)
            
            quality_count = {}
            for record in sleep_records:
                quality = record['sleep_quality']
                quality_count[quality] = quality_count.get(quality, 0) + 1
            
            for quality, count in quality_count.items():
                pct = int((count / len(sleep_records)) * 100)
                bar_frame = ttk.Frame(quality_frame)
                bar_frame.pack(fill=tk.X, pady=3)
                
                ttk.Label(bar_frame, text=f"{quality}: {count}d ({pct}%)", 
                         width=20, font=('Arial', 9)).pack(side=tk.LEFT)
                
                bar = ttk.Progressbar(bar_frame, length=150, mode='determinate', value=pct)
                bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            if sleep_records:
                latest = sleep_records[0]
                latest_frame = ttk.LabelFrame(parent, text="Ghi gần nhất", padding="10")
                latest_frame.pack(fill=tk.X, pady=5)
                
                ttk.Label(latest_frame, text=f"📅 {latest['record_date']}: "
                         f"{latest['sleep_hours']:.1f}h - {latest['sleep_quality']}", 
                         font=('Arial', 10)).pack(anchor=tk.W)
                
        except Exception as e:
            self.logger.error(f"Error setting up sleep content: {e}")
            ttk.Label(parent, text=f"Lỗi: {e}", foreground='red').pack()
    
    def setup_heart_rate_content(self, parent):
        """Thiết lập nội dung nhịp tim"""
        try:
            latest_hr = self.db.get_latest_heart_rate(self.user['user_id'])
            
            if not latest_hr:
                ttk.Label(parent, text="Chưa có dữ liệu nhịp tim", 
                         font=('Arial', 10), foreground='gray').pack(pady=20)
                return
            
            from models.heart_rate import HeartRateRecord
            
            stats_frame = ttk.Frame(parent)
            stats_frame.pack(fill=tk.X, pady=10)
            
            bpm = latest_hr['bpm']
            ttk.Label(stats_frame, text=f"Nhịp tim: {bpm} BPM", 
                     font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
            
            hr_rec = HeartRateRecord(
                user_id=latest_hr['user_id'],
                record_date=latest_hr['record_date'],
                record_time=latest_hr['record_time'],
                bpm=bpm,
                activity_type=latest_hr['activity_type']
            )
            status = hr_rec.get_health_status()
            
            if "Quá chậm" in status or "Quá nhanh" in status:
                color = "#e74c3c"
            elif "Chậm" in status or "Hơi nhanh" in status:
                color = "#f39c12"
            else:
                color = "#27ae60"
            
            ttk.Label(stats_frame, text=status, font=('Arial', 11, 'bold'),
                     foreground=color).pack(side=tk.RIGHT, padx=5)
            
            details_frame = ttk.Frame(parent)
            details_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(details_frame, text=f"⏰ {latest_hr['record_time']} | "
                     f"📍 {latest_hr['activity_type']}", 
                     font=('Arial', 10)).pack(anchor=tk.W)
            
            avg_hr = self.db.get_average_heart_rate(self.user['user_id'], days=7)
            if avg_hr > 0:
                avg_frame = ttk.LabelFrame(parent, text="Thống kê tuần", padding="10")
                avg_frame.pack(fill=tk.X, pady=5)
                
                ttk.Label(avg_frame, text=f"Trung bình: {int(avg_hr)} BPM", 
                         font=('Arial', 10)).pack(anchor=tk.W)
            
            recent_records = self.db.get_heart_rate_records(self.user['user_id'], days=7)
            if recent_records:
                recent_frame = ttk.LabelFrame(parent, text="Đo gần đây (7 ngày)", padding="10")
                recent_frame.pack(fill=tk.X, pady=5)
                
                for i, record in enumerate(recent_records[:5]):
                    ttk.Label(recent_frame, 
                             text=f"{record['record_date']} {record['record_time']}: "
                                  f"{record['bpm']} BPM ({record['activity_type']})", 
                             font=('Arial', 9)).pack(anchor=tk.W, pady=2)
                
        except Exception as e:
            self.logger.error(f"Error setting up heart rate content: {e}")
            ttk.Label(parent, text=f"Lỗi: {e}", foreground='red').pack()
