# models/sleep.py
from datetime import datetime
from typing import Optional

class SleepRecord:
    """Model quản lý dữ liệu giấc ngủ"""
    
    # Chất lượng giấc ngủ
    QUALITY_OPTIONS = ["Rất tốt", "Tốt", "Trung bình", "Không tốt", "Rất không tốt"]
    
    def __init__(self, sleep_id: int = None, user_id: int = None, 
                 record_date: str = None, sleep_hours: float = 0,
                 sleep_quality: str = "Trung bình", notes: str = ""):
        self.sleep_id = sleep_id
        self.user_id = user_id
        self.record_date = record_date or datetime.now().strftime("%Y-%m-%d")
        self.sleep_hours = sleep_hours
        self.sleep_quality = sleep_quality
        self.notes = notes
    
    def to_dict(self) -> dict:
        """Chuyển thành dict"""
        return {
            'sleep_id': self.sleep_id,
            'user_id': self.user_id,
            'record_date': self.record_date,
            'sleep_hours': self.sleep_hours,
            'sleep_quality': self.sleep_quality,
            'notes': self.notes
        }
    
    def is_valid(self) -> bool:
        """Kiểm tra dữ liệu hợp lệ"""
        return (self.user_id and 
                0 <= self.sleep_hours <= 24 and
                self.sleep_quality in self.QUALITY_OPTIONS)
    
    def get_health_status(self) -> str:
        """Đánh giá tình trạng sức khỏe dựa trên giấc ngủ"""
        if self.sleep_hours < 6:
            return "Thiếu ngủ"
        elif self.sleep_hours < 7:
            return "Hơi thiếu ngủ"
        elif self.sleep_hours <= 9:
            return "Bình thường"
        else:
            return "Ngủ quá nhiều"
