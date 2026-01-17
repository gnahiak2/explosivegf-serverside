"""
Flask server for Explosive Girlfriend AI
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from girlfriend_ai import ExplosiveGirlfriendAI

load_dotenv()

app = Flask(__name__)
CORS(app)

ai = ExplosiveGirlfriendAI()


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"success": False, "error": "Missing message"}), 400

    message = data["message"].strip()
    expression = data.get("user_expression", "neutral")

    if not message:
        return jsonify({"success": False, "error": "Empty message"}), 400

    result = ai.chat(message, expression)
    return jsonify(result), 200


@app.route("/api/reset", methods=["POST"])
def reset():
    ai.reset_conversation()
    return jsonify({"success": True})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("Server running at http://localhost:8888")
    app.run(port=8888, debug=True)
