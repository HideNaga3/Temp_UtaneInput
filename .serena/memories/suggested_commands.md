# よく使うコマンド

**重要**: このプロジェクトはWindows環境で開発されています。Claude CodeのBashツールを使用する際は、必ず`powershell -Command`でラップして実行してください。

## Python仮想環境の操作

### 仮想環境の確認
```powershell
powershell -Command "Test-Path .venv"
```

### 仮想環境の作成
```powershell
powershell -Command "python -m venv .venv"
```

### 仮想環境でPythonスクリプト実行
```powershell
powershell -Command ".venv\Scripts\python.exe MAIN_APP.py"
```

## パッケージ管理

### pipのアップグレード
```powershell
powershell -Command ".venv\Scripts\python.exe -m pip install --upgrade pip"
```

### パッケージのインストール
```powershell
# 単一パッケージ
powershell -Command ".venv\Scripts\python.exe -m pip install pandas"

# 複数パッケージ
powershell -Command ".venv\Scripts\python.exe -m pip install pandas openpyxl oletools"

# requirements.txtから一括インストール
powershell -Command ".venv\Scripts\python.exe -m pip install -r requirements.txt"
```

### インストール済みパッケージの確認
```powershell
powershell -Command ".venv\Scripts\python.exe -m pip list"
```

### 特定パッケージの情報確認
```powershell
powershell -Command ".venv\Scripts\python.exe -m pip show pandas"
```

## アプリケーション実行

### メインアプリケーションの起動
```powershell
powershell -Command ".venv\Scripts\python.exe MAIN_APP.py"
```

### テストの実行
```powershell
powershell -Command ".venv\Scripts\python.exe test_main_app.py"
```

## ファイル操作

### ファイル一覧
```powershell
powershell -Command "Get-ChildItem"
powershell -Command "Get-ChildItem -Recurse"
```

### ファイル移動・リネーム
```powershell
powershell -Command "Move-Item -Path 'old.txt' -Destination 'new.txt'"
powershell -Command "Rename-Item -Path 'temp_folder' -NewName 'new_folder'"
```

### ファイル削除
```powershell
powershell -Command "Remove-Item 'file.txt'"
```

### ディレクトリ作成
```powershell
powershell -Command "New-Item -ItemType Directory -Path 'newfolder'"
```

### ファイルコピー
```powershell
powershell -Command "Copy-Item -Path 'source.txt' -Destination 'dest.txt'"
```

## Git操作

### 変更確認
```bash
git status
git diff
```

### コミット
```bash
git add .
git commit -m "コミットメッセージ"
```

### プッシュ
```bash
# 通常のpush
git push

# 初回push（upstream設定）
git push --set-upstream origin main
```

### リモートの確認
```bash
git remote -v
```

### ログ確認
```bash
git log --oneline -10
```

## PyQt5 UI変換

### .uiファイルから.pyファイルへの変換
```powershell
powershell -Command ".venv\Scripts\python.exe -m PyQt5.uic.pyuic -x main_app_ui.ui -o main_app_ui.py"
```

## PyInstallerでexe化

### exeファイルの作成
```powershell
powershell -Command ".venv\Scripts\python.exe -m PyInstaller 給与計算検定入力アプリ_試作V1.spec"
```

## ファイル検索

### 特定パターンのファイルを検索
```powershell
powershell -Command "Get-ChildItem -Recurse -Filter '*.py'"
```

### 特定の文字列を含むファイルを検索
```powershell
powershell -Command "Get-ChildItem -Recurse -Include *.py | Select-String -Pattern 'search_pattern'"
```

## その他のユーティリティコマンド

### Pythonバージョン確認
```powershell
powershell -Command ".venv\Scripts\python.exe --version"
```

### ディレクトリサイズ確認
```powershell
powershell -Command "Get-ChildItem -Recurse | Measure-Object -Property Length -Sum"
```

### プロセス確認
```powershell
powershell -Command "Get-Process python"
```

## 注意事項

1. **必ずPowerShellでラップ**: Claude CodeのBashツールはUnix互換のため、Windowsのパスを正しく解釈するにはPowerShellでラップする必要があります。
2. **仮想環境を使用**: パッケージのインストールは必ず`.venv\Scripts\python.exe`経由で実行してください。
3. **パスの引用符**: スペースを含むパスは必ずシングルクォートで囲んでください（例: `'C:\Program Files\...'`）
