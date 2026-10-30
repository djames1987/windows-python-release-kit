"""ReleaseCheck: hash local files; no network, telemetry, or file modification."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

VERSION = "0.1.0"


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Print or compare a local file's SHA-256. A hash is not a signature.")
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("file", type=Path)
    parser.add_argument("--expect", help="Expected SHA-256 from a trusted independent source")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args(argv)
    expected = args.expect
    if expected is not None:
        expected = expected.lower()
        if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
            parser.error("--expect must be exactly 64 hexadecimal characters")
    try:
        actual = digest(args.file)
    except (OSError, ValueError) as exc:
        print(f"Cannot read file: {exc}", file=sys.stderr)
        return 2
    matched = None if expected is None else actual == expected
    if args.json:
        print(json.dumps({"file": str(args.file), "sha256": actual, "matches": matched}, ensure_ascii=True))
    else:
        print(f"{actual}  {args.file}")
        if matched is not None:
            print("MATCH" if matched else "MISMATCH")
    return 1 if matched is False else 0


if __name__ == "__main__":
    sys.exit(main())
