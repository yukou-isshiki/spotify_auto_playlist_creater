from watson_developer_cloud import LanguageTranslatorV3 as LanguageTranslator

def translate_word(text):
    langage_translator = LanguageTranslator(username="", password="", version="2018-11-17")
    text_list = []
    text_list.append(text)
    translation = langage_translator.translate(text=text_list, model_id="en-ja")
    result = translation.get_result()
    translations = result["translations"]
    word_list = translations[0]
    trans_word = word_list["translation"]
    return trans_word