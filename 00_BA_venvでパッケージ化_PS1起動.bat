@echo off
echo Searching for BA_venv*.ps1 files...
pause

:: BA_venvで始まるps1ファイルを検索
for %%f in (BA_venv*.ps1) do (
    echo Found: %%f
    echo Executing: %%f
    powershell -ExecutionPolicy Bypass -File "%%f"
    goto :end
)

echo No BA_venv*.ps1 files found in current directory.
pause
exit /b 1

:end

