ACTION_CARD_REQUIRED_FIELDS = {
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


def is_jsonl_action_card_valid(card: dict) -> bool:
    return isinstance(card, dict) and ACTION_CARD_REQUIRED_FIELDS.issubset(card)
