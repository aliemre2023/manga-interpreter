from translate import Translator

def translator_TR(text):
    translator = Translator(from_lang="ja", to_lang="tr")
    translation = translator.translate(f"{text}")
    return translation
def translator_EN(text):
    translator = Translator(from_lang="ja", to_lang="en")
    translation = translator.translate(f"{text}")
    return translation