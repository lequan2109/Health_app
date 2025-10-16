# database/db_manager.py
import sqlite3
import datetime
import logging
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_name: str = "health_app.db"):
        self.db_name = db_name
        self.logger = logging.getLogger(__name__)
    
    def get_connection(self):
        """Tạo kết nối đến database"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Khởi tạo database và các bảng"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Bảng người dùng
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    birth_date DATE,
                    gender TEXT,
                    height REAL DEFAULT 170.0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Bảng theo dõi cân nặng
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weight_records (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    record_date DATE NOT NULL,
                    weight REAL NOT NULL,
                    bmi REAL,
                    notes TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    UNIQUE(user_id, record_date)
                )
            ''')
            
            # Bảng hoạt động thể thao
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activities (
                    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    activity_date DATE NOT NULL,
                    activity_type TEXT NOT NULL,
                    duration INTEGER NOT NULL,
                    calories_burned REAL,
                    intensity TEXT,
                    notes TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # Bảng mục tiêu sức khỏe
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_goals (
                    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    goal_type TEXT NOT NULL,
                    target_value REAL,
                    current_value REAL,
                    deadline DATE,
                    status TEXT DEFAULT 'active',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            conn.commit()
            self.logger.info("Database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
            raise
        finally:
            conn.close()
    
    # ========== USER MANAGEMENT ==========
    
    def create_user(self, username: str, password: str, full_name: str, 
                   height: float = 170.0, birth_date: str = None, gender: str = None) -> bool:
        """Tạo user mới"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, password, full_name, height, birth_date, gender)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, password, full_name, height, birth_date, gender))
            
            conn.commit()
            self.logger.info(f"User created: {username}")
            return True
            
        except sqlite3.IntegrityError:
            self.logger.warning(f"Username already exists: {username}")
            return False
        except Exception as e:
            self.logger.error(f"Error creating user: {e}")
            return False
        finally:
            conn.close()
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Xác thực user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, username, full_name, height, birth_date, gender
                FROM users 
                WHERE username = ? AND password = ?
            ''', (username, password))
            
            result = cursor.fetchone()
            if result:
                user = {
                    'user_id': result[0],
                    'username': result[1],
                    'full_name': result[2],
                    'height': result[3],
                    'birth_date': result[4],
                    'gender': result[5]
                }
                self.logger.info(f"User authenticated: {username}")
                return user
            return None
            
        except Exception as e:
            self.logger.error(f"Error authenticating user: {e}")
            return None
        finally:
            conn.close()
    
    def get_user_height(self, user_id: int) -> float:
        """Lấy chiều cao của user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT height FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            return result[0] if result else 170.0
            
        except Exception as e:
            self.logger.error(f"Error getting user height: {e}")
            return 170.0
        finally:
            conn.close()
    
    # ========== WEIGHT RECORDS ==========
    
    def add_weight_record(self, user_id: int, weight: float, date: str = None, 
                         notes: str = None) -> Optional[float]:
        """Thêm bản ghi cân nặng và tính BMI"""
        from utils.bmi_calculator import BMICalculator
        
        try:
            if date is None:
                date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Lấy chiều cao và tính BMI
            height = self.get_user_height(user_id) / 100  # chuyển sang mét
            bmi = BMICalculator.calculate_bmi(weight, height)
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Insert hoặc update record cho ngày đó
            cursor.execute('''
                INSERT OR REPLACE INTO weight_records 
                (user_id, record_date, weight, bmi, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, date, weight, bmi, notes))
            
            conn.commit()
            self.logger.info(f"Weight record added: user={user_id}, weight={weight}, bmi={bmi}")
            return bmi
            
        except Exception as e:
            self.logger.error(f"Error adding weight record: {e}")
            return None
        finally:
            conn.close()
    
    def get_weight_records(self, user_id: int, days: int = 30) -> List[Dict]:
        """Lấy lịch sử cân nặng"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT record_date, weight, bmi, notes
                FROM weight_records 
                WHERE user_id = ? 
                AND record_date >= date('now', ?)
                ORDER BY record_date DESC
            ''', (user_id, f'-{days} days'))
            
            records = []
            for row in cursor.fetchall():
                records.append({
                    'date': row[0],
                    'weight': row[1],
                    'bmi': row[2],
                    'notes': row[3]
                })
            
            return records
            
        except Exception as e:
            self.logger.error(f"Error getting weight records: {e}")
            return []
        finally:
            conn.close()
    
    def get_recent_weight_records(self, user_id: int, days: int = 7) -> List[Dict]:
        """Lấy bản ghi cân nặng gần đây"""
        return self.get_weight_records(user_id, days)
    
    # ========== ACTIVITY RECORDS ==========
    
    def add_activity(self, user_id: int, activity_type: str, duration: int, 
                    calories_burned: float = None, intensity: str = "medium",
                    date: str = None, notes: str = None) -> bool:
        """Thêm bản ghi hoạt động"""
        try:
            if date is None:
                date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO activities 
                (user_id, activity_date, activity_type, duration, calories_burned, intensity, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, date, activity_type, duration, calories_burned, intensity, notes))
            
            conn.commit()
            self.logger.info(f"Activity added: user={user_id}, type={activity_type}, duration={duration}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding activity: {e}")
            return False
        finally:
            conn.close()
    
    def get_activities(self, user_id: int, days: int = 30) -> List[Dict]:
        """Lấy lịch sử hoạt động"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT activity_date, activity_type, duration, calories_burned, intensity, notes
                FROM activities 
                WHERE user_id = ? 
                AND activity_date >= date('now', ?)
                ORDER BY activity_date DESC
            ''', (user_id, f'-{days} days'))
            
            activities = []
            for row in cursor.fetchall():
                activities.append({
                    'date': row[0],
                    'activity_type': row[1],
                    'duration': row[2],
                    'calories_burned': row[3],
                    'intensity': row[4],
                    'notes': row[5]
                })
            
            return activities
            
        except Exception as e:
            self.logger.error(f"Error getting activities: {e}")
            return []
        finally:
            conn.close()
    
    def get_weekly_activity_minutes(self, user_id: int) -> int:
        """Tính tổng thời gian hoạt động trong tuần"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT SUM(duration) 
                FROM activities 
                WHERE user_id = ? 
                AND activity_date >= date('now', '-7 days')
            ''', (user_id,))
            
            result = cursor.fetchone()
            return int(result[0]) if result[0] else 0
            
        except Exception as e:
            self.logger.error(f"Error calculating weekly activity: {e}")
            return 0
        finally:
            conn.close()
    
    # ========== HEALTH STATISTICS ==========
    
    def get_current_weight(self, user_id: int) -> Optional[float]:
        """Lấy cân nặng hiện tại (mới nhất)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT weight FROM weight_records 
                WHERE user_id = ? 
                ORDER BY record_date DESC 
                LIMIT 1
            ''', (user_id,))
            
            result = cursor.fetchone()
            return result[0] if result else None
            
        except Exception as e:
            self.logger.error(f"Error getting current weight: {e}")
            return None
        finally:
            conn.close()
    
    def get_weight_history(self, user_id: int, from_date: str, to_date: str) -> List[Dict]:
        """Lấy lịch sử cân nặng theo khoảng thời gian"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT record_date, weight, bmi, notes
                FROM weight_records 
                WHERE user_id = ? 
                AND record_date BETWEEN ? AND ?
                ORDER BY record_date DESC
            ''', (user_id, from_date, to_date))
            
            records = []
            for row in cursor.fetchall():
                records.append({
                    'date': row[0],
                    'weight': row[1],
                    'bmi': row[2],
                    'notes': row[3]
                })
            
            return records
            
        except Exception as e:
            self.logger.error(f"Error getting weight history: {e}")
            return []
        finally:
            conn.close()