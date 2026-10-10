"""Validate the preserved skill, documentation links, and optional release ZIP."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "undergrad-research-outreach"
CORE_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/opportunities.md",
    "references/writing.md",
    "references/follow-through.md",
    "references/learning.md",
    "references/records.md",
)


def relative_link_errors(path: Path, root: Path) -> list[str]:
    errors = []
    for target in re.findall(r"\]\(([^)\n]+)\)", path.read_text(encoding="utf-8")):
        target = target.strip().strip("<>")
        if re.match(r"^[A-Za-z]:[/\\]", target) or target.startswith("file:"):
            errors.append(f"{path.relative_to(root)}: machine-specific link")
            continue
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith("#"):
            continue
        resolved = (path.parent / unquote(parsed.path)).resolve()
        if not resolved.is_relative_to(root.resolve()):
            errors.append(f"{path.relative_to(root)}: link escapes repository")
        elif not resolved.exists():
            errors.append(f"{path.relative_to(root)}: missing relative link {parsed.path}")
    return errors


def validate(root: Path, archive: Path | None = None) -> list[str]:
    root = root.resolve()
    core = root / SKILL_NAME
    errors: list[str] = []
    manifest_path = root / "checksums/skill-sha256.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict) or set(manifest) != set(CORE_FILES):
            return ["Integrity manifest must contain exactly the seven core files"]
        if any(not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value) for value in manifest.values()):
            return ["Integrity manifest contains an invalid SHA256"]
    except (OSError, ValueError, TypeError):
        return ["Integrity manifest is missing or invalid"]

    actual = {p.relative_to(core).as_posix() for p in core.rglob("*") if p.is_file()}
    if actual != set(CORE_FILES):
        errors.append("Skill directory must contain exactly the seven public core files")
    for name in CORE_FILES:
        path = core / name
        if not path.is_file() or path.is_symlink():
            errors.append(f"Core file is missing or is a symlink: {name}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != manifest[name]:
            errors.append(f"Protected core bytes changed: {name}")

    main = core / "SKILL.md"
    if main.is_file():
        text = main.read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
        try:
            front = yaml.safe_load(match.group(1)) if match else None
            if not isinstance(front, dict):
                errors.append("Skill YAML frontmatter is missing or invalid")
            else:
                if front.get("name") != SKILL_NAME:
                    errors.append("Skill name does not match its directory")
                if not isinstance(front.get("description"), str) or not front["description"].strip():
                    errors.append("Skill description is missing")
                metadata = front.get("metadata")
                if not isinstance(metadata, dict) or metadata.get("version") != "1.0.0":
                    errors.append("Skill metadata version must be 1.0.0")
        except yaml.YAMLError:
            errors.append("Skill YAML frontmatter is malformed")

    ui_path = core / "agents/openai.yaml"
    if ui_path.is_file():
        try:
            ui = yaml.safe_load(ui_path.read_text(encoding="utf-8"))
            interface = ui["interface"]
            if not 25 <= len(interface["short_description"]) <= 64:
                errors.append("UI description length is invalid")
            if "$" + SKILL_NAME not in interface["default_prompt"]:
                errors.append("UI prompt does not explicitly invoke the skill")
            if ui.get("policy", {}).get("allow_implicit_invocation") is not True:
                errors.append("The original implicit invocation policy was changed")
        except (yaml.YAMLError, KeyError, TypeError, AttributeError):
            errors.append("UI YAML is malformed or incomplete")

    documents = list(core.rglob("*.md")) + list((root / "docs").rglob("*.md")) + list(
        (root / "examples").rglob("*.md")
    )
    for name in ("README.md", "README.zh-CN.md", "COPYRIGHT.md"):
        path = root / name
        if not path.is_file():
            errors.append(f"Required documentation missing: {name}")
        else:
            documents.append(path)
    for path in documents:
        errors.extend(relative_link_errors(path, root))
        text = path.read_text(encoding="utf-8")
        if re.search(r"[A-Za-z]:[/\\](?:Users|home)[/\\]", text):
            errors.append(f"{path.relative_to(root)}: author-specific absolute path")
    en = root / "README.md"
    zh = root / "README.zh-CN.md"
    if en.is_file() and "README.zh-CN.md" not in en.read_text(encoding="utf-8").splitlines()[0]:
        errors.append("English README must link to Chinese README at the top")
    if zh.is_file() and "README.md" not in zh.read_text(encoding="utf-8").splitlines()[0]:
        errors.append("Chinese README must link to English README at the top")

    if archive is not None:
        expected = {f"{SKILL_NAME}/{name}": digest for name, digest in manifest.items()}
        try:
            with zipfile.ZipFile(archive) as package:
                infos = [item for item in package.infolist() if not item.is_dir()]
                names = [item.filename for item in infos]
                if len(names) != len(set(names)) or set(names) != set(expected):
                    errors.append("Archive must contain only the seven unique core paths")
                else:
                    for item in infos:
                        if hashlib.sha256(package.read(item)).hexdigest() != expected[item.filename]:
                            errors.append(f"Archive bytes changed: {item.filename}")
        except (OSError, zipfile.BadZipFile):
            errors.append("Archive is missing or invalid")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    errors = validate(args.root, args.archive)
    if errors:
        for error in errors:
            print("FAIL:", error, file=sys.stderr)
        return 1
    print("PASS: 7 core files unchanged; YAML and local documentation links valid.")
    if args.archive is not None:
        print("PASS: archive contains exactly the 7 original core files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
