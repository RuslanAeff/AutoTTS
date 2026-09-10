"""Ses dosyalarının atomik dışa aktarımı; GUI ve modelden bağımsızdır."""
import os
from pathlib import Path
import tempfile

import soundfile as sf

from tts_engine import AudioResult, TTSError


def export_path(destination: Path, selected_format: str) -> Path:
    """Kayıt diyaloğundan gelen eski uzantı seçilen codec'i değiştirmemeli."""
    extension = "." + selected_format.lower().lstrip(".")
    if extension not in {".wav", ".mp3"}:
        raise TTSError("Kayıt formatı WAV veya MP3 olmalı.")
    destination = Path(destination)
    if destination.suffix.lower() in {".wav", ".mp3"}:
        return destination.with_suffix(extension)
    # Noktalı dosya adlarını koru; yalnız bilinen ses uzantılarını değiştir.
    return destination.with_name(destination.name + extension)


def save_audio(audio: AudioResult, destination: Path) -> Path:
    destination = Path(destination)
    fmt = destination.suffix.lower()
    if fmt not in {".wav", ".mp3"}:
        raise TTSError("Dosya uzantısı .wav veya .mp3 olmalı.")
    if fmt == ".mp3" and not sf.check_format("MP3"):
        raise TTSError("Bu libsndfile kurulumu MP3 yazamıyor. Soundfile paketini güncelleyin veya WAV seçin.")
    temporary = None
    try:
        # Aynı klasörde geçici dosya: başarısız yazım mevcut çıktıyı bozmaz.
        with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=fmt, delete=False) as handle:
            temporary = Path(handle.name)
        sf.write(temporary, audio.samples, audio.sample_rate,
                 format="WAV" if fmt == ".wav" else "MP3",
                 subtype="PCM_16" if fmt == ".wav" else None)
        os.replace(temporary, destination)
        return destination
    except (OSError, RuntimeError, ValueError) as exc:
        raise TTSError("Ses kaydedilemedi. Klasör yazma iznini ve disk alanını kontrol edin.") from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
