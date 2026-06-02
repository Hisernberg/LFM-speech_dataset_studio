from lfm_speech_dataset_studio.text_bn import normalize_bangla_text, bn_ratio


def test_normalize_bangla_text():
    assert normalize_bangla_text("আমি, ভালো।") == "আমি ভালো"


def test_bn_ratio_positive():
    assert bn_ratio("বাংলা") > 0.9
