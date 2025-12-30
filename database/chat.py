from flask import Blueprint, request, jsonify
from openai import OpenAI
import config

chat = Blueprint("chat", __name__)
client = OpenAI(api_key=config.OPENAI_API_KEY)

@chat.route("/chat", methods=["POST"])
def chat_ai():
    user_input = request.json.get("message")
    language = request.json.get("language", "English")

    prompt = f"Reply in {language}: {user_input}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    return jsonify({"reply": answer})
