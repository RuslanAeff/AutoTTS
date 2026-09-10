"""Git olmayan çalışma için kaynak/artefakt SHA-256 manifesti üretir.

Commit yerine geçmez. Mevcut kanıtın üzerine yazmayı reddeder.
"""
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path

SOURCES = ["main.py", "ui.py", "scripts/preview_ui.py", "tts_engine.py", "audio_io.py", "playback.py", "batch.py",
           "requirements.txt", "tests/test_core.py", "scripts/smoke_tts.py",
           "scripts/smoke_gui.py", "scripts/evidence_snapshot.py", "assets/sample.txt",
           "tests/test_playback.py", "tests/test_export.py", "scripts/smoke_timeline.py", "scripts/check_evidence.py"]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    files = {name: digest(name) for name in SOURCES}
    build = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    outputs = {str(path): digest(path) for path in sorted(Path("outputs").rglob("sample.*"))}
    record = {"recorded_at": datetime.now(timezone.utc).isoformat(), "build_id": build,
              "commit": "kaydedilmedi — Git deposu yok", "sources": files, "artifacts": outputs}
    target = args.output
    with target.open("x", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(json.dumps({"build_id": build, "source_count": len(files), "artifact_count": len(outputs)}))
