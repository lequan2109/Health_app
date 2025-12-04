# models/heart_rate.py
from datetime import datetime
from typing import Optional

class HeartRateRecord:
    """Model quản lý dữ liệu nhịp tim"""
    
    # Loại hoạt động
    ACTIVITY_TYPES = ["Nghỉ ngơi", "Nhẹ", "Vừa", "Mạnh", "Tập luyện"]
    
    # Bảng đánh giá nhịp tim theo độ tuổi
    NORMAL_RANGES = {
        "child": (70, 100),      # Trẻ em
        "adult": (60, 100),      # Người lớn
        "athlete": (40, 60),     # Vận động viên
    }
    
    def __init__(self, heart_rate_id: int = None, user_id: int = None,
                 record_date: str = None, record_time: str = None,
                 bpm: int = 0, activity_type: str = "Nghỉ ngơi", notes: str = ""):
        self.heart_rate_id = heart_rate_id
        self.user_id = user_id
        self.record_date = record_date or datetime.now().strftime("%Y-%m-%d")
        self.record_time = record_time or datetime.now().strftime("%H:%M:%S")
        self.bpm = bpm
        self.activity_type = activity_type
        self.notes = notes
    
    def to_dict(self) -> dict:
        """Chuyển thành dict"""
        return {
            'heart_rate_id': self.heart_rate_id,
            'user_id': self.user_id,
            'record_date': self.record_date,
            'record_time': self.record_time,
            'bpm': self.bpm,
            'activity_type': self.activity_type,
            'notes': self.notes
        }
    
    def is_valid(self) -> bool:
        """Kiểm tra dữ liệu hợp lệ"""
        return (self.user_id and 
                30 <= self.bpm <= 200 and
                self.activity_type in self.ACTIVITY_TYPES)
    
    def get_health_status(self) -> str:
        """Đánh giá tình trạng sức khỏe dựa trên nhịp tim"""
        if self.bpm < 40:
            return "Quá chậm (Bradycardia)"
        elif self.bpm < 60:
            return "Chậm"
        elif self.bpm <= 100:
            return "Bình thường"
        elif self.bpm <= 120:
            return "Hơi nhanh"
        else:
            return "Quá nhanh (Tachycardia)"
