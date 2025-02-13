import random

class ChatbotResponseHandler:
    def __init__(self):
        self.responses = {
            "warmup": [
                "Hello. How was your shift?",
                "Hey, how did your day go?",
                "Hope you're doing well. How has work been?"
            ],
            "context_exploration": [
                "That sounds intense. Anything specific that stood out?",
                "I see. Would you say today was more demanding than usual?",
                "Was there a case or situation that was particularly challenging?"
            ],
            "stress_check": [
                "That situation sounds tough. Were you able to take a break?",
                "Do you usually manage to step away during shifts?",
                "Did you have a moment to reset?"
            ],
            "reflection": [
                "That's understandable. How do you usually unwind after work?",
                "It's important to decompress. Do you have a routine that helps?",
                "Everyone needs a moment to reset. What works for you?"
            ],
            "supportive": [
                "That makes sense. Even a small break can help. Would that be an option?",
                "It's good to have ways to manage stress. Maybe a short pause later?",
                "If you need to take a breather, that's completely okay."
            ],
            "closing": [
                "If you want to check in again later, I'll be here. Anything else on your mind?",
                "I'm always here if you need a moment to reflect. Want to talk again soon?",
                "You can always come back whenever you need to chat."
            ],
            "exit": [
                "Okay. Take care and get some rest.",
                "Alright. Stay safe and take care.",
                "Hope you have a restful evening. Talk soon!"
            ]
        }

        # Define low-context responses to detect
        self.low_context_responses = {
            "fine", "okay", "good", "not really", "the usual", "same as always", "nothing special"
        }

        self.step_order = [
            "warmup", "context_exploration", "stress_check", "reflection",
            "supportive", "closing", "exit"
        ]
    
    def get_response(self, user_input, step):
        """Generate a chatbot response based on user input and conversation step."""
        # Convert input to lowercase for comparison
        cleaned_input = user_input.lower().strip()

        # If the response lacks context, re-prompt
        if cleaned_input in self.low_context_responses:
            return self.re_prompt(step)

        # Otherwise, proceed with the conversation normally
        return random.choice(self.responses[step])

    def re_prompt(self, step):
        """Generate a follow-up question when user input lacks context."""
        re_prompts = {
            "warmup": "Glad to hear that! Was it a routine day, or did something stand out?",
            "context_exploration": "I see. Would you say today was more demanding than normal?",
            "stress_check": "That makes sense. Do you usually manage to take breaks?",
            "reflection": "If you could, what's something small that might help you unwind?",
            "supportive": "Even taking a moment later could help. Would that be possible?",
            "closing": "Just making sure. Feel free to chat again anytime.",
            "exit": "Alright. Talk soon!"
        }
        return re_prompts.get(step, "Can you tell me more about that?")


if __name__ == "__main__":
    chatbot = ChatbotResponseHandler()
    conversation_step = 0

    print("Chatbot: " + chatbot.get_response("", "warmup"))

    while conversation_step < 6:  # Max 7 exchanges
        user_input = input("User: ")
        step_key = chatbot.step_order[conversation_step + 1]  # Get next step
        response = chatbot.get_response(user_input, step_key)
        print("Chatbot:", response)

        conversation_step += 1
