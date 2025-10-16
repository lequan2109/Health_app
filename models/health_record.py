# models/health_record.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .user import User

@dataclass
class WeightRecord:
    """Lớp đại diện cho bản ghi cân nặng"""
    record_id: int
    user_id: int
    record_date: str
    weight: float
    bmi: Optional[float] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    
    def __post_init__(self):
        """Khởi tạo sau khi tạo object"""
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> dict:
        """Chuyển đổi thành dictionary"""
        return {
            'record_id': self.record_id,
            'user_id': self.user_id,
            'record_date': self.record_date,
            'weight': self.weight,
            'bmi': self.bmi,
            'notes': self.notes,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'WeightRecord':
        """Tạo WeightRecord từ dictionary"""
        return cls(
            record_id=data.get('record_id'),
            user_id=data.get('user_id'),
            record_date=data.get('record_date'),
            weight=data.get('weight'),
            bmi=data.get('bmi'),
            notes=data.get('notes'),
            created_at=data.get('created_at')
        )

@dataclass
class ActivityRecord:
    """Lớp đại diện cho bản ghi hoạt động"""
    activity_id: int
    user_id: int
    activity_date: str
    activity_type: str
    duration: int
    calories_burned: Optional[float] = None
    intensity: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    
    def __post_init__(self):
        """Khởi tạo sau khi tạo object"""
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def calories_per_minute(self) -> float:
        """Calories đốt cháy mỗi phút"""
        if self.duration > 0:
            return self.calories_burned / self.duration if self.calories_burned else 0
        return 0
    
    def to_dict(self) -> dict:
        """Chuyển đổi thành dictionary"""
        return {
            'activity_id': self.activity_id,
            'user_id': self.user_id,
            'activity_date': self.activity_date,
            'activity_type': self.activity_type,
            'duration': self.duration,
            'calories_burned': self.calories_burned,
            'intensity': self.intensity,
            'notes': self.notes,
            'created_at': self.created_at,
            'calories_per_minute': self.calories_per_minute
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ActivityRecord':
        """Tạo ActivityRecord từ dictionary"""
        return cls(
            activity_id=data.get('activity_id'),
            user_id=data.get('user_id'),
            activity_date=data.get('activity_date'),
            activity_type=data.get('activity_type'),
            duration=data.get('duration'),
            calories_burned=data.get('calories_burned'),
            intensity=data.get('intensity'),
            notes=data.get('notes'),
            created_at=data.get('created_at')
        )

@dataclass
class HealthGoal:
    """Lớp đại diện cho mục tiêu sức khỏe"""
    goal_id: int
    user_id: int
    goal_type: str
    target_value: float
    current_value: Optional[float] = None
    deadline: Optional[str] = None
    status: str = 'active'
    created_at: Optional[str] = None
    
    def __post_init__(self):
        """Khởi tạo sau khi tạo object"""
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def progress(self) -> float:
        """Tiến độ hoàn thành mục tiêu"""
        if self.current_value is None or self.target_value == 0:
            return 0.0
        
        if self.goal_type in ['weight_loss', 'bmi_reduction']:
            # For reduction goals, progress is based on current vs start
            return min((self.current_value / self.target_value) * 100, 100)
        else:
            # For achievement goals
            return min((self.current_value / self.target_value) * 100, 100)
    
    @property
    def days_remaining(self) -> Optional[int]:
        """Số ngày còn lại đến deadline"""
        if not self.deadline:
            return None
        
        try:
            deadline_dt = datetime.strptime(self.deadline, '%Y-%m-%d')
            today = datetime.now()
            remaining = (deadline_dt - today).days
            return max(remaining, 0)
        except ValueError:
            return None
    
    def to_dict(self) -> dict:
        """Chuyển đổi thành dictionary"""
        return {
            'goal_id': self.goal_id,
            'user_id': self.user_id,
            'goal_type': self.goal_type,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'deadline': self.deadline,
            'status': self.status,
            'created_at': self.created_at,
            'progress': self.progress,
            'days_remaining': self.days_remaining
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'HealthGoal':
        """Tạo HealthGoal từ dictionary"""
        return cls(
            goal_id=data.get('goal_id'),
            user_id=data.get('user_id'),
            goal_type=data.get('goal_type'),
            target_value=data.get('target_value'),
            current_value=data.get('current_value'),
            deadline=data.get('deadline'),
            status=data.get('status', 'active'),
            created_at=data.get('created_at')
        )