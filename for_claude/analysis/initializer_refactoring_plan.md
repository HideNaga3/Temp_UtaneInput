# initializer メソッド分割計画

## 現状

- initializerメソッド：L337-L1177（841行）
- 既に分割済み：
  - `_init_basic_setup()` - 基本UI設定
  - `_init_test_variables()` - テスト変数
  - `_init_logger_and_icons()` - ロガー・アイコン（途中）

## 分割計画

### Phase 1: 残りのヘルパーメソッドを作成

各セクションを個別のメソッドとして作成：

1. ✅ `_init_basic_setup()` - L337-391
2. ✅ `_init_test_variables()` - L392-417
3. 🔄 `_init_logger_and_icons()` - L418-453
4. ⏳ `_init_instance_variables()` - L454-548
5. ⏳ `_init_mode_configuration()` - L550-593
6. ⏳ `_init_config_and_dialog()` - L594-622
7. ⏳ `_init_data_list_setup()` - L623-639
8. ⏳ `_init_dictionaries()` - L644-698
9. ⏳ `_init_rect_config()` - L700-717
10. ⏳ `_assign_objects_to_data_list()` - L718-754
11. ⏳ `_init_widget_visibility()` - L755-773
12. ⏳ `_init_additional_dictionaries()` - L774-802
13. ⏳ `_init_palette_and_colors()` - L803-856
14. ⏳ `_init_file_paths()` - L844-856の一部
15. ⏳ `_init_graphics_view_setup()` - L857-914
16. ⏳ `_init_csv_and_list_widgets()` - L865-942
17. ⏳ `_init_event_filters_and_connections()` - L943-1124
18. ⏳ `_init_final_setup()` - L1125-1177

### Phase 2: initializer メソッド本体を簡潔化

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
    self._init_event_filters_and_connections()
    self._init_final_setup()
```

## 実行方法

### オプションA: 段階的リファクタリング（推奨 - 安全）
1. 各セクションを一つずつサブメソッドとして作成
2. 作成したら、元のinitializer内の該当コードをメソッド呼び出しに置き換え
3. テストして動作確認
4. 次のセクションへ

### オプションB: 一括リファクタリング（速い - リスク高）
1. 全てのサブメソッドを一度に作成
2. 新しいinitializerメソッドを作成
3. 元のinitializerメソッドを削除
4. テスト

## 推奨: オプションA（段階的）

安全のため、オプションAで進めます。
