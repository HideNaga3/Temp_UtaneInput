# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 重要 / Important

**このファイルを読み込む際は、必ず `CLAUDE_GLOBAL.md` も一緒に読み込んでください。**

`CLAUDE_GLOBAL.md` には、すべてのプロジェクトに共通するグローバル設定が記載されています。

**When reading this file, always read `CLAUDE_GLOBAL.md` together.**

`CLAUDE_GLOBAL.md` contains global settings that apply to all projects.

---

## セッション開始時の必須手順 / Mandatory Steps at Session Start

**セッション開始時は必ず以下の順番で実行すること（絶対厳守）:**

1. **C:\Users\永井秀和\Documents\AutoHotKey\CLAUDE_GLOBAL.md を Read ツールで読む**
   - すべてのプロジェクトに共通するグローバル設定
   - 言語設定、コマンド実行環境、バックアップ方針など

2. **for_claude/log.txt を Read ツールで読む（末尾200行程度）**
   - 前回セッションからの引継ぎ情報
   - 作業履歴と次回への申し送り事項
   - ファイルが大きい場合はoffset/limitパラメータで末尾を読む

3. **作業完了時は必ず for_claude/log.txt に Edit ツールで追記する**
   - 完了した作業内容
   - 次回セッションへの引継ぎ事項

これらを実行せずに作業を開始してはいけません。

**IMPORTANT: Always execute the following in order at session start (strictly mandatory):**

1. **Read C:\Users\永井秀和\Documents\AutoHotKey\CLAUDE_GLOBAL.md using Read tool**
   - Global settings common to all projects
   - Language settings, command execution environment, backup policy, etc.

2. **Read for_claude/log.txt using Read tool (last 200 lines approx.)**
   - Handover information from previous session
   - Work history and notes for next session
   - Use offset/limit parameters for large files

3. **Append to for_claude/log.txt using Edit tool when work is completed**
   - Completed work details
   - Handover notes for next session

Do not start work without executing these steps.

### グローバル設定パスの環境依存 / Global Settings Path Environment Dependency

**重要: グローバル設定フォルダのパスはPC環境によって異なります**

**パスパターン（環境依存）:**
- **パターン1**: `C:\AutoHotKey\claude\`
- **パターン2**: `C:\Users\永井秀和\Documents\AutoHotKey\claude\`

**セッション開始時の確認:**
セッション開始時、グローバル設定を読む前に以下のコマンドでパスの存在を確認すること:

```powershell
# パターン1を確認
powershell -Command "Test-Path 'C:\AutoHotKey\claude\CLAUDE_GLOBAL.md'"

# パターン2を確認
powershell -Command "Test-Path 'C:\Users\永井秀和\Documents\AutoHotKey\claude\CLAUDE_GLOBAL.md'"
```

**存在する方のパスを使用すること**。両方 `False` の場合は、ユーザーに確認すること。

**IMPORTANT: Global settings folder path varies by PC environment**

**Path patterns (environment dependent):**
- **Pattern 1**: `C:\AutoHotKey\claude\`
- **Pattern 2**: `C:\Users\永井秀和\Documents\AutoHotKey\claude\`

**Session start verification:**
Before reading global settings at session start, verify path existence with:

```powershell
# Check Pattern 1
powershell -Command "Test-Path 'C:\AutoHotKey\claude\CLAUDE_GLOBAL.md'"

# Check Pattern 2
powershell -Command "Test-Path 'C:\Users\永井秀和\Documents\AutoHotKey\claude\CLAUDE_GLOBAL.md'"
```

**Use the path that exists**. If both return `False`, confirm with the user.

---

## 【プロジェクト設定】Project Settings

このセクションには、このプロジェクト固有の設定を記載します。

### 概要

このドキュメントは、Claude Code がこのプロジェクトで作業する際のガイドラインを提供します。

### プロジェクト固有のルール

#### ファイル作成場所のルール / File Creation Location Rules

**重要: 一時ファイル・テストファイル・検証ファイルを作成する場所を厳守すること**

Claudeが作業中に一時的なファイルを作成する際は、必ず以下のルールに従うこと:

**作成して良い場所:**
- `temp/` フォルダ - 一時ファイル、作業用ファイル
- `for_claude/` フォルダ - Claude専用作業領域、セッション間で保持するファイル

**絶対に作成してはいけない場所:**
- `_lib/` フォルダ - exeに組み込まれる実際のプログラムモジュール
- その他の実際のプログラムフォルダ - ユーザーがGitで管理している領域

**理由:**
- `_lib/` などのプログラムフォルダはexe化の対象であり、不要なファイルを含めてはいけない
- ユーザーがGitで管理しているフォルダに勝手にファイルを追加すると、バージョン管理が煩雑になる
- テストファイルや一時ファイルは開発用フォルダで管理するべき

**具体例:**

OK:
- `temp/test_create_data_list.py` - テストファイル
- `for_claude/verify_refactoring.py` - 検証スクリプト
- `temp/temp_data.json` - 一時データ

NG:
- `_lib/test_xxx.py` - プログラムフォルダにテストファイル
- `_lib/temp_xxx.py` - プログラムフォルダに一時ファイル
- `_lib/original_xxx.py` - プログラムフォルダにバックアップファイル

**本番ファイルの編集について:**
ユーザーが明示的に指示した本番ファイル（例: `_lib/_create_data_list.py`）の編集は問題ありません。
新規ファイル作成時のみ、このルールを厳守すること。

**IMPORTANT: Strictly follow file creation location rules for temporary/test/verification files**

When Claude creates temporary files during work, always follow these rules:

**Allowed locations:**
- `temp/` folder - Temporary files, working files
- `for_claude/` folder - Claude's dedicated workspace, files to keep between sessions

**Forbidden locations:**
- `_lib/` folder - Actual program modules to be embedded in exe
- Other actual program folders - User-managed Git areas

**Reason:**
- Program folders like `_lib/` are targets for exe compilation and should not contain unnecessary files
- Adding files arbitrarily to Git-managed folders complicates version control
- Test files and temporary files should be managed in development folders

**Examples:**

OK:
- `temp/test_create_data_list.py` - Test file
- `for_claude/verify_refactoring.py` - Verification script
- `temp/temp_data.json` - Temporary data

NG:
- `_lib/test_xxx.py` - Test file in program folder
- `_lib/temp_xxx.py` - Temporary file in program folder
- `_lib/original_xxx.py` - Backup file in program folder

**About editing production files:**
Editing production files explicitly instructed by the user (e.g., `_lib/_create_data_list.py`) is acceptable.
Only when creating new files, strictly follow this rule.


#### ツール使用の優先順位 / Tool Usage Priority

**重要: ファイル読み込み・検索時は専用ツールを優先すること**

Claudeがファイルを読み込んだり、コードを検索したりする際は、以下の優先順位でツールを使用すること:

**推奨ツール (優先度: 高):**
1. **Serena MCP** - プロジェクト全体の探索・シンボル検索に最適
   - プロジェクトのアクティブ化
   - シンボルの検索と本体の読み取り
   - 関数本体の一括置換
   - ファイル一覧の取得

2. **Read** - 特定ファイルの内容を読み込む
   - ファイルパスが明確な場合に使用
   - UTF-8エンコーディングで正しく読み込める

3. **Grep** - コード内のパターン検索
   - キーワード検索
   - 正規表現検索

4. **Glob** - ファイル名パターンでファイルを探す
   - ワイルドカードでファイル検索

**避けるべきツール (優先度: 低):**
- **PowerShellのGet-Content** - 日本語の文字化けが発生する
- **Bashのcat/grep** - Windows環境では非推奨

**理由:**
- PowerShellのGet-Contentは日本語(UTF-8)ファイルで文字化けが発生する
- Serenaは大規模プロジェクトの探索に最適化されている
- 専用ツールの方が高速で信頼性が高い

**具体例:**

OK (推奨):
```python
# Serenaでシンボル検索
mcp__serena__find_symbol("create_frame_list")

# Readでファイル読み込み
Read("_lib/_create_data_list.py")

# Grepでパターン検索
Grep(pattern="def create_", path="_lib/")
```

NG (非推奨):
```bash
# PowerShellで日本語ファイルを読み込み (文字化けする)
powershell -Command "Get-Content 'for_claude\log.txt'"

# Bashでファイル検索 (Windows環境では非推奨)
cat _lib/_create_data_list.py | grep "def create_"
```

**IMPORTANT: Prioritize specialized tools when reading files or searching code**

When Claude reads files or searches code, use tools in the following priority order:

**Recommended Tools (High Priority):**
1. **Serena MCP** - Ideal for project-wide exploration and symbol search
   - Activate project
   - Search symbols and read their bodies
   - Batch replace function bodies
   - Get file listings

2. **Read** - Read specific file contents
   - Use when file path is clear
   - Correctly reads UTF-8 encoding

3. **Grep** - Search for patterns in code
   - Keyword search
   - Regular expression search

4. **Glob** - Find files by filename patterns
   - Wildcard file search

**Tools to Avoid (Low Priority):**
- **PowerShell Get-Content** - Causes Japanese character corruption
- **Bash cat/grep** - Not recommended in Windows environment

**Reason:**
- PowerShell Get-Content corrupts Japanese (UTF-8) files
- Serena is optimized for large project exploration
- Specialized tools are faster and more reliable

**Examples:**

OK (Recommended):
```python
# Search symbols with Serena
mcp__serena__find_symbol("create_frame_list")

# Read file with Read tool
Read("_lib/_create_data_list.py")

# Search patterns with Grep
Grep(pattern="def create_", path="_lib/")
```

NG (Not Recommended):
```bash
# Read Japanese file with PowerShell (causes corruption)
powershell -Command "Get-Content 'for_claude\log.txt'"

# Search files with Bash (not recommended in Windows)
cat _lib/_create_data_list.py | grep "def create_"
```


#### 応答スタイル / Response Style

**重要: 簡潔で要点を押さえた応答を心がけること**

Claudeが応答する際は、以下のスタイルを守ること:

**基本方針:**
- 説明は要点のみ、簡潔に
- 長い表や例は最小限（必要な場合のみ）
- コード例は1-2個程度
- 詳細な説明は明示的に求められた場合のみ

**具体例:**

NG (冗長):
```
はい、安全なのは各メソッド（def）ごとにimportする方法です。

## メソッドごとのimportが安全な理由

### 1. スコープが明確
長い説明...
### 2. 名前の衝突を防ぐ
長い説明...
（さらに続く）
```

OK (簡潔):
```
メソッド内importが最も安全:
- スコープ限定、名前衝突なし
- Pythonはキャッシュするので速度低下なし
- 例: `def method(): import json`

通常は「ファイル先頭import」が慣習（PEP8）。
```

**IMPORTANT: Keep responses concise and focused**

When responding, Claude should follow these style guidelines:

**Basic Policy:**
- Explanations should be brief, key points only
- Minimize long tables or examples (only when necessary)
- Limit code examples to 1-2
- Detailed explanations only when explicitly requested

**Examples:**

NG (Verbose):
```
Yes, the safest approach is to import in each method (def).

## Why method-level imports are safe

### 1. Clear scope
Long explanation...
### 2. Prevents name collisions
Long explanation...
(continues...)
```

OK (Concise):
```
Method-level imports are safest:
- Limited scope, no name collisions
- Python caches, so no speed penalty
- Example: `def method(): import json`

Standard practice is "top-of-file imports" (PEP8).
```
