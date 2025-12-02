# initializer メソッドを18個のサブメソッドに自動分割するスクリプト
# このスクリプトは、セクションの境界を特定してサブメソッドとして抽出します

import re

# MAIN_APP.pyを読み込む
with open('MAIN_APP.py', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# セクション定義（コメントやコードの特徴から境界を検出）
sections = [
    # 既に分割済み
    # ("_init_basic_setup", "if not self.is_first_init:", "self.setWindowTitle('テストタイトル')"),
    # ("_init_test_variables", "# ************************** テスト用変数開始", "# ************************** テスト用変数終了"),
    # ("_init_logger_and_icons", "# ロガーの設定", "icon_path = None"),

    # これから分割
    ("_init_instance_variables", "# ******** インスタンス変数設定 ********", "self.config_dict = None"),
    ("_init_mode_configuration", "# ========== モード設定", "self.data_list_payroll ="),
    ("_init_config_and_dialog", "# 初期設定辞書の取得", "self.setWindowTitle(self.mode_config_manager"),
    ("_init_data_list_setup", "self.is_multi_pdf_mode =", "# ****** メインデータリスト設定 終了"),
    ("_init_dictionaries", "self.obj_name_to_info_dict =", "# type_info_dictの確認 終了"),
    ("_init_rect_config", "self.rect_path = './data/rect.json'", "self.rect_config_manager.write(self.rect_config)"),
    ("_assign_objects_to_data_list", "# ************* data_listにオブジェクトを追加 開始", "# ************* data_listにオブジェクトを追加 終了"),
    ("_init_widget_visibility", "# is_showが Falseを非表示にする", "data['frame_b_obj'].hide()"),
]

# 現在のファイル構造を確認
print("現在のMAIN_APP.pyの構造を確認...")
print("ファイル全体の行数:", len(lines))

# 各セクションを見つける
for section_name, start_marker, end_marker in sections:
    start_line = -1
    end_line = -1

    for i, line in enumerate(lines):
        if start_marker in line and start_line == -1:
            start_line = i + 1  # 1-based
        if end_marker in line and start_line != -1 and end_line == -1:
            end_line = i + 1
            break

    if start_line != -1 and end_line != -1:
        print(f"{section_name}: L{start_line}-L{end_line} ({end_line - start_line + 1}行)")
    else:
        print(f"{section_name}: 見つかりません (start:{start_line}, end:{end_line})")

print("\n分割作業を手動で続行する必要があります。")
print("各セクションのメソッドを作成し、最後にinitializerメソッドを簡潔に書き換えます。")
