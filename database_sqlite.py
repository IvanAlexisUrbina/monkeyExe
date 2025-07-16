import sqlite3
import bcrypt
import os

class Database:
    def __init__(self):
        self.db_path = "bot_database.db"
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                credits INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, username, password, credits=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash, credits) VALUES (?, ?, ?)",
                (username, password_hash, credits)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def authenticate(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT password_hash, credits FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            return result[1]
        return None
    
    def deduct_credits(self, username, amount=1):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT credits FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if result and result[0] >= amount:
            cursor.execute(
                "UPDATE users SET credits = credits - ? WHERE username = ?",
                (amount, username)
            )
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False