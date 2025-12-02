@echo off
echo "PUSH?"
set /p "commit_msg=Enter commit message (empty = 'auto push'): "

REM Check if empty
if "%commit_msg%"=="" (
    set "commit_msg=auto push"
    echo Commit message: auto push (default)
) else (
    echo Commit message: %commit_msg%
)

echo.
git add .
git commit -m "%commit_msg%"
git push origin main
echo.
echo Push completed.
pause
