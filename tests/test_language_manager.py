from language_manager import LanguageManager

def test_load_existing_locale():
    lm = LanguageManager("en")
    assert isinstance(lm.translate("welcome"), str)

def test_missing_key_returns_key():
    lm = LanguageManager("en")
    assert lm.translate("this_key_does_not_exist") == "this_key_does_not_exist"
