"""
定数取得関数

アプリケーション全体で使用される定数や設定辞書を提供する関数群。
"""

from PyQt5.QtCore import Qt


def _get_init_config_dict():
    """初期設定辞書を取得

    Returns:
        dict: 初期設定の辞書
    """
    return {
        'splitter_1a_height': 600, 'splitter_1b_height': 200,
        'splitter_2a_width': 1000, 'splitter_2b_width': 200,
        'splitter_3a_width': 800, 'splitter_3b_width': 200,
        'splitter_4a_height': 400, 'splitter_4b_height': 200,
        'splitter_5a_height': 100, 'splitter_5b_height': 600,
        'splitter_6a_width': 200, 'splitter_6b_width': 50,
        'is_maximized_screen': True, 'window_width': 0, 'window_height': 0,
        'current_angle': 0, 'current_scale': 1.0,
        'username': '', 'img_dir_path': '', 'output_path': '',
        'img_dir_parent_path': '', 'output_parent_path': '',
        'input_mode': 'new1', 'is_copy_csv_path': True, 'encode_type': 'cp932',
        'collation_dialog_width': 500, 'collation_dialog_height': 350, 'auto_move': False,
        'is_rect_show': False, 'layout_type': 'v', 'is_info_show': True, "is_rept": False,
        'delta_scale': 0.1, 'main_mode': 'foreigner', 'max_side_length': 10000, 'matrix': 2,
        'insert_char': '●', 'insert_char2': '（韓国語のため内容不明）', 'insert_char3': '（他言語のため内容不明）',
        'is_show_rect_frame': True,
    }


def _get_delta_scale_dicts():
    """スケール設定辞書を取得

    Returns:
        tuple: (index_to_delta_scale_dict, delta_scale_to_index_dict)
    """
    index_to_delta = {0: 0.01, 1: 0.02, 2: 0.05, 3: 0.1, 4: 0.15, 5: 0.2, 6: 0.3}
    delta_to_index = {v: k for k, v in index_to_delta.items()}
    return index_to_delta, delta_to_index


def _get_encode_dicts():
    """エンコーディング辞書を取得

    Returns:
        tuple: (name_to_encode_dict, encode_to_name_dict)
    """
    name_to_encode = {
        'UTF-8': 'utf-8', 'Sjift_JIS': 'shift_jis', 'UTF-8 with BOM': 'utf-8-sig',
        'CP932': 'cp932', 'UTF-16 LE': 'utf-16-le', 'UTF-16 BE': 'utf-16-be'
    }
    encode_to_name = {v: k for k, v in name_to_encode.items()}
    return name_to_encode, encode_to_name


def _get_global_color_dict():
    """グローバル色辞書を取得

    Returns:
        dict: 色設定の辞書
    """
    return {
        'black': Qt.GlobalColor.black,
        'red': Qt.GlobalColor.red
    }
