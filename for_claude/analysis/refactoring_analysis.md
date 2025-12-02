# MAIN_APP.py リファクタリング分析レポート

作成日: 2025-10-24

---

## 現状の問題点

### 1. 巨大な単一ファイル
- **総行数: 5,138行**
- ファイルサイズ: 約312KB
- これは保守性、可読性、テスト容易性すべてにおいて問題です

### 2. 神クラス (God Class) の問題
**MyMainWindow クラスが約130個のメソッドを持つ**

```
MyMainWindow (約4000行)
    ├── 初期化関連: __init__, initializer, initializer_sub
    ├── UI操作: 約40メソッド
    ├── イベント処理: 約30メソッド
    ├── データ検証: 約20メソッド
    ├── ファイル/画像操作: 約20メソッド
    ├── 設定管理: 約10メソッド
    └── その他: 約10メソッド
```

### 3. クラス構成

```python
1. MainData (dataclass)                           # 54行目
2. MyMainWindow (QMainWindow)                     # 61行目 - 約4000行
3. CustomEventFilterForGraphicsView (QObject)     # 4104行目
4. CustomEventFilterForLineEditScale (QObject)    # 4126行目
5. CustomEventFilterForLineEdit (QObject)         # 4139行目 - 約150行
6. CustomEventFilterForPlaneTextEdit (QObject)    # 4490行目 - 約110行
7. CustomEventFilterForDD (QObject)               # 4606行目
8. CustomEventFilterForButtonScrollArea (QObject) # 4633行目
9. InitDialog (QDialog)                           # 4649行目 - 約450行
10. CollationDialog (QDialog)                     # 5134行目 - 約180行
11. IMEThread (QThread)                           # 5316行目
12. SingleApplication (QApplication)              # 5334行目
```

---

## MyMainWindow メソッド一覧と分類

### A. 初期化系 (3メソッド)
- `__init__()` - 63行目
- `initializer()` - 256行目
- `initializer_sub()` - 2600行目

### B. UI操作・レイアウト系 (15メソッド)
- `set_screen_mode_toggle()` - 2326行目
- `set_screen_mode_toggle_full_or_max()` - 2334行目
- `change_layout_vertical()` - 2481行目
- `change_layout_horizontal()` - 2527行目
- `info_label_show()` - 2660行目
- `info_label_hide()` - 2665行目
- `rect_area_show_or_hide()` - 2670行目
- `show_info_to_two_labels()` - 2515行目
- `show_angle_and_scale()` - 3489行目
- `change_color_of_all_line_edits()` - 3147行目
- `change_color_of_line_edit()` - 3154行目
- `change_color_black_or_red()` - 3160行目
- `scroll_to_position()` - 2623行目
- `set_value_to_scrollbar()` - 1202行目
- `pressed_h_button()` - 2471行目, `pressed_v_button()` - 2476行目

### C. 画像・PDF操作系 (17メソッド)
- `init_graphics_view()` - 2910行目
- `init_graphics_view_pdf()` - 2924行目
- `get_rotate_exif()` - 2964行目
- `get_image_filepath_obj_dict()` - 2985行目
- `set_image_from_pixmap()` - 3278行目
- `adjust_image()` - 3333行目
- `rotate_image()` - 3373行目
- `scaling_image()` - 3393行目
- `change_scale_on_line_edit()` - 3451行目
- `reset_scroll_and_align_item()` - 3472行目
- `align_image_to_top_left()` - 3484行目
- `change_image()` - 3003行目
- `change_pdf_image()` - 1544行目
- `process_of_before_change_image()` - 1581行目
- `helper_of_before_change_for_pdf()` - 1614行目
- `helper_of_last_image_before_change()` - 1919行目
- `helper_of_not_last_image_before_change()` - 1960行目

### D. フォーカス・入力制御系 (15メソッド)
- `get_focused_line_edit_obj()` - 2378行目
- `set_focus_to_first_line_edit()` - 2462行目
- `set_focus_to_target_edit_for_timer()` - 2096行目
- `set_focus_ime_and_rect()` - 2115行目
- `goto_first_or_last_line_edit()` - 3074行目
- `goto_first_visible_line_edit()` - 3086行目
- `next_line_edit()` - 2764行目
- `pressed_enter_key_in_line_edit()` - 2752行目
- `processing_enter_key_in_line_edit_after_check()` - 1359行目
- `do_event_of_line_edit_focus_out()` - 1214行目
- `on_line_edit_canceled()` - 2106行目
- `on_line_edit_canceled_for_listwidget()` - 2126行目
- `install_event_filter_to_all_line_edit()` - 2730行目
- `remove_event_filter_to_all_line_edit()` - 2736行目
- `activate_all_event_filter()` - 4090行目, `deactivate_all_event_filter()` - 4096行目

### E. データ検証系 (26メソッド)
- `check_type_line_edit_and_verify_text()` - 1231行目
- `check_type_line_edit()` - 3861行目
- `check_type_all_line_edit()` - 3911行目
- `is_not_empty()` - 3632行目
- `is_valid_date()` - 3635行目
- `is_int()` - 3647行目
- `is_float()` - 3656行目
- `is_post_number()` - 3665行目
- `is_post_number_kuromaru()` - 3670行目
- `is_tel_number()` - 3675行目
- `is_hankaku()` - 3681行目
- `is_zenkaku()` - 3690行目
- `is_value_in_list()` - 3699行目
- `is_value_in_list_kuromaru()` - 3711行目
- `is_correct_length()` - 3725行目
- `is_in_range()` - 3735行目
- `is_in_len_range()` - 3755行目
- `is_len_equal()` - 3772行目
- `is_alphanumeric()` - 3784行目
- `is_re_match()` - 3790行目
- `is_hankaku_eisu_kuromaru()` - 3800行目
- `is_hankaku_kuromaru()` - 3806行目
- `is_zenkaku_katakana_kuromaru()` - 3815行目
- `is_hiragana_kuromaru()` - 3821行目
- `is_encodable()` - 3828行目
- `check_encoding_line_edits()` - 3842行目

### F. リストウィジェット操作系 (9メソッド)
- `set_items_to_list_widget()` - 2895行目
- `set_item_to_list_widget()` - 2900行目
- `change_text_of_list_widget()` - 2905行目
- `on_list_widget_selected()` - 3092行目
- `on_list_widget_selected_for_pdf()` - 3031行目
- `on_list_widget_selected_for_pdf_record()` - 2139行目
- `select_next_item_of_list_widget()` - 3131行目
- `select_item_for_list_widget_for_pdf()` - 3054行目
- `create_new_list_item_on_rept()` - 2180行目

### G. データ入出力系 (11メソッド)
- `add_record()` - 2186行目
- `add_record_for_pdf()` - 1813行目
- `output_log()` - 2211行目
- `output_log_for_pdf()` - 1836行目
- `output_csv()` - 3191行目
- `create_another_log()` - 2316行目
- `create_rept_list_texts()` - 3176行目
- `set_previous_data_to_line_edits()` - 2798行目
- `set_blank_to_line_edits()` - 2809行目
- `set_new_text_to_line_edits()` - 3258行目
- `get_error_info()` - 2755行目

### H. 設定管理系 (6メソッド)
- `check_config()` - 3497行目
- `write_config()` - 3509行目
- `read_config()` - 3514行目
- `write_rect_config()` - 3522行目
- `read_rect_config()` - 3527行目
- `init_config()` - 2888行目

### I. ダイアログ系 (3メソッド)
- `show_init_dialog()` - 2998行目
- `close_after_dialog()` - 2995行目
- `create_multi_button_msg()` - 2864行目

### J. ドロップダウン系 (3メソッド)
- `show_dd_list_widget()` - 2396行目
- `activated_dd_list_widget()` - 2444行目
- `change_delta_scale()` - 2458行目

### K. IME制御系 (5メソッド)
- `set_ime_from_ime_mode_text()` - 2687行目
- `set_ime_on_jp()` - 2696行目
- `set_ime_on_en()` - 2703行目
- `on_thread_finished()` - 2710行目
- `clean_up_thread()` - 2714行目

### L. 矩形選択系 (4メソッド)
- `pressed_radioButton_automove_on()` - 2562行目
- `pressed_get_rect()` - 2566行目
- `change_rect_mode()` - 2679行目
- (矩形の詳細な処理は_draggable_pixmap_item.pyに分離済み)

### M. テキスト変換・郵便番号系 (2メソッド)
- `set_values_pref_city_and_town()` - 3930行目
- `conversion_inputted_text()` - 3975行目

### N. イベントハンドラ系 (3メソッド)
- `eventFilter()` - 3536行目
- `showEvent()` - 3557行目
- `closeEvent()` - 3585行目
- `close_event_processing()` - 3595行目

### O. ユーティリティ系 (9メソッド)
- `get_timestamp()` - 3272行目
- `set_today_text()` - 3065行目
- `get_img_file_obj_list()` - 2741行目
- `save_log_and_raise()` - 2746行目
- `restart_app()` - 2835行目
- `set_connect()` - 2344行目
- `pr()` - 1195行目 (デバッグ用print)
- `on_test_button_pressed()` - 1182行目
- `on_test_button_pressed_2()` - 1190行目

---

## リファクタリング戦略

### フェーズ1: 分析と計画 (現在のフェーズ)
1. [完了] 現状の構造を把握
2. [作業中] 問題点の洗い出し
3. [次] 分割方針の決定

### フェーズ2: バリデーション層の分離
**優先度: 高**

26個のバリデーションメソッドを独立したクラスに分離

```python
# 提案: _validators.py
class InputValidator:
    """入力値の検証を担当するクラス"""

    # 基本検証
    def is_not_empty(self, s: str) -> bool
    def is_int(self, s: str) -> bool
    def is_float(self, s: str) -> bool

    # 日付・時刻検証
    def is_valid_date(self, s: str) -> bool

    # 郵便番号・電話番号検証
    def is_post_number(self, s: str) -> bool
    def is_tel_number(self, s: str) -> bool

    # 文字種検証
    def is_hankaku(self, s: str) -> bool
    def is_zenkaku(self, s: str) -> bool
    def is_alphanumeric(self, s: str) -> bool
    def is_hiragana_kuromaru(self, s: str) -> bool
    def is_zenkaku_katakana_kuromaru(self, s: str) -> bool

    # 範囲・長さ検証
    def is_in_range(self, s: str, min_val, max_val) -> bool
    def is_in_len_range(self, s: str, min_len, max_len) -> bool
    def is_len_equal(self, s: str, length) -> bool

    # リスト検証
    def is_value_in_list(self, s: str, value_list: list) -> bool

    # エンコーディング検証
    def is_encodable(self, s: str, encoding='cp932') -> bool

    # 正規表現マッチ
    def is_re_match(self, s: str, pattern: str) -> bool

    # 複合検証
    def check_type(self, value: str, data_type: str, **kwargs) -> bool
```

**メリット:**
- 単一責任の原則に従う
- テストが容易になる
- 他のプロジェクトでも再利用可能
- MyMainWindowの行数を約500行削減

---

### フェーズ3: 画像操作層の分離
**優先度: 高**

17個の画像・PDF操作メソッドを独立したクラスに分離

```python
# 提案: _image_controller.py
class ImageController:
    """画像表示・操作を担当するクラス"""

    def __init__(self, graphics_view: QGraphicsView, scene: QGraphicsScene):
        self.graphics_view = graphics_view
        self.scene = scene
        self.pixmap_item = None
        self.current_scale = 1.0
        self.current_angle = 0

    # 初期化
    def init_graphics_view(self)
    def init_graphics_view_pdf(self)

    # 画像読み込み
    def load_image_from_file(self, filepath: str) -> bool
    def load_image_from_pixmap(self, pixmap: QPixmap) -> bool
    def get_rotate_exif(self, file_path: str) -> int

    # 画像変換
    def rotate_image(self, angle: int, is_absolute=False)
    def scale_image(self, scale: float, is_absolute=False)
    def adjust_to_fit(self, mode: str = 'w')
    def reset_scale_and_rotation(self)

    # 表示制御
    def align_to_top_left(self)
    def reset_scroll_and_align(self)
    def update_display_info(self) -> dict

    # 状態取得
    def get_current_scale(self) -> float
    def get_current_angle(self) -> int
```

```python
# 提案: _pdf_controller.py
class PDFController:
    """PDF操作を担当するクラス"""

    def __init__(self, pdf_util: PdfImgReader, image_controller: ImageController):
        self.pdf_util = pdf_util
        self.image_controller = image_controller
        self.current_file_index = 0
        self.current_page_index = 0

    def load_pdf_folder(self, folder_path: str) -> bool
    def change_page(self, page_index: int) -> bool
    def next_page(self) -> bool
    def previous_page(self) -> bool
    def get_page_count(self) -> int
    def get_current_page_info(self) -> dict
```

**メリット:**
- 画像操作ロジックを明確に分離
- GraphicsView関連の処理をカプセル化
- MyMainWindowの行数を約400行削減

---

### フェーズ4: データ入出力層の分離
**優先度: 中**

11個のデータ入出力メソッドを独立したクラスに分離

```python
# 提案: _data_manager.py
class DataManager:
    """データの入出力を担当するクラス"""

    def __init__(self, data_list: list):
        self.data_list = data_list
        self.current_record = {}
        self.records_history = []

    # レコード操作
    def create_new_record(self, line_edit_values: dict) -> dict
    def add_record(self, record: dict) -> bool
    def get_previous_record(self) -> dict

    # CSV出力
    def export_to_csv(self, filepath: str) -> bool
    def create_rept_list(self) -> list

    # ログ出力
    def output_log(self, log_type: str, filepath: str) -> bool
    def create_log_dataframe(self) -> pd.DataFrame

    # データ復元
    def load_previous_data(self) -> dict
    def set_blank_data(self) -> dict
```

**メリット:**
- データ処理ロジックを集約
- CSV/ログ出力を統一的に管理
- テストが容易
- MyMainWindowの行数を約300行削減

---

### フェーズ5: UI操作層の整理
**優先度: 中**

15個のUI操作メソッドをグループ化

```python
# 提案: _ui_controller.py
class UIController:
    """UI表示・レイアウトを担当するクラス"""

    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window
        self.current_layout_mode = 'vertical'
        self.screen_mode = 'normal'

    # レイアウト制御
    def change_layout(self, mode: str)  # 'vertical' or 'horizontal'
    def toggle_screen_mode(self)  # normal, maximized, fullscreen

    # ラベル表示
    def show_info_labels(self, info_dict: dict)
    def hide_info_labels(self)

    # LineEdit色変更
    def set_line_edit_color(self, obj: QLineEdit, color: str)
    def set_all_line_edits_color(self, color: str)
    def update_validation_colors(self, validation_results: list)

    # スクロール制御
    def scroll_to_position(self, view_obj, orientation: str)
    def set_scrollbar_value(self, orientation: str)
```

**メリット:**
- UI関連の処理を一元管理
- レイアウト変更のロジックを明確化
- MyMainWindowの行数を約200行削減

---

### フェーズ6: フォーカス制御層の分離
**優先度: 中**

15個のフォーカス・入力制御メソッドを整理

```python
# 提案: _focus_controller.py
class FocusController:
    """フォーカス制御を担当するクラス"""

    def __init__(self, line_edit_list: list):
        self.line_edit_list = line_edit_list
        self.current_focus_obj = None
        self.focus_history = []

    # フォーカス移動
    def move_to_next(self) -> QLineEdit
    def move_to_previous(self) -> QLineEdit
    def move_to_first(self) -> QLineEdit
    def move_to_last(self) -> QLineEdit

    # フォーカス取得
    def get_current_focused(self) -> QLineEdit
    def get_focus_index(self) -> int

    # イベントフィルタ管理
    def install_all_event_filters(self)
    def remove_all_event_filters(self)
    def activate_event_filters(self)
    def deactivate_event_filters(self)

    # IME制御
    def set_ime_mode(self, mode: str)  # 'jp' or 'en'
```

**メリット:**
- フォーカス制御を集約
- 入力フロー管理を明確化
- MyMainWindowの行数を約250行削減

---

### フェーズ7: リストウィジェット操作層の分離
**優先度: 低**

9個のリストウィジェット操作メソッドを整理

```python
# 提案: _list_widget_controller.py
class ListWidgetController:
    """リストウィジェット操作を担当するクラス"""

    def __init__(self, list_widget: QListWidget):
        self.list_widget = list_widget
        self.current_index = 0

    # アイテム操作
    def set_items(self, items: list)
    def add_item(self, item: str)
    def update_item_text(self, index: int, text: str)

    # 選択操作
    def select_next(self)
    def select_previous(self)
    def select_by_index(self, index: int)

    # イベント処理
    def on_item_selected(self, callback: callable)
```

**メリット:**
- リストウィジェット操作を集約
- MyMainWindowの行数を約100行削減

---

### フェーズ8: 設定管理層の整理
**優先度: 低**

6個の設定管理メソッドを整理

```python
# 提案: _config_manager.py
class ConfigManager:
    """設定ファイルの読み書きを担当するクラス"""

    def __init__(self, config_dir: str = './config'):
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / 'config.json'
        self.rect_config_file = self.config_dir / 'rect_config.json'
        self.config = {}
        self.rect_config = {}

    # 設定読み書き
    def load_config(self) -> dict
    def save_config(self, config: dict) -> bool
    def check_config(self) -> bool

    # 矩形設定読み書き
    def load_rect_config(self) -> dict
    def save_rect_config(self, rect_config: dict) -> bool

    # 初期化
    def init_config(self) -> dict
```

**メリット:**
- 設定管理を一元化
- JSONファイルの読み書きを集約
- MyMainWindowの行数を約50行削減

---

## 削減効果の見積もり

### 現状
- **MAIN_APP.py**: 5,138行
- **MyMainWindow**: 約4,000行

### リファクタリング後の見積もり

| 分離クラス | 削減行数 | 新ファイル |
|-----------|---------|-----------|
| InputValidator | 500行 | _validators.py |
| ImageController | 400行 | _image_controller.py |
| PDFController | 200行 | _pdf_controller.py |
| DataManager | 300行 | _data_manager.py |
| UIController | 200行 | _ui_controller.py |
| FocusController | 250行 | _focus_controller.py |
| ListWidgetController | 100行 | _list_widget_controller.py |
| ConfigManager | 50行 | _config_manager.py |
| **合計削減** | **2,000行** | **8ファイル** |

### リファクタリング後
- **MAIN_APP.py**: 約3,100行 (5,138 - 2,000)
- **MyMainWindow**: 約2,000行 (4,000 - 2,000)

まだ大きいですが、現在の半分になります。

---

## リファクタリング時の注意事項

### 1. テスト戦略
リファクタリング前に既存機能のテストを実施
- 手動テスト項目リストの作成
- 主要な操作フローの記録
- スクリーンショットでの動作確認

### 2. 段階的な移行
一度にすべてを変更せず、フェーズごとに進める
1. 新しいクラスを作成
2. メソッドを移動（元のメソッドは残す）
3. MyMainWindowから新クラスを呼び出す
4. 動作確認
5. 元のメソッドを削除

### 3. バックアップ
- Gitでコミット管理
- 各フェーズ完了時にタグを作成
- CLAUDE_GLOBAL.mdのバックアップ方針に従う

### 4. ドキュメント整備
- 各クラスの役割を明確に記述
- メソッドのdocstringを追加
- 使用例を記載

---

## 即座に実施可能な改善

### 1. コメントの整理
- 不要なコメントアウトコードの削除
- TODOコメントの整理

### 2. 命名の統一
- `pr()` -> `debug_print()`
- `is_valid_date()` など、統一的な命名規則

### 3. マジックナンバーの定数化
```python
# 悪い例
if len(text) > 10:
    ...

# 良い例
MAX_TEXT_LENGTH = 10
if len(text) > MAX_TEXT_LENGTH:
    ...
```

---

## 推奨する作業順序

### ステップ1: バリデーション層の分離 (1日)
- 最も独立性が高い
- テストが容易
- 影響範囲が明確

### ステップ2: 画像操作層の分離 (2日)
- ビジネスロジックから分離
- 再利用性が高い

### ステップ3: データ管理層の分離 (1日)
- 入出力を一元化
- エラーハンドリングの改善

### ステップ4: UI・フォーカス制御の整理 (2日)
- ユーザー体験に直結
- 慎重な動作確認が必要

### ステップ5: その他の整理 (1日)
- 残りの小さな改善

**合計見積もり: 約7日間**

---

## 次のステップ

1. このレポートをレビュー
2. ユーザーの優先順位を確認
3. フェーズ2（バリデーション層の分離）から着手
4. for_claudeフォルダ内で新クラスのプロトタイプを作成

---

## 質問事項

ユーザーへの確認が必要な項目:

1. どのフェーズから着手したいですか？
   - 推奨: フェーズ2（バリデーション層）

2. リファクタリング中も元のMAIN_APP.pyは動作する状態を維持しますか？
   - 推奨: はい（段階的移行）

3. テストはどの程度必要ですか？
   - 最小限の動作確認のみ
   - 主要機能の手動テスト
   - 包括的なテスト

4. 新しいクラスのファイル配置は？
   - ルートディレクトリ（現在の_xxx.py形式）
   - 専用フォルダ（例: controllers/, validators/）

---

作成者: Claude Code
作成日: 2025-10-24
