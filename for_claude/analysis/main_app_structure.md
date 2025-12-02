# MAIN_APP.py インポート構造と全体像

## 基本情報
- **ファイル**: MAIN_APP.py
- **総行数**: 2,778行
- **メインクラス**: MyMainWindow
- **継承**: QMainWindow, Ui_MainWindow, InitializerMixin
- **メソッド数**: 106個

---

## カスタムモジュールインポート構造

### MAIN_APP.py が直接インポートするモジュール (23個)

1. **_create_logger** - ロガー作成
2. **_draggable_pixmap_item** - ドラッグ可能な画像アイテム
3. **_init_dialog_main** - 初期化ダイアログ
4. **_collation_dialog_main** - 照合ダイアログ
5. **_ime_control** - IME制御
6. **_helper_classes** - ヘルパークラス (IMEThread, SingleApplication)
7. **_postnum_reader** - 郵便番号読み取り
8. **_collation_two_text** - テキスト照合
9. **_sub_lib** - サブライブラリ (SubLib, pri)
10. **_pdf_util** - PDF読み取り
11. **_create_data_list** - データリスト・フレームリスト作成
12. **_text_edit_dialog** - テキスト編集ダイアログ
13. **_mode_config** - モード設定管理
14. **_validators** - 入力検証
15. **_image_utils** - 画像ユーティリティ
16. **_data_io** - データ入出力
17. **_config_manager** - 設定管理 (ConfigManager, RectConfigManager)
18. **_main_data** - メインデータ
19. **_event_filters** - イベントフィルター (6クラス)
20. **_data_transform** - データ変換
21. **_constants** - 定数定義
22. **initializer_mixin** - 初期化Mixin

---

## 主要クラスとその役割

### モード設定 (_mode_config.py)
- **ModeConfig**: データクラス - 各モードの設定
- **ModeConfigManager**: モード設定の管理クラス

### イベントフィルター (_event_filters.py) - 6クラス
1. **CustomEventFilterForGraphicsView**: グラフィックスビュー用
2. **CustomEventFilterForLineEditScale**: スケール付きライン編集用
3. **CustomEventFilterForLineEdit**: ライン編集用
4. **CustomEventFilterForPlaneTextEdit**: プレーンテキスト編集用
5. **CustomEventFilterForDD**: ドラッグ&ドロップ用
6. **CustomEventFilterForButtonScrollArea**: ボタンスクロールエリア用

### ヘルパークラス (_helper_classes.py)
- **IMEThread**: IME制御スレッド
- **SingleApplication**: 単一インスタンスアプリケーション

---

## モジュール間の依存関係

### _lib内の相互インポート
- **_collation_dialog_main** → _sub_lib, _collation_two_text
- **_event_filters** → _text_edit_dialog
- **_helper_classes** → _ime_control
- **_init_dialog_main** → _data_io

---

## MAIN_APP.py メソッドカテゴリ (106個)

### 1. 矩形操作 (3個)
- `pressed_get_rect()` [1517] - 矩形取得
- `copy_rect_from_previous()` [1551] - 前の矩形をコピー (Ctrl+Shift+R)
- `fill_rect_json_null_with_previous()` [1609] - null値を埋める (Ctrl+Shift+Alt+R)

### 2. 設定ファイル操作 (4個)
- `read_config()` [2524] - 設定読み込み
- `write_config()` [2520] - 設定書き込み
- `read_rect_config()` [2533] - 矩形設定読み込み
- `write_rect_config()` [2529] - 矩形設定書き込み

### 3. フォーカス・IME制御
- `set_focus_to_target_edit_for_timer()` [1045]
- `set_focus_ime_and_rect()` [1064]
- `set_ime_on_jp()` [1755]
- `set_ime_on_en()` [1762]
- `set_ime_from_ime_mode_text()` [1746]
- `get_focused_line_edit_obj()` [1329]
- `set_focus_to_first_line_edit()` [1413]

### 4. データ入力制御
- `set_new_text_to_line_edits()` [2275]
- `set_previous_data_to_line_edits()` [1843]
- `set_blank_to_line_edits()` [1854]

### 5. 画面表示制御
- `set_screen_mode_toggle()` [1277] - 3種トグル
- `set_screen_mode_toggle_full_or_max()` [1285] - 2種トグル
- `set_image_from_pixmap()` [2295]

### 6. リスト・ウィジェット操作
- `set_items_to_list_widget()` [1937]
- `set_item_to_list_widget()` [1942]

### 7. ボタン操作
- `pressed_h_button()` [1422]
- `pressed_v_button()` [1427]
- `pressed_radioButton_automove_on()` [1513]

### 8. その他ユーティリティ
- `get_error_info()` [1800] - エラー情報取得
- `get_timestamp()` [2289] - タイムスタンプ取得
- `set_today_text()` [2076] - 今日の日付設定
- `set_connect()` [1295] - シグナル接続
- `set_value_to_scrollbar()` [136] - スクロールバー設定
- `set_values_pref_city_and_town()` [2713] - 都道府県・市町村設定

---

## 標準ライブラリインポート

### Python標準
- traceback, datetime, time, os, pathlib, sys, json, re, ctypes
- typing (List), dataclasses (dataclass), collections (Counter)

### PyQt5
- QtWidgets, QtCore, QtGui
- QApplication, QMainWindow, QMessageBox, QFileDialog
- QGraphicsScene, QPixmap, QTransform, QKeySequence
- QShortcut, QTimer, QThread, QObject, QEvent

### サードパーティ
- pandas (pd)
- sip (PyQt5 内部)

---

## 次回リファクタリング候補

### 優先度: 高
1. **共通パターンの統一** (推定削減: 100-150行)
   - スクロールエリア更新制御のコンテキストマネージャ化
   - モード判定ロジックの統一メソッド化
   - 連続実行防止のデコレーター化

### 優先度: 中
2. **initializer の完全分割** (残り629行を14メソッドに分割)
3. **helper系メソッドの統一** (BeforeChangeProcessorクラス)

---

**作成日**: 2025-11-06
**セッション**: 11 (Serena MCP探索テスト)
