"""
routes.py: route manager for scripted sessions
"""

from flask import Blueprint, render_template, request, jsonify
from scripted.conversation_session import ConversationSession
import os, json


scripted_blueprint = Blueprint("scripted", __name__)
sessions = {}

def load_chat_data():
    """
    load the demonstration chat messages

    Returns:
        json: loaded file data
    """
    file_path = os.path.join(os.path.dirname(__file__), "demo.json")
    with open(file_path, "r") as file:
        return json.load(file)

chat_data = load_chat_data()

def get_session(session_id):
    """
    getter to check if session is alredy active, if not initalise the session

    Args:
        session_id (str): IP of user for uniqueness
    Returns:
        str: sessionID
    """
    if session_id not in sessions:
        sessions[session_id] = ConversationSession()
    return sessions[session_id]


@scripted_blueprint.route("/chat", methods=["POST"])
def chat():
    """
    route for initalising and chat messages, as soon as a user makes this request a chat is started

    Args:
        request (object): user request header
    Returns:
        json: response to the user, usually a message response
    """
    session_id = request.remote_addr
    user_message = request.json.get("message", "").strip()
    session = get_session(session_id)

    if not user_message:
        return jsonify({"response": "I didn't catch that."})

    response, stress_level = session.process_user_message(user_message)
    return jsonify({"response": response, "stressLevel": stress_level})

@scripted_blueprint.route("/scenarios")
def get_scenarios():
    """
    index scenarios file listing for main page
    Returns:
        json: all titles and images
    """
    return jsonify({
        key: {
            "title": value["title"],
            "image": value["image"]
        } for key, value in chat_data.items()
    })

@scripted_blueprint.route("/chat/<scenario>")
def get_chat(scenario):
    """
    specific scenario selection with image, text and header
    Returns:
        json: specific scenario to the client
    """
    if scenario in chat_data:
        return jsonify(chat_data[scenario])
    return jsonify({"error": "Scenario not found"}), 404

@scripted_blueprint.route("/reset", methods=["POST"])
def reset():
    """
    reset the chatbot steps and session from within the scripted session controller

    Args:
        request (object): user request header
    Returns:
        json: response to the user, usually a message response
    """
    session_id = request.remote_addr
    get_session(session_id).reset()
    return jsonify({"response": "Conversation reset."})
