"""
semantic_session.py: controls semantic chats with response and stress management
"""
from preprocessor import TextPreprocessor
from semantic.semantic_stress_matcher import SemanticStressMatcher
from scripted.chatbot import ChatbotResponseHandler
class ConversationSession:
    """
    route logic controller
    handels semantic chat capabilites
    """
    def __init__(self):
        """
        loads relevent classes;
        preprocessing (minimal), embeddings, and chatbot response
        """
        try:
            self.preprocessor = TextPreprocessor(2)
            self.semantic_analyser = SemanticStressMatcher("src/semantic/SAD_semantic_dataset.xlsx", "paraphrase-mpnet-base-v2")
            self.chatbot = ChatbotResponseHandler()
            self.stress_level = None
            self.endChat = False
        except Exception as e:
            print(f"Error initializing ConversationSession: {e}")
            raise  #get_session() catches it

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
        # not first (init) or last message
        if self.chatbot.get_conversation_step() not in {0, 6}:
            cleaned = self.preprocessor.preprocess(message)
            self.semantic_analyser.find_closest(cleaned)
            stress_level = self.semantic_analyser.threshold_serverity()
            self.stress_level = stress_level 
        response = self.chatbot.get_response(stress_level)
        return response, stress_level #only current result

    def reset(self):
        """
        reset severside stress level and conversation steps
        """
        self.chatbot.reset_conversation()
        self.stress_level = None
