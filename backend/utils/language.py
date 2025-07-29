from langdetect import detect

def detect_language(text: str) -> str:
    try:
        lang_code = detect(text)

        if lang_code == "hi":
            return "hindi"

        elif lang_code == "en":
            # Smart check for Hinglish words
            if any(word in text.lower() for word in ["tum", "nahi", "kya", "acha", "kaise", "haan"]):
                return "hinglish"
            else:
                return "english"
        else:
            return "english"

    except:
        return "english"
