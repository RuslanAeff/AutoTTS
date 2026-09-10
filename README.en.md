<p align="center">
  <img src="assets/docs/readme-banner-en.svg" alt="AutoTTS — Give your text a voice" width="100%">
</p>

<p align="center">
  <strong>Write it. Pick a voice. Listen.</strong><br>
  A local English text-to-speech app built on Kokoro for macOS Apple Silicon.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/macOS-Apple%20Silicon-182932?style=flat-square&amp;logo=apple&amp;logoColor=white" alt="macOS Apple Silicon">
  <img src="https://img.shields.io/badge/Python-3.11-087F73?style=flat-square&amp;logo=python&amp;logoColor=white" alt="Python 3.11">
  <img src="https://img.shields.io/badge/Engine-Kokoro-087F73?style=flat-square" alt="Engine: Kokoro">
  <img src="https://img.shields.io/badge/Export-WAV%20%2B%20MP3-087F73?style=flat-square" alt="WAV and MP3 export">
</p>

<p align="center">
  <strong>English</strong> · <a href="README.md">Türkçe</a>
</p>

<p align="center">
  <a href="#features">Features</a> ·
  <a href="#setup">Setup</a> ·
  <a href="#usage">Usage</a> ·
  <a href="#development">Development</a> ·
  <a href="#thesis-and-traceability">Thesis and traceability</a>
</p>

---

## Features

AutoTTS brings text editing, speech synthesis and listening into a single workspace. Prepare your text, choose a voice character and speed, then review the result on the timeline and save it in the format you want.

| | Feature | What you can do |
| :---: | :--- | :--- |
| **01** | **28 English voices** | Choose between female and male voices in US and British accents. |
| **02** | **Adjustable speed** | Set the speaking rate between **0.5x and 2.0x**. |
| **03** | **Timeline** | Play, pause, seek to a position or skip **±10 seconds**. |
| **04** | **Waveform view** | See the waveform of the generated audio and the part being played. |
| **05** | **WAV / MP3 export** | Pick the format explicitly and save the audio wherever you want. |
| **06** | **Batch synthesis** | Process multiple TXT files in sequence; one bad file does not stop the rest. |
| **07** | **Studio interface** | Work with a wide editor, a word/character counter and the **⌘+Enter** shortcut. |
| **08** | **MPS / CPU** | Use MPS where the device supports it, and fall back to CPU where it does not. |

> [!NOTE]
> Your text is never sent to a remote TTS API. On first use the model, voice and language resources are downloaded from the internet. Once those resources are cached, synthesis runs locally.

## Setup

### 1. Prepare the environment

**Requirements:** macOS Apple Silicon, Python 3.11 with Tk support. An internet connection is required for the first model download.

With Homebrew:

```bash
brew install python@3.11 python-tk@3.11 espeak-ng
```

Alternatively you can use the Python.org macOS universal2 build, which ships with Tk. Prefer a dedicated Python 3.11 for this project over the macOS system Python.

### 2. Get the project and install dependencies

```bash
git clone https://github.com/RuslanAeff/AutoTTS.git
cd AutoTTS

python3.11 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Launch the app

```bash
python main.py
```

For later runs a single command from the project folder is enough:

```bash
.venv/bin/python main.py
```

<details>
<summary><strong>Having trouble with the setup?</strong></summary>

<br>

| Symptom | Check / fix |
| :--- | :--- |
| `_tkinter` not found | Install a Python build with Tk support and recreate the virtual environment with it. `python -m tkinter` should open a test window. |
| First synthesis takes a long time | The model and the selected voice may still be downloading. Check the status message and your internet connection. |
| English language resource fails to load | Run `python -m spacy download en_core_web_sm` inside the active virtual environment. |
| Preview does not play | Check your audio output device and make sure the AVFoundation binding is installed via `python -m pip install -r requirements.txt`. |
| MP3 writing is not supported | Check your soundfile/libsndfile installation. You can also choose WAV instead; no extra FFmpeg dependency is required. |

The model and voice cache lives in `.cache/huggingface/`; its location can be changed with the `HF_HOME` environment variable. The G2P language package is installed into the virtual environment.

</details>

## Usage

### Text to speech

1. Type or paste your English text into the **text editor**.
2. Choose the voice and speaking rate in **voice settings**.
3. Press **Synthesize** or use **⌘+Enter**.
4. Listen to the result in the **player** at the bottom; drag the timeline to jump to any position.
5. Choose **WAV** or **MP3** in the **export** area, then pick a destination with **Save**.

> [!TIP]
> To save an MP3, use the **menu next to the Save button**. The format selector in the batch card on the right applies to batch output only.

Seeking in paused audio does not start playback; use **Resume** to listen from the position you picked. At the end of the audio, **Play** starts over from the beginning.

### Synthesizing multiple files

1. Pick UTF-8 text files via **Batch synthesis → TXT files**.
2. Choose the output format in the same card.
3. Press **Batch synthesize** and select a destination folder.

Each run creates its own `AutoTTS-…` folder. Outputs are numbered in the order the files were selected, so entries with the same name never overwrite each other. Empty, unreadable or unprocessable files are listed in the result while the remaining files keep processing.

<details>
<summary><strong>Runtime behavior and limits</strong></summary>

<br>

- Single-text synthesis shows the status and the chunk count; batch runs show the ratio of completed files.
- A second job cannot be started while synthesis is running; closing the app waits for the job to finish.
- For very long texts the audio accumulates in RAM. Splitting large inputs into files reduces memory usage.
- The preview is cleaned up on a normal shutdown. Use **Save** for a persistent file.
- The studio interface uses a light theme; the minimum window size is **980 × 760** pixels.

</details>

## Development

### Technology stack

| Layer | Technology |
| :--- | :--- |
| Speech synthesis | Kokoro · PyTorch |
| Desktop interface | CustomTkinter |
| Audio files | Soundfile · NumPy |
| macOS playback | AVAudioPlayer · PyObjC |

### Module layout

```text
AutoTTS/
├── main.py             # GUI events and background jobs
├── ui.py               # Studio layout, styling and waveform view
├── tts_engine.py       # Abstract engine contract and Kokoro adapter
├── audio_io.py         # Format selection and atomic WAV/MP3 writing
├── playback.py         # Play, pause and seek
├── batch.py            # Sequential TXT processing
├── requirements.txt    # Python dependencies
├── assets/             # Sample text and image files
├── tests/              # Regression tests that download no model
├── scripts/            # Smoke tests and evidence tooling
└── docs/               # Architecture, decisions, evidence and templates
```

A new TTS engine can implement the `TTSEngine` contract and be wired in with `AutoTTSApp(engine=...)`. The GUI does not need to know the pipeline details of the new engine.

<details>
<summary><strong>Apple Silicon: how is MPS selected?</strong></summary>

<br>

The engine sets `PYTORCH_ENABLE_MPS_FALLBACK=1` before Torch is imported. If `torch.backends.mps.is_available()` is true it selects MPS, otherwise CPU.

If MPS loading or inference fails with `RuntimeError` / `NotImplementedError`, the partial audio is discarded and the whole text is retried on CPU. Selecting MPS is not a guarantee of a measured speedup; unsupported operators may still run on CPU.

</details>

### Test commands

Regression tests without downloading a model:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

WAV/MP3 generation with the real model:

```bash
.venv/bin/python scripts/smoke_tts.py --device auto
.venv/bin/python scripts/smoke_tts.py --device cpu --output outputs/cpu
.venv/bin/python scripts/smoke_tts.py --voice bm_george --output outputs/british
```

The smoke test synthesizes the text in `assets/sample.txt`, checks the duration, sample rate and samples of the audio, and reopens the WAV/MP3 output. Pronunciation quality and human acceptance are evaluated separately.

## Thesis and traceability

AutoTTS keeps decision and evidence records so the AI-assisted development process can be traced academically. **Implemented**, **automated test passed**, **verified on target device** and **published** are tracked as separate states.

| Document | Purpose |
| :--- | :--- |
| [Architecture](docs/ARCHITECTURE.md) | Components, responsibilities and engine boundaries |
| [Development guide](docs/DEVELOPMENT_GUIDE.md) | Contribution patterns and verification commands |
| [Quality and security](docs/QUALITY_AND_SECURITY.md) | Evidence levels, privacy and test limits |
| [Architecture decisions](docs/decisions/README.md) | ADR index and decision rationale |
| [Traceability](docs/evidence/TRACEABILITY.md) | Requirement → decision → code → verification links |
| [AI collaboration log](docs/evidence/AI_COLLABORATION_LOG.md) | Human goal, AI contribution and authority boundaries |
| [Portable templates](docs/templates/) | A record structure reusable in other projects |

Living guides may be updated; historical evidence is not silently rewritten. The human owns the product goal and the final acceptance. Contribution contract: [AGENTS.md](AGENTS.md).

**Validation records:** [First setup](docs/evidence/VALIDATION-2026-09-10.md) · [Timeline](docs/evidence/VALIDATION-2026-09-10-TIMELINE.md) · [MP3 export](docs/evidence/VALIDATION-2026-09-10-MP3.md) · [Studio design](docs/evidence/VALIDATION-2026-09-10-UI.md)

## Resources

- [Kokoro — official repository](https://github.com/hexgrad/kokoro)
- [Kokoro — English voice catalog](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)
- [Kokoro — pipeline and device behavior](https://github.com/hexgrad/kokoro/blob/main/kokoro/pipeline.py)
- [Soundfile — API documentation](https://python-soundfile.readthedocs.io/en/latest/)

The voice catalog was checked on 2026-09-10. The canonical source for dependency version ranges is [requirements.txt](requirements.txt); the exact versions used for reproducible measurements are recorded separately.
