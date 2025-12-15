from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    # dummy response (replace with OpenAI later)
    return jsonify(
        reply=f"You said: {message}"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
