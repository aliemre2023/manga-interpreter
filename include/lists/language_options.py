from .. import translator

language_idx = {
    0: "EN",
    1: "TR",
    2: "ES",
    3: "FR",
    4: "DE",
    5: "IT",
    6: "PT",
    7: "RU",
    8: "ZH_CN",
    9: "ZH_TW",
    10: "KO",
    11: "AR",
    12: "HI",
    13: "BN",
    14: "NL",
    15: "SV",
    16: "PL",
    17: "DA",
    18: "NO",
    19: "FI"
}


language_names = {
    "EN": "English",
    "TR": "Turkish",
    "ES": "Spanish",
    "FR": "French",
    "DE": "German",
    "IT": "Italian",
    "PT": "Portuguese",
    "RU": "Russian",
    "ZH_CN": "Chinese (Simplified)",
    "ZH_TW": "Chinese (Traditional)",
    "KO": "Korean",
    "AR": "Arabic",
    "HI": "Hindi",
    "BN": "Bengali",
    "NL": "Dutch",
    "SV": "Swedish",
    "PL": "Polish",
    "DA": "Danish",
    "NO": "Norwegian",
    "FI": "Finnish"
}


language_options = {
    "EN": translator.translator_EN,
    "TR": translator.translator_TR,
    "ES": translator.translator_ES,
    "FR": translator.translator_FR,
    "DE": translator.translator_DE,
    "IT": translator.translator_IT,
    "PT": translator.translator_PT,
    "RU": translator.translator_RU,
    "ZH_CN": translator.translator_ZH_CN,
    "ZH_TW": translator.translator_ZH_TW,
    "KO": translator.translator_KO,
    "AR": translator.translator_AR,
    "HI": translator.translator_HI,
    "BN": translator.translator_BN,
    "NL": translator.translator_NL,
    "SV": translator.translator_SV,
    "PL": translator.translator_PL,
    "DA": translator.translator_DA,
    "NO": translator.translator_NO,
    "FI": translator.translator_FI
}

def to_list():
    return language_options.keys()
def to_name():
    return language_names.keys()

def func_selecter(selected, text):
    options = {
        "EN": lambda text: translator.translator_EN(text),
        "TR": lambda text: translator.translator_TR(text),
        "ES": lambda text: translator.translator_ES(text),
        "FR": lambda text: translator.translator_FR(text),
        "DE": lambda text: translator.translator_DE(text),
        "IT": lambda text: translator.translator_IT(text),
        "PT": lambda text: translator.translator_PT(text),
        "RU": lambda text: translator.translator_RU(text),
        "ZH_CN": lambda text: translator.translator_ZH_CN(text),
        "ZH_TW": lambda text: translator.translator_ZH_TW(text),
        "KO": lambda text: translator.translator_KO(text),
        "AR": lambda text: translator.translator_AR(text),
        "HI": lambda text: translator.translator_HI(text),
        "BN": lambda text: translator.translator_BN(text),
        "NL": lambda text: translator.translator_NL(text),
        "SV": lambda text: translator.translator_SV(text),
        "PL": lambda text: translator.translator_PL(text),
        "DA": lambda text: translator.translator_DA(text),
        "NO": lambda text: translator.translator_NO(text),
        "FI": lambda text: translator.translator_FI(text)
    }
    return options.get(selected, lambda text: f"Translation function for {selected} not found.")(text)

