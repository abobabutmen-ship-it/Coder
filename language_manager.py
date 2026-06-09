import json

class LanguageManager:
    def __init__(self, lang="en"):
        self.lang = lang
        self.translations = self.load_translations(lang)

    def load_translations(self, lang):
        try:
            with open(f"locales/{lang}.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Language file for '{lang}' not found. Defaulting to English.")
            return self.load_translations("en")

    def translate(self, key):
        return self.translations.get(key, key)