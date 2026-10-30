"""Package only the intended kit files, never caches or unrelated workspace data."""
import hashlib
from pathlib import Path
from build import archive, build, get_version, ROOT, DIST
from build_textstats import build_textstats


def main():
    release = build()
    build_textstats()
    names = [
        "README.md", "LICENSE", "THIRD_PARTY_NOTICES.md", ".gitattributes", ".gitignore",
        "app/__main__.py", "app/checksum.py", "tests/test_release.py",
        "scripts/build.py", "scripts/build.ps1", "scripts/test.ps1",
        "scripts/releasecheck.cmd", "scripts/package_source.py",
        "docs/END_USER.txt", "docs/RELEASE_CHECKLIST.md", "docs/VALIDATION.md",
        "examples/hello.txt", "examples/textstats.txt",
        "adaptations/textstats/__main__.py", "adaptations/textstats/textstats.py",
        "scripts/build_textstats.py", "tests/test_textstats.py",
        "docs/WORKED_ADAPTATION.md", "dist/textstats.pyz",
    ]
    names += ["dist/releasecheck.pyz", release.relative_to(ROOT).as_posix(), release.relative_to(ROOT).as_posix() + ".sha256"]
    output = DIST / f"windows-python-release-kit-{get_version()}-preview.zip"
    archive(output, {"windows-release-kit/" + name: (ROOT / name).read_bytes() for name in names})
    print(output)
    print("SHA256", hashlib.sha256(output.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
