# gui/components/history_tab.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import logging
import csv
import json
import os
from utils.bmi_calculator import BMICalculator

class HistoryTab:
    """Tab lịch sử và xuất dữ liệu"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.db = main_window.db
        self.user = main_window.user
        self.logger = logging.getLogger(__name__)
        
        # Khởi tạo biến định dạng xuất file (Mặc định CSV)
        self.export_format_var = tk.StringVar(value="csv")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        self.frame = ttk.Frame(self.parent)
        
        # 1. PHẦN ĐIỀU KHIỂN TRÊN CÙNG (Chia đôi trái/phải)
        self.setup_top_section()
        
        # 2. PHẦN HIỂN THỊ DỮ LIỆU (Ở dưới)
        self.setup_data_display()
    
    def setup_top_section(self):
        """Thiết lập khu vực điều khiển phía trên (Filter + Export)"""
        top_container = ttk.Frame(self.frame)
        top_container.pack(fill=tk.X, padx=10, pady=10)
        
        # --- PHẦN TRÁI: BỘ LỌC (Chiếm không gian chính) ---
        filter_frame = ttk.LabelFrame(top_container, text="🔍 Bộ lọc Dữ liệu", padding="5")
        filter_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Hàng 1: Chọn ngày
        date_frame = ttk.Frame(filter_frame)
        date_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(date_frame, text="Từ:").pack(side=tk.LEFT)
        self.from_date_entry = ttk.Entry(date_frame, width=10)
        self.from_date_entry.pack(side=tk.LEFT, padx=5)
        self.from_date_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        
        ttk.Label(date_frame, text="Đến:").pack(side=tk.LEFT, padx=(10, 0))
        self.to_date_entry = ttk.Entry(date_frame, width=10)
        self.to_date_entry.pack(side=tk.LEFT, padx=5)
        self.to_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Hàng 2: Loại dữ liệu + Nút lọc
        action_frame = ttk.Frame(filter_frame)
        action_frame.pack(fill=tk.X, pady=5)
        
        self.data_type_var = tk.StringVar(value="weight")
        # Radio buttons nhỏ gọn
        ttk.Radiobutton(action_frame, text="Cân nặng", variable=self.data_type_var, 
                       value="weight", command=self.refresh_data).pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(action_frame, text="Hoạt động", variable=self.data_type_var, 
                       value="activity", command=self.refresh_data).pack(side=tk.LEFT, padx=2)
        
        # Nút lọc và xóa nằm cùng hàng để tiết kiệm chỗ
        ttk.Button(action_frame, text="Tải lại", width=8,
                  command=self.refresh_data).pack(side=tk.LEFT, padx=(10, 2))
        ttk.Button(action_frame, text="Xóa lọc", width=8,
                  command=self.clear_filters).pack(side=tk.LEFT, padx=2)

        # --- PHẦN PHẢI: XUẤT DỮ LIỆU (Gọn gàng) ---
        export_frame = ttk.LabelFrame(top_container, text="💾 Xuất file", padding="5")
        export_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        
        # Chọn định dạng (CSV/JSON)
        format_frame = ttk.Frame(export_frame)
        format_frame.pack(fill=tk.X)
        ttk.Radiobutton(format_frame, text="CSV (Excel)", variable=self.export_format_var, 
                       value="csv").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="JSON", variable=self.export_format_var, 
                       value="json").pack(side=tk.LEFT, padx=5)
        
        # NÚT MENU XUẤT DỮ LIỆU (1 Nút duy nhất xổ xuống)
        self.export_btn = ttk.Menubutton(export_frame, text="⬇️ Tải xuống dữ liệu", direction='below', style='Accent.TButton')
        
        # Tạo menu con
        export_menu = tk.Menu(self.export_btn, tearoff=0)
        export_menu.add_command(label="📊 Xuất Cân nặng", command=lambda: self.export_data('weight'))
        export_menu.add_command(label="🏃 Xuất Hoạt động", command=lambda: self.export_data('activity'))
        export_menu.add_separator()
        export_menu.add_command(label="📦 Xuất Tất cả (.zip)", command=lambda: self.export_data('all'))
        
        # Gán menu vào nút
        self.export_btn.configure(menu=export_menu)
        self.export_btn.pack(fill=tk.X, pady=(5, 0))
        
        # Status nhỏ
        self.filter_status = ttk.Label(export_frame, text="Sẵn sàng", font=('Arial', 8), foreground='gray')
        self.filter_status.pack(anchor=tk.E)

    def setup_data_display(self):
        """Thiết lập hiển thị dữ liệu"""
        # Notebook for different data types
        self.data_notebook = ttk.Notebook(self.frame)
        self.data_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Weight history tab
        self.weight_tab = ttk.Frame(self.data_notebook)
        self.data_notebook.add(self.weight_tab, text="⚖️ Cân nặng")
        
        # Activity history tab  
        self.activity_tab = ttk.Frame(self.data_notebook)
        self.data_notebook.add(self.activity_tab, text="🏃 Hoạt động")
        
        self.setup_weight_tab()
        self.setup_activity_tab()
        
        self.data_notebook.bind('<<NotebookTabChanged>>', self.on_data_tab_changed)
    
    def setup_weight_tab(self):
        columns = ('date', 'weight', 'bmi', 'category', 'notes')
        self.weight_tree = ttk.Treeview(self.weight_tab, columns=columns, show='headings', height=15)
        
        self.weight_tree.heading('date', text='Ngày')
        self.weight_tree.heading('weight', text='Cân nặng (kg)')
        self.weight_tree.heading('bmi', text='BMI')
        self.weight_tree.heading('category', text='Phân loại')
        self.weight_tree.heading('notes', text='Ghi chú')
        
        self.weight_tree.column('date', width=100, anchor='center')
        self.weight_tree.column('weight', width=100, anchor='center')
        self.weight_tree.column('bmi', width=80, anchor='center')
        self.weight_tree.column('category', width=120, anchor='center')
        self.weight_tree.column('notes', width=200)
        
        weight_scrollbar = ttk.Scrollbar(self.weight_tab, orient="vertical", command=self.weight_tree.yview)
        self.weight_tree.configure(yscrollcommand=weight_scrollbar.set)
        
        self.weight_tree.pack(side="left", fill="both", expand=True)
        weight_scrollbar.pack(side="right", fill="y")
        
        self.setup_weight_context_menu()
    
    def setup_activity_tab(self):
        activity_columns = ('date', 'type', 'duration', 'calories', 'intensity', 'notes')
        self.activity_tree = ttk.Treeview(self.activity_tab, columns=activity_columns, show='headings', height=15)
        
        self.activity_tree.heading('date', text='Ngày')
        self.activity_tree.heading('type', text='Loại hoạt động')
        self.activity_tree.heading('duration', text='Thời gian (phút)')
        self.activity_tree.heading('calories', text='Calories')
        self.activity_tree.heading('intensity', text='Cường độ')
        self.activity_tree.heading('notes', text='Ghi chú')
        
        self.activity_tree.column('date', width=100, anchor='center')
        self.activity_tree.column('type', width=120, anchor='center')
        self.activity_tree.column('duration', width=100, anchor='center')
        self.activity_tree.column('calories', width=80, anchor='center')
        self.activity_tree.column('intensity', width=80, anchor='center')
        self.activity_tree.column('notes', width=200)
        
        activity_scrollbar = ttk.Scrollbar(self.activity_tab, orient="vertical", command=self.activity_tree.yview)
        self.activity_tree.configure(yscrollcommand=activity_scrollbar.set)
        
        self.activity_tree.pack(side="left", fill="both", expand=True)
        activity_scrollbar.pack(side="right", fill="y")
        
        self.setup_activity_context_menu()
    
    def setup_weight_context_menu(self):
        self.weight_context_menu = tk.Menu(self.weight_tree, tearoff=0)
        self.weight_context_menu.add_command(label="Xem chi tiết", command=self.view_weight_details)
        self.weight_context_menu.add_command(label="Xóa bản ghi", command=self.delete_weight_record)
        self.weight_tree.bind("<Button-3>", self.show_weight_context_menu)
    
    def setup_activity_context_menu(self):
        self.activity_context_menu = tk.Menu(self.activity_tree, tearoff=0)
        self.activity_context_menu.add_command(label="Xem chi tiết", command=self.view_activity_details)
        self.activity_context_menu.add_command(label="Xóa bản ghi", command=self.delete_activity_record)
        self.activity_tree.bind("<Button-3>", self.show_activity_context_menu)

    # --- CÁC HÀM LOGIC (GIỮ NGUYÊN) ---

    def refresh_data(self):
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
            
            if data_type in ['weight', 'all']:
                self.load_weight_data(from_date, to_date)
            
            if data_type in ['activity', 'all']:
                self.load_activity_data(from_date, to_date)
            
            record_count = len(self.weight_tree.get_children()) + len(self.activity_tree.get_children())
            self.filter_status.config(text=f"Tải {record_count} bản ghi", foreground='green')
            
            if data_type == 'weight':
                self.data_notebook.select(0)
            elif data_type == 'activity':
                self.data_notebook.select(1)
                
            self.logger.info(f"Refreshed history data: {data_type}")
            
        except Exception as e:
            self.logger.error(f"Error refreshing: {e}")
            self.filter_status.config(text="Lỗi tải dữ liệu", foreground='red')

    def load_weight_data(self, from_date=None, to_date=None):
        for item in self.weight_tree.get_children():
            self.weight_tree.delete(item)
        
        if from_date and to_date:
            weight_data = self.db.get_weight_history(self.user['user_id'], from_date, to_date)
        else:
            weight_data = self.db.get_weight_records(self.user['user_id'], days=365)
        
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
        for item in self.activity_tree.get_children():
            self.activity_tree.delete(item)
        
        if from_date and to_date:
            activity_data = self.db.get_activities(self.user['user_id'], days=365)
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
        self.from_date_entry.delete(0, tk.END)
        self.from_date_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        self.to_date_entry.delete(0, tk.END)
        self.to_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.data_type_var.set("weight")
        self.refresh_data()

    def on_data_tab_changed(self, event):
        pass

    def show_weight_context_menu(self, event):
        item = self.weight_tree.identify_row(event.y)
        if item:
            self.weight_tree.selection_set(item)
            self.weight_context_menu.post(event.x_root, event.y_root)

    def show_activity_context_menu(self, event):
        item = self.activity_tree.identify_row(event.y)
        if item:
            self.activity_tree.selection_set(item)
            self.activity_context_menu.post(event.x_root, event.y_root)

    def view_weight_details(self):
        selection = self.weight_tree.selection()
        if not selection: return
        item = selection[0]
        values = self.weight_tree.item(item, 'values')
        details = f"Ngày: {values[0]}\nCân nặng: {values[1]} kg\nBMI: {values[2]}\nGhi chú: {values[4]}"
        messagebox.showinfo("Chi tiết Cân nặng", details)

    def delete_weight_record(self):
        selection = self.weight_tree.selection()
        if not selection: return
        item = selection[0]
        if messagebox.askyesno("Xác nhận xóa", "Bạn có chắc muốn xóa bản ghi này?"):
            self.weight_tree.delete(item)
            # Note: Cần implement db.delete_weight(id) để xóa thật trong DB

    def view_activity_details(self):
        selection = self.activity_tree.selection()
        if not selection: return
        item = selection[0]
        values = self.activity_tree.item(item, 'values')
        details = f"Ngày: {values[0]}\nMôn: {values[1]}\nThời gian: {values[2]} phút\nGhi chú: {values[5]}"
        messagebox.showinfo("Chi tiết Hoạt động", details)

    def delete_activity_record(self):
        selection = self.activity_tree.selection()
        if not selection: return
        item = selection[0]
        if messagebox.askyesno("Xác nhận xóa", "Bạn có chắc muốn xóa bản ghi này?"):
            self.activity_tree.delete(item)

    def export_data(self, data_type):
        try:
            export_format = self.export_format_var.get()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Xác định tên file và loại file
            if export_format == 'csv':
                file_types = [('CSV files', '*.csv'), ('All files', '*.*')]
                default_ext = '.csv'
            else:
                file_types = [('JSON files', '*.json'), ('All files', '*.*')]
                default_ext = '.json'
                
            if data_type == 'all':
                default_ext = '.zip'
                file_types = [('ZIP files', '*.zip'), ('All files', '*.*')]

            default_filename = f"health_{data_type}_{timestamp}{default_ext}"
            
            file_path = filedialog.asksaveasfilename(
                title=f"Lưu dữ liệu {data_type}",
                defaultextension=default_ext,
                initialfile=default_filename,
                filetypes=file_types
            )
            
            if not file_path: return
            
            success = False
            if data_type == 'weight':
                success = self.export_weight_data(file_path, export_format)
            elif data_type == 'activity':
                success = self.export_activity_data(file_path, export_format)
            else:
                success = self.export_all_data(file_path, export_format)
            
            if success:
                filename = os.path.basename(file_path)
                self.main_window.show_alert("Thành công", f"Đã xuất file:\n{filename}")
                self.filter_status.config(text=f"Đã xuất: {filename}", foreground='green')
            else:
                self.main_window.show_alert("Lỗi", "Xuất file thất bại", "error")
                
        except Exception as e:
            self.logger.error(f"Error exporting: {e}")
            messagebox.showerror("Lỗi", f"Lỗi xuất file: {e}")

    def export_weight_data(self, file_path, format):
        try:
            weight_data = self.db.get_weight_records(self.user['user_id'], days=365)
            if not weight_data: return False
            
            if format == 'csv':
                with open(file_path, 'w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Ngày', 'Cân nặng', 'BMI', 'Phân loại', 'Ghi chú'])
                    for r in weight_data:
                        cat = BMICalculator.get_bmi_category(r['bmi'])['category']
                        writer.writerow([r['date'], r['weight'], r['bmi'], cat, r['notes'] or ''])
            else:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(weight_data, file, ensure_ascii=False, indent=2)
            return True
        except Exception: return False

    def export_activity_data(self, file_path, format):
        try:
            activity_data = self.db.get_activities(self.user['user_id'], days=365)
            if not activity_data: return False
            
            if format == 'csv':
                with open(file_path, 'w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Ngày', 'Môn', 'Phút', 'Calo', 'Cường độ', 'Ghi chú'])
                    for a in activity_data:
                        writer.writerow([a['date'], a['activity_type'], a['duration'], a['calories_burned'], a['intensity'], a['notes'] or ''])
            else:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(activity_data, file, ensure_ascii=False, indent=2)
            return True
        except Exception: return False

    def export_all_data(self, file_path, format):
        try:
            import zipfile, tempfile
            with tempfile.TemporaryDirectory() as temp_dir:
                ts = datetime.now().strftime("%Y%m%d")
                w_path = os.path.join(temp_dir, f"weight_{ts}.{format}")
                a_path = os.path.join(temp_dir, f"activity_{ts}.{format}")
                
                self.export_weight_data(w_path, format)
                self.export_activity_data(a_path, format)
                
                with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(w_path, os.path.basename(w_path))
                    zipf.write(a_path, os.path.basename(a_path))
            return True
        except Exception as e:
            self.logger.error(str(e))
            return False