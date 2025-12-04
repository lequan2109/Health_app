# These methods should be added to dashboard_tab.py

def setup_sleep_content(self, parent):
    """Thiết lập nội dung giấc ngủ"""
    try:
        # Get sleep data for the current week
        sleep_records = self.db.get_sleep_records(self.user['user_id'], days=7)
        
        if not sleep_records:
            ttk.Label(parent, text="Chưa có dữ liệu giấc ngủ", 
                     font=('Arial', 10), foreground='gray').pack(pady=20)
            return
        
        # Calculate statistics
        sleep_hours = [r['sleep_hours'] for r in sleep_records]
        avg_sleep = sum(sleep_hours) / len(sleep_hours)
        
        # Display average sleep
        stats_frame = ttk.Frame(parent)
        stats_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(stats_frame, text=f"Trung bình tuần: {avg_sleep:.1f} giờ", 
                 font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Sleep status
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
        
        # Quality distribution
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
            
            # Progress bar
            bar = ttk.Progressbar(bar_frame, length=150, mode='determinate', value=pct)
            bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Latest entry
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
        # Get heart rate data
        latest_hr = self.db.get_latest_heart_rate(self.user['user_id'])
        
        if not latest_hr:
            ttk.Label(parent, text="Chưa có dữ liệu nhịp tim", 
                     font=('Arial', 10), foreground='gray').pack(pady=20)
            return
        
        from models.heart_rate import HeartRateRecord
        
        # Display latest heart rate
        stats_frame = ttk.Frame(parent)
        stats_frame.pack(fill=tk.X, pady=10)
        
        bpm = latest_hr['bpm']
        ttk.Label(stats_frame, text=f"Nhịp tim: {bpm} BPM", 
                 font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Create HR record for status evaluation
        hr_rec = HeartRateRecord(
            user_id=latest_hr['user_id'],
            record_date=latest_hr['record_date'],
            record_time=latest_hr['record_time'],
            bpm=bpm,
            activity_type=latest_hr['activity_type']
        )
        status = hr_rec.get_health_status()
        
        # Color based on status
        if "Quá chậm" in status or "Quá nhanh" in status:
            color = "#e74c3c"
        elif "Chậm" in status or "Hơi nhanh" in status:
            color = "#f39c12"
        else:
            color = "#27ae60"
        
        ttk.Label(stats_frame, text=status, font=('Arial', 11, 'bold'),
                 foreground=color).pack(side=tk.RIGHT, padx=5)
        
        # Activity type and time
        details_frame = ttk.Frame(parent)
        details_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(details_frame, text=f"⏰ {latest_hr['record_time']} | "
                 f"📍 {latest_hr['activity_type']}", 
                 font=('Arial', 10)).pack(anchor=tk.W)
        
        # Average HR for the week
        avg_hr = self.db.get_average_heart_rate(self.user['user_id'], days=7)
        if avg_hr > 0:
            avg_frame = ttk.LabelFrame(parent, text="Thống kê tuần", padding="10")
            avg_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(avg_frame, text=f"Trung bình: {int(avg_hr)} BPM", 
                     font=('Arial', 10)).pack(anchor=tk.W)
        
        # Recent measurements
        recent_records = self.db.get_heart_rate_records(self.user['user_id'], days=7)
        if recent_records:
            recent_frame = ttk.LabelFrame(parent, text="Đo gần đây (7 ngày)", padding="10")
            recent_frame.pack(fill=tk.X, pady=5)
            
            # Show last 5 measurements
            for i, record in enumerate(recent_records[:5]):
                ttk.Label(recent_frame, 
                         text=f"{record['record_date']} {record['record_time']}: "
                              f"{record['bpm']} BPM ({record['activity_type']})", 
                         font=('Arial', 9)).pack(anchor=tk.W, pady=2)
            
    except Exception as e:
        self.logger.error(f"Error setting up heart rate content: {e}")
        ttk.Label(parent, text=f"Lỗi: {e}", foreground='red').pack()
