import requests
from collections import defaultdict

try:
    from translate import Translator
except ImportError:
    Translator = None

qwestions = {
    "what's your name": "I'm a super-cool-bot and my purpose is to help you!",
    "how old are you": "That's too philosophical of a question",
}


class TextAnalysis:
    memory = defaultdict(list)

    def __init__(self, text, owner):
        self.text = text
        self.owner = owner

        TextAnalysis.memory[owner].append(self)

        self.translation = self.__translate(self.text, "ru", "en")
        if self.text.lower() in qwestions.keys():
            self.response = qwestions[self.text.lower()]
        else:
            self.response = self.get_answer()

    def get_answer(self):
        res = self.__translate("I don't know how to help", "en", "ru")
        return res

    def __translate(self, text, from_lang, to_lang):
        try:
            if Translator is None:
                return "Перевод не удался"
            translator = Translator(from_lang=from_lang, to_lang=to_lang)
            translation = translator.translate(text)
            return translation
        except Exception:
            return "Перевод не удался"
