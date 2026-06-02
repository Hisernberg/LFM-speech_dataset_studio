from lfm_speech_dataset_studio.router import apply_route_abstention


def test_abstains_on_low_confidence():
    d = apply_route_abstention("sports", 0.2, "বাংলা বাক্য", None)
    assert d.route_domain == "unknown_review"
    assert d.route_status == "abstained"


def test_accepts_high_confidence():
    d = apply_route_abstention("sports", 0.9, "এটি একটি যথেষ্ট বড় বাংলা বাক্য", 0.1)
    assert d.route_domain == "sports"
    assert d.route_status == "accepted"
