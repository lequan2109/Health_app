# gui/components/history_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import logging
import csv
import json
from utils.bmi_calculator import BMICalculator

class HistoryTab:
    """Tab lịch sử và xuất dữ liệu"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.db = main_window.db
        self.user = main_window.user
        self.logger = logging.getLogger(__name__)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        self.frame = ttk.Frame(self.parent)
        
        # Control panel
        self.setup_control_panel()
        
        # Data display
        self.setup_data_display()
        
        # Export panel
        self.setup_export_panel()
    
    def setup_control_panel(self):
        """Thiết lập bảng điều khiển"""
        control_frame = ttk.LabelFrame(self.frame, text="Bộ lọc Dữ liệu", padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Date range
        date_frame = ttk.Frame(control_frame)
        date_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(date_frame, text="Từ ngày:", font=('Arial', 10)).pack(side=tk.LEFT)
        self.from_date_entry = ttk.Entry(date_frame, width=12, font=('Arial', 10))
        self.from_date_entry.pack(side=tk.LEFT, padx=5)
        self.from_date_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        
        ttk.Label(date_frame, text="Đến ngày:", font=('Arial', 10)).pack(side=tk.LEFT, padx=(20, 0))
        self.to_date_entry = ttk.Entry(date_frame, width=12, font=('Arial', 10))
        self.to_date_entry.pack(side=tk.LEFT, padx=5)
        self.to_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Data type
        type_frame = ttk.Frame(control_frame)
        type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(type_frame, text="Loại dữ liệu:", font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.data_type_var = tk.StringVar(value="weight")
        ttk.Radiobutton(type_frame, text="Cân nặng", variable=self.data_type_var,
                       value="weight", command=self.refresh_data).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(type_frame, text="Hoạt động", variable=self.data_type_var,
                       value="activity", command=self.refresh_data).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(type_frame, text="Tất cả", variable=self.data_type_var,
                       value="all", command=self.refresh_data).pack(side=tk.LEFT, padx=10)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="🔍 Tải dữ liệu", 
                  command=self.refresh_data, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="🗑️ Xóa bộ lọc", 
                  command=self.clear_filters).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.filter_status = ttk.Label(control_frame, text="", font=('Arial', 9))
        self.filter_status.pack(anchor=tk.W)
    
    def setup_data_display(self):
        """Thiết lập hiển thị dữ liệu"""
        # Notebook for different data types
        self.data_notebook = ttk.Notebook(self.frame)
        self.data_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Weight history tab
        self.weight_tab = ttk.Frame(self.data_notebook)
        self.data_notebook.add(self.weight_tab, text="⚖️ Cân nặng")
        
        # Activity history tab  
        self.activity_tab = ttk.Frame(self.data_notebook)
        self.data_notebook.add(self.activity_tab, text="🏃 Hoạt động")
        
        # Setup weight tab
        self.setup_weight_tab()
        
        # Setup activity tab
        self.setup_activity_tab()
        
        # Bind tab change
        self.data_notebook.bind('<<NotebookTabChanged>>', self.on_data_tab_changed)
    
    def setup_weight_tab(self):
        """Thiết lập tab cân nặng"""
        # Treeview for weight data
        columns = ('date', 'weight', 'bmi', 'category', 'notes')
        self.weight_tree = ttk.Treeview(self.weight_tab, columns=columns, show='headings', height=15)
        
        # Define headings
        self.weight_tree.heading('date', text='Ngày')
        self.weight_tree.heading('weight', text='Cân nặng (kg)')
        self.weight_tree.heading('bmi', text='BMI')
        self.weight_tree.heading('category', text='Phân loại')
        self.weight_tree.heading('notes', text='Ghi chú')
        
        # Define columns
        self.weight_tree.column('date', width=100, anchor='center')
        self.weight_tree.column('weight', width=100, anchor='center')
        self.weight_tree.column('bmi', width=80, anchor='center')
        self.weight_tree.column('category', width=120, anchor='center')
        self.weight_tree.column('notes', width=200)
        
        # Scrollbar
        weight_scrollbar = ttk.Scrollbar(self.weight_tab, orient="vertical", command=self.weight_tree.yview)
        self.weight_tree.configure(yscrollcommand=weight_scrollbar.set)
        
        self.weight_tree.pack(side="left", fill="both", expand=True)
        weight_scrollbar.pack(side="right", fill="y")
        
        # Context menu
        self.setup_weight_context_menu()
    
    def setup_activity_tab(self):
        """Thiết lập tab hoạt động"""
        # Treeview for activity data
        activity_columns = ('date', 'type', 'duration', 'calories', 'intensity', 'notes')
        self.activity_tree = ttk.Treeview(self.activity_tab, columns=activity_columns, show='headings', height=15)
        
        # Define headings
        self.activity_tree.heading('date', text='Ngày')
        self.activity_tree.heading('type', text='Loại hoạt động')
        self.activity_tree.heading('duration', text='Thời gian (phút)')
        self.activity_tree.heading('calories', text='Calories')
        self.activity_tree.heading('intensity', text='Cường độ')
        self.activity_tree.heading('notes', text='Ghi chú')
        
        # Define columns
        self.activity_tree.column('date', width=100, anchor='center')
        self.activity_tree.column('type', width=120, anchor='center')
        self.activity_tree.column('duration', width=100, anchor='center')
        self.activity_tree.column('calories', width=80, anchor='center')
        self.activity_tree.column('intensity', width=80, anchor='center')
        self.activity_tree.column('notes', width=200)
        
        # Scrollbar
        activity_scrollbar = ttk.Scrollbar(self.activity_tab, orient="vertical", command=self.activity_tree.yview)
        self.activity_tree.configure(yscrollcommand=activity_scrollbar.set)
        
        self.activity_tree.pack(side="left", fill="both", expand=True)
        activity_scrollbar.pack(side="right", fill="y")
        
        # Context menu
        self.setup_activity_context_menu()
    
    def setup_weight_context_menu(self):
        """Thiết lập menu ngữ cảnh cho cân nặng"""
        self.weight_context_menu = tk.Menu(self.weight_tree, tearoff=0)
        self.weight_context_menu.add_command(label="Xem chi tiết", command=self.view_weight_details)
        self.weight_context_menu.add_command(label="Xóa bản ghi", command=self.delete_weight_record)
        
        self.weight_tree.bind("<Button-3>", self.show_weight_context_menu)
    
    def setup_activity_context_menu(self):
        """Thiết lập menu ngữ cảnh cho hoạt động"""
        self.activity_context_menu = tk.Menu(self.activity_tree, tearoff=0)
        self.activity_context_menu.add_command(label="Xem chi tiết", command=self.view_activity_details)
        self.activity_context_menu.add_command(label="Xóa bản ghi", command=self.delete_activity_record)
        
        self.activity_tree.bind("<Button-3>", self.show_activity_context_menu)
    
    def setup_export_panel(self):
        """Thiết lập bảng xuất dữ liệu"""
        export_frame = ttk.LabelFrame(self.frame, text="Xuất Dữ liệu", padding="10")
        export_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Export options
        options_frame = ttk.Frame(export_frame)
        options_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(options_frame, text="Định dạng:", font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.export_format_var = tk.StringVar(value="csv")
        ttk.Radiobutton(options_frame, text="CSV", variable=self.export_format_var,
                       value="csv").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(options_frame, text="JSON", variable=self.export_format_var,
                       value="json").pack(side=tk.LEFT, padx=10)
        
        # Export buttons
        export_button_frame = ttk.Frame(export_frame)
        export_button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(export_button_frame, text="📊 Xuất Cân nặng", 
                  command=lambda: self.export_data('weight')).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(export_button_frame, text="🏃 Xuất Hoạt động", 
                  command=lambda: self.export_data('activity')).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(export_button_frame, text="💾 Xuất Tất cả", 
                  command=lambda: self.export_data('all')).pack(side=tk.LEFT, padx=5)
        
        # Export status
        self.export_status = ttk.Label(export_frame, text="", font=('Arial', 9))
        self.export_status.pack(anchor=tk.W)
    
    def refresh_data(self):
        """Làm mới dữ liệu"""
        try:
            from_date = self.from_date_entry.get().strip()
            to_date = self.to_date_entry.get().strip()
            data_type = self.data_type_var.get()
            
            # Validate dates
            if from_date and to_date:
                try:
                    from_dt = datetime.strptime(from_date, '%Y-%m-%d')
                    to_dt = datetime.strptime(to_date, '%Y-%m-%d')
                    
                    if from_dt > to_dt:
                        messagebox.showerror("Lỗi", "Ngày bắt đầu không thể sau ngày kết thúc")
                        return
                except ValueError:
                    messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ (YYYY-MM-DD)")
                    return
            
            # Load data based on type
            if data_type in ['weight', 'all']:
                self.load_weight_data(from_date, to_date)
            
            if data_type in ['activity', 'all']:
                self.load_activity_data(from_date, to_date)
            
            # Update status
            record_count = len(self.weight_tree.get_children()) + len(self.activity_tree.get_children())
            self.filter_status.config(text=f"Đã tải {record_count} bản ghi", foreground='green')
            
            # Auto-select appropriate tab
            if data_type == 'weight':
                self.data_notebook.select(0)
            elif data_type == 'activity':
                self.data_notebook.select(1)
            
            self.logger.info(f"Refreshed history data: {data_type} from {from_date} to {to_date}")
            
        except Exception as e:
            self.logger.error(f"Error refreshing history data: {e}")
            self.filter_status.config(text=f"Lỗi: {e}", foreground='red')
    
    def load_weight_data(self, from_date=None, to_date=None):
        """Tải dữ liệu cân nặng"""
        # Clear existing data
        for item in self.weight_tree.get_children():
            self.weight_tree.delete(item)
        
        # Get weight data
        if from_date and to_date:
            weight_data = self.db.get_weight_history(self.user['user_id'], from_date, to_date)
        else:
            weight_data = self.db.get_weight_records(self.user['user_id'], days=365)  # 1 year
        
        from utils.bmi_calculator import BMICalculator
        
        for record in weight_data:
            category = BMICalculator.get_bmi_category(record['bmi'])
            self.weight_tree.insert('', 'end', values=(
                record['date'],
                record['weight'],
                record['bmi'],
                category['category'],
                record['notes'] or ''
            ))
    
    def load_activity_data(self, from_date=None, to_date=None):
        """Tải dữ liệu hoạt động"""
        # Clear existing data
        for item in self.activity_tree.get_children():
            self.activity_tree.delete(item)
        
        # Get activity data
        if from_date and to_date:
            # For date range, we need to implement this method in db_manager
            activity_data = self.db.get_activities(self.user['user_id'], days=365)
            # Filter by date range
            activity_data = [act for act in activity_data if from_date <= act['date'] <= to_date]
        else:
            activity_data = self.db.get_activities(self.user['user_id'], days=365)
        
        for activity in activity_data:
            self.activity_tree.insert('', 'end', values=(
                activity['date'],
                activity['activity_type'],
                activity['duration'],
                activity['calories_burned'] or '--',
                activity['intensity'] or 'medium',
                activity['notes'] or ''
            ))
    
    def clear_filters(self):
        """Xóa bộ lọc"""
        self.from_date_entry.delete(0, tk.END)
        self.from_date_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        self.to_date_entry.delete(0, tk.END)
        self.to_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.data_type_var.set("weight")
        self.refresh_data()
    
    def on_data_tab_changed(self, event):
        """Xử lý khi chuyển tab dữ liệu"""
        tab_index = self.data_notebook.index(self.data_notebook.select())
        if tab_index == 0:
            self.main_window.set_status("Đang xem lịch sử cân nặng")
        elif tab_index == 1:
            self.main_window.set_status("Đang xem lịch sử hoạt động")
    
    def show_weight_context_menu(self, event):
        """Hiển thị menu ngữ cảnh cho cân nặng"""
        item = self.weight_tree.identify_row(event.y)
        if item:
            self.weight_tree.selection_set(item)
            self.weight_context_menu.post(event.x_root, event.y_root)
    
    def show_activity_context_menu(self, event):
        """Hiển thị menu ngữ cảnh cho hoạt động"""
        item = self.activity_tree.identify_row(event.y)
        if item:
            self.activity_tree.selection_set(item)
            self.activity_context_menu.post(event.x_root, event.y_root)
    
    def view_weight_details(self):
        """Xem chi tiết bản ghi cân nặng"""
        selection = self.weight_tree.selection()
        if not selection:
            messagebox.showinfo("Thông báo", "Vui lòng chọn một bản ghi để xem chi tiết")
            return
        
        item = selection[0]
        values = self.weight_tree.item(item, 'values')
        
        details = f"""
📊 Chi tiết Cân nặng

📅 Ngày: {values[0]}
⚖️ Cân nặng: {values[1]} kg
🎯 Chỉ số BMI: {values[2]}
📈 Phân loại: {values[3]}
📝 Ghi chú: {values[4] or 'Không có'}
        """
        
        messagebox.showinfo("Chi tiết Cân nặng", details.strip())
    
    def view_activity_details(self):
        """Xem chi tiết bản ghi hoạt động"""
        selection = self.activity_tree.selection()
        if not selection:
            messagebox.showinfo("Thông báo", "Vui lòng chọn một bản ghi để xem chi tiết")
            return
        
        item = selection[0]
        values = self.activity_tree.item(item, 'values')
        
        details = f"""
🏃 Chi tiết Hoạt động

📅 Ngày: {values[0]}
🎯 Loại hoạt động: {values[1]}
⏱️ Thời gian: {values[2]} phút
🔥 Calories: {values[3]}
💪 Cường độ: {values[4]}
📝 Ghi chú: {values[5] or 'Không có'}
        """
        
        messagebox.showinfo("Chi tiết Hoạt động", details.strip())
    
    def delete_weight_record(self):
        """Xóa bản ghi cân nặng"""
        selection = self.weight_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.weight_tree.item(item, 'values')
        
        confirm = messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa bản ghi cân nặng ngày {values[0]}?\n"
            f"Cân nặng: {values[1]} kg"
        )
        
        if confirm:
            # Implement delete method in db_manager
            # For now, just remove from treeview
            self.weight_tree.delete(item)
            self.filter_status.config(text=f"Đã xóa bản ghi ngày {values[0]}", foreground='orange')
    
    def delete_activity_record(self):
        """Xóa bản ghi hoạt động"""
        selection = self.activity_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.activity_tree.item(item, 'values')
        
        confirm = messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa bản ghi hoạt động ngày {values[0]}?\n"
            f"Hoạt động: {values[1]}"
        )
        
        if confirm:
            # Implement delete method in db_manager  
            # For now, just remove from treeview
            self.activity_tree.delete(item)
            self.filter_status.config(text=f"Đã xóa bản ghi hoạt động ngày {values[0]}", foreground='orange')
    
    def export_data(self, data_type):
        """Xuất dữ liệu"""
        try:
            export_format = self.export_format_var.get()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if data_type == 'weight':
                filename = f"weight_data_{timestamp}.{export_format}"
                self.export_weight_data(filename, export_format)
            elif data_type == 'activity':
                filename = f"activity_data_{timestamp}.{export_format}"
                self.export_activity_data(filename, export_format)
            else:  # all
                filename = f"health_data_{timestamp}.{export_format}"
                self.export_all_data(filename, export_format)
            
            self.export_status.config(text=f"Đã xuất dữ liệu thành: {filename}", foreground='green')
            self.main_window.show_alert("Thành công", f"Đã xuất dữ liệu thành: {filename}")
            
        except Exception as e:
            self.logger.error(f"Error exporting data: {e}")
            self.export_status.config(text=f"Lỗi xuất dữ liệu: {e}", foreground='red')
    
    def export_weight_data(self, filename, format):
        """Xuất dữ liệu cân nặng"""
        weight_data = self.db.get_weight_records(self.user['user_id'], days=365)
        
        if format == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Ngày', 'Cân nặng (kg)', 'BMI', 'Phân loại', 'Ghi chú'])
                
                from utils.bmi_calculator import BMICalculator
                
                for record in weight_data:
                    category = BMICalculator.get_bmi_category(record['bmi'])
                    writer.writerow([
                        record['date'],
                        record['weight'],
                        record['bmi'],
                        category['category'],
                        record['notes'] or ''
                    ])
        else:  # json
            export_data = []
            from utils.bmi_calculator import BMICalculator
            
            for record in weight_data:
                category = BMICalculator.get_bmi_category(record['bmi'])
                export_data.append({
                    'date': record['date'],
                    'weight': record['weight'],
                    'bmi': record['bmi'],
                    'category': category['category'],
                    'risk_level': category['risk'],
                    'notes': record['notes']
                })
            
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(export_data, file, ensure_ascii=False, indent=2)
    
    def export_activity_data(self, filename, format):
        """Xuất dữ liệu hoạt động"""
        activity_data = self.db.get_activities(self.user['user_id'], days=365)
        
        if format == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Ngày', 'Loại hoạt động', 'Thời gian (phút)', 'Calories', 'Cường độ', 'Ghi chú'])
                
                for activity in activity_data:
                    writer.writerow([
                        activity['date'],
                        activity['activity_type'],
                        activity['duration'],
                        activity['calories_burned'] or '',
                        activity['intensity'] or '',
                        activity['notes'] or ''
                    ])
        else:  # json
            export_data = []
            for activity in activity_data:
                export_data.append({
                    'date': activity['date'],
                    'activity_type': activity['activity_type'],
                    'duration': activity['duration'],
                    'calories_burned': activity['calories_burned'],
                    'intensity': activity['intensity'],
                    'notes': activity['notes']
                })
            
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(export_data, file, ensure_ascii=False, indent=2)
    
    def export_all_data(self, filename, format):
        """Xuất tất cả dữ liệu"""
        # This would combine both weight and activity data
        # For simplicity, we'll create a zip file with both
        import zipfile
        
        weight_filename = f"weight_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        activity_filename = f"activity_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        
        self.export_weight_data(weight_filename, format)
        self.export_activity_data(activity_filename, format)
        
        # Create zip file
        with zipfile.ZipFile(filename, 'w') as zipf:
            zipf.write(weight_filename)
            zipf.write(activity_filename)
        
        # Clean up temporary files
        import os
        os.remove(weight_filename)
        os.remove(activity_filename)