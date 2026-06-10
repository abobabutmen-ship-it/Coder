import json
import os

DEFAULT_TRANSLATIONS = {
    "welcome": "Welcome!",
    "analyze_prompt": "Enter code to analyze:",
    "error_found": "Errors found:",
    "no_errors": "No errors detected."
}

class LanguageManager:
    def __init__(self, lang="en"):
        self.lang = lang
        self.translations = self.load_translations(lang)

    def load_translations(self, lang):
        path = os.path.join("locales", f"{lang}.json")
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            # fallback to English if requested language missing
            if lang != "en":
                return self.load_translations("en")
            # if English also missing, return defaults
            return DEFAULT_TRANSLATIONS.copy()
        except Exception:
            return DEFAULT_TRANSLATIONS.copy()

    def translate(self, key):
        return self.translations.get(key, key)
