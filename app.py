from flask import Flask, request, jsonify
from ai.core import generate_response
from memory.memory import save_message, get_history
from tools.image import generate_image

app = Flask(__name__)

@app.route("/ai", methods=["POST"])
def ai_chat():
    data = request.json
    user_id = data.get("user_id")
    message = data.get("message")
    mode = data.get("mode", "royal")

    if not user_id or not message:
        return jsonify({"error": "user_id and message required"}), 400

    history = get_history(user_id)
    reply = generate_response(message, mode, history)
    save_message(user_id, "user", message)
    save_message(user_id, "assistant", reply)

    return jsonify({"reply": reply})

@app.route("/image", methods=["POST"])
def image_gen():
    data = request.json
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "prompt required"}), 400
    url = generate_image(prompt)
    return jsonify({"image_url": url})

@app.route("/history/<user_id>", methods=["GET"])
def chat_history(user_id):
    history = get_history(user_id)
    return jsonify({"history": history})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
