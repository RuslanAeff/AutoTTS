"""Gerçek Kokoro üretimi ve WAV/MP3 çözümleme doğrulaması; model indirilebilir."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import soundfile as sf

from audio_io import save_audio
from tts_engine import KokoroEngine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", choices=["auto", "cpu", "mps"], default="auto")
    parser.add_argument("--voice", default="af_heart")
    parser.add_argument("--output", type=Path, default=Path("outputs/smoke"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    engine = KokoroEngine(args.device)
    text = Path("assets/sample.txt").read_text(encoding="utf-8")
    result = engine.synthesize(text, args.voice, status=lambda message: print(message, flush=True))
    assert result.sample_rate == 24000
    assert len(result.samples) > 2400
    assert np.isfinite(result.samples).all()
    assert float(np.max(np.abs(result.samples))) > 0.001
    for extension in ["wav", "mp3"]:
        path = save_audio(result, args.output / f"sample.{extension}")
        decoded, rate = sf.read(path)
        assert rate == 24000 and len(decoded) > 2400
        assert np.isfinite(decoded).all()
    print(json.dumps({"device": engine.device, "voice": args.voice,
                      "sample_rate": result.sample_rate,
                      "duration_seconds": round(len(result.samples) / result.sample_rate, 3),
                      "formats": ["wav", "mp3"], "result": "passed"}))


if __name__ == "__main__":
    main()
