@echo off
chcp 932 >nul
setlocal enabledelayedexpansion

:: このバッチファイルが存在するディレクトリにカレントディレクトリを設定
cd /d "%~dp0"

:: バッチファイル名を取得
set "batname=%~n0"
echo Debug: Original batname = [!batname!]

:: 'batname'の中の'__'を一時的に'\'に置き換える
set "batname_mod=!batname:__=\!"
echo Debug: Modified batname = [!batname_mod!]

:: 一時的に置き換えた文字を使用して'\'で分割
echo Debug: Starting token parsing...
for /f "tokens=1,2,3,4,5 delims=\" %%a in ("!batname_mod!") do (
    set "var1=%%b"
    set "var2=%%c"
    set "var3=%%d"
    set "var4=%%e"
)
echo Debug: Token parsing completed

:: Conda環境をアクティベート（var3にはinput_imgが入る）
echo Conda environment !var3! activating...
call conda activate !var3!

if defined CONDA_DEFAULT_ENV (
    echo Conda環境に成功しました: %CONDA_DEFAULT_ENV%
) else (
    echo Conda環境に成功しませんでした。
    pause
    exit /b 1
)

:: 変数の値を表示
echo.
echo ===== Variables extracted from batch filename =====
echo var1 = !var1!
echo var2 = !var2!
echo var3 = !var3!
echo var4 = !var4!
echo.

echo Press ENTER to execute PyInstaller
pause

:: PyInstallerでパッケージ化
pyinstaller ^
--onefile ^
--noconsole ^
--name "!var1!_!var2!" ^
--exclude-module ipykernel ^
--exclude-module ipython ^
--exclude-module jupyter ^
--exclude-module jupyter_core ^
--exclude-module jupyter_client ^
--exclude-module notebook ^
--exclude-module nbformat ^
--exclude-module nbconvert ^
--exclude-module traitlets ^
--add-data "./_icon/icon.ico;." ^
--add-data "./_icon/cw.ico;." ^
--add-data "./_icon/ccw.ico;." ^
--add-data "./_icon/zoomin.ico;." ^
--add-data "./_icon/zoomout.ico;." ^
--add-data "./_icon/fit_w.ico;." ^
--add-data "./_icon/fit_h.ico;." ^
--add-data "./_icon/reset_scale.ico;." ^
--add-data "./_icon/screen_mode.ico;." ^
--add-data "./_icon/encode_check.ico;." ^
--add-data "./_ime_control.ahk;." ^
--add-data "./AutoHotkey64_2.0.18.exe;." ^
--icon "./_icon/icon.ico" ^
MAIN_APP.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo パッケージ化が正常に完了しました！
    echo 出力ファイル: dist\!var1!_!var2!.exe
) else (
    echo.
    echo パッケージ化中にエラーが発生しました。
)

:: コマンドプロンプトを開いたままにする
echo.
echo 任意のキーを押して終了してください...
pause >nul
endlocal
