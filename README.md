# Windows Python Release Kit — free sample 0.1.0

**A deliberately narrow, offline starter for releasing a Python CLI to Windows
users who already have Python.** Includes a real checksum app, deterministic
archive builder, tests, Windows launcher, release checklist and troubleshooting.
No packages to install, cloud services, AI API keys, subscriptions or paid tools.
AI helped create this kit. This free, MIT-licensed source preview is for learning
and feedback—not a standalone EXE packager or a paid product.

## Start here (about five minutes)

Prerequisite: an existing Python 3.12.x installation. Tested interpreter:
CPython 3.12.14 on Linux. The prior ReleaseCheck kit passed the specific Windows checks recorded in
`docs/VALIDATION.md`. The newly added TextStats example is Linux-tested only.
These commands are run from this folder in a terminal:

```powershell
py -3.12 -m unittest discover -s tests -v
py -3.12 scripts/build.py
py -3.12 dist/releasecheck.pyz examples/hello.txt --json
```

On Linux/macOS replace `py -3.12` with `python3.12` (or your 3.12 interpreter).
The PowerShell convenience scripts are `scripts/test.ps1` and
`scripts/build.ps1`; the latter fails if tests fail. If policy blocks PowerShell
scripts, use the Python commands above. Do not disable organizational policies.

Build outputs:
- `dist/releasecheck.pyz` — Python executable archive, **not a standalone EXE**.
- `dist/releasecheck-0.1.0-windows-python.zip` — end-user distribution.
- Matching `.zip.sha256` — external archive checksum.

Extract the ZIP and run its `releasecheck.cmd` from a Windows terminal, or run
`py -3.12 releasecheck.pyz`. See `docs/END_USER.txt` for exact examples and exits.

To package the entire source kit plus example distribution, run
`py -3.12 scripts/package_source.py`. It includes only an explicit set of project
files, not arbitrary workspace contents.

## A second worked example

Follow `docs/WORKED_ADAPTATION.md` to build TextStats, a UTF-8 line/word counter.
The guide includes exact expected output and corresponding automated tests.

## Adapt it to your own CLI

1. Replace `app/checksum.py` and adjust `app/__main__.py` to call your entrypoint.
2. Change the version, app names in `scripts/build.py`, Windows launcher and tests.
3. Update end-user docs, LICENSE ownership and third-party notices to match reality.
4. Extend tests for your feature and rerun the entire suite.
5. Complete `docs/RELEASE_CHECKLIST.md` before releasing anything.

The builder includes only top-level `app/*.py`: deliberately no packages,
nested data or native extensions. Extend the explicit inclusion rules and tests
if you need those. It uses fixed ZIP metadata, sorted members and no compression
so identical input bytes yield identical archives on this tested interpreter.
This is deterministic packaging, not a claim of independently verified
cross-platform or hermetic builds. Newlines/encoding changes change checksums.

## Who this helps

Python developers shipping small internal command-line tools to Windows
colleagues with Python already installed. This is a small, auditable starting
point rather than a generalized packaging framework.

## Help shape the next version

Try building the sample and open a GitHub issue with your Python/Windows
versions, what you tried, and where you got stuck. Please remove private file
paths, secrets, customer data and other personal details from reports. What
would save you the most work: adding package data, an EXE workflow, or a
release checklist? Feedback does not commit you to purchasing anything.
No paid product, delivery date, support SLA or revenue outcome is promised.

## What it does not do

No EXE freezing, installer, GUI, signing certificate, SmartScreen reputation,
automatic updates, dependency management, encrypted source, licensing server,
telemetry, refund automation, customer service or sales integration. No CI workflow is included. Zero additional
software cost assumes access to a computer and Python; your labor, existing AI
access, taxes, platform transaction fees and optional signing are not free by
implication. No revenue is promised.

## Security and support boundary

Hashes are not signatures and do not establish safety or publisher identity.
Do not use this example for adversarial file-integrity monitoring: files may
change during reading, and links are followed normally. The app is a local
single-file utility, not antivirus or a secure update framework. Never weaken
Windows security settings to make a build launch. Review all generated code.

License: MIT for original kit; Python/runtime notices in
`THIRD_PARTY_NOTICES.md`. See `docs/VALIDATION.md` for actually executed checks.

## Official references

- [Python 3.12 executable archives](https://docs.python.org/3.12/library/zipapp.html)
- [Python 3.12 licensing](https://docs.python.org/3.12/license.html)

References describe underlying mechanisms, not certification of this prototype.
