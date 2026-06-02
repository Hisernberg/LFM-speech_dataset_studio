from .text_bn import normalize_bangla_text


def edit_distance_seq(a, b) -> int:
    a, b = list(a), list(b)
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        ai = a[i - 1]
        for j in range(1, m + 1):
            cost = 0 if ai == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[m]


def cer(ref: object, hyp: object) -> float:
    ref = normalize_bangla_text(ref)
    hyp = normalize_bangla_text(hyp)
    if len(ref) == 0:
        return 0.0 if len(hyp) == 0 else 1.0
    return edit_distance_seq(ref, hyp) / max(1, len(ref))


def clipped_cer(ref: object, hyp: object) -> float:
    return min(1.0, cer(ref, hyp))


def wer_simple(ref: object, hyp: object) -> float:
    ref_w = normalize_bangla_text(ref).split()
    hyp_w = normalize_bangla_text(hyp).split()
    if len(ref_w) == 0:
        return 0.0 if len(hyp_w) == 0 else 1.0
    return edit_distance_seq(ref_w, hyp_w) / max(1, len(ref_w))


def clipped_wer(ref: object, hyp: object) -> float:
    return min(1.0, wer_simple(ref, hyp))


def transcript_scores(ref: object, hyp: object, prefix: str = "") -> dict:
    c = cer(ref, hyp)
    w = wer_simple(ref, hyp)
    cc = min(1.0, c)
    cw = min(1.0, w)
    return {
        f"{prefix}cer": float(c),
        f"{prefix}cer_clipped": float(cc),
        f"{prefix}wer": float(w),
        f"{prefix}wer_clipped": float(cw),
        f"{prefix}char_accuracy": float(max(0.0, 1.0 - cc)),
        f"{prefix}word_accuracy_clipped": float(max(0.0, 1.0 - cw)),
        f"{prefix}exact_match": normalize_bangla_text(ref) == normalize_bangla_text(hyp),
        f"{prefix}empty_prediction": len(normalize_bangla_text(hyp)) == 0,
        f"{prefix}ref_char_len": len(normalize_bangla_text(ref)),
        f"{prefix}pred_char_len": len(normalize_bangla_text(hyp)),
    }


def quality_band_from_cer(value: float) -> str:
    try:
        value = float(value)
    except Exception:
        return "unknown"
    if value <= 0.10:
        return "excellent"
    if value <= 0.25:
        return "good"
    if value <= 0.45:
        return "usable"
    return "poor"
