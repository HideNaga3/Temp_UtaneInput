# CLAUDE_GLOBAL.md

This file provides global guidance to Claude Code (claude.ai/code) for all projects.

---

## ⚠️【最重要】セッション開始時の必須確認事項

**セッション開始時は必ず `for_claude/log.txt` を最初に読むこと**

- **絶対に忘れてはいけません**
- log.txtには全ての作業履歴が記録されています
- 「引継ぎ」「前回の作業」「続きから」と言われた場合は特に必須
- log.txtを読まずに作業を開始すると、前回の作業内容を忘れてしまいます

**⚠️ WARNING: Always read `for_claude/log.txt` at the start of EVERY session**

- **Never forget this step**
- log.txt contains all work history
- Essential when user mentions "handover", "continue", or "previous work"
- Starting work without reading log.txt will cause loss of context

---

## 【グローバル設定】Global Settings

このセクションの設定は**すべてのプロジェクト**に適用されます。

### 言語設定 / Language Settings

**このプロジェクトでは必ず日本語で対応してください。**

- すべての説明を日本語で行うこと
- すべての質問を日本語で行うこと
- すべてのコメントを日本語で記述すること
- エラーメッセージの説明も日本語で行うこと
- コード内のコメントも日本語で記述すること

**IMPORTANT: Always communicate in Japanese for this project.**
- All explanations must be in Japanese
- All questions must be in Japanese
- All comments must be in Japanese
- All error message explanations must be in Japanese
- All code comments must be in Japanese

### プロジェクト設定ファイル (CLAUDE.md) の使用方法 / How to Use Project Settings File (CLAUDE.md)

**CLAUDE.mdはプロジェクト固有の設定ファイルで、自由に編集・追記可能です。**

- **CLAUDE.mdの目的**: プロジェクト固有の情報を記録し、セッション間で引き継ぐ
- **記載すべき内容**:
  - プロジェクトの概要と目的
  - 重要な技術仕様（エンコーディング、データ形式、変換ルールなど）
  - プロジェクト固有のコーディング規約
  - ファイル構成とディレクトリ構造
  - 使用ライブラリとバージョン情報
  - セッション引継ぎに必要な注意事項
  - 進行中のタスクや次回セッションへの申し送り事項
  - よくあるエラーとその対処方法

**CLAUDE.md is a project-specific settings file that can be freely edited and updated.**

- **Purpose of CLAUDE.md**: Record project-specific information and maintain continuity between sessions
- **What to include**:
  - Project overview and objectives
  - Important technical specifications (encoding, data formats, conversion rules, etc.)
  - Project-specific coding conventions
  - File structure and directory organization
  - Libraries used and version information
  - Important notes for session handover
  - Ongoing tasks and notes for next session
  - Common errors and their solutions

**使用例 / Usage Example:**

プロジェクト開始時や重要な仕様が判明したときに、CLAUDE.mdに追記すること。
例えば：

```markdown
## プロジェクト概要
eStaffing勤怠データをStaffExpress形式に変換するツール

## 重要な技術仕様
- すべてのCSVファイルはCP932エンコーディング
- 入力: 1行が1人の半月分（最大16日分）
- 出力: 1行が1人の1日分（最大16行に展開）

## 進行状況
- Phase 1: CSV変換ロジック実装完了 ✓
- Phase 2: GUI実装（次回セッション）
```

**IMPORTANT: Always update CLAUDE.md when you discover important project information or specifications.**

### 作業スタイル / Working Style

- コードレビュー時は丁寧に説明すること
- エラーが発生した場合は、原因と解決策を明確に説明すること
- 変更前に既存のコードを必ず確認すること

### Git操作 / Git Operations

**ユーザーからgit pushをお願いされることがあります。**

- ユーザーから「push」または「git push」と依頼された場合、変更をGitにコミット＆プッシュすること
- Bashツールを使用してgitコマンドを実行可能
- 基本的なgitコマンド（add, commit, push）はすべて実行可能

**User may request git push operations.**

- When user requests "push" or "git push", commit and push changes to Git
- Git commands can be executed using Bash tool
- All basic git commands (add, commit, push) are available

**初回push時のトラブルシューティング / First-time Push Troubleshooting**

初めてpushする際にエラーが発生する場合は、以下の手順を参考にすること：

**ケース1: upstream branchが設定されていない**

```bash
# エラー例
fatal: The current branch main has no upstream branch.

# 解決方法
git push --set-upstream origin main
```

**ケース2: リモートリポジトリが未設定**

```bash
# リモートを確認
git remote -v

# リモートが未設定の場合
git remote add origin <リポジトリURL>

# 再度push
git push --set-upstream origin main
```

**ケース3: 認証エラー**

- SSH鍵の設定を確認
- Git Credential Managerの設定を確認
- HTTPSの場合は、Personal Access Tokenが必要な場合あり

**実践例（2025-10-23実施）:**

```bash
# 1. 変更をステージング
git add .

# 2. コミット
git commit -m "Add project files: scripts, vba_modules, for_claude documentation"

# 3. 初回push（upstreamを設定）
git push --set-upstream origin main

# 4. 2回目以降は通常のpush
git push
```

この実践例を参考に、初回push時の問題を解決すること。

**When pushing for the first time and encountering errors, refer to the following steps:**

**Case 1: Upstream branch not set**

```bash
# Error example
fatal: The current branch main has no upstream branch.

# Solution
git push --set-upstream origin main
```

**Case 2: Remote repository not configured**

```bash
# Check remote
git remote -v

# Add remote if not configured
git remote add origin <repository-URL>

# Push again
git push --set-upstream origin main
```

**Case 3: Authentication error**

- Check SSH key configuration
- Check Git Credential Manager settings
- For HTTPS, Personal Access Token may be required

**Practical example (executed 2025-10-23):**

```bash
# 1. Stage changes
git add .

# 2. Commit
git commit -m "Add project files: scripts, vba_modules, for_claude documentation"

# 3. First push (set upstream)
git push --set-upstream origin main

# 4. Subsequent pushes
git push
```

Refer to this practical example to resolve first-time push issues.

### 絵文字の使用禁止 / No Emoji Policy

**重要: 絵文字は絶対に使用しないこと**

- すべてのテキスト出力で絵文字を使用しない
- Pythonスクリプトの出力でも絵文字を使用しない
- マークダウンファイルでも絵文字を使用しない
  - **特に `global/` ディレクトリ内のドキュメントファイル（.md）は絵文字厳禁**
  - 既存のドキュメントに絵文字があった場合は削除すること
- コメントやログでも絵文字を使用しない
- チェックマークや記号が必要な場合は、テキスト表記を使用すること
  - OK: `[OK]`, `[SUCCESS]`, `[DONE]`, `チェック`, `完了`
  - NG: 絵文字全般

**IMPORTANT: Never use emojis**

- Do not use emojis in any text output
- Do not use emojis in Python script output
- Do not use emojis in markdown files
  - **Especially in documentation files (.md) within the `global/` directory - emojis are strictly prohibited**
  - If emojis are found in existing documents, remove them
- Do not use emojis in comments or logs
- Use text representations when checkmarks or symbols are needed
  - OK: `[OK]`, `[SUCCESS]`, `[DONE]`, `check`, `completed`
  - NG: All emojis

**理由 / Reason:**
- Windows環境のコマンドプロンプトやPowerShellでは絵文字が正しく表示されない
- CP932エンコーディングでは絵文字がサポートされない
- 文字化けやエンコーディングエラーの原因となる

**Reason:**
- Emojis do not display correctly in Windows Command Prompt or PowerShell
- CP932 encoding does not support emojis
- Causes garbled text and encoding errors

### コマンド実行環境 / Command Execution Environment

**コマンドを使用する場合は PowerShell または コマンドプロンプト (cmd) を優先的に使用すること**

- Windows環境では、PowerShellまたはcmdを第一選択とすること
- Bash や他のシェルよりも、Windows標準のコマンド環境を優先すること
- スクリプト実行時も、PowerShellまたはバッチファイルを優先すること

**IMPORTANT: When using commands, prioritize PowerShell or Command Prompt (cmd)**

- In Windows environment, use PowerShell or cmd as the first choice
- Prioritize Windows native command environments over Bash or other shells
- When executing scripts, prefer PowerShell or batch files

**Bashツール使用時の重要な注意事項 / Important Notes for Bash Tool Usage**

Claude Codeには「Bash」ツールしかありませんが、必ずPowerShellコマンドをラップして実行すること。

**正しい使用例:**
```bash
# ファイル一覧
powershell -Command "Get-ChildItem"

# ファイル移動・リネーム
powershell -Command "Move-Item -Path 'old.txt' -Destination 'new.txt'"
powershell -Command "Rename-Item -Path 'temp_folder' -NewName 'new_folder'"

# ファイル削除
powershell -Command "Remove-Item 'file.txt'"

# ディレクトリ作成
powershell -Command "New-Item -ItemType Directory -Path 'newfolder'"

# ファイルコピー
powershell -Command "Copy-Item -Path 'source.txt' -Destination 'dest.txt'"
```

**避けるべき使用例:**
```bash
# ❌ 直接Bashコマンドを使わない
ls
dir
mv old.txt new.txt
rm file.txt
```

**Although Claude Code only has a "Bash" tool, always wrap PowerShell commands inside it.**

**Correct usage examples:**
```bash
# List files
powershell -Command "Get-ChildItem"

# Move/Rename files
powershell -Command "Move-Item -Path 'old.txt' -Destination 'new.txt'"
powershell -Command "Rename-Item -Path 'temp_folder' -NewName 'new_folder'"

# Delete files
powershell -Command "Remove-Item 'file.txt'"

# Create directory
powershell -Command "New-Item -ItemType Directory -Path 'newfolder'"

# Copy files
powershell -Command "Copy-Item -Path 'source.txt' -Destination 'dest.txt'"
```

**Examples to avoid:**
```bash
# ❌ Don't use direct Bash commands
ls
dir
mv old.txt new.txt
rm file.txt
```

### ファイルエンコーディング / File Encoding

**PowerShellファイル (.ps1) は必ずUTF-8 BOMで保存すること**

- `.ps1`ファイルを作成・編集する際は、UTF-8 BOM (Byte Order Mark) エンコーディングを使用すること
- これにより、PowerShellスクリプトでの日本語文字化けを防止できます

**IMPORTANT: Always save PowerShell files (.ps1) with UTF-8 BOM encoding**
- When creating or editing `.ps1` files, use UTF-8 BOM (Byte Order Mark) encoding
- This prevents Japanese character corruption in PowerShell scripts

### Python仮想環境の管理 / Python Virtual Environment Management

**Pythonモジュールをインストールする前に、必ず仮想環境の存在を確認すること**

- Pythonプロジェクトでは、必ず仮想環境 (.venv) を使用すること
- モジュールインストール前に以下を確認:
  1. `.venv` フォルダが存在するか確認
  2. 存在しない場合は、ユーザーに確認してから作成
  3. 仮想環境を有効化してからインストール
- グローバル環境へのインストールは避けること（システム汚染を防ぐため）

**IMPORTANT: Always check for virtual environment before installing Python modules**

- Always use virtual environment (.venv) for Python projects
- Before installing modules, check:
  1. Check if `.venv` folder exists
  2. If not exists, confirm with user before creating
  3. Activate virtual environment before installation
- Avoid installing to global environment (to prevent system pollution)

**仮想環境の確認と作成手順:**

```powershell
# 仮想環境の存在確認
Test-Path .venv

# 存在しない場合は作成 (ユーザー確認後)
python -m venv .venv

# 仮想環境の有効化 (Windows)
.venv\Scripts\activate

# モジュールインストール
pip install <module_name>
```

**Virtual environment check and creation:**

```powershell
# Check if virtual environment exists
Test-Path .venv

# Create if not exists (after user confirmation)
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install modules
pip install <module_name>
```

**Claude Codeでの実践的なコマンド実行方法 / Practical Command Execution in Claude Code**

Claude CodeのBashツールから仮想環境を使用する際は、以下の方法を使用すること:

```powershell
# ❌ 誤った方法（Bashコマンドとして直接実行）
.venv\Scripts\python.exe -m pip install pandas

# ✅ 正しい方法（PowerShell経由で実行）
powershell -Command ".venv\Scripts\python.exe -m pip install pandas"
```

**重要なポイント:**
- Claude CodeのBashツールはUnixシェル互換のため、Windows固有のパスが正しく解釈されない
- 必ず `powershell -Command` でラップすること
- 複数のモジュールを同時にインストールする場合は、スペース区切りで指定可能

**よく使うコマンド集:**

```powershell
# pipのアップグレード
powershell -Command ".venv\Scripts\python.exe -m pip install --upgrade pip"

# 複数モジュールの一括インストール
powershell -Command ".venv\Scripts\python.exe -m pip install pandas openpyxl oletools"

# インストール済みモジュールの確認
powershell -Command ".venv\Scripts\python.exe -m pip list"

# 特定モジュールのバージョン確認
powershell -Command ".venv\Scripts\python.exe -m pip show pandas"

# requirements.txtからインストール
powershell -Command ".venv\Scripts\python.exe -m pip install -r requirements.txt"

# Pythonスクリプトの実行
powershell -Command ".venv\Scripts\python.exe scripts/your_script.py"
```

**When using virtual environment from Claude Code's Bash tool:**

```powershell
# ❌ Wrong (direct execution as Bash command)
.venv\Scripts\python.exe -m pip install pandas

# ✅ Correct (wrap with PowerShell)
powershell -Command ".venv\Scripts\python.exe -m pip install pandas"
```

**Important points:**
- Claude Code's Bash tool is Unix shell compatible, so Windows-specific paths are not interpreted correctly
- Always wrap with `powershell -Command`
- For installing multiple modules, separate with spaces

**Frequently used commands:**

```powershell
# Upgrade pip
powershell -Command ".venv\Scripts\python.exe -m pip install --upgrade pip"

# Install multiple modules at once
powershell -Command ".venv\Scripts\python.exe -m pip install pandas openpyxl oletools"

# List installed modules
powershell -Command ".venv\Scripts\python.exe -m pip list"

# Check specific module version
powershell -Command ".venv\Scripts\python.exe -m pip show pandas"

# Install from requirements.txt
powershell -Command ".venv\Scripts\python.exe -m pip install -r requirements.txt"

# Execute Python script
powershell -Command ".venv\Scripts\python.exe scripts/your_script.py"
```

### uvx と Y:ドライブの設定 / uvx and Y: Drive Configuration

**重要: uvxは必ずY:ドライブのものを使用すること**

このプロジェクトでは、uvxコマンドは以下のパスを使用します:
- **uvxパス**: `Y:\.local\bin\uvx.exe`
- **Y:ドライブ**: C:\Users\永井秀和 へのsubst仮想ドライブ

**IMPORTANT: Always use uvx from Y: drive**

This project uses uvx command from the following path:
- **uvx path**: `Y:\.local\bin\uvx.exe`
- **Y: drive**: subst virtual drive to C:\Users\永井秀和

**Y:ドライブの存在確認 / Check Y: Drive Existence**

セッション開始時、または.mcp.json設定時に以下のコマンドでY:ドライブの存在を確認すること:

```powershell
# Y:ドライブの存在確認
powershell -Command "Test-Path 'Y:\'"

# uvx.exeの存在確認
powershell -Command "Test-Path 'Y:\.local\bin\uvx.exe'"
```

At the start of a session or when configuring .mcp.json, check Y: drive existence with the following commands:

```powershell
# Check if Y: drive exists
powershell -Command "Test-Path 'Y:\'"

# Check if uvx.exe exists
powershell -Command "Test-Path 'Y:\.local\bin\uvx.exe'"
```

**Y:ドライブが存在しない場合の対処 / If Y: Drive Does Not Exist**

Y:ドライブが存在しない場合（Test-Pathの結果がFalse）は、ユーザーにsubstコマンドの実行を提案すること:

```powershell
# Y:ドライブを作成（管理者権限不要）
subst Y: C:\Users\永井秀和
```

このコマンドを実行すると、C:\Users\永井秀和がY:ドライブとしてアクセス可能になります。

**注意事項:**
- substは再起動後に消える（永続化するにはレジストリ編集またはスタートアップスクリプトが必要）
- ユーザーに実行方法を提案し、ユーザー自身に実行してもらうこと
- 実行後、再度Test-Pathで確認すること

If Y: drive does not exist (Test-Path returns False), suggest the user to run the subst command:

```powershell
# Create Y: drive (no admin rights required)
subst Y: C:\Users\永井秀和
```

After running this command, C:\Users\永井秀和 will be accessible as Y: drive.

**Notes:**
- subst mapping disappears after restart (requires registry edit or startup script for persistence)
- Suggest the execution method to the user and let the user execute it
- After execution, verify again with Test-Path

**Y:ドライブが利用できない場合の代替手段 / Alternative When Y: Drive Is Not Available**

何らかの理由でY:ドライブが利用できない場合は、Cドライブの直接パスを使用すること:

```json
{
  "command": "C:/Users/永井秀和/.local/bin/uvx.exe"
}
```

ただし、通常は**Y:ドライブの使用を優先**すること。

If Y: drive is not available for any reason, use the direct C: drive path:

```json
{
  "command": "C:/Users/永井秀和/.local/bin/uvx.exe"
}
```

However, normally **prioritize using Y: drive**.

**Serena MCPサーバーのブラウザー自動起動について / About Serena MCP Browser Auto-launch**

SerenaはデフォルトでWebダッシュボードをブラウザーで自動起動します。
Claude起動時に毎回ブラウザーが開くのを防ぐには、.mcp.jsonに以下の設定を追加すること:

```json
{
  "mcpServers": {
    "serena": {
      "command": "Y:/.local/bin/uvx.exe",
      "args": [
        "--from",
        "git+https://github.com/oraios/serena",
        "serena",
        "start-mcp-server",
        "--enable-web-dashboard",
        "false"
      ]
    }
  }
}
```

**重要ポイント:**
- `--enable-web-dashboard false` を追加してブラウザー自動起動を無効化
- デバッグ時のみダッシュボードが必要な場合は `true` に変更
- 詳細は `global/uvx_serena_setup.md` を参照

By default, Serena automatically launches a web dashboard in the browser.
To prevent the browser from opening every time Claude starts, add the following configuration to .mcp.json:

**Important points:**
- Add `--enable-web-dashboard false` to disable browser auto-launch
- Change to `true` only when dashboard is needed for debugging
- Refer to `global/uvx_serena_setup.md` for details

**Serena MCPプロジェクトセットアップの簡略化 / Simplified Serena MCP Project Setup**

**初回セットアップ（プロジェクトごとに1回のみ）/ First-time Setup (Once per project)**

新しいプロジェクトでSerena MCPを使用する場合の手順:

```bash
# 手順1: .mcp.jsonの作成（プロジェクトルートに）
# 上記の.mcp.json設定を参考に作成

# 手順2: project.ymlの生成
cd "プロジェクトパス"
Y:/.local/bin/uvx.exe --from git+https://github.com/oraios/serena serena project generate-yml --language python .

# 手順3: プロジェクトのインデックス化（初回のみ必須）
Y:/.local/bin/uvx.exe --from git+https://github.com/oraios/serena serena project index

# 手順4（オプション）: ヘルスチェック
Y:/.local/bin/uvx.exe --from git+https://github.com/oraios/serena serena project health-check
```

**重要: 2回目以降は何もする必要なし**

一度セットアップが完了すれば：
- Claude Code起動時にSerena MCPサーバーが自動起動
- インデックスキャッシュが自動的に使用される
- プロジェクト設定は`.serena/project.yml`に保存される
- MCPツール（`mcp__serena__*`）が自動的に利用可能になる

**再インデックスが必要な場合:**
- 大量のファイルを追加・削除した場合
- シンボル検索が古い情報を返す場合

```bash
Y:/.local/bin/uvx.exe --from git+https://github.com/oraios/serena serena project index
```

**トラブルシューティング:**

MCPツールが使えない場合:
1. `.mcp.json`が正しく設定されているか確認
2. Y:ドライブが存在するか確認（`Test-Path Y:\`）
3. Claude Codeを再起動
4. プロジェクトを再インデックス

**When using Serena MCP in a new project:**

```bash
# Step 1: Create .mcp.json (in project root)
# Refer to the .mcp.json configuration above

# Step 2: Generate project.yml
cd "project_path"
Y:/.local/bin/uvx.exe --from git+https://github.com/oraios/serena serena project generate-yml --language python .

# Step 3: Index project (required only first time)
Y:/.local/bin/uvx.exe --from git+https://github.com/oraios/serena serena project index

# Step 4 (Optional): Health check
Y:/.local/bin/uvx.exe --from git+https://github.com/oraios/serena serena project health-check
```

**IMPORTANT: After initial setup, no further action needed**

Once setup is complete:
- Serena MCP server auto-starts when Claude Code launches
- Index cache is automatically used
- Project settings are saved in `.serena/project.yml`
- MCP tools (`mcp__serena__*`) become automatically available

**Re-indexing required when:**
- Many files added/deleted
- Symbol search returns outdated information

```bash
Y:/.local/bin/uvx.exe --from git+https://github.com/oraios/serena serena project index
```

**Troubleshooting:**

If MCP tools are not available:
1. Verify `.mcp.json` is correctly configured
2. Check Y: drive exists (`Test-Path Y:\`)
3. Restart Claude Code
4. Re-index project

### よく使うツール / Frequently Used Tools

ユーザーが日常的に使用するツールとテクノロジー:

- **Python** - スクリプト作成、自動化、データ処理
- **Excel VBA** - Excel自動化、マクロ開発
- **AutoHotkey v1** - Windows自動化、ホットキー管理
- **Excel Power Query** - データ取得、変換、統合
- **PowerShell** - Windowsシステム管理、自動化スクリプト
- **コマンドプロンプト (Command Prompt)** - バッチ処理、基本的なシステム操作

**User's frequently used tools and technologies:**

- **Python** - Scripting, automation, data processing
- **Excel VBA** - Excel automation, macro development
- **AutoHotkey v1** - Windows automation, hotkey management
- **Excel Power Query** - Data retrieval, transformation, integration
- **PowerShell** - Windows system administration, automation scripts
- **Command Prompt** - Batch processing, basic system operations

### バックアップ方針 / Backup Policy

**ファイル編集時は必ず変更前バックアップを作成すること**

- ファイルを編集する前に、自動バックアップを作成すること
- **バックアップ対象**: テキストベースのスクリプトファイルのみ
  - 対象拡張子: `.py`, `.ps1`, `.txt`, `.ahk`, `.vbs`, `.bat`, `.cmd`, `.md`, `.json`, `.xml`, `.csv`, `.ini`, `.config`など
  - バイナリファイル（`.exe`, `.dll`, `.pdf`, `.xlsx`など）は除外
- バックアップの頻度: **約10分間隔**（同じファイルの編集が続く場合）
- バックアップファイル名形式: `元のファイル名_YYYYMMDD_HHMMSS.拡張子`
  - 例: `script.ps1` → `script_20250118_143022.ps1`
- バックアップ保存先: `backup/YYYY-MM-DD/` 形式の日付別フォルダ
  - 例: `backup/2025-01-18/script_20250118_143022.ps1`
- フォルダが存在しない場合は自動的に作成すること
- **古いバックアップの自動削除**: 3日前より古いバックアップフォルダは自動的に削除すること

**IMPORTANT: Always create backup before editing files**

- Create automatic backup before editing files
- **Backup targets**: Text-based script files only
  - Target extensions: `.py`, `.ps1`, `.txt`, `.ahk`, `.vbs`, `.bat`, `.cmd`, `.md`, `.json`, `.xml`, `.csv`, `.ini`, `.config`, etc.
  - Exclude binary files (`.exe`, `.dll`, `.pdf`, `.xlsx`, etc.)
- Backup frequency: **Approximately every 10 minutes** (when editing the same file continuously)
- Backup filename format: `original_filename_YYYYMMDD_HHMMSS.extension`
  - Example: `script.ps1` → `script_20250118_143022.ps1`
- Backup location: Date-based folders in `backup/YYYY-MM-DD/` format
  - Example: `backup/2025-01-18/script_20250118_143022.ps1`
- Automatically create folders if they don't exist
- **Automatic cleanup**: Delete backup folders older than 3 days

### API処理結果の厳重な保存 / Strict Saving of API Processing Results

**重要: API料金が発生する処理（翻訳API、LLM API等）の結果は即座にGitコミットすること**

**【インシデント記録 2025-10-31】API翻訳結果の上書き損失**

**発生した問題:**
- Google Translation API v2で502単語×39言語（19,578翻訳、約$1.41）を実行
- 翻訳を3バッチに分けて実行（1-5言語、6-15言語、16-39言語）
- 各バッチスクリプトが元のCSVを読み込んで上書き保存する設計だった
- 結果: 最後のバッチ（16-39言語）のみ保存され、前の2バッチ（1-15言語、7,028翻訳、約$0.49）が消失
- Gitコミット未実施のため、バックアップなし
- **総損失: 約$0.49 + 再翻訳費用$0.49 = 約$1.00（約140円）**

**根本原因:**
1. 各バッチスクリプトが元のCSV（dict-template_20251029.csv）を読み込んでいた
2. 既存の翻訳結果ファイルを読み込んで追記する設計になっていなかった
3. 各バッチ実行後にGitコミットしていなかった

**必須対策（API料金発生処理の鉄則）:**

1. **各バッチ実行後に即座にGitコミット**
   ```bash
   git add <結果ファイル>
   git commit -m "API処理完了: <処理内容の説明>"
   ```

2. **または、各バッチを別ファイルに保存して最後に統合**
   ```python
   # 良い設計例
   OUTPUT_BATCH1 = 'result_batch1_langs1-5.csv'
   OUTPUT_BATCH2 = 'result_batch2_langs6-15.csv'
   OUTPUT_BATCH3 = 'result_batch3_langs16-39.csv'
   # 最後に統合
   ```

3. **または、既存ファイルを読み込んで追記する設計**
   ```python
   # 間違った設計
   df = pd.read_csv('元のCSV.csv')  # 毎回元を読む

   # 正しい設計
   if os.path.exists(OUTPUT_PATH):
       df = pd.read_csv(OUTPUT_PATH)  # 既存結果を読む
   else:
       df = pd.read_csv('元のCSV.csv')
   ```

4. **処理完了後、ユーザーに確認を促す**
   - 「API処理が完了しました。結果を確認してからGitコミットします。」
   - 結果確認後、即座にコミット

**API処理時のチェックリスト:**
- [ ] 既存の処理結果ファイルを上書きしない設計か？
- [ ] 各バッチ実行後にGitコミットするか？
- [ ] 処理結果を複数ファイルに分けて保存するか？
- [ ] API料金が発生することをユーザーに事前通知したか？
- [ ] 処理完了後、結果ファイルの存在を確認したか？

**IMPORTANT: Immediately commit to Git when API-charged processing (Translation API, LLM API, etc.) is completed**

**[Incident Record 2025-10-31] Loss of API Translation Results Due to Overwriting**

**Problem that occurred:**
- Executed Google Translation API v2 for 502 words × 39 languages (19,578 translations, approx. $1.41)
- Translation divided into 3 batches (languages 1-5, 6-15, 16-39)
- Each batch script was designed to read the original CSV and overwrite
- Result: Only the last batch (languages 16-39) was saved, previous 2 batches (languages 1-15, 7,028 translations, approx. $0.49) were lost
- No Git commit, no backup
- **Total loss: approx. $0.49 + re-translation cost $0.49 = approx. $1.00 (about 140 yen)**

**Root causes:**
1. Each batch script read the original CSV (dict-template_20251029.csv)
2. Not designed to read existing translation results and append
3. Did not commit to Git after each batch execution

**Mandatory countermeasures (Iron rules for API-charged processing):**

1. **Immediately commit to Git after each batch execution**
   ```bash
   git add <result_file>
   git commit -m "API processing completed: <description>"
   ```

2. **Or save each batch to separate files and merge at the end**
   ```python
   # Good design example
   OUTPUT_BATCH1 = 'result_batch1_langs1-5.csv'
   OUTPUT_BATCH2 = 'result_batch2_langs6-15.csv'
   OUTPUT_BATCH3 = 'result_batch3_langs16-39.csv'
   # Merge at the end
   ```

3. **Or design to read existing file and append**
   ```python
   # Wrong design
   df = pd.read_csv('original.csv')  # Read original every time

   # Correct design
   if os.path.exists(OUTPUT_PATH):
       df = pd.read_csv(OUTPUT_PATH)  # Read existing results
   else:
       df = pd.read_csv('original.csv')
   ```

4. **Prompt user confirmation after processing**
   - "API processing completed. Will commit to Git after verification."
   - Commit immediately after verification

**Checklist for API processing:**
- [ ] Design does not overwrite existing processing results?
- [ ] Commit to Git after each batch execution?
- [ ] Save processing results to multiple files?
- [ ] Notified user in advance about API charges?
- [ ] Verified result file existence after completion?

### 作業ログ / Work Log

**前回のセッションからの引継ぎ情報は `for_claude\log.txt` を必ず確認すること**

- セッション開始時は最初に `for_claude\log.txt` を読み込むこと
- このファイルには前回の作業内容、実装した機能、次回への引継ぎ事項が記録されています
- **作業中は定期的に `for_claude\log.txt` に進捗を追記すること（途中で中断しても大丈夫なように）**
  - 重要な作業を完了したタイミングで追記
  - 大きなタスクの途中でも、キリの良いところで追記
  - セッション中断に備えて、こまめに記録を残す
- 作業完了時は必ず `for_claude\log.txt` に作業内容を追記すること

**IMPORTANT: Always check `for_claude\log.txt` for session continuity**

- Read `for_claude\log.txt` at the beginning of each session
- This file contains previous work, implemented features, and handover notes
- **Write progress to `for_claude\log.txt` regularly during work (to ensure continuity if interrupted)**
  - Write after completing important tasks
  - Write at good breakpoints even in the middle of large tasks
  - Record frequently to prepare for session interruptions
- Append work progress to `for_claude\log.txt` when finishing tasks

**log.txtの分割 / Splitting log.txt**

**log.txtが大きくなりすぎた場合（約2,500行以上）は、複数ファイルに分割すること**

- 目的: ファイルサイズを管理しやすくし、セッション開始時の読み込みを高速化
- 分割タイミング: log.txtが約2,500行を超えた場合
- 保存場所: `for_claude/archive/` フォルダ

**命名規則:**
- 古いセッション: `sessions_XX-XX_log.txt`
  - 例: `sessions_01-05_log.txt` (セッション1-5の記録)
  - 例: `sessions_06-10_log.txt` (セッション6-10の記録)
- 完全バックアップ: `log_full_backup.txt` (分割前の元ファイル)
- 最新ログ: `log.txt` (現在のセッションから継続)

**分割手順:**
1. 分割用Pythonスクリプトを作成（行番号で分割）
2. アーカイブフォルダに古いセッションログを保存
3. 元のlog.txtを `log_full_backup.txt` としてアーカイブに保存
4. 最新セッション以降のみを新しい `log.txt` として保存
5. 分割スクリプトをアーカイブに移動

**分割例:**
```
元のlog.txt (2,672行)
  ↓ 分割
- archive/sessions_01-05_log.txt (605行)  ← セッション1-5
- archive/sessions_06-10_log.txt (1,109行) ← セッション6-10
- log.txt (958行)                          ← セッション11以降（最新）
- archive/log_full_backup.txt (2,672行)   ← 完全バックアップ
```

**IMPORTANT: Split log.txt when it becomes too large (approximately 2,500 lines or more)**

- Purpose: Manage file size and speed up session initialization
- Split timing: When log.txt exceeds approximately 2,500 lines
- Storage location: `for_claude/archive/` folder

**Naming convention:**
- Old sessions: `sessions_XX-XX_log.txt`
  - Example: `sessions_01-05_log.txt` (records from sessions 1-5)
  - Example: `sessions_06-10_log.txt` (records from sessions 6-10)
- Full backup: `log_full_backup.txt` (original file before split)
- Current log: `log.txt` (continues from current session)

**Split procedure:**
1. Create Python script for splitting (split by line numbers)
2. Save old session logs to archive folder
3. Save original log.txt as `log_full_backup.txt` in archive
4. Save only recent sessions onwards as new `log.txt`
5. Move split script to archive

**Split example:**
```
Original log.txt (2,672 lines)
  ↓ Split into
- archive/sessions_01-05_log.txt (605 lines)  ← Sessions 1-5
- archive/sessions_06-10_log.txt (1,109 lines) ← Sessions 6-10
- log.txt (958 lines)                          ← Session 11+ (current)
- archive/log_full_backup.txt (2,672 lines)   ← Full backup
```

### 一時ファイル作成ルール / Temporary File Creation Rules

**重要: 一時ファイル・テストファイルは必ず適切なフォルダに作成すること**

**原則:**
- 一時ファイルやテストファイルは `temp/` または `for_claude/` に作成
- 実際のプログラムフォルダ（`_lib/`等）には作成しない
- ユーザーがGitで管理しているフォルダを汚染しない

**詳細はプロジェクト固有のCLAUDE.mdを参照すること**
各プロジェクトのCLAUDE.mdに、そのプロジェクト固有のファイル作成ルールが記載されています。

**IMPORTANT: Always create temporary/test files in appropriate folders**

**Principle:**
- Create temporary and test files in `temp/` or `for_claude/`
- Do not create in actual program folders (like `_lib/`)
- Do not pollute user's Git-managed folders

**See project-specific CLAUDE.md for details**
Each project's CLAUDE.md contains project-specific file creation rules.

---

### ファイル管理方針 / File Management Policy

**重要: 重要なデータファイルは `for_claude/` フォルダで管理すること**

**`output/` フォルダの運用ルール:**
- `output/` フォルダは報告用の一時的な出力先
- スクリプトの実行結果（CSV, JSON, Excel等）を一時的に保存
- ファイルが増えてきたら、7z（または zip）に圧縮して整理すること
- 重要なファイルは必ず `for_claude/` に移動またはコピーすること
- **ユーザーがファイルを移動・削除・圧縮する可能性がある**
- スクリプト実行前に必要なファイルの存在を確認すること

**`for_claude/` フォルダの運用ルール:**
- **Claude専用の作業領域** - ユーザーはこのフォルダを触らない
- 重要なデータファイル（JSON, CSV等）は `for_claude/` に保存
- セッション間で参照が必要なファイルを保管
- ドキュメント類（.md, .txt）も `for_claude/` に保存
- このフォルダのファイルは削除・圧縮せず、常にアクセス可能にすること
- Claudeはこのフォルダを自由に編集・整理できる

**ファイル保存時のベストプラクティス:**
1. スクリプト実行時は `output/` に出力
2. 重要なファイル（マッピング、設定、参照データ等）は `for_claude/` にもコピー
3. `output/` が肥大化したら、古いファイルを 7z 圧縮
4. `for_claude/` のファイルは圧縮せず、常に直接アクセス可能にする

**例:**
```
output/
  ├── code_validation_lists.csv          ← 一時的な出力
  ├── import_mid_export_mapping.xlsx     ← 一時的な出力
  └── archive_2025-10-28.7z              ← 古いファイルを圧縮

for_claude/
  ├── coordinate_validation_mapping.json ← 重要ファイル（常時アクセス）
  ├── code_validation_lists.json         ← 重要ファイル（常時アクセス）
  ├── log.txt                            ← セッションログ
  └── archive/                           ← アーカイブログ
```

**IMPORTANT: Important data files should be managed in the `for_claude/` folder**

**`output/` folder operation rules:**
- `output/` folder is a temporary output destination for reports
- Script execution results (CSV, JSON, Excel, etc.) are temporarily saved here
- When files accumulate, compress them into 7z (or zip) archives
- Important files must be moved or copied to `for_claude/`
- **User may move, delete, or compress files in this folder**
- Always verify file existence before script execution

**`for_claude/` folder operation rules:**
- **Claude's dedicated workspace** - User does not touch this folder
- Save important data files (JSON, CSV, etc.) in `for_claude/`
- Store files that need to be referenced between sessions
- Save documentation (.md, .txt) in `for_claude/`
- Do not delete or compress files in this folder; keep them always accessible
- Claude can freely edit and organize this folder

**Best practices for file saving:**
1. Output to `output/` when running scripts
2. Copy important files (mappings, configurations, reference data, etc.) to `for_claude/`
3. When `output/` becomes bloated, compress old files into 7z archives
4. Keep files in `for_claude/` uncompressed and directly accessible

**Example:**
```
output/
  ├── code_validation_lists.csv          ← Temporary output
  ├── import_mid_export_mapping.xlsx     ← Temporary output
  └── archive_2025-10-28.7z              ← Compressed old files

for_claude/
  ├── coordinate_validation_mapping.json ← Important file (always accessible)
  ├── code_validation_lists.json         ← Important file (always accessible)
  ├── log.txt                            ← Session log
  └── archive/                           ← Archive logs
```

---

## 【セッション開始時のチェックリスト】Session Start Checklist

**Claudeが新しいセッションを開始する際は、必ず以下の手順を実行すること**

### 1. Serena MCPプロジェクトのアクティブ化

**重要: Serena MCPを使用する前に、必ずプロジェクトをアクティブ化すること**

```python
# プロジェクトアクティブ化
mcp__serena__activate_project("プロジェクト名")

# 設定確認
mcp__serena__get_current_config()

# オンボーディング確認
mcp__serena__check_onboarding_performed()
```

**Serena MCPが使えるようになると:**
- シンボル検索・読み取り: `mcp__serena__find_symbol()`
- ファイル一覧取得: `mcp__serena__list_dir()`
- パターン検索: `mcp__serena__search_for_pattern()`
- シンボル本体の一括置換: `mcp__serena__replace_symbol_body()`

### 2. 引継ぎ情報の読み込み（必須）

**読み込む順序:**

```
1. CLAUDE_GLOBAL.md（このファイル）- グローバル設定
2. CLAUDE.md - プロジェクト固有の設定
3. for_claude/log.txt - 作業履歴・引継ぎ事項
```

**ユーザーが「引継ぎ」「前回の続き」と言った場合は特に重要**

### 3. プロジェクト状況の把握

**for_claude/log.txtから以下を確認:**
- 前回のセッションで何をしていたか
- 完了したタスク
- 未完了のタスク
- 次回への引継ぎ事項
- 技術的な留意事項

### 4. 利用可能なメモリの確認（オプション）

```python
# Serenaのメモリ一覧を取得
mcp__serena__list_memories()

# 必要に応じてメモリを読み込む
mcp__serena__read_memory("memory_file_name")
```

**When Claude starts a new session, always follow these steps:**

### 1. Activate Serena MCP Project

**IMPORTANT: Always activate project before using Serena MCP**

```python
# Activate project
mcp__serena__activate_project("project_name")

# Check configuration
mcp__serena__get_current_config()

# Check onboarding status
mcp__serena__check_onboarding_performed()
```

**When Serena MCP is available:**
- Symbol search & read: `mcp__serena__find_symbol()`
- List files: `mcp__serena__list_dir()`
- Pattern search: `mcp__serena__search_for_pattern()`
- Batch replace symbol body: `mcp__serena__replace_symbol_body()`

### 2. Load Handover Information (Required)

**Reading order:**

```
1. CLAUDE_GLOBAL.md (this file) - Global settings
2. CLAUDE.md - Project-specific settings
3. for_claude/log.txt - Work history & handover notes
```

**Especially important when user mentions "handover" or "continue from last time"**

### 3. Understand Project Status

**Check from for_claude/log.txt:**
- What was done in the last session
- Completed tasks
- Incomplete tasks
- Handover notes for next session
- Technical notes

### 4. Check Available Memories (Optional)

```python
# Get Serena memory list
mcp__serena__list_memories()

# Read memory if needed
mcp__serena__read_memory("memory_file_name")
```

---
