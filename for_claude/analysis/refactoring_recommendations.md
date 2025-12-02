# MAIN_APP.py リファクタリング推奨事項

作成日: 2025-10-25
分析対象: MAIN_APP.py (3,687行)

## 概要

MAIN_APP.py内部のコード自体をリファクタリングする場合の優先順位と具体的な提案を記載します。

---

## 1. 最優先: initializer メソッドの分割 (641行)

### 現状の問題点

`initializer` メソッド (L337-978) は641行もあり、以下の18個のセクションが混在しています:

1. **Setup & Validation** (L337-390): 54行 - UI基本設定、ウィジェット検証
2. **Test & Debug Variables** (L391-413): 23行 - デバッグフラグ、テストモード設定
3. **Icon & Logger Setup** (L414-453): 40行 - ロガー設定、アイコンパス検出
4. **Instance Variables Block 1** (L454-536): 83行 - インスタンス変数の大量初期化
5. **Instance Variables Block 2** (L537-548): 12行 - 追加のインスタンス変数
6. **Mode Configuration** (L550-593): 44行 - モード設定、データリスト取得
7. **Config Initialization** (L594-622): 29行 - 設定辞書、初期ダイアログ
8. **Main Data List Setup** (L623-639): 17行 - フレーム表示設定
9. **Dictionary Creation** (L640-698): 59行 - obj_name_to_XXX_dict マッピング作成
10. **Rect Config** (L700-717): 18行 - 矩形設定の初期化
11. **Data List Object Assignment** (L718-754): 37行 - data_listへのQtオブジェクト割り当て
12. **Widget Visibility** (L755-773): 19行 - ウィジェット表示/非表示設定
13. **More Dictionaries** (L774-802): 29行 - 追加の辞書作成、水平線追加
14. **Palette & Color Setup** (L803-842): 40行 - ラベル・テキストエディットの色設定
15. **File Path Setup** (L844-856): 13行 - 出力パス設定
16. **Sub-Initializer & Graphics** (L857-863): 7行 - サブ初期化、グラフィックスビュー初期化
17. **Main Data Dict & CSV Loading** (L864-942): 79行 - メインデータ辞書作成、CSV読み込み
18. **Final Setup** (L943-986): 44行 - イベントフィルタ、ラジオボタン、レイアウト設定

### 推奨リファクタリング案

#### 案A: セクションごとにメソッド分割 (推奨度: ★★★★★)

各セクションを個別のメソッドに抽出:

```python
def initializer(self):
    """メイン初期化処理 - 各サブ初期化メソッドを呼び出す"""
    self._init_basic_setup()              # Setup & Validation
    self._init_test_variables()           # Test & Debug Variables
    self._init_logger_and_icons()         # Icon & Logger Setup
    self._init_instance_variables()       # Instance Variables
    self._init_mode_configuration()       # Mode Configuration
    self._init_config_and_dialog()        # Config Initialization

    if self.is_close_button_pressed:
        return

    self._init_data_list_setup()          # Main Data List Setup
    self._init_dictionaries()             # Dictionary Creation
    self._init_rect_config()              # Rect Config
    self._assign_objects_to_data_list()   # Data List Object Assignment
    self._init_widget_visibility()        # Widget Visibility
    self._init_additional_dictionaries()  # More Dictionaries
    self._init_palette_and_colors()       # Palette & Color Setup
    self._init_file_paths()               # File Path Setup
    self._init_graphics_view_setup()      # Sub-Initializer & Graphics
    self._init_csv_and_list_widgets()     # Main Data Dict & CSV Loading
    self._init_final_setup()              # Final Setup
```

**利点:**
- 各メソッドが30-80行程度になり、理解しやすい
- セクション間の依存関係が明確になる
- テストが容易になる
- 将来的な修正が局所化される

**実装の容易さ:** メソッド抽出は機械的に行えるため、比較的安全

---

#### 案B: 初期化フェーズごとにクラス分割 (推奨度: ★★★☆☆)

初期化処理を機能別のヘルパークラスに分割:

```python
class UIInitializer:
    """UI関連の初期化を担当"""
    def __init__(self, main_window):
        self.main_window = main_window

    def setup_basic_ui(self): ...
    def setup_widget_visibility(self): ...
    def setup_palette_and_colors(self): ...

class DataInitializer:
    """データ構造の初期化を担当"""
    def __init__(self, main_window):
        self.main_window = main_window

    def create_dictionaries(self): ...
    def load_csv_data(self): ...
    def setup_data_list(self): ...

class ConfigInitializer:
    """設定関連の初期化を担当"""
    def __init__(self, main_window):
        self.main_window = main_window

    def init_mode_configuration(self): ...
    def init_rect_config(self): ...
```

**利点:**
- 初期化ロジックがより明確に分離される
- 各クラスが単一責任を持つ

**欠点:**
- MyMainWindowへの依存が増える
- 実装コストが高い

---

## 2. 次優先: __init__ メソッドの分割 (198行)

### 現状の問題点

`__init__` メソッド (L138-336) も198行と長く、以下が混在:

- ウィンドウの基本設定
- モード設定マネージャの初期化
- シグナル・スロット接続
- 多重起動防止
- スプリッターイベント設定

### 推奨リファクタリング案

```python
def __init__(self, mode_config_path=None, app=None):
    """初期化処理"""
    super().__init__()
    self._init_basic_attributes(mode_config_path, app)
    self._init_mutex_and_single_instance()
    self._setup_window_properties()
    self._connect_signals()
    self._setup_splitters()
    self.initializer()
```

**推奨度: ★★★★☆**

---

## 3. 長大メソッド群の分割

### 3.1 _set_scrollarea_size_2 (133行)

**問題:** スクロールエリアのサイズ計算ロジックが複雑

**推奨案:**
```python
def _set_scrollarea_size_2(self):
    """スクロールエリアのサイズを設定"""
    heights = self._calculate_widget_heights()
    total_height = self._sum_visible_heights(heights)
    self._apply_scrollarea_size(total_height)

def _calculate_widget_heights(self) -> dict:
    """各ウィジェットの高さを計算"""
    ...

def _sum_visible_heights(self, heights: dict) -> int:
    """表示中のウィジェット高さを合計"""
    ...

def _apply_scrollarea_size(self, total_height: int):
    """計算された高さをスクロールエリアに適用"""
    ...
```

**推奨度: ★★★☆☆**

---

### 3.2 check_type_line_edit_and_verify_text (122行)

**問題:** 型チェックとテキスト検証のロジックが長大

**推奨案:**
```python
def check_type_line_edit_and_verify_text(self, line_widget_obj, text):
    """型チェックとテキスト検証のエントリポイント"""
    data_type = self._get_data_type(line_widget_obj)
    validator = self._get_validator(data_type)
    return validator.validate(text, line_widget_obj)

class TextValidator:
    """テキスト検証クラス"""
    def validate_int(self, text, widget): ...
    def validate_float(self, text, widget): ...
    def validate_postnum(self, text, widget): ...
    # ... 各型ごとの検証メソッド
```

**推奨度: ★★★★☆** - 型ごとの検証ロジックが分離され、保守性向上

---

### 3.3 conversion_inputted_text (114行)

**問題:** テキスト変換ロジックが複雑

**推奨案:**
```python
def conversion_inputted_text(self, line_widget_obj, text):
    """テキスト変換のエントリポイント"""
    conversion_type = self._get_conversion_type(line_widget_obj)
    converter = self._get_converter(conversion_type)
    return converter.convert(text)

class TextConverter:
    """テキスト変換クラス"""
    def convert_zenkaku_to_hankaku(self, text): ...
    def convert_hankaku_to_zenkaku(self, text): ...
    # ... 各変換タイプごとのメソッド
```

**推奨度: ★★★★☆**

---

### 3.4 output_log (104行)

**問題:** ログ出力ロジックが長大で、MyMainWindowの状態に強く依存

**推奨案 (現時点では保留):**

前回の分析で、`output_log`は以下の理由で分離が困難と判断:
- 10個以上のMyMainWindow属性に依存
- 分離すると引数が10個以上になり、かえって複雑化
- 内部でのメソッド分割は可能

```python
def output_log(self):
    """ログ出力メイン処理"""
    log_data = self._prepare_log_data()
    log_df = self._create_log_dataframe(log_data)
    self._write_log_to_file(log_df)

def _prepare_log_data(self) -> dict:
    """ログデータを準備"""
    return {
        'timestamp': self._get_timestamp(),
        'item': self._get_current_item(),
        'new1_user_name': self.user_name if self.input_mode == 'new1' else '',
        # ...
    }
```

**推奨度: ★★☆☆☆** - 分離より内部メソッド分割が適切

---

## 4. 重複コード・パターンの抽出

### 4.1 辞書作成パターン

`initializer`内で繰り返されるパターン:

```python
# 現状 (L644-650)
self.obj_name_to_info_dict = {data['line_edit_name']: data['info'] for data in self.data_list}
self.obj_name_to_display_name_dict = {data['line_edit_name']: data['display_name'] for data in self.data_list}
self.obj_name_to_name_dict = {data['line_edit_name']: data['name'] for data in self.data_list}
self.obj_name_to_type_dict = {data['line_edit_name']: data['data_type'] for data in self.data_list}
self.obj_name_to_index_dict = {data['line_edit_name']: data['index'] for data in self.data_list}
self.obj_name_to_ime_dict = {data['line_edit_name']: data['ime_mode'] for data in self.data_list}
self.label_name_to_type_dict = {data['name']: data['data_type'] for data in self.data_list}
```

**推奨案:**

```python
def _create_mapping_dicts(self):
    """data_listから各種マッピング辞書を作成"""
    mappings = [
        ('obj_name_to_info_dict', 'line_edit_name', 'info'),
        ('obj_name_to_display_name_dict', 'line_edit_name', 'display_name'),
        ('obj_name_to_name_dict', 'line_edit_name', 'name'),
        ('obj_name_to_type_dict', 'line_edit_name', 'data_type'),
        ('obj_name_to_index_dict', 'line_edit_name', 'index'),
        ('obj_name_to_ime_dict', 'line_edit_name', 'ime_mode'),
        ('label_name_to_type_dict', 'name', 'data_type'),
    ]

    for attr_name, key_field, value_field in mappings:
        setattr(self, attr_name, {
            data[key_field]: data[value_field]
            for data in self.data_list
        })
```

**推奨度: ★★★☆☆**

---

### 4.2 オブジェクト検索パターン

`initializer`内で繰り返される検索パターン (L719-746):

```python
# 現状
for data in self.data_list:
    for line_edit_obj in self.scrollArea_input.findChildren(QtWidgets.QLineEdit):
        if data['line_edit_name'] == line_edit_obj.objectName():
            data['line_edit_obj'] = line_edit_obj

for data in self.data_list:
    for line_edit_obj in self.scrollArea_input.findChildren(QtWidgets.QLabel):
        if data['label_name'] == line_edit_obj.objectName():
            data['label_obj'] = line_edit_obj
```

**推奨案:**

```python
def _assign_qt_objects_to_data_list(self):
    """data_listに各種Qtオブジェクトを割り当て"""
    assignments = [
        ('line_edit_obj', 'line_edit_name', QtWidgets.QLineEdit, self.scrollArea_input),
        ('label_obj', 'label_name', QtWidgets.QLabel, self.scrollArea_input),
        ('frame_a_obj', 'frame_a_name', QtWidgets.QFrame, self.scrollArea_input),
        ('frame_b_obj', 'frame_b_name', QtWidgets.QFrame, self.frame_input_right),
        ('layout_a_obj', 'layout_a_name', QtWidgets.QHBoxLayout, self.scrollArea_input),
        ('layout_b_obj', 'layout_b_name', QtWidgets.QHBoxLayout, self.frame_input_right),
    ]

    for obj_key, name_key, widget_class, parent in assignments:
        self._assign_widgets(obj_key, name_key, widget_class, parent)

def _assign_widgets(self, obj_key, name_key, widget_class, parent):
    """指定されたウィジェットをdata_listに割り当て"""
    widgets = {w.objectName(): w for w in parent.findChildren(widget_class)}
    for data in self.data_list:
        obj_name = data.get(name_key)
        if obj_name and obj_name in widgets:
            data[obj_key] = widgets[obj_name]
```

**推奨度: ★★★★☆** - 検索効率も改善される

---

## 5. 実装優先順位まとめ

### Phase 1: 即座に実行可能（低リスク・高効果）

1. **initializer メソッドの分割** (★★★★★)
   - 641行 → 18個のメソッド（各30-80行程度）
   - 推定削減: 純粋な削減はないが、可読性が大幅向上
   - リスク: 低（機械的な抽出が可能）

2. **オブジェクト検索パターンの統一** (★★★★☆)
   - 重複コードの削減と検索効率の改善
   - 推定削減: 30-40行
   - リスク: 低

### Phase 2: 中期的に実行可能（中リスク・高効果）

3. **check_type_line_edit_and_verify_text の分割** (★★★★☆)
   - 122行 → 型別検証クラスに分離
   - 推定削減: 分離により構造改善
   - リスク: 中（検証ロジックの網羅的テストが必要）

4. **conversion_inputted_text の分割** (★★★★☆)
   - 114行 → 変換タイプ別クラスに分離
   - 推定削減: 分離により構造改善
   - リスク: 中

5. **__init__ メソッドの分割** (★★★★☆)
   - 198行 → 5-6個のメソッド
   - リスク: 中

### Phase 3: 長期的に検討（高リスク・中効果）

6. **_set_scrollarea_size_2 の分割** (★★★☆☆)
   - リスク: 中（UI計算ロジックのため注意が必要）

7. **output_log の内部メソッド分割** (★★☆☆☆)
   - 別クラスへの分離ではなく、内部の小メソッド化
   - リスク: 低

---

## 6. 具体的な実装例: initializer の分割

### ステップ1: _init_basic_setup メソッド抽出

```python
def _init_basic_setup(self):
    """基本的なUIセットアップ"""
    if not self.is_first_init:
        self.init_config()
    self.hide()
    if self.centralWidget() is not None:
        self.centralWidget().destroy()
    self.setupUi(self)
    self.main_mode_init = 'payroll'

    # Graphics view setup
    self.graphicsView_main.setUpdatesEnabled(False)
    self.custom_event_filter_for_graphics_view = CustomEventFilterForGraphicsView(self)
    self.graphicsView_main.viewport().installEventFilter(self.custom_event_filter_for_graphics_view)
    self.window = self
    self.setWindowTitle('テストタイトル')
```

### ステップ2: _init_test_variables メソッド抽出

```python
def _init_test_variables(self):
    """テスト・デバッグ用変数の初期化"""
    self.is_debug = False
    if getattr(sys, 'frozen', False):
        self.is_test_button_show = False
    else:
        self.is_test_button_show = True

    debug_dict = {0: 'new1', 1: 'ver1'}
    if self.is_debug:
        self.test_mode = debug_dict[0]
        self.test_user_name = 'テスト太郎'
        test_img_path = './Sample名刺2枚'
        test_output_path = './Sample名刺2枚'
        self.test_img_dir_path = str(Path(test_img_path).absolute())
        self.test_output_path = str(Path(test_output_path).absolute())
        self.test_is_rept_mode = True
        try:
            os.remove(r"C:\myPython\_QtDesigner\_入力アプリ画像付き\Sample名刺2枚\Sample名刺2枚_NEW1.csv")
        except:
            pass
```

### ステップ3: initializer を簡潔化

```python
def initializer(self):
    """アプリケーションの初期化処理

    各種サブ初期化メソッドを順番に呼び出して、
    アプリケーション全体を初期化します。
    """
    # Phase 1: 基本設定
    self._init_basic_setup()
    self._init_test_variables()
    self._init_logger_and_icons()
    self._init_instance_variables()

    # Phase 2: モード・設定
    self._init_mode_configuration()
    self._init_config_and_dialog()

    if self.is_close_button_pressed:
        return

    # Phase 3: データ構造
    self._init_data_list_setup()
    self._init_dictionaries()
    self._init_rect_config()

    # Phase 4: UIオブジェクト割り当て
    self._assign_objects_to_data_list()
    self._init_widget_visibility()
    self._init_additional_dictionaries()

    # Phase 5: 外観設定
    self._init_palette_and_colors()

    # Phase 6: ファイル・データ読み込み
    self._init_file_paths()
    self._init_graphics_view_setup()
    self._init_csv_and_list_widgets()

    # Phase 7: 最終設定
    self._init_final_setup()
```

---

## 7. テスト戦略

リファクタリング実施時は以下のテストを推奨:

### 7.1 リグレッションテスト
- [ ] アプリケーションの起動確認
- [ ] 各モード（payroll, factory, prevention等）での動作確認
- [ ] new1, ver1モードでの動作確認
- [ ] 画像モード、PDFモードの切り替え確認

### 7.2 機能テスト
- [ ] LineEdit入力・検証の動作確認
- [ ] データ保存・読み込みの確認
- [ ] イベントフィルタの動作確認
- [ ] UI表示の確認（レイアウト、色、アイコン）

---

## 8. 結論

**最優先事項:** `initializer` メソッドの分割 (641行 → 18メソッド)

**理由:**
1. 最も長大で複雑なメソッド
2. セクションが明確で、機械的な分割が可能
3. リスクが低く、効果が高い
4. 将来的な修正・拡張の基盤となる

**次のステップ:**
1. initializerを18個のサブメソッドに分割
2. 重複パターン（辞書作成、オブジェクト検索）の統一
3. check_type_line_edit_and_verify_text の型別クラスへの分離
4. conversion_inputted_text の変換タイプ別クラスへの分離

---

**注意:** いずれのリファクタリングも、実施前に必ずバックアップを取り、段階的にテストを行うことを推奨します。
