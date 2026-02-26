import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/app.db")
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

# TEST CASE LOGS TABLE  ✅ (NEW)
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
