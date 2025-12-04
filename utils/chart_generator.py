# utils/chart_generator.py
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from typing import List, Dict
import logging

class ChartGenerator:
    """Class tạo biểu đồ sức khỏe"""
    
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        # Reserve extra top space so titles are not clipped across different charts
        plt.rcParams['figure.subplot.top'] = 0.85
        plt.rcParams['figure.subplot.bottom'] = 0.10
        plt.rcParams['figure.titlesize'] = 14
        self.logger = logging.getLogger(__name__)
    
    def create_weight_trend_chart(self, weight_data: List[Dict], period: str = 'week') -> plt.Figure:
        """Tạo biểu đồ xu hướng cân nặng"""
        try:
            if not weight_data:
                return self._create_empty_chart("Không có dữ liệu cân nặng")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            dates = [datetime.strptime(item['date'], '%Y-%m-%d') for item in weight_data]
            weights = [item['weight'] for item in weight_data]
            
            # Vẽ đường xu hướng
            ax.plot(dates, weights, marker='o', linewidth=2, markersize=6, 
                   color='#2E86AB', label='Cân nặng')
            
            # Vẽ vùng biến động
            if len(weights) > 1:
                ax.fill_between(dates, weights, alpha=0.2, color='#2E86AB')
            
            ax.set_title('📊 Xu hướng Cân nặng', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylabel('Cân nặng (kg)', fontsize=12)
            ax.grid(True, alpha=0.3)
            
            # Format trục x theo period
            if period == 'week':
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
            elif period == 'month':
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
                ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
            else:  # 3 months
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
                ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
            
            plt.xticks(rotation=45)
            fig.tight_layout()
            return fig
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating weight trend chart: {e}")
            return self._create_empty_chart("Lỗi tạo biểu đồ")
    
    def create_bmi_chart(self, bmi_data: List[Dict]) -> plt.Figure:
        """Tạo biểu đồ BMI với vùng phân loại"""
        try:
            if not bmi_data:
                return self._create_empty_chart("Không có dữ liệu BMI")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            dates = [datetime.strptime(item['date'], '%Y-%m-%d') for item in bmi_data]
            bmis = [item['bmi'] for item in bmi_data]
            
            # Vẽ các vùng BMI với màu sắc
            ax.axhspan(0, 18.5, alpha=0.3, color='#FF6B6B', label='Thiếu cân')
            ax.axhspan(18.5, 23, alpha=0.3, color='#4ECDC4', label='Bình thường')
            ax.axhspan(23, 25, alpha=0.3, color='#FFE66D', label='Thừa cân')
            ax.axhspan(25, 40, alpha=0.3, color='#FF6B6B', label='Béo phì')
            
            # Vẽ đường BMI
            ax.plot(dates, bmis, marker='s', linewidth=2, markersize=6, 
                   color='#1A535C', label='Chỉ số BMI')
            
            ax.set_title('📈 Chỉ số BMI Theo Thời Gian', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylabel('Chỉ số BMI', fontsize=12)
            ax.legend(loc='upper right')
            ax.grid(True, alpha=0.3)
            
            # Đường giới hạn khuyến nghị
            ax.axhline(y=18.5, color='red', linestyle='--', alpha=0.5)
            ax.axhline(y=23, color='orange', linestyle='--', alpha=0.5)
            ax.axhline(y=25, color='red', linestyle='--', alpha=0.5)
            
            plt.xticks(rotation=45)
            fig.tight_layout()
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating BMI chart: {e}")
            return self._create_empty_chart("Lỗi tạo biểu đồ BMI")
    
    def create_activity_chart(self, activity_data: List[Dict]) -> plt.Figure:
        """Tạo biểu đồ hoạt động"""
        try:
            if not activity_data:
                return self._create_empty_chart("Không có dữ liệu hoạt động")
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Chuẩn bị dữ liệu
            activities_by_type = {}
            daily_duration = {}
            
            for activity in activity_data:
                act_type = activity['activity_type']
                duration = activity['duration']
                date = activity['date']
                
                # Thống kê theo loại hoạt động
                if act_type not in activities_by_type:
                    activities_by_type[act_type] = 0
                activities_by_type[act_type] += duration
                
                # Thống kê theo ngày
                if date not in daily_duration:
                    daily_duration[date] = 0
                daily_duration[date] += duration
            
            # Biểu đồ 1: Phân bố loại hoạt động
            if activities_by_type:
                labels = list(activities_by_type.keys())
                sizes = list(activities_by_type.values())
                colors = plt.cm.Set3(range(len(labels)))
                
                ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
                ax1.set_title('Phân bố Loại Hoạt động', fontweight='bold')
            
            # Biểu đồ 2: Thời gian hoạt động theo ngày
            if daily_duration:
                dates = [datetime.strptime(date, '%Y-%m-%d') for date in daily_duration.keys()]
                durations = list(daily_duration.values())
                
                ax2.bar(dates, durations, color='#4ECDC4', alpha=0.7)
                ax2.set_title('Thời gian Hoạt động Theo Ngày', fontweight='bold')
                ax2.set_ylabel('Phút')
                ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
                plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
            
            fig.tight_layout()
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating activity chart: {e}")
            return self._create_empty_chart("Lỗi tạo biểu đồ hoạt động")
    
    def create_weekly_summary_chart(self, weight_data: List[Dict], activity_data: List[Dict]) -> plt.Figure:
        """Tạo biểu đồ tổng quan tuần"""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            
            # 1. Cân nặng tuần
            if weight_data:
                recent_weights = weight_data[:7]  # 7 ngày gần nhất
                dates = [datetime.strptime(item['date'], '%Y-%m-%d') for item in recent_weights]
                weights = [item['weight'] for item in recent_weights]
                
                ax1.plot(dates, weights, marker='o', color='#2E86AB')
                ax1.set_title('Cân nặng 7 ngày')
                ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
                plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
            
            # 2. BMI tuần
            if weight_data:
                bmis = [item['bmi'] for item in recent_weights]
                ax2.plot(dates, bmis, marker='s', color='#1A535C')
                ax2.set_title('BMI 7 ngày')
                ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
                plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
            
            # 3. Tổng hoạt động tuần
            if activity_data:
                weekly_total = sum(act['duration'] for act in activity_data[:7])
                ax3.bar(['Tuần này'], [weekly_total], color='#4ECDC4')
                ax3.set_title('Tổng thời gian hoạt động')
                ax3.axhline(y=150, color='red', linestyle='--', label='Mục tiêu WHO')
                ax3.legend()
            
            # 4. Phân loại BMI hiện tại
            if weight_data:
                from .bmi_calculator import BMICalculator
                current_bmi = weight_data[0]['bmi'] if weight_data else 0
                category = BMICalculator.get_bmi_category(current_bmi)
                
                categories = ['Thiếu cân', 'Bình thường', 'Thừa cân', 'Béo phì']
                values = [0, 0, 0, 0]
                colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#FF6B6B']
                
                # Highlight category hiện tại
                if category['category'] == 'Thiếu cân':
                    values[0] = 1
                elif category['category'] == 'Bình thường':
                    values[1] = 1  
                elif category['category'] == 'Thừa cân':
                    values[2] = 1
                else:
                    values[3] = 1
                
                bars = ax4.bar(categories, values, color=colors, alpha=0.7)
                ax4.set_title('Phân loại BMI hiện tại')
                plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)
            
            fig.tight_layout()
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating weekly summary chart: {e}")
            return self._create_empty_chart("Lỗi tạo biểu đồ tổng quan")
    
    def _create_empty_chart(self, message: str) -> plt.Figure:
        """Tạo biểu đồ trống với thông báo"""
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, message, ha='center', va='center', 
               transform=ax.transAxes, fontsize=12, style='italic')
        ax.set_xticks([])
        ax.set_yticks([])
        return fig
    
    def create_sleep_trend_chart(self, sleep_data: List[Dict], period: str = 'week') -> plt.Figure:
        """Tạo biểu đồ xu hướng giấc ngủ"""
        try:
            if not sleep_data:
                return self._create_empty_chart("Không có dữ liệu giấc ngủ")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            dates = [datetime.strptime(item['record_date'], '%Y-%m-%d') for item in sleep_data]
            sleep_hours = [item['sleep_hours'] for item in sleep_data]
            
            # Vẽ đường xu hướng
            ax.plot(dates, sleep_hours, marker='o', linewidth=2, markersize=6,
                   color='#9B59B6', label='Giờ ngủ')
            
            # Vẽ vùng mục tiêu (7-9 giờ)
            ax.fill_between(dates, 7, 9, alpha=0.1, color='#27AE60', label='Mục tiêu (7-9h)')
            ax.axhline(y=7, color='#27AE60', linestyle='--', linewidth=1, alpha=0.5)
            ax.axhline(y=9, color='#27AE60', linestyle='--', linewidth=1, alpha=0.5)
            
            ax.set_title('😴 Xu hướng Giấc ngủ', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylabel('Giờ ngủ', fontsize=12)
            ax.set_ylim(0, 12)
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Format trục x
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
            plt.xticks(rotation=45)
            fig.tight_layout()
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating sleep trend chart: {e}")
            return self._create_empty_chart("Lỗi tạo biểu đồ giấc ngủ")
    
    def create_heart_rate_trend_chart(self, hr_data: List[Dict], period: str = 'week') -> plt.Figure:
        """Tạo biểu đồ xu hướng nhịp tim"""
        try:
            if not hr_data:
                return self._create_empty_chart("Không có dữ liệu nhịp tim")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            dates = [datetime.strptime(item['record_date'], '%Y-%m-%d') for item in hr_data]
            bpms = [item['bpm'] for item in hr_data]
            
            # Vẽ đường xu hướng
            ax.plot(dates, bpms, marker='o', linewidth=2, markersize=6,
                   color='#E74C3C', label='BPM')
            
            # Vẽ vùng bình thường (60-100 BPM)
            ax.fill_between(dates, 60, 100, alpha=0.1, color='#27AE60', label='Bình thường (60-100)')
            ax.axhline(y=60, color='#27AE60', linestyle='--', linewidth=1, alpha=0.5)
            ax.axhline(y=100, color='#27AE60', linestyle='--', linewidth=1, alpha=0.5)
            
            # Cảnh báo ngưỡng
            ax.axhline(y=120, color='#F39C12', linestyle='--', linewidth=1, alpha=0.5, label='Cảnh báo (120)')
            ax.axhline(y=40, color='#F39C12', linestyle='--', linewidth=1, alpha=0.5)
            
            ax.set_title('❤️ Xu hướng Nhịp tim', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylabel('BPM', fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Format trục x
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
            plt.xticks(rotation=45)
            fig.tight_layout()
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating heart rate trend chart: {e}")
            return self._create_empty_chart("Lỗi tạo biểu đồ nhịp tim")
    
    def create_sleep_quality_chart(self, sleep_data: List[Dict]) -> plt.Figure:
        """Tạo biểu đồ chất lượng giấc ngủ"""
        try:
            if not sleep_data:
                return self._create_empty_chart("Không có dữ liệu giấc ngủ")
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Phân bố chất lượng
            quality_counts = {}
            for item in sleep_data:
                quality = item.get('sleep_quality', 'Không xác định')
                quality_counts[quality] = quality_counts.get(quality, 0) + 1
            
            quality_labels = list(quality_counts.keys())
            quality_values = list(quality_counts.values())
            colors = ['#E74C3C', '#F39C12', '#F1C40F', '#2ECC71', '#27AE60'][:len(quality_labels)]
            
            ax1.pie(quality_values, labels=quality_labels, autopct='%1.1f%%', colors=colors)
            ax1.set_title('Phân bố Chất lượng Giấc ngủ')
            
            # Trung bình giờ ngủ theo ngày
            dates = [datetime.strptime(item['record_date'], '%Y-%m-%d') for item in sleep_data[-7:]]
            sleep_hours = [item['sleep_hours'] for item in sleep_data[-7:]]
            
            ax2.bar(dates, sleep_hours, color='#9B59B6', alpha=0.7)
            ax2.axhline(y=8, color='#27AE60', linestyle='--', label='Mục tiêu (8h)')
            ax2.set_title('Giờ ngủ 7 ngày gần nhất')
            ax2.set_ylabel('Giờ')
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
            ax2.legend()
            
            fig.tight_layout()
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating sleep quality chart: {e}")
            return self._create_empty_chart("Lỗi tạo biểu đồ chất lượng giấc ngủ")
    
    def create_heart_rate_distribution_chart(self, hr_data: List[Dict]) -> plt.Figure:
        """Tạo biểu đồ phân bố nhịp tim"""
        try:
            if not hr_data:
                return self._create_empty_chart("Không có dữ liệu nhịp tim")
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Biểu đồ phân bố hoạt động
            activity_counts = {}
            for item in hr_data:
                activity = item.get('activity_type', 'Không xác định')
                activity_counts[activity] = activity_counts.get(activity, 0) + 1
            
            activity_labels = list(activity_counts.keys())
            activity_values = list(activity_counts.values())
            colors = ['#3498DB', '#2ECC71', '#E74C3C', '#F39C12', '#9B59B6'][:len(activity_labels)]
            
            ax1.barh(activity_labels, activity_values, color=colors)
            ax1.set_title('Nhịp tim theo loại hoạt động')
            ax1.set_xlabel('Số lần đo')
            
            # Phân bố BPM
            bpms = [item['bpm'] for item in hr_data]
            ax2.hist(bpms, bins=10, color='#E74C3C', alpha=0.7, edgecolor='black')
            ax2.axvline(x=sum(bpms)/len(bpms), color='#27AE60', linestyle='--', 
                       linewidth=2, label=f"Trung bình: {sum(bpms)/len(bpms):.0f}")
            ax2.set_title('Phân bố BPM')
            ax2.set_xlabel('BPM')
            ax2.set_ylabel('Tần suất')
            ax2.legend()
            
            fig.tight_layout()
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating heart rate distribution chart: {e}")
            return self._create_empty_chart("Lỗi tạo biểu đồ phân bố nhịp tim")