from ovos_solver_openai_persona import OpenAIPersonaSolver
from ovos_solver_openai_persona.prompts import OpenAIPersonaPromptSolver
from ovos_utils import classproperty
from ovos_utils.log import LOG
from ovos_utils.process_utils import RuntimeRequirements
from ovos_workshop.skills.fallback import FallbackSkill


class ChatGPTSkill(FallbackSkill):

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
        self.current_q = None
        self.current_a = None
        chat_engines = ["gpt-3.5-turbo"]
        text_completions = ["ada", "babbage", "curie", "davinci",
                            "text-davinci-002", "text-davinci-003"]
        code_completions = ["code-cushman-001", "code-davinci-002"]
        engine = self.settings.get("model", "gpt-3.5-turbo")
        if engine in chat_engines:
            self._chat = OpenAIPersonaSolver(config=self.settings)
        elif engine in text_completions:  # davinci/ada ...
            self._chat = OpenAIPersonaPromptSolver(config=self.settings)
        else:
            LOG.warning(f"valid models: {chat_engines + text_completions}")
            raise ValueError(f"invalid OpenAI model: {engine}")
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
        else:
            self.current_a = utt

    def ask_chatgpt(self, message):
        self.current_a = None
        utterance = message.data['utterance']
        answer = self._chat.get_spoken_answer(utterance)
        if not answer:
            return False
        self.current_q = None
        self.speak(answer)
        return True
