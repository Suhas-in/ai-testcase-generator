import sqlite3
import os
from flask import Flask, render_template, request, redirect, session, send_file
from generator import generate_pdf_from_text

# =========================
# APP CONFIG
# =========================
app = Flask(__name__)

# Secret Key
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# =========================
# DATABASE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "database")
DB_PATH = os.path.join(DB_DIR, "app.db")

# Create DB folder if not exists
os.makedirs(DB_DIR, exist_ok=True)

# =========================
# DATABASE INIT
# =========================
def initialize_database():

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

    # TEST CASE LOGS
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
    ('admin@gmail.com', 'admin@123', 'admin'),
    ('demo@gmail.com', 'demo@123', 'user')
    """)

    conn.commit()
    conn.close()

# Initialize database
initialize_database()

# =========================
# LOGIN PAGE
# =========================
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session["username"] = username
            session["role"] = user[0]

            # Admin login
            if user[0] == "admin":
                return redirect("/dashboard")

            # User login
            return redirect("/generate")

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")

# =========================
# ADMIN DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():

    if session.get("role") != "admin":
        return redirect("/")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Total users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    # Total generated test cases
    cursor.execute("SELECT COUNT(*) FROM test_case_logs")
    total_logs = cursor.fetchone()[0]

    # User stats
    cursor.execute("""
        SELECT username, COUNT(*) as count
        FROM test_case_logs
        GROUP BY username
        ORDER BY count DESC
    """)

    user_stats = cursor.fetchall()

    # Recent logs
    cursor.execute("""
        SELECT username, requirements, created_at
        FROM test_case_logs
        ORDER BY created_at DESC
        LIMIT 10
    """)

    recent_logs = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total_users=total_users,
        total_logs=total_logs,
        user_stats=user_stats,
        recent_logs=recent_logs
    )

# =========================
# GENERATE TEST CASES
# =========================
@app.route("/generate", methods=["GET", "POST"])
def generate():

    if session.get("role") != "user":
        return redirect("/")

    preview = None

    if request.method == "POST":

        raw_text = request.form.get("requirements")
        mode = request.form.get("mode", "fast")

        if raw_text:

            try:

                # Generate PDF + Preview
                file_path, preview = generate_pdf_from_text(
                    raw_text,
                    mode
                )

                # Save PDF path in session
                session["pdf_path"] = file_path

                # =========================
                # SAVE LOGS INTO DATABASE
                # =========================
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO test_case_logs
                    (username, requirements)
                    VALUES (?, ?)
                """, (
                    session.get("username"),
                    raw_text
                ))

                conn.commit()
                conn.close()

            except Exception as e:

                preview = f"Error: {str(e)}"

    return render_template(
        "generate.html",
        preview=preview
    )

# =========================
# ADMIN LOGS PAGE
# =========================
@app.route("/admin/logs")
def view_logs():

    if session.get("role") != "admin":
        return redirect("/")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, requirements, created_at
        FROM test_case_logs
        ORDER BY created_at DESC
    """)

    logs = cursor.fetchall()

    conn.close()

    return render_template(
        "logs.html",
        logs=logs
    )

# =========================
# DOWNLOAD PDF
# =========================
@app.route("/download")
def download():

    if session.get("role") != "user":
        return redirect("/")

    file_path = session.get("pdf_path")

    if not file_path:
        return redirect("/generate")

    if not os.path.exists(file_path):
        return redirect("/generate")

    return send_file(
        file_path,
        as_attachment=True
    )

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# =========================
# RUN FLASK APP
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
