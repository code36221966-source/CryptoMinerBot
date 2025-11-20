import sqlite3
import hashlib
import time

DB_NAME = "miner.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the table with the NEW Profile Fields and handles updates"""
    conn = get_connection()
    c = conn.cursor()
    
    # Create table if it doesn't exist (includes new columns for fresh installs)
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
            created_at REAL,
            is_verified INTEGER DEFAULT 0,
            verification_code TEXT
        )
    ''')

    # MIGRATION: Try to add new columns if they don't exist (for old databases)
    try:
        c.execute("ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass # Column likely exists
        
    try:
        c.execute("ALTER TABLE users ADD COLUMN verification_code TEXT")
    except sqlite3.OperationalError:
        pass # Column likely exists

    conn.commit()
    conn.close()
    print("✅ Database Schema Initialized & Updated!")

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, email, first_name, last_name, country, phone, password, verification_code):
    conn = get_connection()
    c = conn.cursor()
    try:
        # Insert all profile fields including verification code
        c.execute('''
            INSERT INTO users 
            (username, email, first_name, last_name, country, phone, password_hash, created_at, is_verified, verification_code) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
        ''', (username, email, first_name, last_name, country, phone, hash_pass(password), time.time(), verification_code))
        conn.commit()
        return True, "Registration Successful! Please check email for code."
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
    
    # Look for the user by EMAIL
    c.execute("SELECT * FROM users WHERE email=? AND password_hash=?", (email, hash_pass(password)))
    user = c.fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None

def activate_account(email, code):
    """Verifies the 6-digit code and activates account"""
    conn = get_connection()
    c = conn.cursor()
    
    # Check if code matches for this email
    c.execute("SELECT * FROM users WHERE email=? AND verification_code=?", (email, code))
    user = c.fetchone()
    
    if user:
        # Update status to verified
        c.execute("UPDATE users SET is_verified=1 WHERE email=?", (email,))
        conn.commit()
        conn.close()
        return True, "Account Verified Successfully!"
    
    conn.close()
    return False, "Invalid Verification Code"

# Run this if file is executed directly
if __name__ == "__main__":
    init_db()
