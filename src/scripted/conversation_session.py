"""
conversation_session.py: controls scripted chats with response and stress management
"""
from preprocessor import TextPreprocessor
from scripted.sentiment_analyser import SentimentAnalyser
from scripted.chatbot import ChatbotResponseHandler
class ConversationSession:
    """
    route logic controller
    handels scripted chat capabilites
    """
    def __init__(self):
        """
        loads relevent classes;
        preprocessing (full), model, and chatbot response
        """
        self.preprocessor = TextPreprocessor(1)
        self.sentiment_analyser = SentimentAnalyser()
        self.chatbot = ChatbotResponseHandler()
        self.stress_level = None

    def process_user_message(self, message):
        """
        run the user message through the preprocessing, then get a stressor score and return a chatbot response

        Args:
            message (str): raw user input
        Returns:
            array: response message and the stress level string of the current message input
        """
        stress_level= None
        print(f"DEBUG: CURRENT STEP {self.chatbot.get_conversation_step()}")
        if self.chatbot.get_conversation_step() not in {0, 6}:
            cleaned = self.preprocessor.preprocess(message)
            stress_level = self.sentiment_analyser.analyse_sentiment(cleaned)
            self.stress_level = stress_level 
        response = self.chatbot.get_response(stress_level)
        return response, stress_level #only current result

    def reset(self):
        """
        reset severside stress level and conversation steps
        """
        self.chatbot.reset_conversation()
        self.stress_level = None
