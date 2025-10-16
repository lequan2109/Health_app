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
        
        self.current_figures = []  # Track current figures
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        self.frame = ttk.Frame(self.parent)
        
        # Control panel
        self.setup_control_panel()
        
        # Chart container
        self.setup_chart_container()
    
    def setup_control_panel(self):
        """Thiết lập bảng điều khiển"""
        control_frame = ttk.LabelFrame(self.frame, text="Tùy chọn Biểu đồ", padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Chart type selection
        type_frame = ttk.Frame(control_frame)
        type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(type_frame, text="Loại biểu đồ:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        self.chart_var = tk.StringVar(value="weight_trend")
        chart_types = [
            ("📊 Xu hướng Cân nặng", "weight_trend"),
            ("🎯 Chỉ số BMI", "bmi"),
            ("🏃 Hoạt động", "activity"),
            ("📈 Tổng quan Tuần", "weekly_summary")
        ]
        
        for text, value in chart_types:
            ttk.Radiobutton(type_frame, text=text, variable=self.chart_var, 
                           value=value).pack(side=tk.LEFT, padx=10)
        
        # Period selection
        period_frame = ttk.Frame(control_frame)
        period_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(period_frame, text="Khoảng thời gian:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        self.period_var = tk.StringVar(value="week")
        periods = [
            ("1 Tuần", "week"),
            ("1 Tháng", "month"), 
            ("3 Tháng", "3months"),
            ("6 Tháng", "6months")
        ]
        
        for text, value in periods:
            ttk.Radiobutton(period_frame, text=text, variable=self.period_var,
                           value=value).pack(side=tk.LEFT, padx=10)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="🔄 Tải lại Biểu đồ", 
                  command=self.refresh_charts, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="💾 Lưu Biểu đồ", 
                  command=self.save_chart).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.chart_status = ttk.Label(control_frame, text="Chọn loại biểu đồ và nhấn 'Tải lại'",
                                     font=('Arial', 9), foreground='gray')
        self.chart_status.pack(anchor=tk.W)
    
    def setup_chart_container(self):
        """Thiết lập container cho biểu đồ"""
        # Create scrollable frame for charts
        self.chart_canvas = tk.Canvas(self.frame, bg='white')
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.chart_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.chart_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chart_canvas.configure(scrollregion=self.chart_canvas.bbox("all"))
        )
        
        self.chart_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.chart_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.chart_canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Bind mousewheel to canvas
        self.chart_canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Initial empty chart
        self.show_empty_chart()
    
    def _on_mousewheel(self, event):
        """Xử lý sự kiện cuộn chuột"""
        self.chart_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def show_empty_chart(self):
        """Hiển thị biểu đồ trống"""
        # Clear existing charts
        self.clear_charts()
        
        empty_frame = ttk.Frame(self.scrollable_frame)
        empty_frame.pack(fill=tk.BOTH, expand=True, pady=50)
        
        ttk.Label(empty_frame, text="📊 Chọn loại biểu đồ và nhấn 'Tải lại' để xem dữ liệu",
                 font=('Arial', 12), foreground='gray').pack(expand=True)
    
    def clear_charts(self):
        """Xóa tất cả biểu đồ hiện tại"""
        # Clear matplotlib figures
        for fig in self.current_figures:
            plt.close(fig)
        self.current_figures.clear()
        
        # Clear TKinter widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def refresh_charts(self):
        """Làm mới biểu đồ"""
        try:
            chart_type = self.chart_var.get()
            period = self.period_var.get()
            
            self.clear_charts()
            self.chart_status.config(text="Đang tạo biểu đồ...", foreground='blue')
            
            # Get data based on period
            days_map = {'week': 7, 'month': 30, '3months': 90, '6months': 180}
            days = days_map.get(period, 30)
            
            weight_data = self.db.get_weight_records(self.user['user_id'], days=days)
            activity_data = self.db.get_activities(self.user['user_id'], days=days)
            
            if not weight_data and not activity_data:
                self.show_no_data_message()
                return
            
            # Generate chart based on type
            if chart_type == "weight_trend":
                self.show_weight_trend_chart(weight_data, period)
            elif chart_type == "bmi":
                self.show_bmi_chart(weight_data)
            elif chart_type == "activity":
                self.show_activity_chart(activity_data)
            elif chart_type == "weekly_summary":
                self.show_weekly_summary_chart(weight_data, activity_data)
            
            self.chart_status.config(text="Biểu đồ đã được tải thành công", foreground='green')
            self.logger.info(f"Refreshed {chart_type} chart for {period}")
            
        except Exception as e:
            self.logger.error(f"Error refreshing charts: {e}")
            self.chart_status.config(text=f"Lỗi tạo biểu đồ: {e}", foreground='red')
            self.show_error_message(str(e))
    
    def show_weight_trend_chart(self, weight_data, period):
        """Hiển thị biểu đồ xu hướng cân nặng"""
        if not weight_data:
            self.show_no_data_message("Không có dữ liệu cân nặng")
            return
        
        fig = self.chart_generator.create_weight_trend_chart(weight_data, period)
        self.display_figure(fig, "Xu hướng Cân nặng")
    
    def show_bmi_chart(self, weight_data):
        """Hiển thị biểu đồ BMI"""
        if not weight_data:
            self.show_no_data_message("Không có dữ liệu để tính BMI")
            return
        
        fig = self.chart_generator.create_bmi_chart(weight_data)
        self.display_figure(fig, "Chỉ số BMI")
    
    def show_activity_chart(self, activity_data):
        """Hiển thị biểu đồ hoạt động"""
        if not activity_data:
            self.show_no_data_message("Không có dữ liệu hoạt động")
            return
        
        fig = self.chart_generator.create_activity_chart(activity_data)
        self.display_figure(fig, "Phân tích Hoạt động")
    
    def show_weekly_summary_chart(self, weight_data, activity_data):
        """Hiển thị biểu đồ tổng quan tuần"""
        if not weight_data and not activity_data:
            self.show_no_data_message("Không có đủ dữ liệu cho tổng quan")
            return
        
        fig = self.chart_generator.create_weekly_summary_chart(weight_data, activity_data)
        self.display_figure(fig, "Tổng quan Tuần")
    
    def display_figure(self, fig, title):
        """Hiển thị figure matplotlib trong TKinter"""
        # Create frame for chart
        chart_frame = ttk.LabelFrame(self.scrollable_frame, text=title, padding="10")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create canvas for matplotlib figure
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        
        # Get the TKinter widget
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add toolbar (optional - would need NavigationToolbar2Tk)
        # toolbar = NavigationToolbar2Tk(canvas, chart_frame)
        # toolbar.update()
        
        # Store figure reference
        self.current_figures.append(fig)
    
    def show_no_data_message(self, message="Không có dữ liệu"):
        """Hiển thị thông báo không có dữ liệu"""
        no_data_frame = ttk.Frame(self.scrollable_frame)
        no_data_frame.pack(fill=tk.BOTH, expand=True, pady=50)
        
        ttk.Label(no_data_frame, text="📭", font=('Arial', 48), 
                 foreground='gray').pack(pady=10)
        ttk.Label(no_data_frame, text=message, 
                 font=('Arial', 12), foreground='gray').pack(pady=5)
        ttk.Label(no_data_frame, text="Hãy nhập dữ liệu trong tab 'Nhập liệu'", 
                 font=('Arial', 10), foreground='gray').pack(pady=5)
    
    def show_error_message(self, error_message):
        """Hiển thị thông báo lỗi"""
        error_frame = ttk.Frame(self.scrollable_frame)
        error_frame.pack(fill=tk.BOTH, expand=True, pady=50)
        
        ttk.Label(error_frame, text="❌", font=('Arial', 48), 
                 foreground='red').pack(pady=10)
        ttk.Label(error_frame, text="Lỗi khi tạo biểu đồ", 
                 font=('Arial', 12), foreground='red').pack(pady=5)
        ttk.Label(error_frame, text=error_message, 
                 font=('Arial', 10), foreground='darkred', wraplength=600).pack(pady=5)
    
    def save_chart(self):
        """Lưu biểu đồ hiện tại thành file"""
        if not self.current_figures:
            self.main_window.show_alert("Thông báo", "Không có biểu đồ nào để lưu", "warning")
            return
        
        try:
            # For simplicity, save the first figure
            fig = self.current_figures[0]
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"health_chart_{timestamp}.png"
            
            # Save figure
            fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
            
            self.main_window.show_alert("Thành công", f"Đã lưu biểu đồ thành: {filename}")
            self.logger.info(f"Chart saved as: {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving chart: {e}")
            self.main_window.show_alert("Lỗi", f"Không thể lưu biểu đồ: {e}", "error")
    
    def get_chart_data_statistics(self, weight_data, activity_data):
        """Lấy thống kê dữ liệu cho biểu đồ"""
        stats = {}
        
        if weight_data:
            weights = [item['weight'] for item in weight_data]
            bmis = [item['bmi'] for item in weight_data]
            
            stats['weight'] = {
                'min': min(weights) if weights else 0,
                'max': max(weights) if weights else 0,
                'avg': sum(weights) / len(weights) if weights else 0,
                'trend': 'stable'  # Simplified trend calculation
            }
            
            stats['bmi'] = {
                'min': min(bmis) if bmis else 0,
                'max': max(bmis) if bmis else 0,
                'avg': sum(bmis) / len(bmis) if bmis else 0
            }
        
        if activity_data:
            durations = [item['duration'] for item in activity_data]
            stats['activity'] = {
                'total_duration': sum(durations) if durations else 0,
                'avg_duration': sum(durations) / len(durations) if durations else 0,
                'activity_count': len(activity_data)
            }
        
        return stats