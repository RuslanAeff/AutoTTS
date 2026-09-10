"""Format seçimi dosya diyaloğunun eski WAV uzantısına yenilmemeli."""
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import Mock, patch

import numpy as np
import soundfile as sf
from audio_io import export_path, save_audio
from main import AutoTTSApp
from tts_engine import AudioResult


class ExportTests(unittest.TestCase):
    def test_selected_format_controls_extension(self):
        for name, fmt, expected in [('ses.wav', 'MP3', 'ses.mp3'),
                                    ('ses.MP3', 'WAV', 'ses.wav'),
                                    ('ses', 'MP3', 'ses.mp3'),
                                    ('bolum.01', 'MP3', 'bolum.01.mp3'),
                                    ('ses.MP3', 'MP3', 'ses.mp3')]:
            with self.subTest(name=name, fmt=fmt):
                self.assertEqual(export_path(Path(name), fmt), Path(expected))

    def app(self):
        return SimpleNamespace(audio=AudioResult(np.sin(np.arange(24000) * .1).astype('float32') * .2),
                               busy=False, export_format=SimpleNamespace(get=lambda: 'MP3'),
                               _start=Mock())

    def test_mp3_selection_writes_real_mp3_even_if_dialog_returns_wav(self):
        app = self.app()
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'ses.wav'
            with patch('main.filedialog.asksaveasfilename', return_value=str(target)) as dialog:
                AutoTTSApp._save(app)
            self.assertEqual(dialog.call_args.kwargs['defaultextension'], '.mp3')
            self.assertEqual(dialog.call_args.kwargs['initialfile'], 'ses.mp3')
            kind, saved = app._start.call_args.args[0]()
            self.assertEqual(kind, 'save')
            self.assertEqual(saved.suffix, '.mp3')
            self.assertFalse(target.exists())
            self.assertEqual(sf.info(saved).format, 'MP3')
            decoded, rate = sf.read(saved)
            self.assertEqual(rate, 24000)
            self.assertEqual(len(decoded), 24000)
            self.assertGreater(np.max(np.abs(decoded)), .05)

    def test_cancel_does_not_start_export(self):
        app = self.app()
        with patch('main.filedialog.asksaveasfilename', return_value=''):
            AutoTTSApp._save(app)
        app._start.assert_not_called()

    def test_overwrite_checks_corrected_target_and_respects_no(self):
        app = self.app()
        with tempfile.TemporaryDirectory() as directory:
            mp3 = Path(directory) / 'ses.mp3'
            mp3.write_bytes(b'previous')
            with patch('main.filedialog.asksaveasfilename', return_value=str(mp3.with_suffix('.wav'))), \
                 patch('main.messagebox.askyesno', return_value=False) as confirm:
                AutoTTSApp._save(app)
            confirm.assert_called_once()
            self.assertIn('ses.mp3', confirm.call_args.args[1])
            self.assertEqual(mp3.read_bytes(), b'previous')
            app._start.assert_not_called()
