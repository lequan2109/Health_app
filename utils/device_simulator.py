# utils/device_simulator.py
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List
from .bmi_calculator import BMICalculator

class HealthDeviceSimulator:
    """Lớp giả lập thiết bị đo sức khỏe"""
    
    def __init__(self, user_height: float, initial_weight: float = 65.0):
        """
        Khởi tạo simulator
        
        Args:
            user_height: Chiều cao người dùng (cm)
            initial_weight: Cân nặng ban đầu (kg)
        """
        self.user_height = user_height / 100  # Chuyển sang mét
        self.last_weight = initial_weight
        self.activity_intensity = "medium"  # low, medium, high
        self.logger = logging.getLogger(__name__)
        
        # Calorie burn rates (calories per minute)
        self.calorie_rates = {
            "Đi bộ": {"low": 4, "medium": 5, "high": 6},
            "Chạy bộ": {"low": 8, "medium": 10, "high": 12},
            "Đạp xe": {"low": 6, "medium": 8, "high": 10},
            "Bơi lội": {"low": 7, "medium": 9, "high": 11},
            "Gym": {"low": 5, "medium": 7, "high": 9},
            "Yoga": {"low": 3, "medium": 4, "high": 5},
            "Nhảy dây": {"low": 9, "medium": 11, "high": 13},
            "Leo cầu thang": {"low": 7, "medium": 9, "high": 11}
        }
    
    def set_activity_intensity(self, intensity: str):
        """Thiết lập cường độ hoạt động"""
        if intensity in ["low", "medium", "high"]:
            self.activity_intensity = intensity
            self.logger.info(f"Activity intensity set to: {intensity}")
    
    def generate_weight_measurement(self, trend: str = "stable") -> Dict[str, float]:
        """
        Tạo dữ liệu cân nặng giả lập
        
        Args:
            trend: Xu hướng cân nặng - "stable", "loss", "gain"
            
        Returns:
            Dict chứa thông tin cân nặng và BMI
        """
        try:
            # Biến động dựa trên xu hướng
            if trend == "loss":
                base_change = random.uniform(-0.8, -0.1)  # Giảm cân
            elif trend == "gain":
                base_change = random.uniform(0.1, 0.8)    # Tăng cân
            else:  # stable
                base_change = random.uniform(-0.3, 0.3)   # Ổn định
            
            # Thêm nhiễu ngẫu nhiên
            noise = random.uniform(-0.2, 0.2)
            weight_change = base_change + noise
            
            # Giới hạn thay đổi tối đa
            weight_change = max(min(weight_change, 1.0), -1.0)
            
            new_weight = round(self.last_weight + weight_change, 1)
            self.last_weight = new_weight
            
            # Tính BMI
            bmi = BMICalculator.calculate_bmi(new_weight, self.user_height)
            
            measurement = {
                'weight': new_weight,
                'bmi': bmi,
                'timestamp': datetime.now(),
                'trend': '↔️' if abs(weight_change) < 0.1 else '⬇️' if weight_change < 0 else '⬆️'
            }
            
            self.logger.info(f"Generated weight measurement: {new_weight}kg, BMI: {bmi}")
            return measurement
            
        except Exception as e:
            self.logger.error(f"Error generating weight measurement: {e}")
            return {
                'weight': self.last_weight,
                'bmi': BMICalculator.calculate_bmi(self.last_weight, self.user_height),
                'timestamp': datetime.now(),
                'trend': '↔️'
            }
    
    def generate_activity_data(self) -> Dict[str, any]:
        """
        Tạo dữ liệu hoạt động giả lập
        
        Returns:
            Dict chứa thông tin hoạt động
        """
        try:
            # Danh sách hoạt động có trọng số
            activities = [
                ("Đi bộ", 0.3),
                ("Chạy bộ", 0.2),
                ("Đạp xe", 0.15),
                ("Bơi lội", 0.1),
                ("Gym", 0.1),
                ("Yoga", 0.08),
                ("Nhảy dây", 0.05),
                ("Leo cầu thang", 0.02)
            ]
            
            # Chọn hoạt động ngẫu nhiên dựa trên trọng số
            activity_choices = [act[0] for act in activities]
            weights = [act[1] for act in activities]
            activity_type = random.choices(activity_choices, weights=weights, k=1)[0]
            
            # Thời gian hoạt động (phút)
            if activity_type in ["Chạy bộ", "Nhảy dây"]:
                duration = random.randint(15, 45)
            elif activity_type in ["Đi bộ", "Yoga"]:
                duration = random.randint(20, 60)
            else:
                duration = random.randint(30, 90)
            
            # Tính calories đốt cháy
            base_rate = self.calorie_rates[activity_type][self.activity_intensity]
            calories_burned = round(base_rate * duration * random.uniform(0.9, 1.1), 1)
            
            # Xác định cường độ dựa trên duration và type
            if duration > 60 or activity_type in ["Chạy bộ", "Nhảy dây"]:
                intensity = "high"
            elif duration > 30:
                intensity = "medium"
            else:
                intensity = "low"
            
            activity_data = {
                'activity_type': activity_type,
                'duration': duration,
                'calories_burned': calories_burned,
                'intensity': intensity,
                'timestamp': datetime.now(),
                'date': datetime.now().strftime("%Y-%m-%d")
            }
            
            self.logger.info(f"Generated activity: {activity_type}, {duration}min, {calories_burned}cal")
            return activity_data
            
        except Exception as e:
            self.logger.error(f"Error generating activity data: {e}")
            return {
                'activity_type': 'Đi bộ',
                'duration': 30,
                'calories_burned': 150.0,
                'intensity': 'medium',
                'timestamp': datetime.now(),
                'date': datetime.now().strftime("%Y-%m-%d")
            }
    
    def generate_sleep_data(self) -> Dict[str, any]:
        """Tạo dữ liệu giấc ngủ giả lập"""
        try:
            # Thời gian ngủ (giờ)
            sleep_hours = random.uniform(5.0, 9.0)
            sleep_quality = random.choice(["poor", "fair", "good", "excellent"])
            
            # Tính điểm chất lượng giấc ngủ
            quality_scores = {"poor": 60, "fair": 75, "good": 85, "excellent": 95}
            sleep_score = quality_scores[sleep_quality]
            
            # Thời gian thức dậy và đi ngủ
            bedtime = datetime.now().replace(hour=22, minute=0, second=0) - timedelta(hours=8)
            wakeup_time = bedtime + timedelta(hours=sleep_hours)
            
            return {
                'sleep_hours': round(sleep_hours, 1),
                'sleep_quality': sleep_quality,
                'sleep_score': sleep_score,
                'bedtime': bedtime.strftime("%H:%M"),
                'wakeup_time': wakeup_time.strftime("%H:%M"),
                'deep_sleep_hours': round(sleep_hours * random.uniform(0.15, 0.25), 1),
                'light_sleep_hours': round(sleep_hours * random.uniform(0.55, 0.65), 1),
                'rem_sleep_hours': round(sleep_hours * random.uniform(0.2, 0.25), 1)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating sleep data: {e}")
            return {
                'sleep_hours': 7.0,
                'sleep_quality': 'good',
                'sleep_score': 85
            }
    
    def generate_heart_rate_data(self) -> Dict[str, any]:
        """Tạo dữ liệu nhịp tim giả lập"""
        try:
            # Nhịp tim nghỉ ngơi (bpm)
            resting_hr = random.randint(58, 72)
            
            # Nhịp tim tối đa ước tính (220 - tuổi, giả sử tuổi 30)
            max_hr = 190
            
            # Nhịp tim hiện tại (dao động quanh nghỉ ngơi)
            current_hr = resting_hr + random.randint(-5, 15)
            
            # Phần trăm nhịp tim tối đa
            hr_percentage = min(int((current_hr / max_hr) * 100), 100)
            
            # Phân vùng nhịp tim
            if current_hr < resting_hr + 10:
                zone = "Nghỉ ngơi"
            elif current_hr < max_hr * 0.6:
                zone = "Vùng 1 - Nhẹ nhàng"
            elif current_hr < max_hr * 0.7:
                zone = "Vùng 2 - Đốt mỡ"
            elif current_hr < max_hr * 0.8:
                zone = "Vùng 3 - Aerobic"
            elif current_hr < max_hr * 0.9:
                zone = "Vùng 4 - Anaerobic"
            else:
                zone = "Vùng 5 - Tối đa"
            
            return {
                'resting_heart_rate': resting_hr,
                'current_heart_rate': current_hr,
                'max_heart_rate': max_hr,
                'heart_rate_zone': zone,
                'hr_percentage': hr_percentage,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating heart rate data: {e}")
            return {
                'resting_heart_rate': 65,
                'current_heart_rate': 72,
                'max_heart_rate': 190,
                'heart_rate_zone': "Nghỉ ngơi"
            }
    
    def generate_daily_summary(self) -> Dict[str, any]:
        """Tạo báo cáo tổng quan hàng ngày"""
        try:
            weight_data = self.generate_weight_measurement()
            activity_data = self.generate_activity_data()
            sleep_data = self.generate_sleep_data()
            heart_data = self.generate_heart_rate_data()
            
            # Tính điểm sức khỏe hàng ngày
            health_score = self._calculate_health_score(
                weight_data, activity_data, sleep_data, heart_data
            )
            
            summary = {
                'date': datetime.now().strftime("%Y-%m-%d"),
                'weight_data': weight_data,
                'activity_data': activity_data,
                'sleep_data': sleep_data,
                'heart_data': heart_data,
                'health_score': health_score,
                'recommendations': self._generate_recommendations(
                    weight_data, activity_data, sleep_data, heart_data
                )
            }
            
            self.logger.info(f"Generated daily summary with health score: {health_score}")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating daily summary: {e}")
            return {}
    
    def _calculate_health_score(self, weight_data: Dict, activity_data: Dict, 
                              sleep_data: Dict, heart_data: Dict) -> int:
        """Tính điểm sức khỏe tổng hợp"""
        score = 100
        
        # Đánh giá cân nặng (30%)
        bmi = weight_data['bmi']
        if 18.5 <= bmi <= 23:
            weight_score = 30
        elif 17 <= bmi < 18.5 or 23 < bmi <= 25:
            weight_score = 20
        else:
            weight_score = 10
        
        # Đánh giá hoạt động (30%)
        activity_mins = activity_data['duration']
        if activity_mins >= 60:
            activity_score = 30
        elif activity_mins >= 30:
            activity_score = 25
        elif activity_mins >= 15:
            activity_score = 20
        else:
            activity_score = 10
        
        # Đánh giá giấc ngủ (25%)
        sleep_hours = sleep_data['sleep_hours']
        if 7 <= sleep_hours <= 9:
            sleep_score = 25
        elif 6 <= sleep_hours < 7 or 9 < sleep_hours <= 10:
            sleep_score = 20
        else:
            sleep_score = 10
        
        # Đánh giá nhịp tim (15%)
        resting_hr = heart_data['resting_heart_rate']
        if 60 <= resting_hr <= 70:
            heart_score = 15
        elif 55 <= resting_hr < 60 or 70 < resting_hr <= 75:
            heart_score = 12
        else:
            heart_score = 8
        
        total_score = weight_score + activity_score + sleep_score + heart_score
        return min(total_score, 100)
    
    def _generate_recommendations(self, weight_data: Dict, activity_data: Dict,
                                sleep_data: Dict, heart_data: Dict) -> List[str]:
        """Tạo đề xuất sức khỏe dựa trên dữ liệu"""
        recommendations = []
        
        # Đề xuất về cân nặng
        bmi = weight_data['bmi']
        if bmi < 18.5:
            recommendations.append("🎯 Cần tăng cường dinh dưỡng để đạt BMI bình thường")
        elif bmi > 25:
            recommendations.append("🎯 Cần giảm cân để cải thiện sức khỏe")
        
        # Đề xuất về hoạt động
        activity_mins = activity_data['duration']
        if activity_mins < 30:
            recommendations.append("🏃‍♂️ Nên tăng thời gian tập luyện lên ít nhất 30 phút/ngày")
        
        # Đề xuất về giấc ngủ
        sleep_hours = sleep_data['sleep_hours']
        if sleep_hours < 7:
            recommendations.append("😴 Cần ngủ đủ 7-9 tiếng mỗi đêm")
        elif sleep_hours > 9:
            recommendations.append("😴 Ngủ quá nhiều có thể ảnh hưởng đến sức khỏe")
        
        # Đề xuất về nhịp tim
        resting_hr = heart_data['resting_heart_rate']
        if resting_hr > 75:
            recommendations.append("❤️ Nhịp tim nghỉ cao, nên tập thể dục thường xuyên hơn")
        
        if not recommendations:
            recommendations.append("✅ Chúc mừng! Bạn đang duy trì lối sống lành mạnh")
        
        return recommendations
    
    def generate_historical_data(self, days: int = 30, trend: str = "stable") -> List[Dict]:
        """Tạo dữ liệu lịch sử cho nhiều ngày"""
        historical_data = []
        
        for i in range(days):
            # Tạo ngày trong quá khứ
            date = datetime.now() - timedelta(days=days - i - 1)
            
            # Cập nhật cân nặng với xu hướng
            weight_data = self.generate_weight_measurement(trend)
            weight_data['timestamp'] = date
            weight_data['date'] = date.strftime("%Y-%m-%d")
            
            # Tạo hoạt động cho ngày đó (có thể không có hoạt động)
            if random.random() > 0.3:  # 70% có hoạt động
                activity_data = self.generate_activity_data()
                activity_data['timestamp'] = date
                activity_data['date'] = date.strftime("%Y-%m-%d")
            else:
                activity_data = None
            
            day_data = {
                'date': date.strftime("%Y-%m-%d"),
                'weight_data': weight_data,
                'activity_data': activity_data
            }
            
            historical_data.append(day_data)
        
        return historical_data