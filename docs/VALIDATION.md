# Validation record

Executed 2026-10-30 in the provided Linux workspace using CPython 3.12.14.
Command: `python -m unittest discover -s tests -v`.
Result: **15 tests passed**, including a repeat from a clean extracted source-kit
archive. The suite executes the built `.pyz` in subprocesses. The source-kit
archive was also rebuilt twice and compared byte-for-byte successfully.

Covered:
- Known SHA-256 vector (`abc`), JSON schema and uppercase expected hash.
- Match/mismatch exit codes, invalid expected hash, absent file, directory input.
- Empty file and multi-chunk (>2 MiB) file.
- Help, version, missing argument.
- Paths containing spaces and Unicode; input bytes unchanged after hashing.
- Byte-identical repeated build in this environment.
- Exact release inventory, inner manifest and external ZIP checksum.
- Extracted end-user archive runs via Python outside the source tree.
- Source packaging follows a changed app version and excludes stale releases
  and an unexpected private-notes fixture.

## Windows evidence for the prior archive

The parent task reported this completed validation on the user's machine on
2026-10-30: Windows 10 build 19045, Python 3.12. The **10-test suite passed twice**,
`build.ps1` passed, and the packaged release launcher successfully hashed the
example file. The tested source-kit archive SHA-256 was:

`532f1f49f83c50f7ba4f5494baf8f9b85e09f914e51553388c1f91deebd965c3`

These are reported Windows execution results, not Windows executions performed
inside this Linux build task. Exact Python patch version and CPU architecture
were not provided. This evidence applies to the prior archive, before TextStats
and these documentation changes, not to the current 15-test archive.

## Windows evidence for the 15-test archive

On 2026-10-30, the source-kit archive with SHA-256:

`2d6a470d64faff20bf4fc832310d597b60a9f1af7543944e83d6ceabf7bf2b1d`

passed **all 15 tests** on the owner's Windows 10 build 19045 machine with
Python 3.12, executed via the local debugger. This includes the TextStats tests.
The evidence is specific to that archive and environment; it does not establish
other Windows versions, Python patch versions, CPU architectures, or security
software behavior. These are reported local-debugger results, not Windows
executions performed inside this Linux build task. Documentation edits change
archive bytes: do not identify a later rebuilt archive by the tested hash above.

## Added worked adaptation

TextStats and its guide are covered by five additional Linux subprocess tests:
exact guide output; Unicode/BOM/CRLF and unterminated final line; empty file;
invalid UTF-8/missing file/directory; deterministic build. The complete 15-test
suite passes locally and from a clean extraction. The 15-test Windows result
for the specific archive above also covers the new example.

Still not established: missing Windows launcher behavior, Defender/SmartScreen,
installation policy, all Windows path edge cases, multiple Python versions or
architectures, simultaneous file modification, code signing, checkout, download
hosting or customer delivery. Cross-platform reproducibility has not been
demonstrated. This is a source prototype, not a broadly Windows-certified or
sales-ready distribution.

No dependencies were installed, accounts created, payments made, software
published, remote CI enabled, or external user messages sent by this build task.
