from flask import Flask, render_template, session, redirect, request, jsonify, send_file
from database import init_db
from auth import auth
from chat import chat
from io import BytesIO
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Secret key fix
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_key")

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(chat)

# Initialize database if needed
init_db()

# ---------------- ROUTES ----------------

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/ai")
def ai_page():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    return render_template("dashboard.html")

# ---------- NEW CHAT API ----------
@app.route("/new_chat", methods=["POST"])
def new_chat():
    chat_id = str(int(time.time()))
    return jsonify({"chat_id": chat_id})

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
