# utils/bmi_calculator.py
from typing import Dict, List

class BMICalculator:
    """Class tính toán và đánh giá chỉ số BMI"""
    
    @staticmethod
    def calculate_bmi(weight: float, height: float) -> float:
        """
        Tính BMI từ cân nặng (kg) và chiều cao (m)
        
        Args:
            weight: Cân nặng (kg)
            height: Chiều cao (m)
            
        Returns:
            Chỉ số BMI (làm tròn 1 chữ số thập phân)
        """
        if height <= 0:
            return 0.0
        return round(weight / (height ** 2), 1)
    
    @staticmethod
    def get_bmi_category(bmi: float) -> Dict[str, str]:
        """
        Phân loại BMI theo tiêu chuẩn châu Á
        
        Args:
            bmi: Chỉ số BMI
            
        Returns:
            Dict chứa thông tin phân loại
        """
        if bmi < 18.5:
            return {
                "category": "Thiếu cân",
                "risk": "Cao",
                "color": "red",
                "description": "Cần tăng cân để đạt mức BMI bình thường"
            }
        elif 18.5 <= bmi < 23:
            return {
                "category": "Bình thường", 
                "risk": "Thấp",
                "color": "green",
                "description": "Duy trì chế độ ăn uống và tập luyện hiện tại"
            }
        elif 23 <= bmi < 25:
            return {
                "category": "Thừa cân",
                "risk": "Trung bình", 
                "color": "orange",
                "description": "Cần chú ý đến chế độ ăn uống và tập luyện"
            }
        elif 25 <= bmi < 30:
            return {
                "category": "Béo phì cấp I",
                "risk": "Cao",
                "color": "red", 
                "description": "Cần giảm cân để cải thiện sức khỏe"
            }
        else:
            return {
                "category": "Béo phì cấp II",
                "risk": "Rất cao",
                "color": "darkred",
                "description": "Cần can thiệp y tế và giảm cân ngay lập tức"
            }
    
    @staticmethod
    def get_health_recommendations(bmi: float) -> List[str]:
        """
        Đưa ra gợi ý sức khỏe dựa trên BMI
        
        Args:
            bmi: Chỉ số BMI
            
        Returns:
            List các gợi ý sức khỏe
        """
        if bmi < 18.5:
            return [
                "🎯 Tăng cường dinh dưỡng, ăn đủ 3 bữa chính/ngày",
                "🥛 Bổ sung thực phẩm giàu protein (thịt, cá, trứng, sữa)",
                "💪 Tập thể dục vừa phải để tăng cơ (tạ nhẹ, bodyweight)",
                "🍌 Ăn thêm bữa phụ với trái cây, hạt dinh dưỡng",
                "📊 Theo dõi cân nặng hàng tuần để điều chỉnh kịp thời"
            ]
        elif 18.5 <= bmi < 23:
            return [
                "✅ Duy trì chế độ ăn cân bằng và lành mạnh",
                "🏃 Tập thể dục đều đặn 30-45 phút/ngày",
                "💤 Ngủ đủ 7-8 tiếng mỗi đêm",
                "💧 Uống đủ 2 lít nước mỗi ngày",
                "📈 Theo dõi sức khỏe định kỳ"
            ]
        elif 23 <= bmi < 25:
            return [
                "⚠️ Giảm lượng đường và tinh bột trong khẩu phần ăn",
                "🥬 Tăng cường rau xanh và chất xơ",
                "🚶 Tập cardio 45-60 phút/ngày (đi bộ, chạy bộ)",
                "🍳 Ưu tiên thực phẩm luộc, hấp thay vì chiên xào",
                "⏰ Ăn tối trước 19h và không ăn khuya"
            ]
        else:  # BMI >= 25
            return [
                "🚨 Giảm cân dưới sự hướng dẫn của bác sĩ",
                "🎯 Đặt mục tiêu giảm 0.5-1kg/tuần",
                "🏃 Kết hợp cardio và strength training",
                "📝 Ghi nhật ký thực phẩm hàng ngày",
                "👥 Tham gia nhóm hỗ trợ giảm cân nếu cần"
            ]
    
    @staticmethod
    def calculate_ideal_weight_range(height: float) -> Dict[str, float]:
        """
        Tính khoảng cân nặng lý tưởng theo chiều cao
        
        Args:
            height: Chiều cao (m)
            
        Returns:
            Dict chứa cân nặng min và max lý tưởng
        """
        bmi_min = 18.5
        bmi_max = 22.9
        
        weight_min = round(bmi_min * (height ** 2), 1)
        weight_max = round(bmi_max * (height ** 2), 1)
        
        return {
            "min": weight_min,
            "max": weight_max,
            "bmi_range": f"{bmi_min}-{bmi_max}"
        }
    
    @staticmethod
    def calculate_weight_to_goal(current_weight: float, current_height: float, 
                               target_bmi: float = 22.0) -> Dict[str, float]:
        """
        Tính toán cân nặng cần đạt để đạt BMI mục tiêu
        
        Args:
            current_weight: Cân nặng hiện tại (kg)
            current_height: Chiều cao (m)
            target_bmi: BMI mục tiêu (mặc định 22.0)
            
        Returns:
            Dict chứa thông tin về mục tiêu
        """
        current_bmi = BMICalculator.calculate_bmi(current_weight, current_height)
        target_weight = round(target_bmi * (current_height ** 2), 1)
        weight_diff = round(target_weight - current_weight, 1)
        
        return {
            "current_bmi": current_bmi,
            "target_bmi": target_bmi,
            "target_weight": target_weight,
            "weight_to_change": weight_diff,
            "direction": "tăng" if weight_diff > 0 else "giảm" if weight_diff < 0 else "duy trì"
        }