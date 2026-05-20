import os
from flask import Flask, render_template, request, redirect, session, send_file
from generator import generate_pdf_from_text

app = Flask(__name__)

app.secret_key = "supersecretkey"

# =========================
# LOGIN PAGE
# =========================
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # SIMPLE LOGIN
        if username == "admin" and password == "admin":
            session["user"] = username
            return redirect("/generate")

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")

# =========================
# GENERATE TEST CASES
# =========================
@app.route("/generate", methods=["GET", "POST"])
def generate():

    if "user" not in session:
        return redirect("/")

    preview = None

    if request.method == "POST":

        raw_text = request.form.get("requirements")

        mode = request.form.get("mode", "fast")

        if raw_text:

            try:

                file_path, preview = generate_pdf_from_text(
                    raw_text,
                    mode
                )

                session["pdf_path"] = file_path

            except Exception as e:

                preview = f"Error: {str(e)}"

    return render_template(
        "generate.html",
        preview=preview
    )

# =========================
# DOWNLOAD PDF
# =========================
@app.route("/download")
def download():

    if "user" not in session:
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
# RUN APP
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
