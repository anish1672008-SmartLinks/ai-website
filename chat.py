from flask import Blueprint, request, jsonify, session
from groq import Groq
from database import get_db
import os
from dotenv import load_dotenv

load_dotenv()

chat = Blueprint("chat", __name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ================= CHAT =================
@chat.route("/chat", methods=["POST"])
def ai_chat():
    data = request.json
    user_msg = data.get("message", "").strip()
    mode = data.get("mode", "hindi")
    session_id = data.get("session_id")

    if not user_msg:
        return jsonify({"reply": "Please type a message."})

    if not session_id:
        return jsonify({"reply": "Please click New Chat first."})

    db = get_db()

    old_msgs = db.execute(
        "SELECT role, content FROM messages WHERE session_id=? ORDER BY id DESC LIMIT 10",
        (session_id,)
    ).fetchall()

    messages = []

    for m in reversed(old_msgs):
        messages.append({"role": m["role"], "content": m["content"]})

    if mode == "english":
        system_prompt = "You are a helpful assistant. Reply only in English."
    else:
        system_prompt = "Tum sirf Hindi me jawab doge."

    messages.insert(0, {"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_msg})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        reply = response.choices[0].message.content

    except Exception as e:
        print("API ERROR:", e)
        reply = "Server error hai, baad me try karo."

    db.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?,?,?)",
        (session_id, "user", user_msg)
    )

    db.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?,?,?)",
        (session_id, "assistant", reply)
    )

    db.commit()

    return jsonify({"reply": reply})


# ================= NEW CHAT =================
@chat.route("/new_chat", methods=["POST"])
def new_chat():
    db = get_db()
    cur = db.cursor()

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Login required"}), 401

    cur.execute(
        "INSERT INTO chat_sessions (user_id, title) VALUES (?, ?)",
        (user_id, "New Chat")
    )

    db.commit()

    session_id = cur.lastrowid
    session["session_id"] = session_id

    # IMPORTANT: return session_id
    return jsonify({"session_id": session_id})


# ================= HISTORY =================
@chat.route("/history")
def history():
    db = get_db()
    user_id = session.get("user_id")

    chats = db.execute(
        "SELECT id, title FROM chat_sessions WHERE user_id=? ORDER BY id DESC",
        (user_id,)
    ).fetchall()

    return jsonify([dict(row) for row in chats])


# ================= LOAD OLD CHAT =================
@chat.route("/load_chat/<int:session_id>")
def load_chat(session_id):
    db = get_db()

    msgs = db.execute(
        "SELECT role, content FROM messages WHERE session_id=? ORDER BY id",
        (session_id,)
    ).fetchall()

    return jsonify([dict(row) for row in msgs])


# ================= DELETE CHAT =================
@chat.route("/delete_chat/<int:chat_id>", methods=["POST"])
def delete_chat(chat_id):
    db = get_db()

    db.execute("DELETE FROM messages WHERE session_id=?", (chat_id,))
    db.execute("DELETE FROM chat_sessions WHERE id=?", (chat_id,))
    db.commit()

    return jsonify({"status": "deleted"})


# ================= RENAME CHAT =================
@chat.route("/rename_chat/<int:chat_id>", methods=["POST"])
def rename_chat(chat_id):
    data = request.json
    title = data.get("title", "New Chat")

    db = get_db()
    db.execute(
        "UPDATE chat_sessions SET title=? WHERE id=?",
        (title, chat_id),
    )
    db.commit()

    return jsonify({"status": "ok"})
@chat.route("/me")
def me():
    return jsonify({
        "username": session.get("username", "User")
    })
