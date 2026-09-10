"""Sıralı toplu üretim; tek dosya hatası kalan kuyruğu durdurmaz."""
from dataclasses import dataclass
from pathlib import Path

from audio_io import save_audio
from tts_engine import TTSEngine, TTSError


@dataclass
class BatchResult:
    outputs: list[Path]
    failures: list[tuple[str, str]]


def run_batch(engine: TTSEngine, files, folder, voice, speed, extension=".wav",
              status=lambda _: None, progress=lambda _: None):
    result = BatchResult([], [])
    for index, source in enumerate(files):
        source = Path(source)
        try:
            text = source.read_text(encoding="utf-8-sig")
            audio = engine.synthesize(text, voice, speed, status)
            # Özel çıktı klasöründe bile aynı adlı girişler birbirini ezmez.
            destination = Path(folder) / f"{index + 1:03d}_{source.stem}{extension}"
            if destination.exists():
                raise FileExistsError("Çıktı zaten var")
            result.outputs.append(save_audio(audio, destination))
        except Exception as exc:
            if isinstance(exc, TTSError):
                reason = str(exc)
            elif isinstance(exc, UnicodeError):
                reason = "Dosya UTF-8 kodlamasıyla okunamadı."
            elif isinstance(exc, OSError):
                reason = "Dosya erişimi veya çıktı çakışması; izinleri kontrol edin."
            else:
                reason = f"İşlem tamamlanamadı ({type(exc).__name__})."
            result.failures.append((source.name, reason))
        progress((index + 1) / len(files))
    return result
