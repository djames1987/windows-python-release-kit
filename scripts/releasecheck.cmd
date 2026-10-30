@echo off
setlocal
rem Requires an existing Python 3.12 installation and the py launcher.
py -3.12 "%~dp0releasecheck.pyz" %*
exit /b %errorlevel%
