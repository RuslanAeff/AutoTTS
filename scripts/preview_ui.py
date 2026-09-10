"""Yerel görsel QA: uygulamanın kendi penceresini geçici klasöre yakalar."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import AutoTTSApp
import soundfile as sf
from audio_io import save_audio
from tts_engine import AudioResult

app = AutoTTSApp()
app.text.insert('1.0', Path('assets/sample.txt').read_text())
samples, rate = sf.read('outputs/smoke/sample.wav', dtype='float32')
audio = AudioResult(samples, rate)
save_audio(audio, app.preview)
app.events.put(('done', ('single', audio)))
app._update_editor()


def capture():
    from AppKit import NSApplication, NSBitmapImageFileTypePNG
    for window in NSApplication.sharedApplication().windows():
        if str(window.title()).startswith('AutoTTS'):
            view = window.contentView()
            bitmap = view.bitmapImageRepForCachingDisplayInRect_(view.bounds())
            view.cacheDisplayInRect_toBitmapImageRep_(view.bounds(), bitmap)
            target = '/tmp/autotts-ui-' + str(app.winfo_width()) + '.png'
            data = bitmap.representationUsingType_properties_(NSBitmapImageFileTypePNG, {})
            print({'image': target, 'saved': bool(data.writeToFile_atomically_(target, True))}, flush=True)
            break
    for name in ['text', 'voice', 'generate', 'batch_button', 'play', 'save', 'timeline', 'status']:
        widget = getattr(app, name)
        print(name, widget.winfo_rootx() - app.winfo_rootx(), widget.winfo_rooty() - app.winfo_rooty(), widget.winfo_width(), widget.winfo_height(), flush=True)
    if app.winfo_width() > 980:
        app.geometry('980x760')
        app.after(700, capture)
    else:
        app._close()


app.after(1000, capture)
app.mainloop()
