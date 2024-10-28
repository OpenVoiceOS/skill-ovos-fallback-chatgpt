from ovos_bus_client.session import SessionManager
from ovos_solver_openai_persona import OpenAIPersonaSolver
from ovos_utils import classproperty
from ovos_utils.process_utils import RuntimeRequirements
from ovos_workshop.skills.fallback import FallbackSkill


DEFAULT_SETTINGS = {
    "persona": "You are a helpful voice assistant with a friendly tone and fun sense of humor. You respond in 40 words or fewer.",
    "model": "gpt-3.5-turbo",
}


class ChatGPTSkill(FallbackSkill):
    sessions = {}

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(
            internet_before_load=True,
            network_before_load=True,
            requires_internet=True,
            requires_network=True,
        )

    def initialize(self):
        self.settings.merge(DEFAULT_SETTINGS, new_only=True)
        self.add_event("speak", self.handle_speak)
        self.add_event("recognizer_loop:utterance", self.handle_utterance)
        self.register_fallback(self.ask_chatgpt, 85)

    @property
    def ai_name(self):
        return self.settings.get("name", "Chat G.P.T.")

    @property
    def confirmation(self):
        return self.settings.get("confirmation", True)

    @property
    def chat(self):
        """created fresh to allow key/url rotation when settings.json is edited"""
        try:
            return OpenAIPersonaSolver(config=self.settings)
        except Exception as err:
            self.log.error(err)
            return None

    def handle_utterance(self, message):
        utt = message.data.get("utterances")[0]
        sess = SessionManager.get(message)
        if sess.session_id not in self.sessions:
            self.sessions[sess.session_id] = []
        self.sessions[sess.session_id].append(("user", utt))

    def handle_speak(self, message):
        utt = message.data.get("utterance")
        sess = SessionManager.get(message)
        if sess.session_id in self.sessions:
            self.sessions[sess.session_id].append(("ai", utt))

    def build_msg_history(self, message):
        sess = SessionManager.get(message)
        if sess.session_id not in self.sessions:
            return []
        messages = []  # tuple of question, answer

        q = None
        ans = None
        for m in self.sessions[sess.session_id]:
            if m[0] == "user":
                if ans is not None and q is not None:
                    # save previous q/a pair
                    messages.append((q, ans))
                    q = None
                ans = None
                q = m[1]  # track question
            elif m[0] == "ai":
                if ans is None:
                    ans = m[1]  # track answer
                else:  # merge multi speak answers
                    ans = f"{ans}. {m[1]}"

        # save last q/a pair
        if ans is not None and q is not None:
            messages.append((q, ans))
        return messages

    def _async_ask(self, message):
        utterance = message.data["utterance"]
        chat = self.chat
        chat.qa_pairs = self.build_msg_history(message)
        answered = False
        try:
            for utt in chat.stream_utterances(utterance):
                answered = True
                self.speak(utt)
        except Exception as err:  # speak error on any network issue / no credits etc
            self.log.error(err)
        if not answered:
            self.speak_dialog("gpt_error", data={"name": self.ai_name})

    def ask_chatgpt(self, message):
        if "key" not in self.settings:
            self.log.error(
                "ChatGPT not configured yet, please set your API key in %s",
                self.settings.path,
            )
            return False  # ChatGPT not configured yet
        utterance = message.data["utterance"]
        if self.confirmation:
            self.speak_dialog("asking", data={"name": self.ai_name})
        # ask in a thread so fallback doesnt timeout
        self.bus.once("async.chatgpt.fallback", self._async_ask)
        self.bus.emit(
            message.forward("async.chatgpt.fallback", {"utterance": utterance})
        )
        return True
