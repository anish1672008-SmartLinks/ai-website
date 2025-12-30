from flask import Blueprint, request, jsonify, session
from openai import OpenAI
from database import get_db
import os
from dotenv import load_dotenv

load_dotenv()

chat = Blueprint("chat", __name__)

# ✅ Sirf ek hi client, .env se
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

@chat.route("/chat", methods=["POST"])
def ai_chat():
    user_msg = request.json["message"]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Tum sirf Hindi me jawab doge"},
            {"role": "user", "content": user_msg}
        ]
    )

    reply = response.choices[0].message.content

    db = get_db()
    db.execute(
        "INSERT INTO chats (user_id, message, reply) VALUES (?,?,?)",
        (session["user_id"], user_msg, reply)
    )
    db.commit()

    return jsonify({"reply": reply})
