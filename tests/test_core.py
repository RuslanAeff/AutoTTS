"""İndirme gerektirmeyen sözleşme ve hata yolu testleri."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import soundfile as sf

from audio_io import save_audio
from batch import run_batch
from tts_engine import AudioResult, KokoroEngine, TTSError


class CoreTests(unittest.TestCase):
    def test_validation_does_not_load_model(self):
        engine = KokoroEngine()
        for text, voice, speed in [(" ", "af_heart", 1), ("Hello", "bad", 1),
                                   ("Hello", "af_heart", 0.4), ("Hello", "af_heart", float("nan"))]:
            with self.subTest(text=text, voice=voice, speed=speed), self.assertRaises(TTSError):
                engine.synthesize(text, voice, speed)
        self.assertEqual(engine._pipelines, {})

    def test_mps_failure_retries_whole_request_on_cpu(self):
        engine = KokoroEngine("mps")
        expected = AudioResult(np.ones(100, dtype=np.float32))
        with patch.object(engine, "_generate", side_effect=[RuntimeError("MPS"), expected]) as generate:
            self.assertIs(engine.synthesize("Hello", "af_heart"), expected)
            self.assertEqual(generate.call_count, 2)
            self.assertEqual(engine.device, "cpu")

    def test_cpu_failure_is_actionable(self):
        with patch.object(KokoroEngine, "_generate", side_effect=RuntimeError("private text")):
            with self.assertRaises(TTSError) as error:
                KokoroEngine("cpu").synthesize("Hello", "af_heart")
            self.assertNotIn("private text", str(error.exception))

    def test_language_installer_exit_becomes_user_error(self):
        with patch.object(KokoroEngine, "_generate", side_effect=SystemExit(1)):
            with self.assertRaisesRegex(TTSError, "dil kaynağı"):
                KokoroEngine("cpu").synthesize("Hello", "af_heart")

    def test_wave_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = save_audio(AudioResult(np.zeros(2400)), Path(folder) / "test.wav")
            audio, rate = sf.read(path)
            self.assertEqual(rate, 24000)
            self.assertEqual(len(audio), 2400)

    def test_failed_export_preserves_original_and_cleans_temp(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.wav"
            path.write_bytes(b"original")
            with patch("audio_io.sf.write", side_effect=RuntimeError("disk")), self.assertRaises(TTSError):
                save_audio(AudioResult(np.zeros(100)), path)
            self.assertEqual(path.read_bytes(), b"original")
            self.assertEqual(list(Path(folder).iterdir()), [path])

    def test_batch_continues_and_preserves_duplicate_stems(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            files = []
            for name, text in [("a", "Hello"), ("b", ""), ("c", "World")]:
                (root / name).mkdir()
                source = root / name / "same.txt"
                source.write_text(text)
                files.append(source)
            engine = KokoroEngine("cpu")
            progress = []
            with patch.object(engine, "_generate", return_value=AudioResult(np.zeros(100))):
                result = run_batch(engine, files, root, "af_heart", 1, progress=progress.append)
            self.assertEqual(len(result.outputs), 2)
            self.assertEqual(len(result.failures), 1)
            self.assertNotEqual(result.outputs[0], result.outputs[1])
            self.assertEqual(progress[-1], 1)

    def test_mp3_unavailable_has_clear_error(self):
        with patch("audio_io.sf.check_format", return_value=False), self.assertRaisesRegex(TTSError, "MP3"):
            save_audio(AudioResult(np.zeros(100)), Path("unused.mp3"))


if __name__ == "__main__":
    unittest.main()
