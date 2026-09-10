"""Önceden üretilmiş örnek sesle gerçek Tk ve AVAudioPlayer sarma testi."""
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import soundfile as sf
from main import AutoTTSApp
from tts_engine import AudioResult, KokoroEngine
import main


class RecordedEngine(KokoroEngine):
    def synthesize(self, *args, **kwargs):
        samples, rate = sf.read('outputs/smoke/sample.wav', dtype='float32')
        return AudioResult(samples, rate)


app = AutoTTSApp(engine=RecordedEngine())
failures = []
started = time.monotonic()


def fail(message):
    failures.append(message)
    app.player.stop()
    app.destroy()


def guard(action):
    def run():
        try:
            action()
        except Exception as exc:
            fail(f'{action.__name__}: {type(exc).__name__}: {exc}')
    return run


def finish():
    assert not app.player.active
    assert abs(app.player.position - app.player.duration) < .05
    app.play.invoke()  # Sondan yeniden oynat.
    assert app.player.active and app.player.position < .5
    app.player.stop()
    app._update_timeline()
    assert app.timeline.get() == 0
    print(json.dumps({'result':'passed', 'backend':'AVAudioPlayer',
                      'checks':['load', 'seek-before-play', 'playing-forward-backward',
                                'pause-seek-resume', 'clamp-start-end', 'natural-end', 'replay'],
                      'manual_audio_acceptance':'pending'}))
    app._close()


def near_end():
    assert app.player.active and not app.player.paused
    app._seek(app.player.duration - .25)
    app.after(800, guard(finish))


def paused_seek():
    app.play.invoke()
    assert app.player.paused
    app._seek(2)
    assert abs(app.player.position - 2) < .05
    assert app.player.paused
    app.after(250, guard(resume))


def resume():
    assert abs(app.player.position - 2) < .05
    app.play.invoke()
    app.after(250, guard(near_end))


def playing_seek():
    assert app.player.position > 1
    app._seek(5)
    assert abs(app.player.position - 5) < .15 and app.player.active
    app._seek(3)
    assert abs(app.player.position - 3) < .15 and app.player.active
    app.rewind.invoke()
    assert app.player.position < .15
    app.forward.invoke()
    assert abs(app.player.position - app.player.duration) < .05
    app._seek(1)
    app.play.invoke()
    app.after(200, guard(paused_seek))


def check_loaded():
    if app.busy:
        assert time.monotonic() - started < 20
        app.after(100, guard(check_loaded))
        return
    assert app.audio is not None and app.timeline.cget('state') == 'normal'
    assert app.player.duration > 6
    app._seek(1)
    assert abs(app.timeline.get() - 1) < .05
    app.play.invoke()
    app.after(250, guard(playing_seek))


def begin():
    assert app.timeline.cget('state') == 'disabled'
    app.text.insert('1.0', 'Use the previously synthesized recording.')
    app.generate.invoke()
    assert app.timeline.cget('state') == 'disabled'
    app.after(100, guard(check_loaded))


main.messagebox.showerror = lambda title, message: fail(message)
app.after(200, guard(begin))
app.mainloop()
if failures:
    print(json.dumps({'result':'failed', 'errors':failures}))
    sys.exit(1)
