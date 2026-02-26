import sqlite3

conn = sqlite3.connect("database/app.db")
cursor = conn.cursor()

cursor.execute("SELECT username, requirements, created_at FROM test_case_logs")
rows = cursor.fetchall()

conn.close()

print(rows)
