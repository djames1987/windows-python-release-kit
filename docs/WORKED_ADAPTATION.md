# Worked adaptation: TextStats

A second complete CLI shows how to replace the checksum business logic while
reusing the packaging pattern. It counts lines, whitespace-separated words, and
blank lines in UTF-8 text. Nothing is uploaded or modified. This is not natural
language tokenization, a document converter, or a PDF/Word reader.

## Run the example

From the source-kit root, with Python 3.12 already installed:

```powershell
py -3.12 scripts/build_textstats.py
py -3.12 dist/textstats.pyz examples/textstats.txt --json
py -3.12 -m unittest discover -s tests -v
```

The middle command prints exactly:

```json
{"blank_lines": 1, "lines": 3, "words": 7}
```

On Linux use your Python 3.12 executable instead of `py -3.12`. The guide's
fixture/output and build command are covered by automated subprocess tests.
The newly added example has been executed on Linux, not yet on Windows.

## What changed from ReleaseCheck

1. **Business logic:** `adaptations/textstats/textstats.py` replaces SHA-256 with
   `summarize(path)`. It streams by line, accepts an optional UTF-8 BOM, and
   treats LF/CRLF/CR as line boundaries through Python universal-newline input.
2. **Entrypoint:** its `__main__.py` imports `textstats.main`, not checksum.main.
   Keeping entrypoints tiny makes the same function usable from source and ZIP.
3. **Build inventory:** `scripts/build_textstats.py` explicitly includes these
   two files and calls `archive()` from the original builder. It produces
   `dist/textstats.pyz` without altering the original app or release ZIP.
4. **Contract:** success exits 0; invalid UTF-8, unreadable file or invalid CLI
   input exits 2. JSON contains exactly three integer counts. An empty file
   has zero lines; a final nonempty unterminated line counts as a line.
5. **Tests:** `tests/test_textstats.py` exercises the guide, Unicode/spaces in
   paths, BOM, CRLF, blank lines, empty input, invalid encoding, missing input,
   directory input, unchanged source bytes and deterministic rebuild.

## Adapt to a third utility

Copy this two-file layout, change the import and CLI name, then define your
input/output and exit-code contract before changing the logic. Make a dedicated
builder with exact file names. Add known-answer and failure-path subprocess
tests against the built `.pyz`, not only the source module. Update the source-kit
packager's explicit inventory if the new example should be distributed.

For a standalone customer release, add your own end-user instructions, license,
notices, versioned ZIP, checksum manifest and Windows launcher using the
ReleaseCheck builder as the reference. TextStats here is an adaptation lesson,
not an independently versioned product distribution. Complete the release
checklist and Windows tests before making compatibility promises.

## Limits

Only UTF-8 (with or without BOM) is supported. A binary file that happens to be
valid UTF-8 may still be counted; no reliable file-type detection is attempted.
Very long individual lines can consume substantial memory. Counts can become
inconsistent if a file is changed while it is being read. This is an educational
small-tool example, not a hardened file-processing service.
