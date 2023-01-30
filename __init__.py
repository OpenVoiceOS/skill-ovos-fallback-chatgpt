import openai as ai
from ovos_workshop.skills.fallback import FallbackSkill


class ChatGPTSkill(FallbackSkill):

    def __init__(self):
        super().__init__("ChatGPT")
        self._chat = None
        self._chatlog = ""

    def initialize(self):
        # lazy load
        initchat = self.chatgpt is not None
        self.add_event("speak", self.handle_speak)
        self.add_event("recognizer_loop:utterance", self.handle_utterance)
        self.register_fallback(self.ask_chatgpt, 85)

    def handle_utterance(self, message):
        utt = message.data.get("utterances")[0]
        # TODO: imperfect, subject to race conditions between bus messages
        if self.memory and self._chatlog.endswith("Human: "):
            self._chatlog += f"{utt}\nAI: "

    def handle_speak(self, message):
        utt = message.data.get("utterance")
        # TODO: imperfect, subject to race conditions between bus messages
        # does not handle multi speak answers
        if self.memory and self._chatlog.endswith("AI: "):
            self._chatlog += f"{utt}\nHuman: "

    @property
    def memory(self):
        return self.settings.get("memory", True)

    @property
    def initial_prompt(self):
        start_chat_log = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.

Human: Hello, who are you?
AI: I am an AI created by OpenAI. How can I help you today?
Human: """
        return self.settings.get("initial_prompt", start_chat_log)

    @property
    def chatgpt(self):
        # this is a property to allow lazy init
        # the key may be set after skill is loaded
        key = self.settings.get("key")
        if not key:
            raise ValueError("OpenAI api key not set in skill settings.json")
        if not self._chat:
            ai.api_key = key
            self._chat = ai.Completion()
        return self._chat

    def get_prompt(self, utt):
        start_chat = self.initial_prompt
        if self.memory:
            self._chatlog = self._chatlog or start_chat
            if self._chatlog.endswith("\nHuman: "):
                self._chatlog += f"{utt}\nAI: "
            elif self._chatlog.endswith("\nAI: "):
                self._chatlog += f"Please rephrase the question\nHuman: {utt}\nAI: "
            else:
                self._chatlog += f"\nHuman: {utt}\nAI: "
            prompt = self._chatlog
        else:
            prompt = start_chat + f"{utt}?\nAI: "
        return prompt

    def ask_chatgpt(self, message):
        utterance = message.data['utterance']
        prompt = self.get_prompt(utterance)
        # TODO - params from skill settings
        response = self.chatgpt.create(prompt=prompt, engine="davinci", temperature=0.85, top_p=1, frequency_penalty=0,
                                       presence_penalty=0.7, best_of=2, max_tokens=100, stop="\nHuman: ")
        answer = response.choices[0].text.split("Human: ")[0].split("AI: ")[0].strip()
        if not answer or not answer.strip("?"):
            return False
        if self.memory:
            self._chatlog += answer
        self.speak(answer)
        return True


def create_skill():
    return ChatGPTSkill()


if __name__ == "__main__":
    from ovos_utils.messagebus import FakeBus, Message

    s = ChatGPTSkill()
    s._startup(bus=FakeBus())
    msg = Message("intent_failure", {"utterance": "Explain quantum computing in simple terms"})
    s.ask_chatgpt(msg)
    # funny failure cases:
    #    ????
    #    Are you seriously asking that?
    #    I hardly understand quantum physics myself, but I found an article that you might find useful.
