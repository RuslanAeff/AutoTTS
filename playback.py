"""macOS AVAudioPlayer ile konum bilgili oynatma; yalnız GUI thread'inde kullanılır."""
from pathlib import Path
import math


class AudioPlayer:
    def __init__(self):
        self._player = None
        self._path = None
        self._state = "empty"

    def load(self, path: Path):
        # Tembel import: motor ve unit testler macOS köprüsünü yüklemek zorunda değil.
        from AVFoundation import AVAudioPlayer
        from Foundation import NSURL

        player, error = AVAudioPlayer.alloc().initWithContentsOfURL_error_(
            NSURL.fileURLWithPath_(str(Path(path).resolve())), None)
        if player is None or not player.prepareToPlay():
            raise OSError("Ses dosyası oynatıcıya yüklenemedi.")
        self.stop()
        self._player, self._path = player, Path(path)
        self._state = "ready"

    def _refresh(self):
        if self._state == "playing" and not self._player.isPlaying():
            self._state = "ended"

    @property
    def duration(self):
        return float(self._player.duration()) if self._player is not None else 0.0

    @property
    def position(self):
        self._refresh()
        if self._state == "ended":
            return self.duration
        return float(self._player.currentTime()) if self._player is not None else 0.0

    @property
    def active(self):
        self._refresh()
        return self._state in {"playing", "paused"}

    @property
    def paused(self):
        return self._state == "paused"

    def toggle(self, path: Path):
        if self._player is None or Path(path) != self._path:
            self.load(path)
        self._refresh()
        if self._state == "playing":
            self._player.pause()
            self._state = "paused"
        else:
            if self._state == "ended":
                self._player.setCurrentTime_(0.0)
            if not self._player.play():
                raise OSError("Ses çıkış aygıtı başlatılamadı.")
            self._state = "playing"

    def seek(self, seconds: float):
        """Konumu sınırla; oynuyorsa sürdür, duraklatılmışsa sessiz kal."""
        if self._player is None or not math.isfinite(seconds):
            return
        self._refresh()
        target = max(0.0, min(float(seconds), self.duration))
        if target >= self.duration:
            self._player.pause()
            self._player.setCurrentTime_(self.duration)
            self._state = "ended"
        else:
            self._player.setCurrentTime_(target)
            if self._state == "ended":
                self._state = "ready"

    def stop(self):
        if self._player is not None:
            self._player.stop()
            self._player.setCurrentTime_(0.0)
            self._state = "ready"
