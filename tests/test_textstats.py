import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TextStatsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "scripts/build_textstats.py")], check=True, capture_output=True)

    def run_app(self, path):
        return subprocess.run([sys.executable, str(ROOT / "dist/textstats.pyz"), str(path), "--json"], capture_output=True, text=True)

    def test_guide_example_exact_output(self):
        result = self.run_app(ROOT / "examples/textstats.txt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"blank_lines": 1, "lines": 3, "words": 7})

    def test_unicode_bom_crlf_and_unterminated_last_line(self):
        with tempfile.TemporaryDirectory(prefix="text space ") as tmp:
            path = Path(tmp) / "café notes.txt"
            data = b"\xef\xbb\xbf" + "caf\u00e9 tea\r\n  \r\nlast".encode("utf-8")
            path.write_bytes(data)
            result = self.run_app(path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), {"lines": 3, "words": 3, "blank_lines": 1})
            self.assertEqual(path.read_bytes(), data)

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.txt"
            path.write_bytes(b"")
            self.assertEqual(json.loads(self.run_app(path).stdout), {"lines": 0, "words": 0, "blank_lines": 0})

    def test_invalid_utf8_missing_file_and_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "invalid.txt"
            path.write_bytes(b"\xff")
            for item in (path, Path(tmp) / "missing", Path(tmp)):
                result = self.run_app(item)
                self.assertEqual(result.returncode, 2)
                self.assertIn("Cannot read UTF-8 text", result.stderr)

    def test_deterministic_build(self):
        artifact = ROOT / "dist/textstats.pyz"
        before = artifact.read_bytes()
        subprocess.run([sys.executable, str(ROOT / "scripts/build_textstats.py")], check=True, capture_output=True)
        self.assertEqual(artifact.read_bytes(), before)
