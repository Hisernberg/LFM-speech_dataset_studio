from lfm_speech_dataset_studio.metrics import cer, clipped_cer, wer_simple


def test_cer_exact_match():
    assert cer("বাংলা", "বাংলা") == 0.0


def test_cer_non_empty():
    assert cer("বাংলা", "") == 1.0


def test_clipped_cer():
    assert clipped_cer("অ", "অনেক অনেক") == 1.0


def test_wer_exact_match():
    assert wer_simple("আমি ভালো", "আমি ভালো") == 0.0
