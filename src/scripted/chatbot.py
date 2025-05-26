import random

class ChatbotResponseHandler:
    def __init__(self):

        self.responses = {
            "warmup": [
                "Hello. How was your shift?",
                "Hey, how did your day go?",
                "Hope you're doing well. How has work been?"
            ],
            "context_exploration": {
                "high_stress": ["That sounds intense. Anything specific that stood out?"],
                "moderate_stress": ["I see. Would you say today was more demanding than usual?"],
                "low_stress": ["Was there a case or situation that was particularly challenging?"]
            },
            "stress_check": {
                "high_stress": ["That situation sounds tough. Were you able to take a break?"],
                "moderate_stress": ["Do you usually manage to step away during shifts?", "Did you have a moment to reset?"],
                "low_stress": ["Sounds like a good day, did you manage okay?"]
            },
            "reflection": {
                "high_stress": [
                    "That sounds incredibly overwhelming. You have been handling a lot, please dont forget to care for yourself too.",
                    "Its okay to feel drained after days like this. Have you thought about talking to someone or just unwinding a bit?",
                    "These days take a toll. Do you have any downtime planned soon?"
                ],
                "moderate_stress": [
                    "Its been a bit of a grind, huh? Hopefully you will get a breather later.",
                    "Sounds like its been a demanding day, but manageable. What usually helps you reset?",
                    "You are handling a lot. Do you have something you are looking forward to?"
                ],
                "low_stress": [
                    "Sounds like you managed today quite well. Any highlights?",
                    "Even steady days deserve a break. How will you relax tonight?",
                    "Nice to hear it wasnt too intense. Got any plans to wind down?"
                ]
            },
            "supportive": {
                "high_stress": ["That makes sense. Even a small break can help. Would that be an option?", "Its good to have ways to manage stress. Maybe a short pause later?", "If you need to take a breather, thats completely okay."],
                "moderate_stress": ["That makes sense. Even a small break can help. Would that be an option?", "Its good to have ways to manage stress. Maybe a short pause later?"],
                "low_stress": ["Sounds like you have got a plan. Ready to go home?"]
            },
            "closing": [
                "If you want to check in again later, I'll be here.",
                "I'm always here if you need a moment.",
                "You can always come back whenever you need to chat."
            ]
        }

        self.low_context_responses = {
            "fine", "okay", "good", "not really", "the usual", "same as always", "nothing special"
        }

        self.step_order = [
            "warmup", "context_exploration", "stress_check", "reflection",
            "supportive", "closing"
        ]

        self.conversation_step = 0 

    def get_response(self, stress_level):
        # lacks context, re-prompt (needs to be moved)
        #if cleaned_input in self.low_context_responses:
        #    return self.re_prompt()

        # normal conversation step
        if self.conversation_step < len(self.step_order):
            step = self.step_order[self.conversation_step]
            # step to next for next message
            self.conversation_step += 1
            # typecheck for variable response
            if isinstance(self.responses[step], dict):
                return random.choice(self.responses[step][stress_level])
            else:
                return random.choice(self.responses[step])

        # Added if the chat runs over. not expected to be called
        return "Alright, talk soon!"

    def re_prompt(self):
        # not included in final
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

    def is_chat_ended(self):
        step = self.get_conversation_step()
        stepname = self.step_order[step]
        if(stepname == "closing"):
            return True
        else:
            return False