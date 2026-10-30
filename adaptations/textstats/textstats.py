"""Worked adaptation: stream UTF-8 text without changing the input."""
import argparse
import json
from pathlib import Path
import sys

VERSION = "0.1.0"


def summarize(path):
    lines = words = blank_lines = 0
    with path.open("r", encoding="utf-8-sig") as stream:
        for line in stream:
            lines += 1
            words += len(line.split())
            blank_lines += not line.strip()
    return {"lines": lines, "words": words, "blank_lines": blank_lines}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Count lines, whitespace-separated words and blank lines in UTF-8 text.")
    parser.add_argument("file", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)
    try:
        result = summarize(args.file)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Cannot read UTF-8 text: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(f"Lines: {result['lines']}\nWords: {result['words']}\nBlank lines: {result['blank_lines']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
