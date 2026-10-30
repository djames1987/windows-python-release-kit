import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("builder", ROOT / "scripts/build.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.release = builder.build()

    def run_app(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "dist/releasecheck.pyz"), *map(str, args)], capture_output=True, text=True)

    def test_known_sha256_json_unicode_space_path(self):
        with tempfile.TemporaryDirectory(prefix="release space ") as tmp:
            path = Path(tmp) / "café file.txt"
            path.write_bytes(b"abc")
            result = self.run_app(path, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), {"file": str(path), "sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad", "matches": None})
            self.assertEqual(path.read_bytes(), b"abc")

    def test_expected_hash_match_and_mismatch(self):
        path = ROOT / "examples/hello.txt"
        expected = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(self.run_app(path, "--expect", expected.upper()).returncode, 0)
        result = self.run_app(path, "--expect", "0" * 64, "--json")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)["matches"])

    def test_invalid_expected(self):
        for expected in ("123", "z" * 64):
            self.assertEqual(self.run_app(ROOT / "examples/hello.txt", "--expect", expected).returncode, 2)

    def test_missing_and_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.run_app(Path(tmp) / "missing").returncode, 2)
            self.assertEqual(self.run_app(tmp).returncode, 2)

    def test_empty_and_large_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "file"
            for data in (b"", b"x" * (2 * 1024 * 1024 + 7)):
                path.write_bytes(data)
                result = self.run_app(path, "--expect", hashlib.sha256(data).hexdigest())
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_help_and_version(self):
        self.assertEqual(self.run_app("--help").returncode, 0)
        self.assertEqual(self.run_app("--version").stdout.strip(), "0.1.0")
        self.assertEqual(self.run_app().returncode, 2)

    def test_reproducible_build(self):
        before = self.release.read_bytes()
        self.assertEqual(builder.build().read_bytes(), before)

    def test_release_inventory_and_checksums(self):
        with zipfile.ZipFile(self.release) as bundle:
            self.assertEqual(set(bundle.namelist()), {"releasecheck.pyz", "releasecheck.cmd", "README.txt", "LICENSE.txt", "THIRD_PARTY_NOTICES.txt", "SHA256SUMS.txt"})
            for line in bundle.read("SHA256SUMS.txt").decode().splitlines():
                checksum, name = line.split("  ", 1)
                self.assertEqual(hashlib.sha256(bundle.read(name)).hexdigest(), checksum)
            for entry in bundle.infolist():
                self.assertEqual(entry.date_time, (2020, 1, 1, 0, 0, 0))
        external = self.release.with_name(self.release.name + ".sha256").read_text().split()[0]
        self.assertEqual(hashlib.sha256(self.release.read_bytes()).hexdigest(), external)

    def test_source_package_tracks_version_bump_without_stale_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "kit"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns("dist", "__pycache__"))
            (root / "docs/private-notes.txt").write_text("FAKE_SECRET_NOT_FOR_DISTRIBUTION")
            app = root / "app/checksum.py"
            app.write_text(app.read_text().replace('VERSION = "0.1.0"', 'VERSION = "0.2.7"'))
            subprocess.run([sys.executable, str(root / "scripts/package_source.py")], check=True, capture_output=True)
            output = root / "dist/windows-python-release-kit-0.2.7-preview.zip"
            self.assertTrue(output.is_file())
            with zipfile.ZipFile(output) as bundle:
                names = bundle.namelist()
                self.assertIn("windows-release-kit/dist/releasecheck-0.2.7-windows-python.zip", names)
                self.assertIn("windows-release-kit/dist/releasecheck-0.2.7-windows-python.zip.sha256", names)
                self.assertFalse(any("0.1.0" in name for name in names))
                self.assertFalse(any("private-notes" in name for name in names))

    def test_extracted_release_runs_from_unrelated_directory(self):
        with tempfile.TemporaryDirectory(prefix="extracted release ") as tmp:
            with zipfile.ZipFile(self.release) as bundle:
                bundle.extractall(tmp)
            result = subprocess.run([sys.executable, str(Path(tmp) / "releasecheck.pyz"), "--version"], cwd=tmp, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "0.1.0")


if __name__ == "__main__":
    unittest.main()
