"""Integrity and packaging regressions, using isolated temporary fixtures."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_package import build
from validate_project import CORE_FILES, ROOT, SKILL_NAME, relative_link_errors, validate


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        for directory in (SKILL_NAME, "checksums", "docs", "examples"):
            shutil.copytree(ROOT / directory, self.root / directory)
        for name in ("README.md", "README.zh-CN.md", "COPYRIGHT.md", "requirements-dev.txt"):
            shutil.copyfile(ROOT / name, self.root / name)
        # Documentation navigates to these published directories.
        shutil.copytree(ROOT / "scripts", self.root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(ROOT / "tests", self.root / "tests", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(ROOT / ".github", self.root / ".github")

    def tearDown(self):
        self.temp.cleanup()

    def test_original_project_is_valid(self):
        self.assertEqual(validate(self.root), [])

    def test_modified_core_is_rejected(self):
        path = self.root / SKILL_NAME / "references/writing.md"
        path.write_bytes(path.read_bytes() + b"\nchanged\n")
        self.assertTrue(any("Protected core bytes changed" in error for error in validate(self.root)))

    def test_missing_core_is_rejected(self):
        (self.root / SKILL_NAME / "references/records.md").unlink()
        self.assertTrue(any("Core file is missing" in error for error in validate(self.root)))

    def test_private_record_inside_skill_is_rejected(self):
        (self.root / SKILL_NAME / "profile.md").write_text("private fixture", encoding="utf-8")
        self.assertTrue(any("exactly the seven" in error for error in validate(self.root)))

    def test_invalid_manifest_paths_are_rejected(self):
        path = self.root / "checksums/skill-sha256.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["../private.md"] = "0" * 64
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(any("exactly the seven" in error for error in validate(self.root)))

    def test_malformed_frontmatter_is_rejected(self):
        (self.root / SKILL_NAME / "SKILL.md").write_text("---\nname: [\n---\n", encoding="utf-8")
        self.assertTrue(any("frontmatter is malformed" in error for error in validate(self.root)))

    def test_missing_document_link_is_rejected(self):
        path = self.root / "docs/broken.md"
        path.write_text("[Missing](missing.md)", encoding="utf-8")
        self.assertTrue(any("missing relative link" in error for error in validate(self.root)))

    def test_link_cannot_escape_repository(self):
        path = self.root / "docs/broken.md"
        path.write_text("[Outside](../../outside.md)", encoding="utf-8")
        self.assertTrue(any("escapes repository" in error for error in relative_link_errors(path, self.root)))

    def test_package_is_stable_and_skill_only(self):
        (self.root / "private-record.md").write_text("local fixture", encoding="utf-8")
        first = build(self.root, Path(self.temp.name) / "first.zip")
        second = build(self.root, Path(self.temp.name) / "second.zip")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as archive:
            self.assertEqual(set(archive.namelist()), {f"{SKILL_NAME}/{name}" for name in CORE_FILES})
        self.assertEqual(validate(self.root, first), [])

    def test_archive_with_extra_private_content_is_rejected(self):
        path = build(self.root, Path(self.temp.name) / "package.zip")
        with zipfile.ZipFile(path, "a") as archive:
            archive.writestr("private.md", "not a release file")
        self.assertTrue(any("only the seven unique" in error for error in validate(self.root, path)))

    def test_corrupt_archive_is_rejected(self):
        path = Path(self.temp.name) / "broken.zip"
        path.write_bytes(b"not a zip")
        self.assertTrue(any("missing or invalid" in error for error in validate(self.root, path)))

    def test_output_inside_core_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "protected skill directory"):
            build(self.root, self.root / SKILL_NAME / "output.zip")


if __name__ == "__main__":
    unittest.main()
