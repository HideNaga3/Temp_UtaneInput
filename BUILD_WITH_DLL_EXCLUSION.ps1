# .specファイルから直接ビルド（DLL除外版）

# このスクリプトが存在するディレクトリを取得
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# 既存のX:, P:ドライブを削除（エラーは無視）
cmd /c "subst X: /d 2>nul"
cmd /c "subst P: /d 2>nul"

# Python本体をP:ドライブにマップ
cmd /c "subst P: `"C:\Users\永井秀和\AppData\Local\Programs\Python\Python311`""

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

# PyInstaller実行（.specファイルから）
Write-Host "`n=== PyInstaller実行中（.specファイル使用） ===`n" -ForegroundColor Green
Write-Host "使用する.spec: 給与計算検定1級入力アプリ_試作V1.spec" -ForegroundColor Yellow
Write-Host "DLL除外処理: フェーズ2（opengl32sw.dll + Qt5モジュール除外）" -ForegroundColor Yellow
Write-Host "  - opengl32sw.dll (19.95 MB) ← NEW!" -ForegroundColor Cyan
Write-Host "  - Qt5関連DLL（約30個）`n" -ForegroundColor Yellow

# .specファイルから直接ビルド（--cleanで前回のビルドをクリーン）
& "P:\python.exe" -m PyInstaller "X:\給与計算検定1級入力アプリ_試作V1.spec" --clean

# 実行結果の確認
$ExeFileName = "給与計算検定1級入力アプリ_試作V1.exe"
$XDrivePath = "X:\dist\$ExeFileName"
$RealPath = "$ScriptDir\dist\$ExeFileName"

Write-Host "`n=== ファイル存在確認 ===`n" -ForegroundColor Cyan
Write-Host "確認パス1 (X:ドライブ): $XDrivePath"
Write-Host "確認パス2 (実パス): $RealPath`n"

if (Test-Path $XDrivePath) {
    Write-Host "✓ EXEファイルの作成を確認しました" -ForegroundColor Green
    Write-Host "場所: $RealPath`n" -ForegroundColor Yellow

    # ファイルサイズも表示
    $FileSize = (Get-Item $XDrivePath).Length
    $FileSizeMB = [Math]::Round($FileSize / 1MB, 2)
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "ファイルサイズ: $FileSizeMB MB" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

    # 前回のサイズと比較
    Write-Host "比較:" -ForegroundColor Cyan
    Write-Host "  前回のビルド: 79.08 MB" -ForegroundColor Gray
    Write-Host "  今回のビルド: $FileSizeMB MB" -ForegroundColor Green

    $Reduction = 79.08 - $FileSizeMB
    if ($Reduction -gt 0) {
        Write-Host "`n削減サイズ: $Reduction MB" -ForegroundColor Yellow
        $Percent = [Math]::Round(($Reduction / 79.08) * 100, 1)
        Write-Host "削減率: $Percent %" -ForegroundColor Yellow
    } elseif ($Reduction -lt 0) {
        $Increase = [Math]::Abs($Reduction)
        Write-Host "`n増加サイズ: $Increase MB" -ForegroundColor Red
    } else {
        Write-Host "`nサイズ変化なし" -ForegroundColor Gray
    }
} elseif (Test-Path $RealPath) {
    Write-Host "✓ EXEファイルの作成を確認しました" -ForegroundColor Green
    Write-Host "場所: $RealPath`n" -ForegroundColor Yellow

    # ファイルサイズも表示
    $FileSize = (Get-Item $RealPath).Length
    $FileSizeMB = [Math]::Round($FileSize / 1MB, 2)
    Write-Host "ファイルサイズ: $FileSizeMB MB" -ForegroundColor Green
} else {
    Write-Host "✗ EXEファイルの作成に失敗しました" -ForegroundColor Red
    Write-Host "確認した場所:" -ForegroundColor Red
    Write-Host "  - $XDrivePath" -ForegroundColor Red
    Write-Host "  - $RealPath" -ForegroundColor Red
    Write-Host "`ndistフォルダを確認してください: $ScriptDir\dist\`n" -ForegroundColor Red
}

# 元のディレクトリに戻る
Set-Location $ScriptDir

Write-Host "`n===================================`n" -ForegroundColor Cyan
Write-Host "処理が完了しました" -ForegroundColor Green
Write-Host "===================================`n" -ForegroundColor Cyan

# 処理完了後の待機
Read-Host "続行するには何かキーを押してください"
