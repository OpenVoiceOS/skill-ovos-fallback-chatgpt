from ovos_workshop.skills.fallback import FallbackSkill
from ovos_utils.process_utils import RuntimeRequirements
from ovos_utils import classproperty
from ovos_solver_openai_persona import OpenAIPersonaSolver


class ChatGPTSkill(FallbackSkill):

    def __init__(self):
        super().__init__("ChatGPT")
        self.current_q = None
        self.current_a = None

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(internet_before_load=True,
                                   network_before_load=True,
                                   gui_before_load=False,
                                   requires_internet=True,
                                   requires_network=True,
                                   requires_gui=False,
                                   no_internet_fallback=False,
                                   no_network_fallback=False,
                                   no_gui_fallback=True)

    def initialize(self):
        self._chat = OpenAIPersonaSolver(config=self.settings)
        self.add_event("speak", self.handle_speak)
        self.add_event("recognizer_loop:utterance", self.handle_utterance)
        self.register_fallback(self.ask_chatgpt, 85)

    def handle_utterance(self, message):
        utt = message.data.get("utterances")[0]
        if self.current_q and self.current_a:
            self._chat.qa_pairs.append((self.current_q, utt))
        self.current_q = utt
        self.current_a = None
        # TODO: imperfect, subject to race conditions between bus messages
        # use session_id/ident to track all matches

    def handle_speak(self, message):
        utt = message.data.get("utterance")
        if not self.current_q:
            # TODO - use session_id/ident to track all matches
            # append to previous question if multi-speak answer
            return
        if self.current_a:
            self.current_a += ". " + utt

    def ask_chatgpt(self, message):
        self.current_a = None
        utterance = message.data['utterance']
        answer = self._chat.get_spoken_answer(utterance)
        if not answer:
            return False
        self.current_q = None
        self.speak(answer)
        return True


def create_skill():
    return ChatGPTSkill()

