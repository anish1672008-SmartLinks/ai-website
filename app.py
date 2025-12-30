from flask import Flask, render_template, session, redirect, request, jsonify
from database import init_db
from auth import auth
from chat import chat
import requests
import base64
from flask import send_file
from io import BytesIO
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()   
app.secret_key = os.getenv("SECRET_KEY")

# ✅ Register blueprints
app.register_blueprint(auth)
app.register_blueprint(chat)

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

if __name__ == "__main__":
    app.run(debug=True)
