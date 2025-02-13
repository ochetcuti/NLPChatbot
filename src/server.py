from flask import Flask, render_template, request, jsonify
from chatbot import ChatbotResponseHandler

app = Flask(__name__)
chatbot = ChatbotResponseHandler()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    bot_response = chatbot.get_response(user_message)
    return jsonify({"response": bot_response})

@app.route("/reset", methods=["POST"])
def reset():
    chatbot.reset_conversation()
    return jsonify({"response": "Conversation reset."})

if __name__ == "__main__":
    app.run(debug=True)
