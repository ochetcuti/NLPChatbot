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

        self.low_context_responses = {
            "fine", "okay", "good", "not really", "the usual", "same as always", "nothing special"
        }

        self.step_order = [
            "warmup", "context_exploration", "stress_check", "reflection",
            "supportive", "closing", "exit"
        ]

        self.conversation_step = 0 

    def get_response(self, stress_level):
        # lacks context, re-prompt (needs to be moved)
        #if cleaned_input in self.low_context_responses:
        #    return self.re_prompt()

        # normal conversation step
        if self.conversation_step < len(self.step_order):
            step = self.step_order[self.conversation_step]
            self.conversation_step += 1
            return random.choice(self.responses[step])

        return "Alright, talk soon!"

    def re_prompt(self):
        re_prompts = [
            "Can you tell me more about that?",
            "I see. Would you say today was more demanding than usual?",
            "Do you usually manage to take breaks?",
            "If you could, what's something small that might help you unwind?",
            "Just making sure. Feel free to chat again anytime."
        ]
        return random.choice(re_prompts)

    def reset_conversation(self):
        self.conversation_step = 0

    def get_conversation_step(self):
        return self.conversation_step
