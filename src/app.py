import sqlite3
import os
from flask import Flask, render_template, request, redirect, session, send_file
from generator import generate_pdf_from_text

# =========================
# APP CONFIG
# =========================
app = Flask(__name__)

# Use environment secret in production
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# Absolute path (important for deployment)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "app.db")


# =========================
# LOGIN
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

            if user[0] == "admin":
                return redirect("/dashboard")
            else:
                return redirect("/generate")

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# =========================
# DASHBOARD (ADMIN ONLY)
# =========================
@app.route("/dashboard")
def dashboard():
    if session.get("role") != "admin":
        return redirect("/")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM test_case_logs")
    total_logs = cursor.fetchone()[0]

    cursor.execute("""
        SELECT username, COUNT(*) as count
        FROM test_case_logs
        GROUP BY username
        ORDER BY count DESC
    """)
    user_stats = cursor.fetchall()

    cursor.execute("""
        SELECT username, requirements, created_at
        FROM test_case_logs
        ORDER BY created_at DESC
        LIMIT 5
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
            file_path, preview = generate_pdf_from_text(raw_text, mode)
            session["pdf_path"] = file_path

    return render_template("generate.html", preview=preview)


# =========================
# ADMIN LOGS
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

    return render_template("logs.html", logs=logs)


# =========================
# DOWNLOAD PDF
# =========================
@app.route("/download")
def download():
    if session.get("role") != "user":
        return redirect("/")

    file_path = session.get("pdf_path")

    if not file_path or not os.path.exists(file_path):
        return redirect("/generate")

    return send_file(file_path, as_attachment=True)


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =========================
# PRODUCTION ENTRY POINT
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

