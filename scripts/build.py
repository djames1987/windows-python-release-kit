"""Offline, deterministic ZIP_STORED archive builder. Run from any directory."""
import hashlib
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def archive(path, members):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as bundle:
        for name, data in sorted(members.items()):
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, data)


def get_version():
    return re.search(r'^VERSION = "([0-9.]+)"$', (ROOT / "app/checksum.py").read_text(), re.M).group(1)


def build():
    version = get_version()
    DIST.mkdir(exist_ok=True)
    pyz = DIST / "releasecheck.pyz"
    archive(pyz, {p.name: p.read_bytes() for p in (ROOT / "app").glob("*.py")})
    members = {
        "releasecheck.pyz": pyz.read_bytes(),
        "releasecheck.cmd": (ROOT / "scripts/releasecheck.cmd").read_bytes(),
        "README.txt": (ROOT / "docs/END_USER.txt").read_bytes(),
        "LICENSE.txt": (ROOT / "LICENSE").read_bytes(),
        "THIRD_PARTY_NOTICES.txt": (ROOT / "THIRD_PARTY_NOTICES.md").read_bytes(),
    }
    members["SHA256SUMS.txt"] = "".join(f"{hashlib.sha256(data).hexdigest()}  {name}\n" for name, data in sorted(members.items())).encode()
    release = DIST / f"releasecheck-{version}-windows-python.zip"
    archive(release, members)
    (DIST / (release.name + ".sha256")).write_text(hashlib.sha256(release.read_bytes()).hexdigest() + "  " + release.name + "\n", encoding="ascii", newline="\n")
    print(release)
    return release


if __name__ == "__main__":
    build()
