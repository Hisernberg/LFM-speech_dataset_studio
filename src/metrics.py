from dataclasses import dataclass
from pathlib import Path


@dataclass
class StudioConfig:
    dataset_id: str = "SUST-CSE-Speech/banspeech"
    lfm_audio_gguf_repo: str = "LiquidAI/LFM2.5-Audio-1.5B-GGUF"
    lfm_audio_quant: str = "Q4_0"
    lfm_text_id: str = "LiquidAI/LFM2.5-1.2B-Instruct"
    lfm_text_fallback_id: str = "LiquidAI/LFM2.5-350M"
    bangla_asr_id: str = "bangla-speech-processing/BanglaASR"
    target_sr: int = 16000
    route_conf_threshold: float = 0.50
    auto_route_conf_threshold: float = 0.65
    min_route_chars: int = 12
    max_auto_cer: float = 0.35
    out_root: Path = Path("outputs")
