from flask import Blueprint, request, jsonify, session
from groq import Groq
from database import get_db
import os
from dotenv import load_dotenv

load_dotenv()

chat = Blueprint("chat", __name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@chat.route("/chat", methods=["POST"])
def ai_chat():
    data = request.json
    user_msg = data.get("message", "").strip()
    mode = data.get("mode", "hindi")

    if not user_msg:
        return jsonify({"reply": "Please type a message."})

    if mode == "english":
        system_prompt = (
            "You are an English AI assistant. "
            "Always reply ONLY in clear, simple English."
        )
    else:
        system_prompt = "Tum sirf Hindi me jawab doge."

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ]
        )

        reply = response.choices[0].message.content

    except Exception as e:
        print("API ERROR:", e)
        reply = "Server error hai, baad me try karo."

    db = get_db()
    db.execute(
        "INSERT INTO chats (user_id, message, reply) VALUES (?,?,?)",
        (session.get("user_id"), user_msg, reply)
    )
    db.commit()

    return jsonify({"reply": reply})
