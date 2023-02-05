from ovos_workshop.skills.fallback import FallbackSkill
from ovos_backend_client.api import ChatbotApi, BackendType


class ChatGPTSkill(FallbackSkill):

    def __init__(self):
        super().__init__("ChatGPT")

    def initialize(self):
        if "persona" not in self.settings:
            self.settings["persona"] = "helpful, creative, clever, and very friendly."
        self.api = ChatbotApi(backend_type=BackendType.OVOS_API)
        self.register_fallback(self.ask_chatgpt, 85)

    def ask_chatgpt(self, message):
        utterance = message.data['utterance']
        answer = self.api.ask(utterance, params=self.settings)
        if answer:
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
    print(s.qa_pairs[-1])
    msg = Message("intent_failure", {"utterance": "Got any creative ideas for a 10 year old’s birthday?"})
    s.ask_chatgpt(msg)
    print(s.qa_pairs[-1])
    msg = Message("intent_failure", {"utterance": "Do you think aliens exist?"})
    s.ask_chatgpt(msg)
    print(s.qa_pairs[-1])
    msg = Message("intent_failure", {"utterance": "When will the world end?"})
    s.ask_chatgpt(msg)
    print(s.qa_pairs[-1])
    print("##################################3")
    print(s.chat_history)
    # funny failure cases:
    #    ????
    #    Are you seriously asking that?
    #    I hardly understand quantum physics myself, but I found an article that you might find useful.
