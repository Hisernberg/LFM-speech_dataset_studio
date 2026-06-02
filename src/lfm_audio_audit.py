from pathlib import Path
import io
import math

import numpy as np
import soundfile as sf


def decode_audio_value(value, target_sr: int = 16000):
    y, sr = None, None

    if isinstance(value, dict):
        if value.get("array") is not None:
            y = np.asarray(value["array"], dtype=np.float32)
            sr = int(value.get("sampling_rate", target_sr))
        elif value.get("bytes") is not None:
            y, sr = sf.read(io.BytesIO(value["bytes"]), dtype="float32", always_2d=False)
        elif value.get("path") is not None and Path(str(value["path"])).exists():
            y, sr = sf.read(str(value["path"]), dtype="float32", always_2d=False)
    elif isinstance(value, (np.ndarray, list, tuple)):
        y = np.asarray(value, dtype=np.float32)
        sr = target_sr
    elif isinstance(value, str) and Path(value).exists():
        y, sr = sf.read(value, dtype="float32", always_2d=False)

    if y is None or sr is None:
        raise ValueError(f"Could not decode audio value of type={type(value)}")

    y = np.asarray(y, dtype=np.float32)
    if y.ndim > 1:
        y = y.mean(axis=1)
    y = np.nan_to_num(y)
    y = np.clip(y, -1.0, 1.0)

    if int(sr) != int(target_sr):
        import scipy.signal
        g = math.gcd(int(sr), int(target_sr))
        y = scipy.signal.resample_poly(y, int(target_sr) // g, int(sr) // g).astype(np.float32)
        sr = target_sr

    return y, int(sr)
