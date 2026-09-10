"""CustomTkinter giriş noktası. Tk işlemleri yalnız ana iş parçacığında yapılır."""
from pathlib import Path
from queue import Empty, Queue
import tempfile
from threading import Thread
from tkinter import filedialog, messagebox

import customtkinter as ctk

from audio_io import export_path, save_audio
from batch import run_batch
from playback import AudioPlayer
from tts_engine import KokoroEngine, TTSEngine
from ui import build_interface


class AutoTTSApp(ctk.CTk):
    def __init__(self, engine: TTSEngine | None = None):
        super().__init__()
        self.engine = engine or KokoroEngine()
        self.title("AutoTTS · Yerel İngilizce seslendirme")
        self.events = Queue()
        self.busy = False
        self.audio = None
        self.files = []
        self.player = AudioPlayer()
        self.temp = tempfile.TemporaryDirectory(prefix="autotts-")
        self.preview = Path(self.temp.name) / "preview.wav"
        self.voice_map = {voice.label: voice.id for voice in self.engine.voices}

        build_interface(self)
        self.text.bind("<<Modified>>", self._text_modified)
        self.text.bind("<FocusIn>", self._update_editor)
        self.text.bind("<FocusOut>", self._update_editor)
        self.bind("<Command-Return>", self._shortcut_generate)
        self._editor_text = None
        self.protocol("WM_DELETE_WINDOW", self._close)
        self.after(100, self._poll)

    def _shortcut_generate(self, event=None):
        if not self.busy:
            self._generate()
        return "break"

    def _update_editor(self, event=None):
        content = self.text.get("1.0", "end-1c")
        if content != self._editor_text:
            self._editor_text = content
            self.word_count.configure(text=f"{len(content.split())} kelime · {len(content)} karakter")
        if content or self.text.focus_get() == self.text._textbox:
            self.placeholder.place_forget()
        else:
            self.placeholder.place(x=8, y=8)

    def _text_modified(self, event=None):
        if self.text.edit_modified():
            self._update_editor()
            self.text.edit_modified(False)

    def _speed_changed(self, value):
        self.speed_label.configure(text=f"{value:.2f}x")

    def _start(self, job, determinate=False, status_message="Seslendiriliyor…"):
        self.player.stop()
        self.busy = True
        for control in self.controls + self.playback_controls + [self.save]:
            control.configure(state="disabled")
        self.progress.configure(mode="determinate" if determinate else "indeterminate")
        self.progress.set(0)
        if not determinate:
            self.progress.start()
        self.status.configure(text=status_message)

        def worker():
            try:
                self.events.put(("done", job()))
            except Exception as exc:
                from tts_engine import TTSError
                message = str(exc) if isinstance(exc, TTSError) else f"İşlem başarısız ({type(exc).__name__})."
                self.events.put(("error", message))
        Thread(target=worker, daemon=True).start()

    def _report(self, message):
        self.events.put(("status", message))

    def _generate(self):
        text = self.text.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Metin gerekli", "Lütfen İngilizce metin girin.")
            return
        voice, speed = self.voice_map[self.voice.get()], self.speed.get()

        def job():
            audio = self.engine.synthesize(text, voice, speed, self._report)
            save_audio(audio, self.preview)
            return ("single", audio)
        self._start(job)

    def _pick(self):
        files = filedialog.askopenfilenames(filetypes=[("Metin dosyaları", "*.txt")])
        if files:
            self.files = list(files)
            self.batch_label.configure(text=f"{len(files)} TXT dosyası hazır · seçilen sırayla işlenecek")

    def _batch(self):
        if not self.files:
            messagebox.showwarning("Dosya gerekli", "Önce bir veya daha fazla UTF-8 .txt dosyası seçin.")
            return
        folder = filedialog.askdirectory(title="Toplu çıktı klasörünü seçin")
        if not folder:
            return
        voice, speed = self.voice_map[self.voice.get()], self.speed.get()
        extension, files = "." + self.batch_format.get().lower(), tuple(self.files)

        def job():
            # Her çalışma yeni klasör alır; önceki batch çıktıları korunur.
            output = Path(tempfile.mkdtemp(prefix="AutoTTS-", dir=folder))
            result = run_batch(self.engine, files, output, voice, speed, extension,
                               self._report, lambda value: self.events.put(("progress", value)))
            return ("batch", (result, output))
        self._start(job, determinate=True)

    def _play(self):
        try:
            self.player.toggle(self.preview)
        except (OSError, ImportError):
            messagebox.showerror("Oynatılamadı", "Ses oynatıcı başlatılamadı. Ses çıkışını ve README bağımlılık kurulumunu kontrol edin.")

    def _seek(self, seconds):
        if not self.busy:
            self.player.seek(float(seconds))
            self._update_timeline()

    def _skip(self, seconds):
        self._seek(self.player.position + seconds)

    @staticmethod
    def _format_time(seconds):
        seconds = max(0, int(seconds))
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"

    def _update_timeline(self):
        self.timeline.set(self.player.position)
        self.waveform.set_position(self.player.position / self.player.duration if self.player.duration else 0)
        self.time_label.configure(text=f"{self._format_time(self.player.position)} / "
                                       f"{self._format_time(self.player.duration)}")

    def _save(self):
        if self.audio is None or self.busy:
            return
        selected_format = self.export_format.get()
        extension = "." + selected_format.lower()
        path = filedialog.asksaveasfilename(
            title=f"{selected_format} olarak kaydet", defaultextension=extension,
            initialfile=f"ses{extension}", filetypes=[(selected_format, f"*{extension}")],
            confirmoverwrite=False)
        if not path:
            return
        destination = export_path(Path(path), selected_format)
        # Uzantı düzeltildikten SONRA gerçek hedef için onay al.
        if destination.exists() and not messagebox.askyesno(
                "Dosya zaten var", f"{destination.name} dosyasının üzerine yazılsın mı?"):
            return
        audio = self.audio
        self._start(lambda: ("save", save_audio(audio, destination)),
                    status_message=f"{selected_format} kaydediliyor…")

    def _poll(self):
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == "status":
                    self.status.configure(text=value)
                elif kind == "progress":
                    self.progress.set(value)
                else:
                    self.busy = False
                    self.progress.stop()
                    self.progress.configure(mode="determinate")
                    self.progress.set(0 if kind == "error" else 1)
                    for control in self.controls:
                        control.configure(state="normal")
                    if kind == "error":
                        self.status.configure(text="İşlem tamamlanamadı")
                        messagebox.showerror("AutoTTS", value)
                    else:
                        task, result = value
                        self.status.configure(text="Tamamlandı")
                        if task == "save":
                            self.status.configure(text=f"Kaydedildi · {result.name} · {result.suffix[1:].upper()}")
                        elif task == "single":
                            self.audio = result
                            self.waveform.set_audio(result.samples)
                            self.audio_title.configure(text="Sesiniz hazır")
                            try:
                                self.player.load(self.preview)
                            except (OSError, ImportError):
                                # Ses yine kaydedilebilir; oynatma hatası olay döngüsünü kesmez.
                                self.player = AudioPlayer()
                                messagebox.showerror("Oynatılamadı", "Önizleme yüklenemedi. README bağımlılık kurulumunu kontrol edin; sesi Kaydet ile dışa aktarabilirsiniz.")
                            self.timeline.configure(to=max(self.player.duration, 0.001))
                            self.status.configure(text=f"Tamamlandı · {len(result.samples) / result.sample_rate:.1f} saniye")
                        elif task == "batch":
                            summary, output = result
                            self.status.configure(text=f"Toplu işlem bitti · {len(summary.outputs)} başarılı, {len(summary.failures)} hatalı")
                            details = "\n".join(f"{name}: {error}" for name, error in summary.failures)
                            messagebox.showinfo("Toplu işlem", f"{len(summary.outputs)} dosya kaydedildi.\nKlasör: {output.name}\n{details}")
                    self.save.configure(state="normal" if self.audio is not None else "disabled")
                    for control in self.playback_controls:
                        control.configure(state="normal" if self.player.duration > 0 else "disabled")
        except Empty:
            pass
        self._update_timeline()
        self.play.configure(text="Devam et" if self.player.paused else "Ⅱ Duraklat" if self.player.active else "▶ Oynat")
        self.after(100, self._poll)

    def _close(self):
        if self.busy:
            messagebox.showinfo("İşlem sürüyor", "Dosyaların tamamlanması için lütfen işlem bitince kapatın.")
            return
        self.player.stop()
        self.temp.cleanup()
        self.destroy()


if __name__ == "__main__":
    AutoTTSApp().mainloop()
