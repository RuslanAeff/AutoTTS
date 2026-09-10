"""Gerçek Tk olay döngüsünde üretim ve oynatıcı yaşam döngüsü kontrolü.

Manuel görsel/işitsel kabul değildir. Pencere test sonunda kapanır.
"""
import json
import platform
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import AutoTTSApp


app = AutoTTSApp()
started = time.monotonic()
failures = []


def fail(message):
    failures.append(message)
    app.player.stop()
    app.destroy()


def finish():
    try:
        assert app.player.active and not app.player.paused
        app.player.stop()
        assert not app.player.active
        print(json.dumps({"gui": "opened", "synthesis": "passed", "device": app.engine.device,
                          "platform": platform.mac_ver()[0], "architecture": platform.machine(),
                          "processor": subprocess.check_output(
                              ["sysctl", "-n", "machdep.cpu.brand_string"], text=True).strip(),
                          "play_pause_resume_stop": "native player state passed",
                          "manual_visual_audio_acceptance": "pending"}))
        app._close()
    except Exception as exc:
        fail(type(exc).__name__)


def resume():
    try:
        assert app.player.active and app.player.paused
        app.play.invoke()
        app.after(300, finish)
    except Exception as exc:
        fail(type(exc).__name__)


def pause():
    try:
        assert app.player.active
        app.play.invoke()
        app.after(300, resume)
    except Exception as exc:
        fail(type(exc).__name__)


def check():
    if time.monotonic() - started > 300:
        fail("timeout")
    elif app.busy:
        app.after(200, check)
    else:
        try:
            assert app.audio is not None and app.preview.exists()
            assert app.save.cget("state") == "normal"
            app.play.invoke()
            app.after(300, pause)
        except Exception as exc:
            fail(type(exc).__name__)


def begin():
    app.text.insert("1.0", Path("assets/sample.txt").read_text())
    app.generate.invoke()
    app.after(200, check)


# Testte modal hata diyaloğu yerine başarısızlığı terminale aktar.
import main
main.messagebox.showerror = lambda title, message: fail(message)
app.after(300, begin)
app.mainloop()
if failures:
    print(json.dumps({"result": "failed", "errors": failures}))
    sys.exit(1)
