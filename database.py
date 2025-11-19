import sqlite3
import hashlib
import time

DB_NAME = "miner.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the table with the NEW Profile Fields"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            country TEXT,
            phone TEXT,
            password_hash TEXT NOT NULL,
            mining_balance REAL DEFAULT 0.00,
            crypto_balance REAL DEFAULT 0.00,
            created_at REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database Schema Initialized!")

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, email, first_name, last_name, country, phone, password):
    conn = get_connection()
    c = conn.cursor()
    try:
        # Insert all profile fields
        c.execute('''
            INSERT INTO users 
            (username, email, first_name, last_name, country, phone, password_hash, created_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, email, first_name, last_name, country, phone, hash_pass(password), time.time()))
        conn.commit()
        return True, "Registration Successful!"
    except sqlite3.IntegrityError:
        return False, "Username or Email already exists!"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def verify_user(email, password):
    """Checks EMAIL and PASSWORD for login"""
    conn = get_connection()
    c = conn.cursor()
    
    # Look for the user by EMAIL, not username
    c.execute("SELECT * FROM users WHERE email=? AND password_hash=?", (email, hash_pass(password)))
    user = c.fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None

# Run this if file is executed directly
if __name__ == "__main__":
    init_db()
