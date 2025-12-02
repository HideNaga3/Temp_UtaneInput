# COPILOT_GLOBAL.md

このファイルは、**GitHub Copilot**がすべてのプロジェクトで共通して参照するグローバル設定ファイルです。

---

## 【このファイルの目的】Purpose of This File

**GitHub Copilotのエージェントモードで、すべてのプロジェクトに共通する設定・ルール・ベストプラクティスを記載します。**

- プロジェクト固有の設定は各プロジェクトの`README.md`または専用設定ファイルに記載
- このファイルは、開発環境・ツール・コーディング規約など、横断的な設定を管理

**This file defines global settings, rules, and best practices for GitHub Copilot Agent Mode across all projects.**

- Project-specific settings should be in each project's `README.md` or dedicated config files
- This file manages cross-cutting concerns: dev environment, tools, coding conventions

---

## 【重要】Serena MCP サーバーの使用方法

### Serena MCPとは

**Serena**は、大規模コードベースを効率的に探索・編集するためのMCP（Model Context Protocol）サーバーです。

**主な機能:**
- プロジェクト全体のシンボル検索（クラス、関数、メソッド等）
- ファイル構造の把握とナビゲーション
- 参照箇所の検索
- コードの一括置換・リファクタリング
- プロジェクト知識の記憶（memories機能）

### クイックスタート

**1. `.vscode/mcp.json`の作成**

```json
{
  "inputs": [],
  "servers": {
    "serena": {
      "command": "Y:/.local/bin/uvx.exe",
      "args": [
        "--from",
        "git+https://github.com/oraios/serena",
        "serena",
        "start-mcp-server",
        "--enable-web-dashboard",
        "false"
      ],
      "env": {
        "PROJECT_ROOT": "${workspaceFolder}"
      }
    }
  }
}
```

**2. プロジェクトのインデックス化（初回のみ）**

```powershell
uvx --from git+https://github.com/oraios/serena serena project generate-yml --language python .
uvx --from git+https://github.com/oraios/serena serena project index
```

**3. MCPサーバーの起動**

`.vscode/mcp.json`を開いて`[Start]`ボタンをクリック

**4. 使い方**

Copilot Chat のエージェントモードで:
```
@serena MAIN_APP.pyの構造を説明して
@serena h2z_kana_digit関数が使われている箇所を全て探して
@serena この関数を_lib/に移動する影響範囲を調査して
```

### 詳細なセットアップガイド

**完全なセットアップ手順、トラブルシューティング、ベストプラクティスは以下を参照:**

`global/copilot/serena_setup_guide.md`

このガイドには以下の情報が含まれています:
- 詳細なセットアップ手順
- プロジェクト設定のカスタマイズ方法
- メモリファイルの活用方法
- 実際の使用例
- トラブルシューティング
- よくある質問---

## 【グローバル設定】Global Settings

### 言語設定 / Language Settings

**すべてのプロジェクトで日本語で対応してください。**

- すべての説明を日本語で行うこと
- すべての質問を日本語で行うこと
- コード内のコメントも日本語で記述すること

**IMPORTANT: Always communicate in Japanese for all projects.**

### 応答スタイル / Response Style

**重要: トークン節約のため、できるだけ要約して話すこと**
**重要: 絵文字禁止（例: NG, OK, *, - などのテキスト記号を使用すること）**

**基本方針:**
- **説明は要点のみ、簡潔に** - 冗長な説明を避ける
- **長い表や例は最小限** - 必要な場合のみ使用
- **コード例は1-2個程度** - 過度な例示を避ける
- **詳細な説明は明示的に求められた場合のみ** - ユーザーが「詳しく」と言った時だけ
- **箇条書きを活用** - 長い文章より簡潔な箇条書き
- **不要な前置きを削除** - 「それでは」「まず」などの冗長な接続詞を避ける

**トークン節約の例:**

NG (冗長):
```
はい、承知しました。それでは、h2z_kana_digit関数について詳しく説明させていただきます。

まず、この関数は_lib/_sub_lib.pyファイルのSubLibクラス内に定義されています。
この関数の主な目的は、半角の数字とカナ文字を全角に変換することです。
ただし、重要な点として、ASCII文字（英字や記号）はそのまま保持されます。

具体的な実装としては、jaconvライブラリのh2z関数を使用しており...
（さらに続く）
```

OK (簡潔):
```
h2z_kana_digit関数:
- 場所: _lib/_sub_lib.py の SubLib.h2z_kana_digit()
- 処理: 半角の数字・カナを全角に変換（ASCII除外）
- 実装: jaconv.h2z(text, digit=True, ascii=False, kana=True)
- 例: "abc123ｱｲｳ" → "abc１２３アイウ"
```

**IMPORTANT: Minimize token usage by keeping responses concise**

**Best practices:**
- **Key points only** - Avoid verbose explanations
- **Minimal tables/examples** - Only when necessary
- **1-2 code examples max** - No excessive examples
- **Details only when asked** - Wait for "tell me more" from user
- **Use bullet points** - Brief lists over long paragraphs
- **Remove unnecessary preambles** - Skip redundant connectors

### ツール使用の優先順位 / Tool Usage Priority

**推奨ツール（優先度: 高）:**

1. **Serena MCP** - プロジェクト全体の探索・シンボル検索
   - プロジェクトのアクティブ化
   - シンボルの検索と本体の読み取り
   - 関数本体の一括置換
   - ファイル一覧の取得

2. **Read** - 特定ファイルの内容を読み込む

3. **Grep** - コード内のパターン検索

4. **Glob** - ファイル名パターンでファイルを探す

**避けるべきツール:**
- PowerShellの`Get-Content` - 日本語(UTF-8)ファイルで文字化けが発生する

### コマンド実行環境 / Command Execution Environment

**PowerShellまたはcmdを優先的に使用すること**

Windows環境では、PowerShellまたはコマンドプロンプトを第一選択とする。

### ファイルエンコーディング / File Encoding

**PowerShellファイル (.ps1) は必ずUTF-8 BOMで保存すること**

- これにより、PowerShellスクリプトでの日本語文字化けを防止

**IMPORTANT: Always save PowerShell files (.ps1) with UTF-8 BOM encoding**

### Python仮想環境の管理 / Python Virtual Environment Management

**Pythonモジュールをインストールする前に、必ず仮想環境の存在を確認すること**

確認手順:
```powershell
# 仮想環境の存在確認
Test-Path .venv

# 存在しない場合は作成（ユーザー確認後）
python -m venv .venv

# 仮想環境の有効化（Windows）
.venv\Scripts\activate

# モジュールインストール
pip install <module_name>
```

**IMPORTANT: Always check for virtual environment before installing Python modules**

### Git操作 / Git Operations

**基本的なgitコマンドはすべて実行可能**

```bash
# 変更をステージング
git add .

# コミット
git commit -m "コミットメッセージ"

# 初回push（upstreamを設定）
git push --set-upstream origin main

# 2回目以降は通常のpush
git push
```

### バックアップ方針 / Backup Policy

**重要: ファイル編集時はgit commitを優先すること**

**基本方針:**
1. **git commit優先** - ファイル編集後は適切なタイミングでgit commitを実施
2. **ローカルバックアップは補助** - git管理されていないファイルや、git commit前の一時的な保護として使用

**git commitのタイミング:**
- 意味のある単位で変更をまとめてcommit
- 大きな機能追加や修正の前後
- 重要なファイルの編集後
- 作業セッションの区切りで

**コミットメッセージの例:**
```bash
git add <ファイル>
git commit -m "機能追加: h2z_kana_digit関数の実装"
git commit -m "リファクタリング: _mode_config.pyの分離"
git commit -m "修正: CSVエンコーディングの文字化け対応"
```

**ローカルバックアップ（補助的に使用）:**
- バックアップ対象: テキストベースのスクリプトファイル（`.py`, `.ps1`, `.txt`, `.ahk`, `.md`, `.json`, `.csv`等）
- バックアップタイミング: 大規模な変更前、または実験的なコード編集前
- バックアップ保存先: `backup/YYYY-MM-DD/`
- ファイル名形式: `元のファイル名_YYYYMMDD_HHMMSS.拡張子`

**IMPORTANT: Prioritize git commit over local file backup**

**Best practice:**
1. **Git commit first** - Commit changes at appropriate points
2. **Local backup as supplement** - Use for non-git files or temporary protection before commit

**When to commit:**
- After meaningful changes
- Before/after major features or fixes
- After editing important files
- At session boundaries

**Commit message examples:**
```bash
git commit -m "Add feature: implement h2z_kana_digit function"
git commit -m "Refactor: separate _mode_config.py module"
git commit -m "Fix: CSV encoding character corruption"
```

---

## 【CLAUDE.md / CLAUDE_GLOBAL.md との関係】

### ファイルの役割分担

**COPILOT_GLOBAL.md（このファイル）:**
- GitHub Copilot専用のグローバル設定
- Serena MCPの使い方
- VS Code + GitHub Copilot固有の設定

**CLAUDE_GLOBAL.md:**
- Claude Code専用のグローバル設定
- log.txt読み込みの重要性
- Bashツールのラップ方法
- uvx と Y:ドライブの詳細設定

**CLAUDE.md:**
- プロジェクト固有の設定（Claude Code用）
- ファイル作成場所のルール
- 応答スタイル

### 共通項目の扱い

以下の項目は、COPILOT_GLOBAL.mdとCLAUDE_GLOBAL.mdで共通:
- 言語設定（日本語）
- 応答スタイル（簡潔）
- ファイルエンコーディング（UTF-8 BOM for .ps1）
- Python仮想環境の管理
- Git操作
- バックアップ方針

ただし、**ツールの使い方は異なる**:
- GitHub Copilot: Serena MCPを`.vscode/mcp.json`で設定
- Claude Code: Serena MCPを`.mcp.json`（ルート）で設定

---

## 【参照ドキュメント】Reference Documents

**必ず以下のファイルも確認すること:**

1. **CLAUDE.md** - プロジェクト固有の設定（Claude Code用だがルールは共通）
2. **CLAUDE_GLOBAL.md** - Claude Code用グローバル設定（参考情報として有用）
3. **for_claude/log.txt** - 作業履歴・引継ぎ事項（Claude専用だが参考になる）
4. **.serena/memories/** - Serenaのプロジェクト知識ベース

---

## 【よく使うツール】Frequently Used Tools

ユーザーが日常的に使用するツールとテクノロジー:

- **Python** - スクリプト作成、自動化、データ処理
- **Excel VBA** - Excel自動化、マクロ開発
- **AutoHotkey v1** - Windows自動化、ホットキー管理
- **Excel Power Query** - データ取得、変換、統合
- **PowerShell** - Windowsシステム管理、自動化スクリプト
- **コマンドプロンプト (Command Prompt)** - バッチ処理、基本的なシステム操作
- **GitHub Copilot** - コード補完、エージェントモード
- **Serena MCP** - コードベース探索、リファクタリング支援

**User's frequently used tools and technologies**

---

## 【更新履歴】Update History

- 2025-01-07: COPILOT_GLOBAL.md作成、Serena MCP使用方法を記載
