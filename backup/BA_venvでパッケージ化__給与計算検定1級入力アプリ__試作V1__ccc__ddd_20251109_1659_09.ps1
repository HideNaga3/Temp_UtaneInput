# PowerShellスクリプト - PyInstaller日本語パス対応

# このスクリプトが存在するディレクトリを取得
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# 既存のX:, P:ドライブを削除（エラーは無視）
cmd /c "subst X: /d 2>nul"
cmd /c "subst P: /d 2>nul"

# Pythonの実行ファイルのパスを動的に検出
$PythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $PythonExe) {
    # Get-Commandで見つからない場合はwhere.exeで検索
    $PythonExe = (where.exe python 2>$null | Select-Object -First 1)
}

if (-not $PythonExe) {
    Write-Host "エラー: Pythonが見つかりません。PATHにPythonが登録されているか確認してください。" -ForegroundColor Red
    Read-Host "`n続行するには何かキーを押してください"
    exit 1
}

# Pythonのインストールディレクトリを取得（python.exeの親ディレクトリ）
$PythonHome = Split-Path -Parent $PythonExe

Write-Host "検出したPythonパス: $PythonHome" -ForegroundColor Cyan

# Python本体をP:ドライブにマップ
cmd /c "subst P: `"$PythonHome`""

# プロジェクトフォルダをX:ドライブにマップ
cmd /c "subst X: `"$ScriptDir`""

# 環境変数設定
$env:VIRTUAL_ENV = "X:\.venv"
$env:PYTHONHOME = "P:"
$env:PYTHONPATH = "X:\.venv\Lib\site-packages;X:\"
$env:PATH = "P:;P:\Scripts;X:\.venv\Scripts;$env:PATH"
$env:TEMP = "X:\temp"

# TEMPディレクトリ作成
if (-not (Test-Path "X:\temp")) {
    New-Item -ItemType Directory -Path "X:\temp" | Out-Null
}

Write-Host "=== 環境変数設定後 ===" -ForegroundColor Cyan
Write-Host "VIRTUAL_ENV: $env:VIRTUAL_ENV"
Write-Host "PYTHONHOME: $env:PYTHONHOME"
Write-Host "PYTHONPATH: $env:PYTHONPATH"
Write-Host "TEMP: $env:TEMP"
Write-Host "========================" -ForegroundColor Cyan

# バッチファイル名からパラメータ取得
$batname = [System.IO.Path]::GetFileNameWithoutExtension($MyInvocation.MyCommand.Name)
$parts = $batname -split '__'
$var1 = $parts[1]
$var2 = $parts[2]
$var3 = $parts[3]
$var4 = $parts[4]

Write-Host "var1 = $var1"
Write-Host "var2 = $var2"
Write-Host "var3 = $var3"
Write-Host "var4 = $var4"

# PyInstallerオプションを配列で定義（見やすく改行）

# 基本オプション
$BasicOptions = @(
    "--onefile"
    "--noconsole"
    "--noupx"
)

# アイコン設定
$IconOptions = @(
    "--icon", "X:\_icon\icon.ico"
)

# アプリ名設定
$NameOptions = @(
    "--name", "$var1`_$var2"
)

# データファイル追加
$AddDataOptions = @(
    "--add-data", "X:\AutoHotkey64_2.0.18.exe;."
    "--add-data", "X:\_icon\icon.ico;."
    "--add-data", "X:\_ime_control.ahk;."
    "--add-data", "X:\_icon\ccw.ico;."
    "--add-data", "X:\_icon\cw.ico;."
    "--add-data", "X:\_icon\fit_h.ico;."
    "--add-data", "X:\_icon\fit_w.ico;."
    "--add-data", "X:\_icon\reset_scale.ico;."
    "--add-data", "X:\_icon\zoomin.ico;."
    "--add-data", "X:\_icon\zoomout.ico;."
    "--add-data", "X:\_icon\screen_mode.ico;."
    "--add-data", "X:\_icon\encode_check.ico;."
)

# 除外モジュール
$ExcludeOptions = @(
    # Jupyter関連（開発環境のみで使用）
    "--exclude-module", "ipykernel"
    "--exclude-module", "ipython"
    "--exclude-module", "jupyter"
    "--exclude-module", "jupyter_core"
    "--exclude-module", "jupyter_client"
    "--exclude-module", "notebook"
    "--exclude-module", "nbformat"
    "--exclude-module", "nbconvert"
    "--exclude-module", "traitlets"

    # 画像処理・科学計算（未使用）
    "--exclude-module", "PIL"
    "--exclude-module", "Pillow"
    "--exclude-module", "matplotlib"
    "--exclude-module", "scipy"
    "--exclude-module", "sympy"

    # GUI関連（PyQt5を使用するためTkinterは不要）
    "--exclude-module", "tkinter"
    "--exclude-module", "_tkinter"

    # PyQt5の不要モジュール（未使用確認済み）
    "--exclude-module", "PyQt5.QtWebEngine"
    "--exclude-module", "PyQt5.QtWebEngineCore"
    "--exclude-module", "PyQt5.QtWebEngineWidgets"
    "--exclude-module", "PyQt5.QtWebEngineProcess"
    "--exclude-module", "PyQt5.QtMultimedia"
    "--exclude-module", "PyQt5.QtMultimediaWidgets"
    "--exclude-module", "PyQt5.QtNetwork"
    "--exclude-module", "PyQt5.QtPositioning"
    "--exclude-module", "PyQt5.QtQml"
    "--exclude-module", "PyQt5.QtQuick"
    "--exclude-module", "PyQt5.QtQuickWidgets"
    "--exclude-module", "PyQt5.QtSensors"
    "--exclude-module", "PyQt5.QtSerialPort"
    "--exclude-module", "PyQt5.QtSql"
    "--exclude-module", "PyQt5.QtSvg"
    "--exclude-module", "PyQt5.QtTest"
    "--exclude-module", "PyQt5.QtWebSockets"
    "--exclude-module", "PyQt5.QtXml"
    "--exclude-module", "PyQt5.QtXmlPatterns"
    "--exclude-module", "PyQt5.Qt3DCore"
    "--exclude-module", "PyQt5.Qt3DRender"
    "--exclude-module", "PyQt5.QtBluetooth"
    "--exclude-module", "PyQt5.QtDBus"
    "--exclude-module", "PyQt5.QtDesigner"
    "--exclude-module", "PyQt5.QtHelp"
    "--exclude-module", "PyQt5.QtLocation"
    "--exclude-module", "PyQt5.QtNfc"
    "--exclude-module", "PyQt5.QtOpenGL"
    "--exclude-module", "PyQt5.QtPrintSupport"
    "--exclude-module", "PyQt5.QtWinExtras"

    # テスト・デバッグ関連
    "--exclude-module", "unittest"
    "--exclude-module", "test"
    "--exclude-module", "doctest"
    "--exclude-module", "pdb"
    "--exclude-module", "pydoc"
    "--exclude-module", "pydoc_data"

    # 型チェック・リンター（開発時のみ）
    "--exclude-module", "mypy"
    "--exclude-module", "typing_extensions"
    "--exclude-module", "pylint"
    "--exclude-module", "flake8"

    # ネットワーク・Web関連（未使用）
    "--exclude-module", "http"
    "--exclude-module", "urllib3"
    "--exclude-module", "requests"
    "--exclude-module", "flask"
    "--exclude-module", "django"

    # 暗号化・セキュリティ（未使用）
    "--exclude-module", "cryptography"
    # 注意: sslは標準ライブラリで依存関係がある可能性があるため除外しない

    # XML・HTML処理（サードパーティのみ除外）
    # 注意: xml, html は標準ライブラリのため除外しない
    "--exclude-module", "lxml"
    "--exclude-module", "BeautifulSoup"

    # データベース（未使用）
    "--exclude-module", "sqlite3"
    "--exclude-module", "sqlalchemy"

    # その他の大きなモジュール
    # 注意: setuptools, distutils, email, multiprocessing は依存関係があるため除外しない
    "--exclude-module", "asyncio"
    "--exclude-module", "concurrent"
)

# 出力パス設定
$PathOptions = @(
    "--distpath", "X:\dist"
    "--workpath", "X:\build"
    "--specpath", "X:\"
)

# メインファイル
$MainFile = @(
    "X:\MAIN_APP.py"
)

# すべてのオプションを結合
$PyInstallerArgs = $BasicOptions + $IconOptions + $NameOptions + $AddDataOptions + $ExcludeOptions + $PathOptions + $MainFile

# PyInstaller実行（ランチャーを回避してPythonモジュールとして直接実行）
Write-Host "`n=== PyInstaller実行中 ===" -ForegroundColor Green
Write-Host "実行方法: python -m PyInstaller (ランチャー回避)" -ForegroundColor Gray
& "P:\python.exe" -m PyInstaller @PyInstallerArgs

# 実行結果の確認（実際の出力先で確認）
$ExeFileName = "$var1`_$var2.exe"
$XDrivePath = "X:\dist\$ExeFileName"
$RealPath = "$ScriptDir\dist\$ExeFileName"

Write-Host "`n=== ファイル存在確認 ===" -ForegroundColor Cyan
Write-Host "確認パス1 (X:ドライブ): $XDrivePath"
Write-Host "確認パス2 (実パス): $RealPath"

if (Test-Path $XDrivePath) {
    Write-Host "`nEXEファイルの作成を確認しました: $XDrivePath" -ForegroundColor Green
    Write-Host "EXEファイルの場所: $RealPath" -ForegroundColor Yellow

    # ファイルサイズも表示
    $FileSize = (Get-Item $XDrivePath).Length
    $FileSizeMB = [Math]::Round($FileSize / 1MB, 2)
    Write-Host "ファイルサイズ: $FileSizeMB MB" -ForegroundColor Gray
} elseif (Test-Path $RealPath) {
    Write-Host "`nEXEファイルの作成を確認しました: $RealPath" -ForegroundColor Green
    Write-Host "EXEファイルの場所: $RealPath" -ForegroundColor Yellow

    # ファイルサイズも表示
    $FileSize = (Get-Item $RealPath).Length
    $FileSizeMB = [Math]::Round($FileSize / 1MB, 2)
    Write-Host "ファイルサイズ: $FileSizeMB MB" -ForegroundColor Gray
} else {
    Write-Host "`nEXEファイルの作成に失敗しました。" -ForegroundColor Red
    Write-Host "確認した場所:" -ForegroundColor Red
    Write-Host "  - $XDrivePath" -ForegroundColor Red
    Write-Host "  - $RealPath" -ForegroundColor Red
    Write-Host "distフォルダを確認してください: $ScriptDir\dist\" -ForegroundColor Red
}

# クリーンアップ（tempとspecファイルのみ削除、buildとdistは残す）
# if (Test-Path "X:\temp") { Remove-Item "X:\temp" -Recurse -Force }
# Get-ChildItem "X:\*.spec" -ErrorAction SilentlyContinue | Remove-Item -Force

# 元のディレクトリに戻る
Set-Location $ScriptDir

# ドライブのマウント解除
# cmd /c "subst X: /d"
# cmd /c "subst P: /d"

Write-Host "`n===================================" -ForegroundColor Cyan
Write-Host "処理が完了しました" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Cyan

# 処理完了後の待機
Read-Host "`n続行するには何かキーを押してください"
