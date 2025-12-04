# utils/alert_system.py
import logging
from typing import List, Dict
from database.db_manager import DatabaseManager

class AlertSystem:
    """Hệ thống cảnh báo sức khỏe"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.logger = logging.getLogger(__name__)
    
    def check_weight_alerts(self, user_id: int, current_weight: float) -> List[Dict]:
        """Kiểm tra cảnh báo về cân nặng"""
        alerts = []
        
        try:
            # Lấy lịch sử 7 ngày gần nhất
            recent_records = self.db.get_recent_weight_records(user_id, days=7)
            
            if len(recent_records) >= 2:
                # Kiểm tra thay đổi đột ngột
                weight_change = current_weight - recent_records[1]['weight']  # record trước đó
                if abs(weight_change) > 2:  # thay đổi > 2kg trong 1 ngày
                    alerts.append({
                        'type': 'weight_change',
                        'message': f'⚠️ Cảnh báo: Cân nặng thay đổi {weight_change:+.1f}kg trong ngày',
                        'level': 'warning',
                        'icon': '⚡'
                    })
            
            # Kiểm tra xu hướng tuần
            if len(recent_records) >= 7:
                weights = [record['weight'] for record in recent_records[:7]]
                weekly_change = weights[0] - weights[-1]  # so sánh đầu và cuối tuần
                
                if weekly_change > 3:  # Giảm > 3kg/tuần
                    alerts.append({
                        'type': 'rapid_weight_loss',
                        'message': f'📉 Giảm {weekly_change:.1f}kg trong tuần. Giảm cân quá nhanh!',
                        'level': 'danger',
                        'icon': '🚨'
                    })
                elif weekly_change < -3:  # Tăng > 3kg/tuần  
                    alerts.append({
                        'type': 'rapid_weight_gain',
                        'message': f'📈 Tăng {abs(weekly_change):.1f}kg trong tuần. Tăng cân quá nhanh!',
                        'level': 'danger',
                        'icon': '🚨'
                    })
                    
        except Exception as e:
            self.logger.error(f"Error checking weight alerts: {e}")
        
        return alerts
    
    def check_bmi_alerts(self, bmi: float) -> List[Dict]:
        """Kiểm tra cảnh báo BMI"""
        alerts = []
        
        try:
            from .bmi_calculator import BMICalculator
            category = BMICalculator.get_bmi_category(bmi)
            
            if category['risk'] in ['Cao', 'Rất cao']:
                alerts.append({
                    'type': 'bmi_risk',
                    'message': f'🎯 BMI {bmi} - {category["category"]}. Nguy cơ: {category["risk"]}',
                    'level': 'danger' if category['risk'] == 'Rất cao' else 'warning',
                    'icon': '⚠️'
                })
            
            # Cảnh báo BMI quá thấp
            if bmi < 16:
                alerts.append({
                    'type': 'critical_bmi_low',
                    'message': f'🚨 BMI quá thấp ({bmi}). Cần can thiệp y tế ngay!',
                    'level': 'critical',
                    'icon': '💀'
                })
                
            # Cảnh báo BMI quá cao
            elif bmi > 35:
                alerts.append({
                    'type': 'critical_bmi_high', 
                    'message': f'🚨 BMI quá cao ({bmi}). Cần can thiệp y tế ngay!',
                    'level': 'critical',
                    'icon': '💀'
                })
                
        except Exception as e:
            self.logger.error(f"Error checking BMI alerts: {e}")
        
        return alerts
    
    def check_activity_alerts(self, user_id: int) -> List[Dict]:
        """Kiểm tra cảnh báo hoạt động"""
        alerts = []
        
        try:
            weekly_activity = self.db.get_weekly_activity_minutes(user_id)
            
            if weekly_activity == 0:
                alerts.append({
                    'type': 'no_activity',
                    'message': '🛌 Bạn chưa ghi nhận hoạt động nào trong tuần!',
                    'level': 'warning',
                    'icon': '😴'
                })
            elif weekly_activity < 150:  # Ít hơn 150 phút/tuần (WHO recommendation)
                alerts.append({
                    'type': 'inactive',
                    'message': f'🏃 Hoạt động tuần: {weekly_activity} phút. Mục tiêu: 150 phút',
                    'level': 'info',
                    'icon': '📊'
                })
            elif weekly_activity >= 300:  # Hoạt động tích cực
                alerts.append({
                    'type': 'active_achievement',
                    'message': f'🎉 Xuất sắc! Bạn đã hoạt động {weekly_activity} phút tuần này!',
                    'level': 'success', 
                    'icon': '🌟'
                })
                
        except Exception as e:
            self.logger.error(f"Error checking activity alerts: {e}")
        
        return alerts
    
    def check_consistency_alerts(self, user_id: int) -> List[Dict]:
        """Kiểm tra cảnh báo về tính nhất quán trong theo dõi"""
        alerts = []
        
        try:
            # Kiểm tra số ngày không nhập liệu
            recent_records = self.db.get_recent_weight_records(user_id, days=7)
            if len(recent_records) == 0:
                alerts.append({
                    'type': 'no_data_week',
                    'message': '📝 Bạn chưa nhập số liệu nào trong 7 ngày qua!',
                    'level': 'warning',
                    'icon': '✏️'
                })
            elif len(recent_records) <= 2:
                alerts.append({
                    'type': 'low_frequency',
                    'message': f'📊 Chỉ {len(recent_records)} bản ghi trong tuần. Nên theo dõi hàng ngày!',
                    'level': 'info',
                    'icon': '📅'
                })
                
        except Exception as e:
            self.logger.error(f"Error checking consistency alerts: {e}")
        
        return alerts
    
    def check_sleep_alerts(self, user_id: int) -> List[Dict]:
        """Kiểm tra cảnh báo về giấc ngủ"""
        alerts = []
        
        try:
            # Lấy bản ghi giấc ngủ 7 ngày gần nhất
            recent_records = self.db.get_sleep_records(user_id, days=7)
            
            if not recent_records:
                return alerts
            
            # Tính giờ ngủ trung bình
            sleep_hours = [record['sleep_hours'] for record in recent_records]
            avg_sleep = sum(sleep_hours) / len(sleep_hours)
            
            # Kiểm tra thiếu ngủ
            if avg_sleep < 6:
                alerts.append({
                    'type': 'insufficient_sleep',
                    'message': f'😴 Cảnh báo: Trung bình {avg_sleep:.1f}h/ngày - Thiếu ngủ nghiêm trọng!',
                    'level': 'danger',
                    'icon': '🚨'
                })
            elif avg_sleep < 7:
                alerts.append({
                    'type': 'low_sleep',
                    'message': f'😴 Cảnh báo: Trung bình {avg_sleep:.1f}h/ngày - Hơi thiếu ngủ',
                    'level': 'warning',
                    'icon': '⚠️'
                })
            elif avg_sleep > 9:
                alerts.append({
                    'type': 'excessive_sleep',
                    'message': f'😴 Cảnh báo: Trung bình {avg_sleep:.1f}h/ngày - Ngủ quá nhiều',
                    'level': 'warning',
                    'icon': '⚠️'
                })
            
            # Kiểm tra chất lượng giấc ngủ
            quality_count = {}
            for record in recent_records:
                quality = record['sleep_quality']
                quality_count[quality] = quality_count.get(quality, 0) + 1
            
            bad_quality = quality_count.get('Không tốt', 0) + quality_count.get('Rất không tốt', 0)
            if bad_quality >= 3:
                alerts.append({
                    'type': 'poor_sleep_quality',
                    'message': f'😴 Chất lượng giấc ngủ kém: {bad_quality}/7 ngày',
                    'level': 'warning',
                    'icon': '⚠️'
                })
                
        except Exception as e:
            self.logger.error(f"Error checking sleep alerts: {e}")
        
        return alerts
    
    def check_heart_rate_alerts(self, user_id: int) -> List[Dict]:
        """Kiểm tra cảnh báo về nhịp tim"""
        alerts = []
        
        try:
            # Lấy nhịp tim mới nhất
            latest = self.db.get_latest_heart_rate(user_id)
            if not latest:
                return alerts
            
            bpm = latest['bpm']
            activity = latest['activity_type']
            
            # Kiểm tra nhịp tim bất thường
            if bpm < 40:
                alerts.append({
                    'type': 'bradycardia',
                    'message': f'❤️ Cảnh báo: Nhịp tim {bpm} BPM - Quá chậm (Bradycardia)',
                    'level': 'danger',
                    'icon': '🚨'
                })
            elif bpm < 60:
                alerts.append({
                    'type': 'low_heart_rate',
                    'message': f'❤️ Cảnh báo: Nhịp tim {bpm} BPM - Hơi chậm',
                    'level': 'warning',
                    'icon': '⚠️'
                })
            elif bpm > 120:
                alerts.append({
                    'type': 'tachycardia',
                    'message': f'❤️ Cảnh báo: Nhịp tim {bpm} BPM - Quá nhanh (Tachycardia)',
                    'level': 'danger',
                    'icon': '🚨'
                })
            elif bpm > 100 and activity == "Nghỉ ngơi":
                alerts.append({
                    'type': 'elevated_resting_heart_rate',
                    'message': f'❤️ Cảnh báo: Nhịp tim {bpm} BPM khi nghỉ ngơi - Hơi nhanh',
                    'level': 'warning',
                    'icon': '⚠️'
                })
            
            # Kiểm tra thay đổi đột ngột nhịp tim (so sánh với hôm trước)
            recent = self.db.get_heart_rate_records(user_id, days=2)
            if len(recent) >= 2:
                hr_change = abs(recent[0]['bpm'] - recent[1]['bpm'])
                if hr_change > 30:  # thay đổi > 30 BPM trong ngày
                    alerts.append({
                        'type': 'heart_rate_spike',
                        'message': f'❤️ Cảnh báo: Nhịp tim thay đổi {hr_change} BPM',
                        'level': 'warning',
                        'icon': '⚠️'
                    })
                
        except Exception as e:
            self.logger.error(f"Error checking heart rate alerts: {e}")
        
        return alerts
    
    def get_all_alerts(self, user_id: int, current_weight: float = None, current_bmi: float = None) -> List[Dict]:
        """Lấy tất cả cảnh báo"""
        all_alerts = []
        
        # Kiểm tra cảnh báo cân nặng nếu có current_weight
        if current_weight is not None:
            all_alerts.extend(self.check_weight_alerts(user_id, current_weight))
        
        # Kiểm tra cảnh báo BMI nếu có current_bmi
        if current_bmi is not None:
            all_alerts.extend(self.check_bmi_alerts(current_bmi))
        
        # Kiểm tra cảnh báo hoạt động
        all_alerts.extend(self.check_activity_alerts(user_id))
        
        # Kiểm tra cảnh báo nhất quán
        all_alerts.extend(self.check_consistency_alerts(user_id))
        
        # Kiểm tra cảnh báo giấc ngủ
        all_alerts.extend(self.check_sleep_alerts(user_id))
        
        # Kiểm tra cảnh báo nhịp tim
        all_alerts.extend(self.check_heart_rate_alerts(user_id))
        
        # Sắp xếp theo mức độ ưu tiên
        priority_order = {'critical': 0, 'danger': 1, 'warning': 2, 'info': 3, 'success': 4}
        all_alerts.sort(key=lambda x: priority_order.get(x['level'], 5))
        
        return all_alerts