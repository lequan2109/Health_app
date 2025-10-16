# utils/validators.py
import re
from datetime import datetime
from typing import Dict, Tuple

class HealthDataValidator:
    """Lớp validation cho dữ liệu sức khỏe"""
    
    @staticmethod
    def validate_weight(weight: float) -> Tuple[bool, str]:
        """
        Validate cân nặng
        
        Args:
            weight: Cân nặng (kg)
            
        Returns:
            Tuple (is_valid, message)
        """
        if not isinstance(weight, (int, float)):
            return False, "Cân nặng phải là số"
        
        if weight < 20 or weight > 300:
            return False, "Cân nặng phải từ 20-300 kg"
        
        return True, "Hợp lệ"
    
    @staticmethod
    def validate_height(height: float) -> Tuple[bool, str]:
        """
        Validate chiều cao
        
        Args:
            height: Chiều cao (cm)
            
        Returns:
            Tuple (is_valid, message)
        """
        if not isinstance(height, (int, float)):
            return False, "Chiều cao phải là số"
        
        if height < 50 or height > 250:
            return False, "Chiều cao phải từ 50-250 cm"
        
        return True, "Hợp lệ"
    
    @staticmethod
    def validate_activity_duration(duration: int) -> Tuple[bool, str]:
        """
        Validate thời gian hoạt động
        
        Args:
            duration: Thời gian (phút)
            
        Returns:
            Tuple (is_valid, message)
        """
        if not isinstance(duration, int):
            return False, "Thời gian phải là số nguyên"
        
        if duration < 1 or duration > 480:
            return False, "Thời gian hoạt động phải từ 1-480 phút"
        
        return True, "Hợp lệ"
    
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        """
        Validate định dạng ngày tháng
        
        Args:
            date_str: Chuỗi ngày tháng (YYYY-MM-DD)
            
        Returns:
            Tuple (is_valid, message)
        """
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True, "Hợp lệ"
        except ValueError:
            return False, "Định dạng ngày không hợp lệ (YYYY-MM-DD)"
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """
        Validate tên đăng nhập
        
        Args:
            username: Tên đăng nhập
            
        Returns:
            Tuple (is_valid, message)
        """
        if not username:
            return False, "Tên đăng nhập không được để trống"
        
        if len(username) < 3:
            return False, "Tên đăng nhập phải có ít nhất 3 ký tự"
        
        if len(username) > 20:
            return False, "Tên đăng nhập không được quá 20 ký tự"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Tên đăng nhập chỉ được chứa chữ cái, số và dấu gạch dưới"
        
        return True, "Hợp lệ"
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate mật khẩu
        
        Args:
            password: Mật khẩu
            
        Returns:
            Tuple (is_valid, message)
        """
        if not password:
            return False, "Mật khẩu không được để trống"
        
        if len(password) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự"
        
        if len(password) > 50:
            return False, "Mật khẩu quá dài"
        
        return True, "Hợp lệ"
    
    @staticmethod
    def validate_full_name(full_name: str) -> Tuple[bool, str]:
        """
        Validate họ tên
        
        Args:
            full_name: Họ và tên
            
        Returns:
            Tuple (is_valid, message)
        """
        if not full_name:
            return False, "Họ tên không được để trống"
        
        if len(full_name) < 2:
            return False, "Họ tên quá ngắn"
        
        if len(full_name) > 50:
            return False, "Họ tên quá dài"
        
        # Kiểm tra ký tự đặc biệt
        if re.search(r'[0-9!@#$%^&*()_+=\[\]{};\':"\\|,.<>?]', full_name):
            return False, "Họ tên không được chứa số hoặc ký tự đặc biệt"
        
        return True, "Hợp lệ"
    
    @staticmethod
    def validate_gender(gender: str) -> Tuple[bool, str]:
        """
        Validate giới tính
        
        Args:
            gender: Giới tính
            
        Returns:
            Tuple (is_valid, message)
        """
        if not gender:
            return True, "Hợp lệ"  # Giới tính có thể để trống
        
        valid_genders = ['Nam', 'Nữ', 'Khác']
        if gender not in valid_genders:
            return False, f"Giới tính phải là: {', '.join(valid_genders)}"
        
        return True, "Hợp lệ"
    
    @staticmethod
    def validate_birth_date(birth_date: str) -> Tuple[bool, str]:
        """
        Validate ngày sinh
        
        Args:
            birth_date: Ngày sinh (YYYY-MM-DD)
            
        Returns:
            Tuple (is_valid, message)
        """
        if not birth_date:
            return True, "Hợp lệ"  # Ngày sinh có thể để trống
        
        # Validate định dạng
        is_valid, message = HealthDataValidator.validate_date(birth_date)
        if not is_valid:
            return False, message
        
        # Validate ngày sinh hợp lý
        try:
            birth_dt = datetime.strptime(birth_date, '%Y-%m-%d')
            today = datetime.now()
            
            if birth_dt > today:
                return False, "Ngày sinh không thể ở tương lai"
            
            age = today.year - birth_dt.year
            if age > 120:
                return False, "Ngày sinh không hợp lệ"
            
            return True, "Hợp lệ"
            
        except ValueError:
            return False, "Ngày sinh không hợp lệ"
    
    @staticmethod
    def validate_activity_type(activity_type: str) -> Tuple[bool, str]:
        """
        Validate loại hoạt động
        
        Args:
            activity_type: Loại hoạt động
            
        Returns:
            Tuple (is_valid, message)
        """
        if not activity_type:
            return False, "Loại hoạt động không được để trống"
        
        valid_activities = [
            'Đi bộ', 'Chạy bộ', 'Đạp xe', 'Bơi lội', 
            'Gym', 'Yoga', 'Nhảy dây', 'Leo cầu thang'
        ]
        
        if activity_type not in valid_activities:
            return False, f"Loại hoạt động phải là: {', '.join(valid_activities)}"
        
        return True, "Hợp lệ"
    
    @staticmethod
    def validate_intensity(intensity: str) -> Tuple[bool, str]:
        """
        Validate cường độ hoạt động
        
        Args:
            intensity: Cường độ
            
        Returns:
            Tuple (is_valid, message)
        """
        if not intensity:
            return True, "Hợp lệ"  # Có thể để trống
        
        valid_intensities = ['low', 'medium', 'high']
        if intensity not in valid_intensities:
            return False, f"Cường độ phải là: {', '.join(valid_intensities)}"
        
        return True, "Hợp lệ"
    
    @staticmethod
    def validate_health_data(weight: float = None, height: float = None, 
                           duration: int = None, date: str = None) -> Dict[str, Tuple[bool, str]]:
        """
        Validate nhiều trường dữ liệu cùng lúc
        
        Args:
            weight: Cân nặng
            height: Chiều cao  
            duration: Thời gian hoạt động
            date: Ngày tháng
            
        Returns:
            Dict chứa kết quả validation cho từng trường
        """
        results = {}
        
        if weight is not None:
            results['weight'] = HealthDataValidator.validate_weight(weight)
        
        if height is not None:
            results['height'] = HealthDataValidator.validate_height(height)
        
        if duration is not None:
            results['duration'] = HealthDataValidator.validate_activity_duration(duration)
        
        if date is not None:
            results['date'] = HealthDataValidator.validate_date(date)
        
        return results
    
    @staticmethod
    def validate_user_registration(username: str, password: str, full_name: str, 
                                 height: float = None) -> Dict[str, Tuple[bool, str]]:
        """
        Validate dữ liệu đăng ký user
        
        Args:
            username: Tên đăng nhập
            password: Mật khẩu
            full_name: Họ tên
            height: Chiều cao
            
        Returns:
            Dict chứa kết quả validation
        """
        results = {
            'username': HealthDataValidator.validate_username(username),
            'password': HealthDataValidator.validate_password(password),
            'full_name': HealthDataValidator.validate_full_name(full_name)
        }
        
        if height is not None:
            results['height'] = HealthDataValidator.validate_height(height)
        
        return results