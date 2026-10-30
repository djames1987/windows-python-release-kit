# Dependency and licensing inventory

Original kit code and documentation: MIT, see LICENSE. AI-assisted original
prototype; review before redistribution. MIT permits resale and modification;
it does not confer exclusivity, trademark rights, or proven market value.

Runtime/build prerequisite: an independently installed CPython 3.12.x.
Only Python standard-library modules are imported. No pip packages, external
assets, fonts, JavaScript, or model/API dependencies are required or bundled.
Python itself and its standard library are NOT redistributed in this kit.
Python is licensed under the PSF License Version 2 and contains components with
additional notices. Consult the exact installed Python distribution's LICENSE
and https://docs.python.org/3.12/license.html before bundling a runtime.

The .pyz contains this project's source, not a Python interpreter. Do not remove
required third-party notices if you later add a runtime or dependencies.
PowerShell and cmd.exe are existing operating-system tools, not bundled here.
