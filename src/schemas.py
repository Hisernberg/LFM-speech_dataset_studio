from __future__ import annotations

from .metrics import quality_band_from_cer
from .text_bn import extractive_summary_bn, top_keywords_bn

UNKNOWN_DOMAIN = "unknown_review"

ACTION_BY_DOMAIN = {
    "audio_books": "summarize_passage",
    "biography": "extract_person_note",
    "celebrity_interview": "summarize_interview",
    "class_lecture": "create_study_note",
    "documentary": "summarize_documentary",
    "drama_series": "summarize_dialogue",
    "kid_cartoon": "child_safe_summary",
    "kid_voice": "child_speech_review",
    "medicine": "medical_review_required",
    "parliament_speech": "civic_speech_summary",
    "political_talkshow": "discussion_summary",
    "sports": "sports_summary",
    "television_news": "news_summary",
    UNKNOWN_DOMAIN: "manual_review_required",
}

TASK_BY_DOMAIN = {
    "audio_books": "audio_book_note",
    "biography": "biography_note",
    "celebrity_interview": "interview_note",
    "class_lecture": "lecture_note",
    "documentary": "documentary_summary",
    "drama_series": "dialogue_note",
    "kid_cartoon": "child_content_note",
    "kid_voice": "child_speech_note",
    "medicine": "medical_note_review",
    "parliament_speech": "civic_speech_note",
    "political_talkshow": "discussion_note",
    "sports": "sports_note",
    "television_news": "news_note",
    UNKNOWN_DOMAIN: "manual_review_note",
}

VALID_TASKS = set(TASK_BY_DOMAIN.values())
VALID_ACTIONS = set(ACTION_BY_DOMAIN.values())
VALID_RISKS = {"low", "medium", "high"}


def deterministic_risk(
    route_domain: str,
    confidence: float,
    transcript: str,
    route_status: str,
    asr_cer_value: float | None = None,
    max_auto_cer: float = 0.35,
    min_route_chars: int = 12,
) -> str:
    transcript = transcript or ""
    if route_status == "abstained":
        return "high"
    if route_domain == "medicine":
        return "high"
    if route_domain in {"political_talkshow", "parliament_speech", "television_news"}:
        return "medium" if confidence >= 0.60 else "high"
    if route_domain in {"kid_voice", "kid_cartoon"}:
        return "medium"
    if asr_cer_value is not None:
        try:
            if float(asr_cer_value) > max_auto_cer:
                return "high"
        except Exception:
            pass
    if len(transcript) < min_route_chars:
        return "medium"
    return "low" if confidence >= 0.65 else "medium"


def deterministic_note(route_domain: str, risk: str, route_status: str) -> str:
    if route_status == "abstained" or route_domain == UNKNOWN_DOMAIN:
        return "Manual review is required because the transcript evidence is too weak for reliable routing."
    if risk == "high":
        return f"Review this {route_domain.replace('_', ' ')} transcript before any downstream use."
    if risk == "medium":
        return f"Use this {route_domain.replace('_', ' ')} transcript as a reviewable local note."
    return f"This {route_domain.replace('_', ' ')} transcript appears suitable for a low-risk local summary."


def validate_final_card(card: dict) -> bool:
    required = {
        "sample_uid",
        "language",
        "true_domain",
        "route_domain",
        "route_confidence",
        "route_status",
        "task_type",
        "local_action",
        "risk",
        "summary_bn",
        "keywords_bn",
        "assistant_note_en",
        "transcript_bn",
        "raw_asr",
        "needs_review",
        "review_reasons",
        "final_json_valid",
    }
    if not isinstance(card, dict):
        return False
    if not required.issubset(card):
        return False
    if card["task_type"] not in VALID_TASKS:
        return False
    if card["local_action"] not in VALID_ACTIONS:
        return False
    if card["risk"] not in VALID_RISKS:
        return False
    if card["route_status"] not in {"accepted", "abstained"}:
        return False
    if not isinstance(card["keywords_bn"], list):
        return False
    if not isinstance(card["review_reasons"], list):
        return False
    if not isinstance(card["needs_review"], bool):
        return False
    return True


def make_action_card(
    sample_uid: str,
    true_domain: str,
    forced_route_domain: str,
    route_domain: str,
    route_confidence: float,
    route_status: str,
    transcript_bn: str,
    raw_asr: str,
    review_reasons: list[str],
    raw_cer_eval: float | None = None,
    language: str = "bn",
    subset: str = "unknown",
) -> dict:
    risk = deterministic_risk(route_domain, route_confidence, transcript_bn, route_status, raw_cer_eval)
    task_type = TASK_BY_DOMAIN.get(route_domain, TASK_BY_DOMAIN[UNKNOWN_DOMAIN])
    local_action = ACTION_BY_DOMAIN.get(route_domain, ACTION_BY_DOMAIN[UNKNOWN_DOMAIN])
    reasons = sorted(set(review_reasons + (["high_risk"] if risk == "high" else [])))
    needs_review = bool(reasons or risk in {"medium", "high"})
    card = {
        "sample_uid": sample_uid,
        "language": language,
        "subset": subset,
        "true_domain": true_domain,
        "forced_route_domain": forced_route_domain,
        "route_domain": route_domain,
        "route_confidence": round(float(route_confidence), 6),
        "route_status": route_status,
        "task_type": task_type,
        "local_action": local_action,
        "risk": risk,
        "summary_bn": extractive_summary_bn(transcript_bn),
        "keywords_bn": top_keywords_bn(transcript_bn),
        "assistant_note_en": deterministic_note(route_domain, risk, route_status),
        "transcript_bn": transcript_bn,
        "raw_asr": raw_asr,
        "asr_quality_band": quality_band_from_cer(raw_cer_eval) if raw_cer_eval is not None else "unknown",
        "raw_cer_eval": raw_cer_eval,
        "needs_review": needs_review,
        "review_reasons": reasons,
        "final_json_valid": True,
    }
    card["final_json_valid"] = validate_final_card(card)
    return card
