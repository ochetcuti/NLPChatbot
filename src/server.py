from flask import Flask, render_template, request, jsonify
from chatbot import ChatbotResponseHandler
from preprocessor import TextPreprocessor
from sentiment_analyser import SentimentAnalyser
import json
import os
app = Flask(__name__)
chatbot = ChatbotResponseHandler()
preprocessor = TextPreprocessor()
sentiment_analyser = SentimentAnalyser()

def load_chat_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "demoData/demo.json")
    with open(file_path, "r") as file:
        return json.load(file)

chat_data = load_chat_data()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "I didn't catch that. Could you repeat?"})

    # process & analyse user input during pos 3
    stress_level = None
    if(chatbot.get_conversation_step() == 3):
        processed_message = preprocessor.preprocess(user_message)
        stress_level = sentiment_analyser.analyse_sentiment(processed_message)
        print(f"Stress Level: {stress_level}")        
    #  stress level passed
    bot_response = chatbot.get_response(stress_level)
    
    return jsonify({"response": bot_response, "stressLevel": stress_level})

@app.route("/chat/<scenario>")
def get_chat(scenario):
    if scenario in chat_data:
        return jsonify(chat_data[scenario])
    return jsonify({"error": "Scenario not found"}), 404

@app.route("/reset", methods=["POST"])
def reset():
    chatbot.reset_conversation()
    return jsonify({"response": "Conversation reset."})

if __name__ == "__main__":
    app.run(debug=True)
