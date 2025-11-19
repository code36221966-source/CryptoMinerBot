import sqlite3
import hashlib
import time

DB_NAME = "miner.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Create table with Mining Balance AND Crypto Balance
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            mining_balance REAL DEFAULT 0.00,
            crypto_balance REAL DEFAULT 0.00,
            created_at REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized!")

def hash_pass(password):
    # Encrypt password so hackers can't read it
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, email, password):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)", 
                  (username, email, hash_pass(password), time.time()))
        conn.commit()
        return True, "Registration Successful!"
    except sqlite3.IntegrityError:
        return False, "Username already exists!"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, hash_pass(password)))
    user = c.fetchone()
    conn.close()
    if user:
        return dict(user)
    return None

# This runs if you execute the file directly to test it
if __name__ == "__main__":
    init_db()
