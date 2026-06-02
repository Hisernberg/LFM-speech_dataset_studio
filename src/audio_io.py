from .metrics import cer, transcript_scores
from .text_bn import bangla_quality_ok, normalize_bangla_text


def clean_lfm_correction(text: object) -> str:
    text = str(text).strip()
    lines = [normalize_bangla_text(x) for x in text.splitlines() if normalize_bangla_text(x)]
    if not lines:
        return ""
    lines = sorted(lines, key=lambda x: (len(x), x), reverse=True)
    return normalize_bangla_text(lines[0])


def correction_gate(raw: object, candidate: object) -> tuple[bool, str]:
    raw_n = normalize_bangla_text(raw)
    cand_n = normalize_bangla_text(candidate)
    if not cand_n:
        return False, "empty_candidate"
    if not bangla_quality_ok(cand_n):
        return False, "bad_bangla_quality"
    if not raw_n:
        return False, "empty_raw"
    ratio = len(cand_n) / max(1, len(raw_n))
    if ratio < 0.80 or ratio > 1.20:
        return False, f"length_ratio_outside_conservative_range:{ratio:.3f}"
    dist = cer(raw_n, cand_n)
    if dist > 0.12:
        return False, f"too_much_edit_conservative:{dist:.3f}"
    return True, "accepted"


def repair_record(reference: str, raw_asr: str, candidate: str) -> dict:
    accepted, reason = correction_gate(raw_asr, candidate)
    deploy_safe = candidate if accepted else raw_asr

    raw_cer = cer(reference, raw_asr)
    candidate_cer = cer(reference, candidate)
    deploy_safe_cer = cer(reference, deploy_safe)

    eval_oracle = candidate if candidate and candidate_cer < raw_cer else raw_asr
    eval_oracle_cer = min(candidate_cer if candidate else 1.0, raw_cer)

    rec = {
        "raw_asr": raw_asr,
        "lfm_candidate": candidate,
        "deploy_safe_transcript": deploy_safe,
        "eval_oracle_best_transcript": eval_oracle,
        "accepted_by_deploy_gate": accepted,
        "gate_reason": reason,
        "candidate_improved": bool(candidate and candidate_cer < raw_cer),
        "deploy_safe_improved": bool(deploy_safe_cer < raw_cer),
        "eval_oracle_improved": bool(eval_oracle_cer < raw_cer),
        "candidate_delta_positive_is_better": float(raw_cer - candidate_cer) if candidate else None,
        "deploy_safe_delta_positive_is_better": float(raw_cer - deploy_safe_cer),
        "eval_oracle_delta_positive_is_better": float(raw_cer - eval_oracle_cer),
    }
    rec.update(transcript_scores(reference, raw_asr, prefix="raw_"))
    rec.update(transcript_scores(reference, candidate, prefix="candidate_"))
    rec.update(transcript_scores(reference, deploy_safe, prefix="deploy_safe_"))
    rec.update(transcript_scores(reference, eval_oracle, prefix="eval_oracle_"))
    return rec
