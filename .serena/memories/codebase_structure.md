# コードベース構造

## ディレクトリ構成

```
給与計算検定入力ソフト_20251015/
│
├── MAIN_APP.py                    # メインアプリケーション（4,804行）
├── main_app_ui.py                 # Qt DesignerからのUI定義
├── main_app_ui.ui                 # Qt Designer UIファイル
├── test_main_app.py               # テストファイル
│
├── _lib/                          # ライブラリモジュール
│   ├── _mode_config.py           # モード設定管理 [統合済み]
│   ├── _validators.py            # バリデーション処理 [統合済み]
│   ├── _image_utils.py           # 画像ユーティリティ [統合済み]
│   ├── _data_io.py               # CSV入出力 [統合済み]
│   ├── _config_manager.py        # 設定管理 [新規作成]
│   ├── _constants.py             # 定数定義
│   ├── _create_data_list.py      # データリスト作成
│   ├── _create_logger.py         # ロガー作成
│   ├── _data_transform.py        # データ変換
│   ├── _draggable_pixmap_item.py # ドラッグ可能なPixmapアイテム
│   ├── _event_filters.py         # イベントフィルタ
│   ├── _helper_classes.py        # ヘルパークラス
│   ├── _ime_control.py           # IME制御
│   ├── _init_dialog_main.py      # 初期設定ダイアログ
│   ├── _collation_dialog_main.py # 照合ダイアログ
│   ├── _text_edit_dialog.py      # テキスト編集ダイアログ
│   ├── _main_data.py             # メインデータクラス
│   ├── _pdf_util.py              # PDF処理ユーティリティ
│   ├── _postnum_reader.py        # 郵便番号読み取り
│   ├── _sub_lib.py               # サブライブラリ
│   └── initializer_mixin.py      # 初期化Mixin
│
├── _collation_dialog_ui.py        # 照合ダイアログUI定義
├── _collation_dialog_ui.ui        # 照合ダイアログUIファイル
├── _init_dialog_ui.py             # 初期設定ダイアログUI定義
├── _init_dialog_ui.ui             # 初期設定ダイアログUIファイル
├── _text_edit_dialog_ui.py        # テキスト編集ダイアログUI定義
├── _text_edit_dialog_ui.ui        # テキスト編集ダイアログUIファイル
│
├── _ime_control.ahk               # IME制御AutoHotkeyスクリプト
│
├── for_claude/                    # Claude用ドキュメント
│   ├── log.txt                    # 作業ログ（1,762行）
│   ├── analysis/                  # 分析レポート
│   │   └── session6_main_app_structure.md
│   ├── prototype/                 # プロトタイプ資料
│   └── backup/                    # バックアップファイル
│
├── data/                          # データファイル
├── SampleImg/                     # サンプル画像
│
├── DOC_給与検定/                  # 給与検定ドキュメント
├── DOC_ウタネ回覧/                # ウタネ回覧ドキュメント
├── DOC_工場見学/                  # 工場見学ドキュメント
│
├── backup/                        # 自動バックアップ先
│   └── YYYY-MM-DD/               # 日付別フォルダ
│
├── global/                        # グローバル設定・ドキュメント
│
├── .venv/                         # Python仮想環境
├── .venv_claude/                  # Claude用仮想環境
│
├── build/                         # PyInstallerビルド作業用
├── dist/                          # PyInstallerビルド出力先
│
├── requirements.txt               # Python依存パッケージ
├── python_version.txt             # Pythonバージョン（3.10）
├── 給与計算検定入力アプリ_試作V1.spec  # PyInstaller設定
│
├── CLAUDE.md                      # Claudeへのプロジェクト固有指示
├── CLAUDE_GLOBAL.md               # Claudeへのグローバル設定
└── .gitignore                     # Git除外設定
```

## MAIN_APP.pyの構造

### クラス構成（12クラス、4,804行）

1. **MainData** (5行) - グローバルデータ保持
2. **MyMainWindow** (3,725行) - メインウィンドウ [最重要・リファクタリング対象]
3. **CustomEventFilterForGraphicsView** (22行) - GraphicsViewイベント処理
4. **CustomEventFilterForLineEditScale** (13行) - スケール入力イベント処理
5. **CustomEventFilterForLineEdit** (351行) - データ入力イベント処理
6. **CustomEventFilterForPlaneTextEdit** (116行) - テキストエディットイベント処理
7. **CustomEventFilterForDD** (27行) - ドロップダウンイベント処理
8. **CustomEventFilterForButtonScrollArea** (16行) - スクロールエリアイベント処理
9. **InitDialog** (471行) - 初期設定ダイアログ
10. **CollationDialog** (182行) - 照合ダイアログ
11. **IMEThread** (18行) - IME制御スレッド
12. **SingleApplication** (48行) - 単一インスタンス制御

### MyMainWindowの主要メソッド分類

- **初期化系** (約15個): `__init__`, `initializer_sub`, `init_graphics_view`等
- **イベントハンドラ系** (約40個): `on_*`, `clicked_*`
- **データ操作系** (約30個): `set_*`, `get_*`, `update_*`
- **検証系** (約10個): `check_*`
- **画像処理系** (約15個): `rotate_image`, `zoom_in`, `fit_to_width`等
- **CSV/ファイル操作系** (約10個): CSV読み書き、ファイルパス管理
- **UI制御系** (約20個): ウィジェット表示/非表示、レイアウト変更
- **その他** (約22個): ログ処理、エラーハンドリング

## 主要な依存関係

### 外部ライブラリ
- PyQt5: UI全般
- pandas: DataFrame操作（111箇所）
- pathlib: ファイルパス操作
- json: 設定ファイル読み書き
- PyMuPDF (fitz): PDF処理

### 内部モジュール依存関係
```
MAIN_APP.py
├── _lib._mode_config (ModeConfigManager)
├── _lib._validators (InputValidator)
├── _lib._image_utils (ImageUtils)
├── _lib._data_io (DataIO)
├── _lib._config_manager (ConfigManager, RectConfigManager)
├── _lib._create_logger (create_logger)
├── _lib._pdf_util (PDFUtility)
├── _lib._ime_control (IMEControl)
└── その他のサブモジュール
```

## データファイル

### 設定ファイル
- **config.json**: アプリケーション設定（29項目）
- **rect.json**: ウィンドウ位置・サイズ設定

### データファイル
- **CSVファイル**: 入出力データ（CP932エンコーディング）
- **log.csv**: 入力ログ
- **export_log.csv**: エクスポートログ

### 画像ファイル
- **PDF**: 入力元画像
- **JPG/PNG**: 入力元画像

## 8つのモード

1. **給与検定1級** (payroll): 給与計算検定1級用
2. **ウタネ回覧** (utane): ウタネ回覧データ入力用
3. **カード見本** (card): カード見本データ入力用
4. **外国人** (foreigner): 外国人データ入力用
5. **防災** (prevention): 防災データ入力用
6. **集英社** (syuei): 集英社データ入力用
7. **防災V2** (prevention2): 防災V2データ入力用
8. **工場見学** (factory): 工場見学データ入力用

各モードは_mode_config.pyで設定管理されています。

## リファクタリングの進行状況

### 完了（セッション1-6）
- ステップ2: 不要なコメント削除
- ステップ3: 画像ユーティリティ統合（20行削減）
- ステップ4: 互換性変数削除（7行削減）
- ステップ5: バリデーション層統合（199行削減）
- ステップ6: frame_list変数整理（9行削減）
- ステップ7: 画像ユーティリティ統合（13行削減）
- ステップ8: 未使用コード整理（11行削減）
- ステップ9: データ入出力層分離（20行削減）

**累計削減**: 279行（5.4%削減）

### 実施中（セッション7）
- Phase A-4: 設定管理層の分離（_config_manager.py作成）

### 今後の予定
- Phase A-1: UI操作層分離（200-300行削減見込み）
- Phase A-2: 画像処理層完全分離（150-200行削減見込み）
- Phase A-3: データ管理層分離（300-400行削減見込み）
- Phase B-1: InitDialog分離（400行削減見込み）

**最終目標**: 3,500行（27%削減）
