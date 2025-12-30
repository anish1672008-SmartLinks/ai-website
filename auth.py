from flask import Blueprint, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["POST"])
def signup():
    db = get_db()
    username = request.form["username"]
    password = generate_password_hash(request.form["password"])

    try:
        db.execute(
            "INSERT INTO users (username, password) VALUES (?,?)",
            (username, password)
        )
        db.commit()
        return redirect("/")
    except:
        return "User already exists"

@auth.route("/login", methods=["POST"])
def login():
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username=?",
        (request.form["username"],)
    ).fetchone()

    if user and check_password_hash(user["password"], request.form["password"]):
        session["user_id"] = user["id"]
        return redirect("/dashboard")

    return "Invalid login"
