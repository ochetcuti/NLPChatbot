"""
routes.py: route manager for semantic sessions
"""

from flask import Blueprint, request, jsonify
from semantic.semantic_session import ConversationSession
semantic_blueprint = Blueprint("semantic", __name__)
sessions = {}

def get_session(session_id):
    """
    getter to check if session is alredy active, if not initalise the session

    Args:
        session_id (str): IP of user for uniqueness
    Returns:
        str: sessionID
    """
    if session_id not in sessions:
        try:
            sessions[session_id] = ConversationSession()
        except:
            return None
    return sessions[session_id]

@semantic_blueprint.route("/chat", methods=["POST"])
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
    if not session:
        return jsonify({"error": "server failed to load session"}), 500
    if not user_message:
        return jsonify({"response": "I didn't catch that."})

    response, stress_level = session.process_user_message(user_message)
    return jsonify({"response": response, "stressLevel": stress_level})


@semantic_blueprint.route("/reset", methods=["POST"])
def reset():
    """
    reset the chatbot steps and session from within the semantic session controller

    Args:
        request (object): user request header
    Returns:
        json: response to the user, usually a message response
    """
    session_id = request.remote_addr
    get_session(session_id).reset()
    return jsonify({"response": "Conversation reset."})
