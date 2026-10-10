"""Build a skill-only archive, with stable ZIP metadata and no private records."""
from __future__ import annotations

import argparse
from pathlib import Path
import zipfile

from validate_project import CORE_FILES, ROOT, SKILL_NAME, validate


def build(root: Path, output: Path) -> Path:
    errors = validate(root)
    if errors:
        raise ValueError("Source validation failed: " + "; ".join(errors))
    output = output.resolve()
    if output.is_relative_to((root / SKILL_NAME).resolve()):
        raise ValueError("Output cannot be inside the protected skill directory")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(CORE_FILES):
            info = zipfile.ZipInfo(f"{SKILL_NAME}/{name}", date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (root / SKILL_NAME / name).read_bytes(), compresslevel=9)
    errors = validate(root, output)
    if errors:
        raise ValueError("Archive validation failed: " + "; ".join(errors))
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/undergrad-research-outreach-v1.0.0.zip")
    args = parser.parse_args()
    try:
        path = build(args.root, args.output)
    except (OSError, ValueError) as error:
        parser.exit(1, f"FAIL: {error}\n")
    print(f"Built {path.name}: 7 verified skill files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
