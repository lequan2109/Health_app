# Temporary file containing sleep and heart rate functions to be added to input_tab.py

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
