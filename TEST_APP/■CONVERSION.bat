@echo off
set CURRENT_FILE=%~f0
for /f %%i in ('echo %~nx0') do set FILENAME=%%~ni
pyuic5.exe test2_main_window.ui -o test2_main_window.py

set CURRENT_FILE=%~f0
for /f %%i in ('echo %~nx0') do set FILENAME=%%~ni
pyuic5.exe test2_sub.ui -o test2_sub.py

@REM set CURRENT_FILE=%~f0
@REM for /f %%i in ('echo %~nx0') do set FILENAME=%%~ni
@REM pyuic5.exe _collation_dialog_ui.ui -o _collation_dialog_ui.py