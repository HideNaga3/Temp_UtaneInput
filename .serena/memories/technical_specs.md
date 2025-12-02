# 技術仕様

## エンコーディング
- **ファイルエンコーディング**: UTF-8
- **log.txt等のドキュメント**: UTF-8 BOM (PowerShellの文字化け対策)

## ファイル命名規則
- **プライベートモジュール**: `_module_name.py` (アンダースコア接頭辞)
- **UI生成ファイル**: `*_ui.py` (QtDesignerから生成)
- **設定ファイル**: JSON形式 (data/rect.json等)

## データ構造

### モード設定 (_lib/_mode_config.py)
- **ModeConfig**: データクラスで各モードの設定を管理
- **主要フィールド**:
  - `df_name_column_index`: 氏名列のインデックス
  - `is_pdfmode_to_read_image_file`: PDF画像読み込みモード
  - `frame_count`: フレーム数
  - `start_index`: 開始インデックス

### 矩形データ (data/rect.json)
- **構造**: `{"0": {"x": int, "y": int, "w": int, "h": int, "scale": float, "angle": int}, ...}`
- **用途**: 画像上の入力領域を定義

## ライブラリバージョン
- **PyQt5**: GUI フレームワーク
- **pandas**: データ処理
- **Pillow**: 画像処理

## プロジェクト構造

### 本番コード (_lib/)
- `MAIN_APP.py`: メインアプリケーション
- `_mode_config.py`: モード設定管理
- `_create_data_list.py`: データリスト生成
- `_event_filters.py`: イベントフィルター (6クラス)
- `_helper_classes.py`: ヘルパークラス

### 開発用フォルダ
- `for_claude/`: Claude専用作業領域・ドキュメント
  - `log.txt`: セッション履歴
  - `session9_10.txt`: 最新セッション記録
- `temp/`: 一時ファイル・テスト用
- `tools/`: ユーティリティスクリプト

### 設定・データ
- `data/`: 設定ファイル (rect.json等)
- `global/`: グローバル設定・ドキュメント

## コーディング規約

### ファイル作成ルール
- **一時ファイル**: `temp/` または `for_claude/` に作成
- **本番ファイル**: `_lib/` に配置 (exe化対象)
- **テストファイル**: `temp/` に作成

### ツール使用優先順位
1. **Serena MCP**: プロジェクト探索・シンボル検索
2. **Read**: 特定ファイル読み込み
3. **Grep**: パターン検索
4. **Glob**: ファイル名検索
5. **避ける**: PowerShell Get-Content (日本語文字化け)

## リファクタリング履歴

### セッション9 (2025-11-05)
- `_create_data_list.py`: 357行→241行 (116行削減)
- 手動リスト→ループ生成に改善

### セッション10 (2025-11-05)
- `df_name_column_index`による氏名列管理の一元化
- MAIN_APP.py: 5行削減
- _mode_config.py: 42行追加 (新機能)

### セッション8 (2025-10-25)
- EventFilter完全分離 (6クラス572行)
- MAIN_APP.py: 4,163行→3,705行 (458行削減)
- 累計削減: 1,433行 (27.9%削減)
