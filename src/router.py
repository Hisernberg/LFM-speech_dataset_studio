import re
import unicodedata

BN_DIGITS = "০১২৩৪৫৬৭৮৯"
EN_DIGITS = "0123456789"
EN_TO_BN_DIGIT = str.maketrans(EN_DIGITS, BN_DIGITS)
BN_TO_EN_DIGIT = str.maketrans(BN_DIGITS, EN_DIGITS)

MULTISPACE_RE = re.compile(r"\s+")
PUNCT_RE = re.compile(r"[“”‘’\"'`´।,;:!?()\[\]{}<>/\\|@#$%^&*_+=~]")
BN_CHAR_RE = re.compile(r"[\u0980-\u09FF]")
BAD_UNICODE_RE = re.compile(r"[�৳\u0900-\u097F\u0B00-\u0B7F]")


def normalize_bangla_text(text: object, digit_mode: str = "bn") -> str:
    if text is None:
        return ""
    text = unicodedata.normalize("NFKC", str(text))
    if digit_mode == "bn":
        text = text.translate(EN_TO_BN_DIGIT)
    elif digit_mode == "en":
        text = text.translate(BN_TO_EN_DIGIT)
    text = PUNCT_RE.sub(" ", text)
    text = re.sub(r"[-–—]+", " ", text)
    return MULTISPACE_RE.sub(" ", text).strip()


def bn_ratio(text: object) -> float:
    text = str(text)
    chars = [c for c in text if not c.isspace()]
    if not chars:
        return 0.0
    return sum(1 for c in chars if BN_CHAR_RE.match(c)) / max(1, len(chars))


def english_ratio(text: object) -> float:
    text = str(text)
    chars = [c for c in text if not c.isspace()]
    if not chars:
        return 0.0
    return sum(1 for c in chars if "a" <= c.lower() <= "z") / max(1, len(chars))


def bangla_quality_ok(text: object, min_bn_ratio: float = 0.35) -> bool:
    text = normalize_bangla_text(text)
    if not text:
        return False
    if BAD_UNICODE_RE.search(text):
        return False
    return bn_ratio(text) >= min_bn_ratio


def extractive_summary_bn(text: object, max_chars: int = 110) -> str:
    text = normalize_bangla_text(text)
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars].rsplit(" ", 1)[0].strip()
    return cut if cut else text[:max_chars].strip()


def top_keywords_bn(text: object, k: int = 6) -> list[str]:
    text = normalize_bangla_text(text)
    words = [w for w in text.split() if len(w) >= 3 and bn_ratio(w) > 0.5]
    stop = set("আমি তুমি তিনি তারা আমরা আপনার কিন্তু এবং জন্য মধ্যে থেকে হলে সেটা এটি এই সেই যেন তবে মানে হচ্ছে ছিল আছে করে করা সকল একজন".split())
    freq = {}
    for w in words:
        if w not in stop:
            freq[w] = freq.get(w, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:k]]
