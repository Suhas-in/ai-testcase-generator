import sqlite3
import os

# Get absolute base directory (important for Render)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "database")
DB_PATH = os.path.join(DB_DIR, "app.db")

# Create database folder if not exists
os.makedirs(DB_DIR, exist_ok=True)

# Connect database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# TEST CASE LOGS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS test_case_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    requirements TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# DEFAULT USERS
cursor.execute("""
INSERT OR IGNORE INTO users (username, password, role)
VALUES 
('admin', 'admin123', 'admin'),
('tester', 'test123', 'user')
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully")