# .specファイルから直接ビルド

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

Write-Host "`n=== .specファイルから直接ビルド ===" -ForegroundColor Green
Write-Host "使用する.spec: 給与計算検定1級入力アプリ_試作V1.spec" -ForegroundColor Yellow

# .specファイルから直接ビルド
& "P:\python.exe" -m PyInstaller "X:\給与計算検定1級入力アプリ_試作V1.spec" --clean

# 実行結果の確認
$ExeFileName = "給与計算検定1級入力アプリ_試作V1.exe"
$XDrivePath = "X:\dist\$ExeFileName"
$RealPath = "$ScriptDir\dist\$ExeFileName"

Write-Host "`n=== ファイル存在確認 ===`n" -ForegroundColor Cyan

if (Test-Path $XDrivePath) {
    Write-Host "EXEファイルの作成を確認しました" -ForegroundColor Green
    Write-Host "場所: $RealPath`n" -ForegroundColor Yellow

    # ファイルサイズも表示
    $FileSize = (Get-Item $XDrivePath).Length
    $FileSizeMB = [Math]::Round($FileSize / 1MB, 2)
    Write-Host "ファイルサイズ: $FileSizeMB MB" -ForegroundColor Cyan

    # 前回のサイズと比較
    Write-Host "`n前回のビルド: 79.08 MB" -ForegroundColor Gray
    $Reduction = 79.08 - $FileSizeMB
    if ($Reduction -gt 0) {
        Write-Host "削減サイズ: $Reduction MB" -ForegroundColor Green
        $Percent = [Math]::Round(($Reduction / 79.08) * 100, 1)
        Write-Host "削減率: $Percent %" -ForegroundColor Green
    }
} else {
    Write-Host "EXEファイルの作成に失敗しました" -ForegroundColor Red
    Write-Host "確認した場所: $XDrivePath" -ForegroundColor Red
}

Write-Host "`n===================================`n" -ForegroundColor Cyan

# 処理完了後の待機
Read-Host "続行するには何かキーを押してください"
