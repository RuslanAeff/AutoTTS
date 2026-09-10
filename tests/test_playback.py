"""Sarma sınırları ve oynatma durumunun korunması; native API yerine test doubles."""
from pathlib import Path
import unittest

from playback import AudioPlayer


class NativePlayer:
    def __init__(self):
        self.time = 0.0
        self.playing = False

    def duration(self): return 30.0
    def currentTime(self): return self.time
    def setCurrentTime_(self, value): self.time = value
    def isPlaying(self): return self.playing
    def play(self):
        self.playing = True
        return True
    def pause(self): self.playing = False
    def stop(self): self.playing = False


class PlaybackTests(unittest.TestCase):
    def setUp(self):
        self.player = AudioPlayer()
        self.native = NativePlayer()
        self.player._player = self.native
        self.player._path = Path('test.wav')
        self.player._state = 'ready'

    def test_seek_before_play_starts_from_selected_position(self):
        self.player.seek(12)
        self.player.toggle(Path('test.wav'))
        self.assertEqual(self.player.position, 12)
        self.assertTrue(self.player.active)

    def test_seek_while_playing_preserves_playback(self):
        self.player.toggle(Path('test.wav'))
        for target in (20, 5):
            self.player.seek(target)
            self.assertTrue(self.native.playing)
            self.assertEqual(self.player.position, target)

    def test_paused_seek_does_not_resume(self):
        self.player.toggle(Path('test.wav'))
        self.player.toggle(Path('test.wav'))
        self.player.seek(15)
        self.assertTrue(self.player.paused)
        self.assertFalse(self.native.playing)
        self.player.toggle(Path('test.wav'))
        self.assertEqual(self.player.position, 15)

    def test_boundaries_and_replay(self):
        self.player.seek(-10)
        self.assertEqual(self.player.position, 0)
        self.player.toggle(Path('test.wav'))
        self.player.seek(99)
        self.assertEqual(self.player.position, 30)
        self.assertFalse(self.player.active)
        self.player.toggle(Path('test.wav'))
        self.assertEqual(self.player.position, 0)

    def test_natural_end_remains_at_end_and_can_seek_back(self):
        self.player.toggle(Path('test.wav'))
        self.native.playing = False
        self.native.time = 0  # Native oynatıcı bitişte sıfıra dönse de GUI sonu gösterir.
        self.assertEqual(self.player.position, 30)
        self.player.seek(8)
        self.assertEqual(self.player.position, 8)
        self.assertFalse(self.player.active)

    def test_stop_resets_position_and_invalid_seek_is_ignored(self):
        self.player.seek(12)
        self.player.seek(float('nan'))
        self.assertEqual(self.player.position, 12)
        self.player.stop()
        self.assertEqual(self.player.position, 0)
        self.assertFalse(self.player.paused)
