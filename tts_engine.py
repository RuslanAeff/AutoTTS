"""GUI bağımsız motor sözleşmesi ve Kokoro adaptörü."""
from __future__ import annotations

import os
from pathlib import Path
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable

# Torch yüklenmeden önce ayarlanmalı; desteklenmeyen MPS işlemleri CPU kullanabilir.
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
# CLI ve GUI aynı proje önbelleğini paylaşır; HF_HOME ile değiştirilebilir.
os.environ.setdefault("HF_HOME", str(Path(__file__).resolve().parent / ".cache" / "huggingface"))

import numpy as np

StatusCallback = Callable[[str], None]


class TTSError(Exception):
    """Kullanıcıya gösterilebilen, girdi içermeyen hata."""


@dataclass(frozen=True)
class Voice:
    id: str
    label: str


@dataclass(frozen=True)
class AudioResult:
    samples: np.ndarray
    sample_rate: int = 24000


class TTSEngine(ABC):
    """Yeni motorlar bu sözleşmeyi uygulayarak GUI'ye enjekte edilir."""

    @property
    @abstractmethod
    def voices(self) -> tuple[Voice, ...]: ...

    @abstractmethod
    def synthesize(self, text: str, voice: str, speed: float = 1.0,
                   status: StatusCallback = lambda _: None) -> AudioResult: ...


VOICE_GROUPS = {
    "af": "heart alloy aoede bella jessica kore nicole nova river sarah sky",
    "am": "adam echo eric fenrir liam michael onyx puck santa",
    "bf": "alice emma isabella lily",
    "bm": "daniel fable george lewis",
}
ENGLISH_VOICES = tuple(
    Voice(f"{prefix}_{name}", f"{name.title()} · {'ABD' if prefix[0] == 'a' else 'Britanya'} · "
          f"{'Kadın' if prefix[1] == 'f' else 'Erkek'}")
    for prefix, names in VOICE_GROUPS.items() for name in names.split()
)


class KokoroEngine(TTSEngine):
    """Tek işçi tarafından kullanılır; model ve dil pipeline'ları tembel yüklenir."""

    def __init__(self, device: str = "auto"):
        if device not in {"auto", "cpu", "mps"}:
            raise ValueError("Geçersiz cihaz")
        self.device = device
        self._pipelines = {}

    @property
    def voices(self):
        return ENGLISH_VOICES

    def _pipeline(self, language, status):
        import torch
        from kokoro import KPipeline

        if self.device == "auto":
            self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        if self.device == "mps" and not torch.backends.mps.is_available():
            self.device = "cpu"
        if language not in self._pipelines:
            status(f"Model yükleniyor ({self.device}); ilk kullanımda indirme gerekebilir…")
            kwargs = {"model": next(iter(self._pipelines.values())).model} if self._pipelines else {}
            self._pipelines[language] = KPipeline(
                lang_code=language, repo_id="hexgrad/Kokoro-82M", device=self.device, **kwargs)
        return self._pipelines[language]

    def _generate(self, text, voice, speed, status):
        import torch

        pipeline = self._pipeline(voice[0], status)
        chunks = []
        with torch.inference_mode():
            for index, (_, _, audio) in enumerate(pipeline(text, voice=voice, speed=speed), 1):
                if audio is not None:
                    chunk = audio.detach().cpu().numpy().astype(np.float32)
                    if chunk.size:
                        chunks.append(chunk)
                        status(f"Seslendiriliyor ({self.device}) · {index} parça üretildi")
        if not chunks:
            raise TTSError("Bu metinden ses üretilemedi. İngilizce sözcükler içeren bir metin girin.")
        samples = np.concatenate(chunks)
        if not np.isfinite(samples).all():
            raise RuntimeError("Invalid audio samples")
        return AudioResult(samples)

    def synthesize(self, text, voice, speed=1.0, status=lambda _: None):
        if not text.strip():
            raise TTSError("Lütfen seslendirilecek İngilizce metni girin.")
        if voice not in {v.id for v in self.voices}:
            raise TTSError("Lütfen listeden geçerli bir ses seçin.")
        if not 0.5 <= speed <= 2.0:
            raise TTSError("Konuşma hızı 0.5–2.0 arasında olmalı.")
        try:
            try:
                return self._generate(text, voice, speed, status)
            except (RuntimeError, NotImplementedError):
                if self.device != "mps":
                    raise
                # Kısmi MPS çıktısı atılır; metnin tamamı CPU ile yeniden üretilir.
                self._pipelines.clear()
                self.device = "cpu"
                status("MPS kullanılamadı; CPU ile yeniden deneniyor…")
                return self._generate(text, voice, speed, status)
        except TTSError:
            raise
        except SystemExit as exc:
            # spaCy kaynak indirme aracı sys.exit kullanabilir; işçi sessizce ölmesin.
            raise TTSError("İngilizce dil kaynağı kurulamadı. Sanal ortamda "
                           "python -m spacy download en_core_web_sm komutunu çalıştırın.") from exc
        except Exception as exc:
            raise TTSError("Model yüklenemedi veya ses üretilemedi. İlk kullanımda interneti, "
                           "model önbelleğini ve README kurulum adımlarını kontrol edin. "
                           f"Hata türü: {type(exc).__name__}") from exc
