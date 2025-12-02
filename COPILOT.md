# COPILOT.md

This file provides guidance to GitHub Copilot when working with code in this repository.

---

## 重要 / Important

**このファイルを読み込む際は、必ず `COPILOT_GLOBAL.md` も一緒に読み込んでください。**

`COPILOT_GLOBAL.md` には、すべてのプロジェクトに共通するグローバル設定が記載されています。

**When reading this file, always read `COPILOT_GLOBAL.md` together.**

`COPILOT_GLOBAL.md` contains global settings that apply to all projects.

---

## 【プロジェクト設定】Project Settings

このセクションには、このプロジェクト固有の設定を記載します。

### プロジェクト概要 / Project Overview

**プロジェクト名:** 給与計算検定入力ソフト

**目的:** 給与計算検定試験のための画像付き入力ソフトウェア

**主要技術スタック:**
- Python 3.10
- PyQt5: GUIフレームワーク
- pandas: データ処理
- Pillow: 画像処理
- PyMuPDF (fitz): PDF処理

**開発環境:**
- Windows専用
- 仮想環境: `.venv`
- PyInstallerでexe化

### プロジェクト構成 / Project Structure

```
給与計算検定入力ソフト_20251015/
│
├── MAIN_APP.py                    # メインアプリケーション
├── main_app_ui.py                 # Qt DesignerからのUI定義
├── main_app_ui.ui                 # Qt Designer UIファイル
│
├── _lib/                          # ライブラリモジュール（exe化対象）
│   ├── _mode_config.py           # モード設定管理
│   ├── _validators.py            # バリデーション処理
│   ├── _image_utils.py           # 画像ユーティリティ
│   ├── _data_io.py               # CSV入出力
│   ├── _config_manager.py        # 設定管理
│   ├── _sub_lib.py               # サブライブラリ（h2z_kana_digit含む）
│   └── その他のモジュール
│
├── temp/                          # 一時ファイル・テスト用
├── for_claude/                    # Claude専用（参考資料として活用可能）
│   ├── log.txt                    # 作業履歴
│   └── archive/                   # アーカイブログ
│
├── data/                          # データファイル
│   ├── config.json               # アプリケーション設定
│   └── rect.json                 # ウィンドウ位置・サイズ設定
│
├── backup/                        # 自動バックアップ先
├── output/                        # スクリプト実行結果（一時）
├── DOC_給与検定/                  # 給与検定ドキュメント
├── DOC_ウタネ回覧/                # ウタネ回覧ドキュメント
│
├── .vscode/                       # VS Code設定
│   └── mcp.json                  # Serena MCP設定
│
├── .serena/                       # Serenaプロジェクト設定
│   ├── project.yml               # プロジェクト設定
│   └── memories/                 # プロジェクト知識ベース
│
├── COPILOT.md                     # このファイル（プロジェクト固有設定）
├── COPILOT_GLOBAL.md              # グローバル設定
├── requirements.txt               # Python依存パッケージ
└── 給与計算検定入力アプリ_試作V1.spec  # PyInstaller設定
```

### 重要な仕様 / Important Specifications

#### エンコーディング / Encoding

**ソースコード:** UTF-8
**CSVファイル:** CP932（日本語Windows標準）
- CSVの読み書きは必ず`encoding='cp932'`を指定
- `pandas.read_csv()`では`encoding='cp932', encoding_errors='ignore'`を使用

#### モード対応 / Mode Support

このアプリケーションは8つのモードをサポート:

1. **payroll** - 給与計算検定1級
2. **card** - カード見本
3. **utane** - ウタネ回覧
4. **foreigner** - 外国人データ
5. **prevention** - 防災
6. **syuei** - 集英社
7. **prevention2** - 防災V2
8. **factory** - 工場見学

**モード設定:** `_lib/_mode_config.py`で一元管理

#### データ変換ルール / Data Conversion Rules

アプリケーションでは様々な文字変換タイプをサポート:

- `zen` - 全角変換
- `zen-an` - 全角英数変換
- `zen-ans` - 全角英数記号変換
- `han` - 半角変換
- `han-ans` - 半角英数記号変換
- `zen-katakana` - 全角カタカナ変換
- `upper` - 大文字変換
- `lower` - 小文字変換
- `z2h-digit-only` - 全角数字→半角数字のみ
- `h2z-kana-digit` - 半角→全角（カナ・数字のみ、ASCII除外）※重要
- `current-ym` - 現在年月
- `zerofill` - ゼロ埋め

**`h2z_kana_digit`について:**
- `_lib/_sub_lib.py`の`SubLib.h2z_kana_digit()`メソッド
- `jaconv.h2z(text, digit=True, ascii=False, kana=True)`を使用
- 半角の数字とカナを全角に変換、ASCII文字（英字・記号）はそのまま
- 使用例: `"abc123ｱｲｳ"` → `"abc１２３アイウ"`

### プロジェクト固有のルール / Project-Specific Rules

#### 1. ファイル作成場所のルール / File Creation Location Rules

**重要: 一時ファイル・テストファイル・検証ファイルを作成する場所を厳守すること**

**作成して良い場所:**
- `temp/` フォルダ - 一時ファイル、作業用ファイル、テストスクリプト
- `for_claude/` フォルダ - セッション間で保持する必要があるファイル（参考として閲覧可能）

**絶対に作成してはいけない場所:**
- `_lib/` フォルダ - exeに組み込まれる実際のプログラムモジュール
- その他の実際のプログラムフォルダ - ユーザーがGitで管理している領域

**理由:**
- `_lib/`などのプログラムフォルダはexe化の対象であり、不要なファイルを含めてはいけない
- ユーザーがGitで管理しているフォルダに勝手にファイルを追加すると、バージョン管理が煩雑になる
- テストファイルや一時ファイルは開発用フォルダで管理するべき

**具体例:**

✅ OK:
```
temp/test_create_data_list.py       # テストファイル
temp/verify_refactoring.py          # 検証スクリプト
temp/temp_data.json                 # 一時データ
```

❌ NG:
```
_lib/test_xxx.py                    # プログラムフォルダにテストファイル
_lib/temp_xxx.py                    # プログラムフォルダに一時ファイル
_lib/original_xxx.py                # プログラムフォルダにバックアップファイル
```

**本番ファイルの編集について:**
ユーザーが明示的に指示した本番ファイル（例: `_lib/_create_data_list.py`）の編集は問題ありません。
新規ファイル作成時のみ、このルールを厳守すること。

#### 2. Serena MCP の活用 / Using Serena MCP

**プロジェクト固有の設定ファイル:**
- `.vscode/mcp.json` - Serena MCP サーバー設定
- `.serena/project.yml` - プロジェクト設定
- `.serena/memories/` - プロジェクト知識ベース

**よく使うSerenaクエリ例:**

```
@serena MAIN_APP.pyのクラス構造を説明して

@serena _lib/_mode_config.pyのModeConfigManagerクラスの使い方を教えて

@serena h2z_kana_digit関数の実装を見せて

@serena SubLibクラスが使われている箇所を全て探して

@serena create_data_list関数の依存関係を調査して
```

**Serenaのメモリ活用:**

`.serena/memories/`には以下のドキュメントが保存されています:

- `project_overview.md` - プロジェクト概要
- `codebase_structure.md` - コードベース構造の詳細
- `code_style_and_conventions.md` - コーディング規約
- `tech_stack.md` - 技術スタック
- `known_issues.md` - 既知の問題
- `progress.md` - 進捗管理

Serenaに質問すると、これらのメモリを参照して回答します。

#### 3. データファイルの管理 / Data File Management

**`output/` フォルダ:**
- 報告用の一時的な出力先
- スクリプトの実行結果（CSV, JSON, Excel等）を一時的に保存
- ファイルが増えてきたら、7z（または zip）に圧縮して整理
- ユーザーがファイルを移動・削除・圧縮する可能性がある

**`for_claude/` フォルダ:**
- Claude専用の作業領域（参考資料として閲覧可能）
- 重要なデータファイル（JSON, CSV等）はここに保存
- セッション間で参照が必要なファイルを保管
- このフォルダのファイルは削除・圧縮されない

#### 4. 応答スタイル / Response Style

**簡潔で要点を押さえた応答を心がけること**

基本方針:
- 説明は要点のみ、簡潔に
- 長い表や例は最小限（必要な場合のみ）
- コード例は1-2個程度
- 詳細な説明は明示的に求められた場合のみ

**例:**

❌ NG (冗長):
```
はい、h2z_kana_digit関数は_sub_lib.pyに実装されています。

## h2z_kana_digitの詳細

### 1. 実装場所
_lib/_sub_lib.py の SubLibクラス内にあります...
### 2. 使用しているライブラリ
jaconvライブラリを使用しています...
（さらに続く）
```

✅ OK (簡潔):
```
h2z_kana_digit関数の概要:
- 場所: _lib/_sub_lib.py の SubLib.h2z_kana_digit()
- 処理: 半角の数字・カナを全角に変換（ASCII除外）
- 実装: jaconv.h2z(text, digit=True, ascii=False, kana=True)
- 例: "abc123ｱｲｳ" → "abc１２３アイウ"
```

### よく使うコマンド / Frequently Used Commands

**Python仮想環境:**
```powershell
# 仮想環境の有効化
.venv\Scripts\activate

# モジュールインストール
pip install <module_name>

# requirements.txtからインストール
pip install -r requirements.txt
```

**Serena MCP:**
```powershell
# プロジェクトのインデックス化（初回のみ）
uvx --from git+https://github.com/oraios/serena serena project index

# プロジェクトのヘルスチェック
uvx --from git+https://github.com/oraios/serena serena project health-check
```

**PyInstaller（exe化）:**
```powershell
# specファイルからビルド
pyinstaller 給与計算検定入力アプリ_試作V1.spec
```

### 既知の問題 / Known Issues

詳細は`.serena/memories/known_issues.md`を参照してください。

Serenaに質問する場合:
```
@serena 既知の問題点を確認して
```

### 次のステップ / Next Steps

新しいタスクを開始する前に:

1. **Serenaを起動** - `.vscode/mcp.json`の[Start]ボタンをクリック
2. **プロジェクト概要を確認** - `@serena プロジェクトの概要を教えて`
3. **進捗状況を確認** - `.serena/memories/progress.md`または`for_claude/log.txt`を参照
4. **関連するコードを検索** - Serenaのシンボル検索を活用

---

## 【参考資料】Reference Materials

**必ず参照するファイル:**
- `COPILOT_GLOBAL.md` - グローバル設定（このファイルと一緒に読むこと）
- `.serena/project.yml` - プロジェクト設定
- `.serena/memories/` - プロジェクト知識ベース

**参考になるファイル:**
- `CLAUDE.md` - Claude Code用の設定（ルールは共通）
- `for_claude/log.txt` - 作業履歴（参考情報として有用）

---

**最終更新:** 2025-01-07
