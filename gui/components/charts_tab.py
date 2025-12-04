# gui/components/charts_tab.py
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
from datetime import datetime, timedelta

class ChartsTab:
    """Tab biểu đồ và phân tích"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.db = main_window.db
        self.user = main_window.user
        self.chart_generator = main_window.chart_generator
        self.logger = logging.getLogger(__name__)
        
        self.current_figures = []
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Thanh điều khiển trên cùng
        self.setup_control_bar()
        
        # Hiển thị biểu đồ full
        self.setup_chart_display()
    
    def setup_control_bar(self):
        """Thanh điều khiển gọn nhất"""
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X, padx=15, pady=12)
        
        # Loại biểu đồ
        ttk.Label(control_frame, text="📊 Biểu đồ:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        self.chart_combo = ttk.Combobox(
            control_frame,
            values=[
                "📊 Cân nặng",
                "🎯 BMI",
                "🏃 Hoạt động",
                "😴 Giấc ngủ",
                "❤️ Nhịp tim",
                "😴 Chất lượng",
                "❤️ Phân bố",
                "📈 Tổng quan"
            ],
            state='readonly',
            width=18,
            font=('Arial', 10)
        )
        self.chart_combo.set("📊 Cân nặng")
        self.chart_combo.pack(side=tk.LEFT, padx=5)
        self.chart_combo.bind('<<ComboboxSelected>>', self.on_chart_changed)
        
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=15)
        
        # Khoảng thời gian
        ttk.Label(control_frame, text="⏰ Thời gian:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        self.period_combo = ttk.Combobox(
            control_frame,
            values=["1 Tuần", "1 Tháng", "3 Tháng", "6 Tháng"],
            state='readonly',
            width=12,
            font=('Arial', 10)
        )
        self.period_combo.set("1 Tuần")
        self.period_combo.pack(side=tk.LEFT, padx=5)
        self.period_combo.bind('<<ComboboxSelected>>', self.on_period_changed)
        
        # Nút lưu
        ttk.Button(control_frame, text="💾 Lưu", command=self.save_chart).pack(side=tk.RIGHT, padx=10)
        
        # Trạng thái
        self.status_label = ttk.Label(control_frame, text="Sẵn sàng", font=('Arial', 9), foreground='gray')
        self.status_label.pack(side=tk.RIGHT, padx=20)
    
    def setup_chart_display(self):
        """Hiển thị biểu đồ full"""
        self.chart_frame = ttk.Frame(self.frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.show_empty_chart()
    
    def show_empty_chart(self):
        """Hiển thị trống"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        empty_frame = ttk.Frame(self.chart_frame)
        empty_frame.pack(fill=tk.BOTH, expand=True, pady=150)
        
        ttk.Label(empty_frame, text="📊", font=('Arial', 64), foreground='lightgray').pack()
        ttk.Label(empty_frame, text="Chọn biểu đồ để bắt đầu", font=('Arial', 14), foreground='gray').pack(pady=10)
    
    def on_chart_changed(self, event=None):
        """Khi thay đổi loại biểu đồ"""
        self.refresh_charts()
    
    def on_period_changed(self, event=None):
        """Khi thay đổi khoảng thời gian"""
        self.refresh_charts()
    
    def refresh_charts(self):
        """Tải biểu đồ"""
        try:
            chart_text = self.chart_combo.get()
            period_text = self.period_combo.get()
            
            # Map dropdown text to chart type
            chart_map = {
                "📊 Cân nặng": "weight_trend",
                "🎯 BMI": "bmi",
                "🏃 Hoạt động": "activity",
                "😴 Giấc ngủ": "sleep_trend",
                "❤️ Nhịp tim": "heart_rate_trend",
                "😴 Chất lượng": "sleep_quality",
                "❤️ Phân bố": "heart_rate_distribution",
                "📈 Tổng quan": "weekly_summary"
            }
            
            period_map = {
                "1 Tuần": "week",
                "1 Tháng": "month",
                "3 Tháng": "3months",
                "6 Tháng": "6months"
            }
            
            chart_type = chart_map.get(chart_text, "weight_trend")
            period = period_map.get(period_text, "week")
            
            # Clear existing
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            for fig in self.current_figures:
                plt.close(fig)
            self.current_figures.clear()
            
            self.status_label.config(text="⏳ Đang tạo...", foreground='blue')
            self.chart_frame.update()
            
            # Get data
            days_map = {'week': 7, 'month': 30, '3months': 90, '6months': 180}
            days = days_map.get(period, 30)
            
            weight_data = self.db.get_weight_records(self.user['user_id'], days=days)
            activity_data = self.db.get_activities(self.user['user_id'], days=days)
            sleep_data = self.db.get_sleep_records(self.user['user_id'], days=days)
            hr_data = self.db.get_heart_rate_records(self.user['user_id'], days=days)
            
            has_data = bool(weight_data or activity_data or sleep_data or hr_data)
            
            if not has_data:
                self.show_no_data_message()
                return
            
            # Render chart
            if chart_type == "weight_trend":
                if weight_data:
                    self.show_weight_trend_chart(weight_data, period)
                else:
                    self.show_no_data_message("Không có dữ liệu cân nặng")
            elif chart_type == "bmi":
                if weight_data:
                    self.show_bmi_chart(weight_data)
                else:
                    self.show_no_data_message("Không có dữ liệu cân nặng")
            elif chart_type == "activity":
                if activity_data:
                    self.show_activity_chart(activity_data)
                else:
                    self.show_no_data_message("Không có dữ liệu hoạt động")
            elif chart_type == "sleep_trend":
                if sleep_data:
                    self.show_sleep_trend_chart(sleep_data, period)
                else:
                    self.show_no_data_message("Không có dữ liệu giấc ngủ")
            elif chart_type == "heart_rate_trend":
                if hr_data:
                    self.show_heart_rate_trend_chart(hr_data, period)
                else:
                    self.show_no_data_message("Không có dữ liệu nhịp tim")
            elif chart_type == "sleep_quality":
                if sleep_data:
                    self.show_sleep_quality_chart(sleep_data)
                else:
                    self.show_no_data_message("Không có dữ liệu giấc ngủ")
            elif chart_type == "heart_rate_distribution":
                if hr_data:
                    self.show_heart_rate_distribution_chart(hr_data)
                else:
                    self.show_no_data_message("Không có dữ liệu nhịp tim")
            elif chart_type == "weekly_summary":
                if weight_data or activity_data:
                    self.show_weekly_summary_chart(weight_data, activity_data)
                else:
                    self.show_no_data_message("Không có dữ liệu")
            
            self.status_label.config(text="✅ Hoàn thành", foreground='green')
            
        except Exception as e:
            self.logger.error(f"Error: {e}")
            self.status_label.config(text="❌ Lỗi", foreground='red')
            self.show_error_message(str(e))
    
    def show_weight_trend_chart(self, weight_data, period):
        fig = self.chart_generator.create_weight_trend_chart(weight_data, period)
        self.display_figure(fig, "📊 Xu hướng Cân nặng")
        self.show_weight_statistics(weight_data)
    
    def show_bmi_chart(self, weight_data):
        fig = self.chart_generator.create_bmi_chart(weight_data)
        self.display_figure(fig, "🎯 Chỉ số BMI")
        self.show_bmi_statistics(weight_data)
    
    def show_activity_chart(self, activity_data):
        fig = self.chart_generator.create_activity_chart(activity_data)
        self.display_figure(fig, "🏃 Hoạt động")
        self.show_activity_statistics(activity_data)
    
    def show_sleep_trend_chart(self, sleep_data, period):
        fig = self.chart_generator.create_sleep_trend_chart(sleep_data, period)
        self.display_figure(fig, "😴 Giấc ngủ")
        self.show_sleep_statistics(sleep_data)
    
    def show_heart_rate_trend_chart(self, hr_data, period):
        fig = self.chart_generator.create_heart_rate_trend_chart(hr_data, period)
        self.display_figure(fig, "❤️ Nhịp tim")
        self.show_heart_rate_statistics(hr_data)
    
    def show_sleep_quality_chart(self, sleep_data):
        fig = self.chart_generator.create_sleep_quality_chart(sleep_data)
        self.display_figure(fig, "😴 Chất lượng")
        self.show_sleep_statistics(sleep_data)
    
    def show_heart_rate_distribution_chart(self, hr_data):
        fig = self.chart_generator.create_heart_rate_distribution_chart(hr_data)
        self.display_figure(fig, "❤️ Phân bố")
        self.show_heart_rate_statistics(hr_data)
    
    def show_weekly_summary_chart(self, weight_data, activity_data):
        fig = self.chart_generator.create_weekly_summary_chart(weight_data, activity_data)
        self.display_figure(fig, "📈 Tổng quan")
    
    def display_figure(self, fig, title):
        chart_frame = ttk.LabelFrame(self.chart_frame, text=title, padding="10")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True)
        
        self.current_figures.append(fig)
    
    def show_weight_statistics(self, weight_data):
        if not weight_data:
            return
        
        stats_frame = ttk.LabelFrame(self.chart_frame, text="📊 Thống kê Cân nặng", padding="10")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        weights = [item['weight'] for item in weight_data]
        bmis = [item['bmi'] for item in weight_data]
        
        min_w = min(weights)
        max_w = max(weights)
        avg_w = sum(weights) / len(weights)
        latest_w = weights[-1] if weights else 0
        
        s1 = f"🔢 Hiện tại: {latest_w}kg | Min: {min_w}kg | Max: {max_w}kg | Trung bình: {avg_w:.1f}kg"
        ttk.Label(stats_frame, text=s1, font=('Arial', 10)).pack(anchor=tk.W, pady=3)
        
        avg_bmi = sum(bmis) / len(bmis)
        s2 = f"🎯 BMI trung bình: {avg_bmi:.1f}"
        ttk.Label(stats_frame, text=s2, font=('Arial', 10)).pack(anchor=tk.W, pady=3)
    
    def show_bmi_statistics(self, weight_data):
        if not weight_data:
            return
        
        stats_frame = ttk.LabelFrame(self.chart_frame, text="📊 Thống kê BMI", padding="10")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        bmis = [item['bmi'] for item in weight_data]
        
        min_b = min(bmis)
        max_b = max(bmis)
        avg_b = sum(bmis) / len(bmis)
        latest_b = bmis[-1] if bmis else 0
        
        s = f"🎯 Hiện tại: {latest_b:.1f} | Min: {min_b:.1f} | Max: {max_b:.1f} | Trung bình: {avg_b:.1f}"
        ttk.Label(stats_frame, text=s, font=('Arial', 10)).pack(anchor=tk.W, pady=3)
    
    def show_activity_statistics(self, activity_data):
        if not activity_data:
            return
        
        stats_frame = ttk.LabelFrame(self.chart_frame, text="📊 Thống kê Hoạt động", padding="10")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        total_d = sum(item['duration'] for item in activity_data)
        total_c = sum(item['calories_burned'] for item in activity_data)
        avg_d = total_d / len(activity_data) if activity_data else 0
        
        s1 = f"⏱️ Tổng thời gian: {total_d}p | Trung bình: {avg_d:.0f}p/lần | 🔥 Calories: {total_c:.0f}"
        ttk.Label(stats_frame, text=s1, font=('Arial', 10)).pack(anchor=tk.W, pady=3)
        
        s2 = f"🏃 Số lần hoạt động: {len(activity_data)} lần"
        ttk.Label(stats_frame, text=s2, font=('Arial', 10)).pack(anchor=tk.W, pady=3)
    
    def show_sleep_statistics(self, sleep_data):
        if not sleep_data:
            return
        
        stats_frame = ttk.LabelFrame(self.chart_frame, text="📊 Thống kê Giấc ngủ", padding="10")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        sleep_h = [item['sleep_hours'] for item in sleep_data]
        
        min_s = min(sleep_h)
        max_s = max(sleep_h)
        avg_s = sum(sleep_h) / len(sleep_h)
        latest_s = sleep_h[-1] if sleep_h else 0
        
        if avg_s < 6:
            status = "⚠️ Thiếu ngủ"
        elif avg_s < 7:
            status = "😴 Hơi thiếu"
        elif avg_s <= 9:
            status = "✅ Bình thường"
        else:
            status = "⚠️ Ngủ quá nhiều"
        
        s1 = f"😴 Hiện tại: {latest_s:.1f}h | Min: {min_s:.1f}h | Max: {max_s:.1f}h | Trung bình: {avg_s:.1f}h"
        ttk.Label(stats_frame, text=s1, font=('Arial', 10)).pack(anchor=tk.W, pady=3)
        
        s2 = f"Tình trạng: {status}"
        ttk.Label(stats_frame, text=s2, font=('Arial', 10)).pack(anchor=tk.W, pady=3)
    
    def show_heart_rate_statistics(self, hr_data):
        if not hr_data:
            return
        
        stats_frame = ttk.LabelFrame(self.chart_frame, text="📊 Thống kê Nhịp tim", padding="10")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        bpm_list = [item['bpm'] for item in hr_data]
        
        min_bpm = min(bpm_list)
        max_bpm = max(bpm_list)
        avg_bpm = sum(bpm_list) / len(bpm_list)
        latest_bpm = bpm_list[-1] if bpm_list else 0
        
        if latest_bpm < 40:
            st = "⚠️ Quá chậm"
        elif latest_bpm < 60:
            st = "😐 Chậm"
        elif latest_bpm <= 100:
            st = "✅ Bình thường"
        elif latest_bpm <= 120:
            st = "⚠️ Hơi nhanh"
        else:
            st = "🔴 Quá nhanh"
        
        s1 = f"❤️ Hiện tại: {latest_bpm}BPM | Min: {min_bpm} | Max: {max_bpm} | Trung bình: {avg_bpm:.0f}"
        ttk.Label(stats_frame, text=s1, font=('Arial', 10)).pack(anchor=tk.W, pady=3)
        
        s2 = f"Tình trạng: {st}"
        ttk.Label(stats_frame, text=s2, font=('Arial', 10)).pack(anchor=tk.W, pady=3)
    
    def show_no_data_message(self, message="Không có dữ liệu"):
        no_data_frame = ttk.Frame(self.chart_frame)
        no_data_frame.pack(fill=tk.BOTH, expand=True, pady=150)
        
        ttk.Label(no_data_frame, text="📭", font=('Arial', 64), foreground='lightgray').pack()
        ttk.Label(no_data_frame, text=message, font=('Arial', 14), foreground='gray').pack(pady=10)
        ttk.Label(no_data_frame, text="Nhập dữ liệu trong tab 'Nhập liệu'", font=('Arial', 11), foreground='gray').pack()
    
    def show_error_message(self, error_message):
        error_frame = ttk.Frame(self.chart_frame)
        error_frame.pack(fill=tk.BOTH, expand=True, pady=150)
        
        ttk.Label(error_frame, text="❌", font=('Arial', 64), foreground='#F44336').pack()
        ttk.Label(error_frame, text="Lỗi", font=('Arial', 14), foreground='#F44336').pack(pady=10)
        ttk.Label(error_frame, text=error_message, font=('Arial', 11), foreground='#D32F2F', wraplength=600).pack()
    
    def save_chart(self):
        if not self.current_figures:
            self.status_label.config(text="❌ Không có biểu đồ", foreground='red')
            return
        
        try:
            fig = self.current_figures[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"health_chart_{timestamp}.png"
            fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
            
            self.status_label.config(text=f"✅ Đã lưu: {filename[:20]}...", foreground='green')
            self.logger.info(f"Chart saved: {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving: {e}")
            self.status_label.config(text="❌ Lỗi lưu", foreground='red')
