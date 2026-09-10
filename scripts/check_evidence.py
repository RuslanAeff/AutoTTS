"""Belge bağlantıları, şablon bölümleri ve kaynak/artefakt hash kontrolü."""
import hashlib
import argparse
import json
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path,
                        default=Path("docs/evidence/SNAPSHOT-2026-09-10-UI.json"))
    args = parser.parse_args()
    documents = [Path("README.md"), Path("AGENTS.md"), Path("CLAUDE.md"),
                 *Path("docs").rglob("*.md")]
    errors = []
    for path in documents:
        content = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if target.startswith(("https://", "http://", "#")):
                continue
            if not (path.parent / target.split("#")[0]).exists():
                errors.append(f"{path}: broken link {target}")
        # Bu tarama tam bir sır tarayıcısı değildir; kullanıcı yolu sızıntısını yakalar.
        if any(prefix in content for prefix in ["/Users/", "/home/"]):
            errors.append(f"{path}: absolute user path")
    manifest = json.loads(args.manifest.read_text())
    for name, expected in {**manifest["sources"], **manifest["artifacts"]}.items():
        path = Path(name)
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(f"{name}: missing or changed")
    for name, count in [("AI_SESSION_TEMPLATE.md", 13), ("PROJECT_DOCUMENTATION_TEMPLATE.md", 12)]:
        content = (Path("docs/templates") / name).read_text()
        if len(re.findall(r"^## \d+\.", content, re.M)) != count:
            errors.append(f"{name}: section count")
    print(json.dumps({"markdown_files": len(documents), "source_hashes": len(manifest["sources"]),
                      "artifact_hashes": len(manifest["artifacts"]), "errors": errors}))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
