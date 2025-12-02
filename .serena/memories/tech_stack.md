# 技術スタック

## プログラミング言語
- **Python 3.10**

## 主要フレームワーク・ライブラリ

### GUIフレームワーク
- **PyQt5 5.15.11**: デスクトップGUIアプリケーション開発
  - PyQt5-Qt5 5.15.2
  - PyQt5_sip 12.15.0

### データ処理
- **pandas 2.2.2**: DataFrame操作、CSV読み書き
- **numpy 2.1.1**: 数値計算

### PDF処理
- **PyMuPDF (fitz) 1.25.1**: PDFファイルの読み込み・表示
- **pymupdf4llm 0.0.17**: PDF→テキスト変換

### 画像処理
- **ExifRead 3.2.0**: 画像メタデータの読み取り（EXIF情報）

### 日本語処理
- **jaconv 0.4.0**: 日本語文字の変換（半角⇔全角等）

### パッケージング
- **pyinstaller 6.10.0**: Pythonスクリプトのexe化
- **pyinstaller-hooks-contrib 2024.8**: PyInstallerのフック集
- **pefile 2024.8.26**: PEファイル操作

### その他ユーティリティ
- **python-dateutil 2.9.0.post0**: 日付処理
- **pytz 2024.1**: タイムゾーン処理
- **pywin32-ctypes 0.2.3**: Windows API呼び出し
- **altgraph 0.17.4**: グラフ構造処理

## 開発ツール

### 仮想環境
- **venv**: Python標準の仮想環境
  - プロジェクトには `.venv` と `.venv_claude` の2つの仮想環境が存在

### バージョン管理
- **Git**: ソースコード管理
  - リモートリポジトリ: あり（GitHub等）
  - 自動push/pullバッチファイルあり

### コードエディタ
- **VS Code**: プロジェクト設定（.vscode/）あり

## プロジェクト固有のツール
- **AutoHotkey v1**: Windows自動化、ホットキー管理（_ime_control.ahk）
- **Qt Designer**: UIデザイン（.uiファイル → .pyファイル生成）

## ビルド・デプロイ
- **PyInstaller**: スタンドアロンexe生成
  - 日本語パス対応の特殊設定が必要（PyInstaller日本語パス対応手順.txt参照）
  - specファイル: 給与計算検定入力アプリ_試作V1.spec
