# database.py

import bcrypt
from db_config import get_connection

class Database:
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                credits INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
    
    def add_user(self, username, password, credits=10):
        conn = get_connection()
        cursor = conn.cursor()
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash, credits) VALUES (%s, %s, %s)",
                (username, password_hash, credits)
            )
            conn.commit()
            return True
        except pymysql.err.IntegrityError:
            return False
        finally:
            conn.close()

    def authenticate(self, username, password):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT password_hash, credits FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and bcrypt.checkpw(password.encode('utf-8'), result['password_hash'].encode('utf-8')):
            return result['credits']
        return None

    def deduct_credits(self, username, amount=1):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT credits FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result and result['credits'] >= amount:
            cursor.execute(
                "UPDATE users SET credits = credits - %s WHERE username = %s",
                (amount, username)
            )
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
