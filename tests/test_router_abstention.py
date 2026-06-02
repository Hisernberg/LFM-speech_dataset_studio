from lfm_speech_dataset_studio.cards import make_action_card, validate_final_card


def test_make_action_card_valid():
    card = make_action_card(
        sample_uid="x1",
        true_domain="audio_books",
        forced_route_domain="audio_books",
        route_domain="audio_books",
        route_confidence=0.91,
        route_status="accepted",
        transcript_bn="শরীফ ওদের বলে দিয়েছে",
        raw_asr="শরীফ ওদের বলে দিয়েছে",
        review_reasons=[],
        raw_cer_eval=0.0,
    )
    assert validate_final_card(card)
    assert card["final_json_valid"] is True
