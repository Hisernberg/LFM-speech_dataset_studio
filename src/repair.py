from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline


@dataclass
class RouteDecision:
    forced_route_domain: str
    route_domain: str
    route_confidence: float
    route_status: str
    review_reasons: list[str]


def build_router(random_state: int = 42) -> Pipeline:
    return Pipeline([
        ("features", FeatureUnion([
            ("charwb", TfidfVectorizer(
                analyzer="char_wb",
                ngram_range=(2, 5),
                min_df=2,
                max_features=140000,
                sublinear_tf=True,
            )),
            ("word", TfidfVectorizer(
                analyzer="word",
                ngram_range=(1, 2),
                min_df=2,
                max_features=50000,
                sublinear_tf=True,
            )),
        ])),
        ("clf", LogisticRegression(
            max_iter=1200,
            class_weight="balanced",
            C=3.0,
            n_jobs=2,
            random_state=random_state,
        )),
    ])


def predict_routes(model: Pipeline, texts: Iterable[str]) -> tuple[list[str], np.ndarray]:
    texts = list(texts)
    if not texts:
        return [], np.array([])
    probs = model.predict_proba(texts)
    pred_ids = probs.argmax(axis=1)
    classes = list(model.named_steps["clf"].classes_)
    pred_domains = [classes[int(i)] for i in pred_ids]
    conf = probs.max(axis=1)
    return pred_domains, conf


def apply_route_abstention(
    pred_domain: str,
    confidence: float,
    transcript: str,
    asr_cer_value: float | None = None,
    route_conf_threshold: float = 0.50,
    min_route_chars: int = 12,
    max_auto_cer: float = 0.35,
    unknown_domain: str = "unknown_review",
) -> RouteDecision:
    reasons: list[str] = []
    transcript = transcript or ""

    if confidence < route_conf_threshold:
        reasons.append("low_route_confidence")
    if len(transcript) < min_route_chars:
        reasons.append("short_transcript")
    if asr_cer_value is not None:
        try:
            if float(asr_cer_value) > max_auto_cer:
                reasons.append("high_asr_cer_eval_guard")
        except Exception:
            pass

    if reasons:
        return RouteDecision(
            forced_route_domain=pred_domain,
            route_domain=unknown_domain,
            route_confidence=float(confidence),
            route_status="abstained",
            review_reasons=reasons,
        )

    return RouteDecision(
        forced_route_domain=pred_domain,
        route_domain=pred_domain,
        route_confidence=float(confidence),
        route_status="accepted",
        review_reasons=[],
    )
