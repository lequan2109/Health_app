# tests/test_basic.py
import unittest
import os
import tempfile
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from utils.bmi_calculator import BMICalculator
from utils.validators import HealthDataValidator

class TestHealthApp(unittest.TestCase):
    """Test cases cho ứng dụng theo dõi sức khỏe"""
    
    def setUp(self):
        """Thiết lập trước mỗi test"""
        # Tạo database tạm thời
        self.test_db_file = tempfile.mktemp(suffix='.db')
        self.db = DatabaseManager(self.test_db_file)
        self.db.init_database()
    
    def tearDown(self):
        """Dọn dẹp sau mỗi test"""
        # Xóa database tạm thời
        if os.path.exists(self.test_db_file):
            os.unlink(self.test_db_file)
    
    def test_database_initialization(self):
        """Test khởi tạo database"""
        # Kiểm tra các bảng đã được tạo
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['users', 'weight_records', 'activities', 'health_goals']
        for table in expected_tables:
            self.assertIn(table, tables)
        
        conn.close()
    
    def test_user_creation(self):
        """Test tạo user"""
        success = self.db.create_user(
            username="testuser",
            password="testpass",
            full_name="Test User",
            height=170.0
        )
        
        self.assertTrue(success)
        
        # Kiểm tra user đã được tạo
        user = self.db.authenticate_user("testuser", "testpass")
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "testuser")
        self.assertEqual(user['full_name'], "Test User")
        self.assertEqual(user['height'], 170.0)
    
    def test_duplicate_username(self):
        """Test tạo user với username trùng"""
        # Tạo user đầu tiên
        self.db.create_user("duplicate", "pass1", "User One", 170.0)
        
        # Thử tạo user thứ hai với cùng username
        success = self.db.create_user("duplicate", "pass2", "User Two", 175.0)
        
        self.assertFalse(success)  # Should fail due to duplicate username
    
    def test_weight_record_creation(self):
        """Test tạo bản ghi cân nặng"""
        # Tạo user test
        self.db.create_user("weightuser", "pass", "Weight User", 170.0)
        user = self.db.authenticate_user("weightuser", "pass")
        
        # Thêm bản ghi cân nặng
        bmi = self.db.add_weight_record(user['user_id'], 65.0)
        
        self.assertIsNotNone(bmi)
        self.assertGreater(bmi, 0)
        
        # Kiểm tra BMI calculation
        expected_bmi = 65.0 / (1.7 ** 2)  # weight / height^2
        self.assertAlmostEqual(bmi, expected_bmi, places=1)
    
    def test_bmi_calculator(self):
        """Test tính toán BMI"""
        # Test case 1: Normal weight
        bmi = BMICalculator.calculate_bmi(65, 1.70)
        self.assertAlmostEqual(bmi, 22.5, places=1)
        
        # Test case 2: Underweight
        bmi = BMICalculator.calculate_bmi(50, 1.70)
        self.assertAlmostEqual(bmi, 17.3, places=1)
        
        # Test case 3: Overweight
        bmi = BMICalculator.calculate_bmi(80, 1.70)
        self.assertAlmostEqual(bmi, 27.7, places=1)
    
    def test_bmi_categories(self):
        """Test phân loại BMI"""
        test_cases = [
            (17.0, "Thiếu cân"),
            (20.0, "Bình thường"),
            (24.0, "Thừa cân"),
            (27.0, "Béo phì cấp I"),
            (35.0, "Béo phì cấp II")
        ]
        
        for bmi, expected_category in test_cases:
            category_info = BMICalculator.get_bmi_category(bmi)
            self.assertEqual(category_info['category'], expected_category)
    
    def test_weight_validation(self):
        """Test validation cân nặng"""
        # Valid weights
        self.assertTrue(HealthDataValidator.validate_weight(50.0)[0])
        self.assertTrue(HealthDataValidator.validate_weight(75.5)[0])
        self.assertTrue(HealthDataValidator.validate_weight(120.0)[0])
        
        # Invalid weights
        self.assertFalse(HealthDataValidator.validate_weight(10.0)[0])   # Too low
        self.assertFalse(HealthDataValidator.validate_weight(350.0)[0])  # Too high
        self.assertFalse(HealthDataValidator.validate_weight(-10.0)[0])  # Negative
    
    def test_height_validation(self):
        """Test validation chiều cao"""
        # Valid heights
        self.assertTrue(HealthDataValidator.validate_height(150.0)[0])
        self.assertTrue(HealthDataValidator.validate_height(175.5)[0])
        self.assertTrue(HealthDataValidator.validate_height(200.0)[0])
        
        # Invalid heights
        self.assertFalse(HealthDataValidator.validate_height(40.0)[0])   # Too low
        self.assertFalse(HealthDataValidator.validate_height(300.0)[0])  # Too high
        self.assertFalse(HealthDataValidator.validate_height(-10.0)[0])  # Negative
    
    def test_activity_validation(self):
        """Test validation hoạt động"""
        # Valid durations
        self.assertTrue(HealthDataValidator.validate_activity_duration(30)[0])
        self.assertTrue(HealthDataValidator.validate_activity_duration(120)[0])
        self.assertTrue(HealthDataValidator.validate_activity_duration(1)[0])
        
        # Invalid durations
        self.assertFalse(HealthDataValidator.validate_activity_duration(0)[0])    # Too low
        self.assertFalse(HealthDataValidator.validate_activity_duration(500)[0])  # Too high
        self.assertFalse(HealthDataValidator.validate_activity_duration(-10)[0])  # Negative
    
    def test_username_validation(self):
        """Test validation username"""
        # Valid usernames
        self.assertTrue(HealthDataValidator.validate_username("user123")[0])
        self.assertTrue(HealthDataValidator.validate_username("test_user")[0])
        self.assertTrue(HealthDataValidator.validate_username("abc")[0])  # Minimum length
        
        # Invalid usernames
        self.assertFalse(HealthDataValidator.validate_username("")[0])      # Empty
        self.assertFalse(HealthDataValidator.validate_username("ab")[0])    # Too short
        self.assertFalse(HealthDataValidator.validate_username("a" * 21)[0]) # Too long
        self.assertFalse(HealthDataValidator.validate_username("user@name")[0])  # Special chars
    
    def test_activity_records(self):
        """Test bản ghi hoạt động"""
        # Tạo user test
        self.db.create_user("activityuser", "pass", "Activity User", 170.0)
        user = self.db.authenticate_user("activityuser", "pass")
        
        # Thêm bản ghi hoạt động
        success = self.db.add_activity(
            user_id=user['user_id'],
            activity_type="Chạy bộ",
            duration=30,
            calories_burned=300.0,
            intensity="high"
        )
        
        self.assertTrue(success)
        
        # Kiểm tra hoạt động đã được thêm
        activities = self.db.get_activities(user['user_id'], days=7)
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['activity_type'], "Chạy bộ")
        self.assertEqual(activities[0]['duration'], 30)
    
    def test_weekly_activity_calculation(self):
        """Test tính tổng hoạt động hàng tuần"""
        # Tạo user test
        self.db.create_user("weeklyuser", "pass", "Weekly User", 170.0)
        user = self.db.authenticate_user("weeklyuser", "pass")
        
        # Thêm nhiều hoạt động
        activities = [
            ("Đi bộ", 60, 240.0),
            ("Chạy bộ", 30, 300.0),
            ("Đạp xe", 45, 360.0)
        ]
        
        for activity_type, duration, calories in activities:
            self.db.add_activity(
                user_id=user['user_id'],
                activity_type=activity_type,
                duration=duration,
                calories_burned=calories
            )
        
        # Kiểm tra tổng thời gian
        total_minutes = self.db.get_weekly_activity_minutes(user['user_id'])
        expected_total = 60 + 30 + 45  # 135 minutes
        self.assertEqual(total_minutes, expected_total)

if __name__ == '__main__':
    unittest.main()