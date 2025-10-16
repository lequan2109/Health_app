# models/user.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """Lớp đại diện cho người dùng"""
    user_id: int
    username: str
    password: str
    full_name: str
    height: float
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    created_at: Optional[str] = None
    
    def __post_init__(self):
        """Khởi tạo sau khi tạo object"""
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def age(self) -> Optional[int]:
        """Tính tuổi từ ngày sinh"""
        if not self.birth_date:
            return None
        
        try:
            birth_dt = datetime.strptime(self.birth_date, '%Y-%m-%d')
            today = datetime.now()
            age = today.year - birth_dt.year
            
            # Adjust if birthday hasn't occurred this year
            if today.month < birth_dt.month or (today.month == birth_dt.month and today.day < birth_dt.day):
                age -= 1
            
            return age
        except ValueError:
            return None
    
    @property
    def height_in_meters(self) -> float:
        """Chiều cao tính bằng mét"""
        return self.height / 100
    
    def to_dict(self) -> dict:
        """Chuyển đổi thành dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'full_name': self.full_name,
            'height': self.height,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'created_at': self.created_at,
            'age': self.age
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Tạo User từ dictionary"""
        return cls(
            user_id=data.get('user_id'),
            username=data.get('username'),
            password=data.get('password', ''),
            full_name=data.get('full_name'),
            height=data.get('height', 170.0),
            birth_date=data.get('birth_date'),
            gender=data.get('gender'),
            created_at=data.get('created_at')
        )