# Release gate — do not mark unexecuted checks passed

## Source and repeatability
- [ ] Review AI-assisted code and adapt all app names, help, version and metadata.
- [ ] Record OS, architecture and exact `py -3.12 --version` output.
- [ ] Run tests from a clean source extraction; retain complete output.
- [ ] Build twice; compare outer ZIP SHA-256. Repeat on your target Windows host.
- [ ] Confirm archive inventory contains no secrets, private files or caches.
- [ ] Recheck licensing for everything added; include required notices.

## Windows gate (see VALIDATION.md for completed checks on one prior archive)
- [ ] Use a supported Windows machine with Python 3.12 and launcher installed.
- [ ] Run `py -3.12 -m unittest discover -s tests -v`.
- [ ] Run `scripts/build.ps1` if local policy permits; validate nonzero failures.
- [ ] Extract release ZIP under a path containing spaces and non-ASCII characters.
- [ ] Run `.cmd` from cmd.exe and PowerShell, including quoted file paths.
- [ ] Check exits 0 (match), 1 (mismatch), 2 (missing/invalid input).
- [ ] Test launcher missing/Python missing behavior; ensure docs explain it.
- [ ] Test `python.exe` by explicit path as the alternative to `py`.
- [ ] Scan with your normal security tools. Record warnings; do not bypass them.
- [ ] Have another person follow end-user instructions without coaching.

## Distribution and support
- [ ] State Python prerequisite, tested Windows version and architecture prominently.
- [ ] Publish checksums via an independently trusted channel, not as authenticity proof.
- [ ] Clarify preview status; no Windows compatibility claim before its gate passes.
- [ ] Define supported versions and support scope before accepting payment.
- [ ] Choose refund/contact policies and comply with platform and local rules.
- [ ] Obtain explicit approval for accounts, publication, payments and external sends.

Stop release if tests fail, a secret is found, a license is unknown, Windows
behavior remains untested, or product copy promises more than verified behavior.
