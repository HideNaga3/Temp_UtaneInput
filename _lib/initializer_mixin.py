"""
初期化処理を提供するMixinクラス

MyMainWindowの初期化関連メソッドを集約したMixinクラス。
MAIN_APP.pyの可読性を向上させるため、初期化ロジックを分離。
"""

import os
import sys
import time
import traceback
from pathlib import Path
import pandas as pd
from typing import TYPE_CHECKING
from pprint import pprint as pp

from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import QMessageBox, QShortcut, QAbstractItemView, QListWidgetItem, QLineEdit
from PyQt5.QtGui import QIcon, QPalette, QColor, QKeySequence
from PyQt5 import QtWidgets

from ._data_io import DataIO
from ._draggable_pixmap_item import DraggablePixmapItem
from ._event_filters import (
    CustomEventFilterForGraphicsView,
    CustomEventFilterForButtonScrollArea,
    CustomEventFilterForLineEditScale
)
from ._config_manager import ConfigManager, RectConfigManager
from ._create_logger import create_logger
from ._main_data import MainData
from ._constants import (
    _get_init_config_dict,
    _get_delta_scale_dicts,
    _get_encode_dicts,
    _get_global_color_dict
)

if TYPE_CHECKING:
    from _lib._mode_config import ModeConfigManager

class InitializerMixin:
    """初期化処理を提供するMixinクラス

    このクラスは単独で使用されることを想定しておらず、
    MyMainWindowクラスと多重継承される必要があります。

    すべてのメソッドは self を通じてMyMainWindowの属性にアクセスします。
    """

    def _init_type_hints(self):
        """UIウィジェットのタイプヒント設定

        PyQt5で自動生成されるウィジェットに対して、型アノテーションを提供します。
        これにより、IDEの型補完機能が正しく動作します。
        """
        ############################## ここからタイプヒント #############################
        self.pushButton_cw: QtWidgets.QPushButton
        self.pushButton_ccw: QtWidgets.QPushButton
        self.pushButton_zoomin: QtWidgets.QPushButton
        self.pushButton_zoomout: QtWidgets.QPushButton
        self.graphicsView_main: QtWidgets.QGraphicsView
        self.pushButton_test: QtWidgets.QPushButton
        self.pushButton_test_2: QtWidgets.QPushButton
        self.label_angle_label: QtWidgets.QLabel
        self.label_scale: QtWidgets.QLabel
        self.pushButton_fit_w: QtWidgets.QPushButton
        self.pushButton_fit_h: QtWidgets.QPushButton
        self.splitter: QtWidgets.QSplitter
        self.splitter_2: QtWidgets.QSplitter
        self.scrollArea_input: QtWidgets.QScrollArea
        self.pushButton_reset_scale: QtWidgets.QPushButton
        self.listWidget_filepath: QtWidgets.QListWidget
        self.listWidget_pdf: QtWidgets.QListWidget
        self.frame_3_spacing: QtWidgets.QFrame
        self.frame_input_1: QtWidgets.QFrame
        self.frame_splitter_below: QtWidgets.QFrame
        self.frame_splitter_after: QtWidgets.QFrame
        self.tabWidget: QtWidgets.QTabWidget
        self.label_username: QtWidgets.QLabel
        self.label_input_mode: QtWidgets.QLabel
        self.lineEdit_angle: QtWidgets.QLineEdit
        self.lineEdit_scale: QtWidgets.QLineEdit
        self.pushButton_select_folder: QtWidgets.QPushButton
        self.scrollAreaWidgetContents: QtWidgets.QWidget
        self.scrollAreaWidgetContents_2: QtWidgets.QWidget
        self.pushButton_goto_tab_index_0: QtWidgets.QPushButton
        self.centralwidget: QtWidgets.QWidget
        self.pushButton_rect_set: QtWidgets.QPushButton
        self.pushButton_rect_get: QtWidgets.QPushButton
        self.frame_test_button: QtWidgets.QFrame
        self.frame_rect_select: QtWidgets.QFrame
        self.radioButton_automove_on: QtWidgets.QRadioButton
        self.radioButton_automove_off: QtWidgets.QRadioButton
        self.radioButton_rect_show: QtWidgets.QRadioButton
        self.radioButton_rect_hide: QtWidgets.QRadioButton
        self.radioButton_rect_select: QtWidgets.QRadioButton
        self.radioButton_rect_move: QtWidgets.QRadioButton
        self.frame_input_right: QtWidgets.QFrame
        self.scrollArea_input_right: QtWidgets.QScrollArea
        self.radioButton_layout_vertival: QtWidgets.QRadioButton
        self.radioButton_layout_horizontal: QtWidgets.QRadioButton

        self.label_0_: QtWidgets.QLabel
        self.label_1_: QtWidgets.QLabel
        self.label_2_: QtWidgets.QLabel
        self.label_3_: QtWidgets.QLabel

        self.frame_0_: QtWidgets.QFrame
        self.frame_1_: QtWidgets.QFrame
        self.frame_2_: QtWidgets.QFrame
        self.frame_3_: QtWidgets.QFrame

        self.horizontalLayout_0_: QtWidgets.QHBoxLayout
        self.horizontalLayout_1_: QtWidgets.QHBoxLayout
        self.horizontalLayout_2_: QtWidgets.QHBoxLayout
        self.horizontalLayout_3_: QtWidgets.QHBoxLayout

        self.lineEdit_0_: QtWidgets.QLineEdit
        self.lineEdit_1_: QtWidgets.QLineEdit
        self.lineEdit_2_: QtWidgets.QLineEdit
        self.lineEdit_3_: QtWidgets.QLineEdit

        self.verticalLayout_left_input: QtWidgets.QVBoxLayout
        self.frame_rect_all: QtWidgets.QFrame
        self.horizontalLayout_for_right_list = QtWidgets.QHBoxLayout
        self.horizontalLayout_for_left_list = QtWidgets.QHBoxLayout

        self.splitter_3: QtWidgets.QSplitter
        self.splitter_4: QtWidgets.QSplitter
        self.frame_for_right_list: QtWidgets.QFrame
        self.scrollArea_top: QtWidgets.QScrollArea
        self.splitter_5: QtWidgets.QSplitter
        self.frame_of_below_scrollarea: QtWidgets.QFrame
        self.label_infomation: QtWidgets.QLabel
        self.label_infomation_right: QtWidgets.QLabel
        self.radioButton_info_hide: QtWidgets.QRadioButton
        self.radioButton_info_show: QtWidgets.QRadioButton
        self.frame_rect_all: QtWidgets.QFrame
        self.label_main_mode: QtWidgets.QLabel
        self.lineEdit_angle: QtWidgets.QLineEdit
        self.label_angle: QtWidgets.QLabel
        self.comboBox_delta: QtWidgets.QComboBox
        self.pushButton_help: QtWidgets.QPushButton
        self.frame_rect_show_hide: QtWidgets.QFrame
        self.verticalLayout_input_right: QtWidgets.QVBoxLayout
        self.pixmap_item: DraggablePixmapItem
        self.label_pdf: QtWidgets.QLabel
        self.frame_pdf: QtWidgets.QFrame
        self.gridLayout_bottom_scroll_area: QtWidgets.QGridLayout
        self.frame_input_below: QtWidgets.QFrame
        self.verticalLayout_frame_input_below: QtWidgets.QVBoxLayout
        self.listWidget_pdf_record: QtWidgets.QListWidget
        self.frame_splitter_list: QtWidgets.QFrame
        self.splitter_6: QtWidgets.QSplitter
        self.plainTextEdit_explain_2: QtWidgets.QPlainTextEdit
        self.plainTextEdit_explain: QtWidgets.QPlainTextEdit
        self.pushButton_change_view_mode: QtWidgets.QPushButton
        self.frame_rect_mode: QtWidgets.QFrame
        self.pushButton_check_encode: QtWidgets.QPushButton

        ############################## ここまでタイプヒント ############################ __hint__

    def _init_shortcut_keys(self):
        """ショートカットキー設定"""
        # 画像操作: Ctrl+1〜7
        self.shortcut_ctrl_1 = QShortcut(QKeySequence("Ctrl+1"), self)
        self.shortcut_ctrl_1.activated.connect(lambda: self.rotate_image(-90, is_button=True))
        self.shortcut_ctrl_2 = QShortcut(QKeySequence("Ctrl+2"), self)
        self.shortcut_ctrl_2.activated.connect(lambda: self.rotate_image(90, is_button=True))
        self.shortcut_ctrl_3 = QShortcut(QKeySequence("Ctrl+3"), self)
        self.shortcut_ctrl_3.activated.connect(lambda: self.scaling_image(-0.1, is_button=True))
        self.shortcut_ctrl_4 = QShortcut(QKeySequence("Ctrl+4"), self)
        self.shortcut_ctrl_4.activated.connect(lambda: self.scaling_image(0.1, is_button=True))
        self.shortcut_ctrl_5 = QShortcut(QKeySequence("Ctrl+5"), self)
        self.shortcut_ctrl_5.activated.connect(lambda: self.adjust_image('w', is_button=True))
        self.shortcut_ctrl_6 = QShortcut(QKeySequence("Ctrl+6"), self)
        self.shortcut_ctrl_6.activated.connect(lambda: self.adjust_image('h', is_button=True))
        self.shortcut_ctrl_7 = QShortcut(QKeySequence("Ctrl+7"), self)
        self.shortcut_ctrl_7.activated.connect(lambda: self.scaling_image(0, is_reset=True, is_button=True))

        # 矩形・再起動: Ctrl+R, Ctrl+Shift+R, Ctrl+Shift+Alt+R, Ctrl+F
        self.shortcut_ctrl_R = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcut_ctrl_R.activated.connect(lambda: self.pressed_get_rect())
        self.shortcut_ctrl_shift_R = QShortcut(QKeySequence("Ctrl+Shift+R"), self)
        self.shortcut_ctrl_shift_R.activated.connect(lambda: self.copy_rect_from_previous()) # 前回と同じ矩形を設定
        self.shortcut_ctrl_shift_alt_R = QShortcut(QKeySequence("Ctrl+Alt+R"), self)
        self.shortcut_ctrl_shift_alt_R.activated.connect(lambda: self.fill_rect_json_null_with_previous()) # rect_jsonをnullから前回値で埋める
        self.shortcut_ctrl_shift_alt_R = QShortcut(QKeySequence("Ctrl+Shift+Alt+R"), self)
        self.shortcut_ctrl_shift_alt_R.activated.connect(lambda: self.reset_rect_json_to_null()) # rect_jsonをnullにリセット

        self.shortcut_ctrl_F = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_ctrl_F.activated.connect(lambda: self.restart_app(is_button_pressed=True))

        # スクロール操作: Ctrl+I/J/K/L (Vim風)
        self.shortcut_ctrl_i = QShortcut(QKeySequence("Ctrl+I"), self)
        self.shortcut_ctrl_i.activated.connect(lambda: self.scroll_to_position(self.graphicsView_main, 'up'))
        self.shortcut_ctrl_k = QShortcut(QKeySequence("Ctrl+K"), self)
        self.shortcut_ctrl_k.activated.connect(lambda: self.scroll_to_position(self.graphicsView_main, 'down'))
        self.shortcut_ctrl_j = QShortcut(QKeySequence("Ctrl+J"), self)
        self.shortcut_ctrl_j.activated.connect(lambda: self.scroll_to_position(self.graphicsView_main, 'left'))
        self.shortcut_ctrl_l = QShortcut(QKeySequence("Ctrl+L"), self)
        self.shortcut_ctrl_l.activated.connect(lambda: self.scroll_to_position(self.graphicsView_main, 'right'))
        # ASDW
        # self.shortcut_ctrl_w = QShortcut(QKeySequence("Ctrl+W"), self)
        # self.shortcut_ctrl_w.activated.connect(lambda: self.scroll_to_position(self.graphicsView_main, 'up'))
        # self.shortcut_ctrl_s = QShortcut(QKeySequence("Ctrl+S"), self)
        # self.shortcut_ctrl_s.activated.connect(lambda: self.scroll_to_position(self.graphicsView_main, 'down'))
        # self.shortcut_ctrl_a = QShortcut(QKeySequence("Ctrl+A"), self)
        # self.shortcut_ctrl_a.activated.connect(lambda: self.scroll_to_position(self.graphicsView_main, 'left'))
        # self.shortcut_ctrl_d = QShortcut(QKeySequence("Ctrl+D"), self)
        # self.shortcut_ctrl_d.activated.connect(lambda: self.scroll_to_position(self.graphicsView_main, 'right'))

        # テスト: Ctrl+T
        self.shortcut_ctrl_t = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcut_ctrl_t.activated.connect(lambda: self.on_test_button_pressed_2())

        # ページ移動: PageUp/PageDown (PDFモード)
        # self.shortcut_ctrl_d = QShortcut(QKeySequence("Alt+Down"), self)
        # self.shortcut_ctrl_d.activated.connect(lambda: self.show_dd_list_widget(self.get_focused_line_edit_obj()))
        self.shortcut_pgup = QShortcut(QKeySequence("PageUp"), self)
        self.shortcut_pgdn = QShortcut(QKeySequence("PageDown"), self)
        if self.is_single_pdf_mode:
            self.shortcut_pgup.activated.connect(lambda: self.select_item_for_list_widget_for_pdf(-1))
            self.shortcut_pgdn.activated.connect(lambda: self.select_item_for_list_widget_for_pdf(1))

        # 入力フィールド移動: Ctrl+Up/Down
        self.shortcut_ctrl_down = QShortcut(QKeySequence("Ctrl+Down"), self)
        self.shortcut_ctrl_down.activated.connect(lambda: self.goto_first_or_last_line_edit(mode='last'))
        self.shortcut_ctrl_up = QShortcut(QKeySequence("Ctrl+Up"), self)
        self.shortcut_ctrl_up.activated.connect(lambda: self.goto_first_or_last_line_edit(mode='first'))

        # 日付入力: Ctrl+;
        self.shortcut_ctrl_semicolon = QShortcut(QKeySequence("Ctrl+;"), self)
        self.shortcut_ctrl_semicolon.activated.connect(lambda: self.set_today_text())

        # 画面モード切替: F7
        # self.shortcut_f11 = QShortcut(QKeySequence("F11"), self)
        # self.shortcut_f11.activated.connect(lambda: self.set_screen_mode_toggle())
        self.shortcut_f7 = QShortcut(QKeySequence("F7"), self)
        self.shortcut_f7.activated.connect(lambda: self.set_screen_mode_toggle())

        # スクロールバー操作: Ctrl+Shift+Up/Down
        self.shortcut_ctrl_shift_up = QShortcut(QKeySequence("Ctrl+Shift+Up"), self)
        self.shortcut_ctrl_shift_up.activated.connect(lambda: self.set_value_to_scrollbar('up'))
        self.shortcut_ctrl_shift_down = QShortcut(QKeySequence("Ctrl+Shift+Down"), self)
        self.shortcut_ctrl_shift_down.activated.connect(lambda: self.set_value_to_scrollbar('down'))

        # エンコーディングチェック: Alt+E
        self.shortcut_alt_e = QShortcut(QKeySequence("Alt+E"), self)
        self.shortcut_alt_e.activated.connect(self.check_encoding_line_edits)

    def _init_basic_setup(self):
        """基本的なUIセットアップとウィジェット検証"""
        if not self.is_first_init:
            self.init_config()
        self.hide()
        if self.centralWidget() is not None:
            self.centralWidget().destroy()
        self.setupUi(self)
        # self.main_mode_init = 'payroll' # ! exe 初期モード設定
        # ************** ウィジェット確認用 開始 **************
        """
        frame_names = [obj.objectName() for obj in self.scrollArea_input.findChildren(QtWidgets.QFrame) if obj.objectName().startswith('frame_') ]
        layout_names = [obj.layout().objectName() for obj in self.scrollArea_input.findChildren(QtWidgets.QFrame) if obj.objectName().startswith('frame_') ]
        frame_names_2 = [obj.objectName() for obj in self.frame_input_right.findChildren(QtWidgets.QFrame) if obj.objectName().startswith('frame_') ]
        layouts_name_2 = [obj.layout().objectName() for obj in self.frame_input_right.findChildren(QtWidgets.QFrame) if obj.objectName().startswith('frame_') ]
        lineedit_names = [obj.objectName() for obj in self.scrollArea_input.findChildren(QtWidgets.QLineEdit)]
        label_names = [obj.objectName() for obj in self.scrollArea_input.findChildren(QtWidgets.QLabel) if obj.objectName().startswith('label_')]
        for li in [frame_names, lineedit_names, label_names, layout_names]:
            li.sort(key=lambda x: int(x.split('_')[1]))
        frame_names_2.sort(key=lambda x: int(x.split('__')[1]))
        layouts_name_2.sort(key=lambda x: int(x.split('__')[1]))
        for i, fn in enumerate(frame_names):
            if not fn.startswith('frame_') or not fn.endswith('_') or not i == int(fn.split('_')[1]):
                raise ValueError(f'frame_name: {fn}')
        for i, fn in enumerate(frame_names_2):
            if not fn.startswith('frame__') or not fn.endswith('__') or not i == int(fn.split('__')[1]):
                raise ValueError(f'frame_name: {fn}')
        for i, ldn in enumerate(lineedit_names):
            if not ldn.startswith('lineEdit_') or not ldn.endswith('_') or not i == int(ldn.split('_')[1]):
                raise ValueError(f'lineEdit_name: {ldn}')
        for i, ln in enumerate(label_names):
            if not ln.startswith('label_') or not ln.endswith('_') or not i == int(ln.split('_')[1]):
                raise ValueError(f'label_name: {ln}')
        for i, l in enumerate(layout_names):
            if not l.startswith('horizontalLayout_') or not l.endswith('_') or not i == int(l.split('_')[1]):
                raise ValueError(f'layout_name: {l}')
        for i, l in enumerate(layouts_name_2):
            if not l.startswith('horizontalLayout__') or not l.endswith('__') or not i == int(l.split('__')[1]):
                raise ValueError(f'layout_name: {l}')
        # print(frame_names)
        # print(frame_names_2)
        # print(lineedit_names)
        # print(label_names)
        for i, li in enumerate([frame_names, frame_names_2, lineedit_names, label_names, layout_names, layouts_name_2]):
            li = [f'{j:03} {item}' for (j, item) in enumerate(li)]
            text = '\n'.join(li)
            with open(f'{i:05}.txt', 'w') as f:
                f.write(text)
        # """
        # ************** ウィジェット確認用 終了 **************
        self.graphicsView_main.setUpdatesEnabled(False)
        self.custom_event_filter_for_graphics_view = CustomEventFilterForGraphicsView(self)
        self.graphicsView_main.viewport().installEventFilter(self.custom_event_filter_for_graphics_view)
        self.window = self
        self.setWindowTitle('テストタイトル')

    def _init_test_variables(self):
        """テスト・デバッグ用変数の初期化"""
        # ************************** テスト用変数開始 **************************
        self.is_debug = False
        if getattr(sys, 'frozen', False): # 実行ファイルの場合
            self.is_test_button_show = False # False固定
        else:
            # テストボタンを表示するかどうかのフラグ...
            self.is_test_button_show = True
        debug_dict = {0: 'new1', 1: 'ver1'}
        if self.is_debug:
            self.test_mode = debug_dict[
                    0
            ]
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
        # ************************** テスト用変数終了 **************************

    def _init_logger_and_icons(self):
        """ロガーとアイコンパスの設定"""
        # ロガーの設定
        error_log_path = os.path.abspath('./data/error.log')
        self.log_ = create_logger(error_log_path)
        # アイコンのパスを取得
        self.widgets_require_icon = [
                self.pushButton_cw, self.pushButton_ccw, self.pushButton_zoomin, self.pushButton_zoomout,
                self.pushButton_fit_w, self.pushButton_fit_h, self.pushButton_reset_scale, self.pushButton_change_view_mode,
                self.pushButton_check_encode,
        ]
        self.icon_names_of_exe = [
                'cw.ico', 'ccw.ico', 'zoomin.ico', 'zoomout.ico',
                'fit_w.ico', 'fit_h.ico', 'reset_scale.ico', 'screen_mode.ico',
                'encode_check.ico',
        ]
        self.icon_paths_of_script = [
                './_icon/cw.ico', './_icon/ccw.ico', './_icon/zoomin.ico', './_icon/zoomout.ico',
                './_icon/fit_w.ico', './_icon/fit_h.ico', './_icon/reset_scale.ico', './_icon/screen_mode.ico',
                './_icon/encode_check.ico',
        ]
        self.is_frozen = False
        try:
            if getattr(sys, 'frozen', False): # 実行ファイルの場合
                application_path = sys._MEIPASS # 実行ファイルのパス
                icon_path_of_app = os.path.join(application_path, 'icon.ico')
                self.icon_paths = [os.path.join(application_path, icon_name) for icon_name in self.icon_names_of_exe]
                self.is_debug = False
                self.is_frozen = True
            else: # スクリプトファイルの場合
                application_path = os.path.dirname(__file__)
                icon_path_of_app = os.path.join(application_path, '_icon', 'icon.ico')
                self.icon_paths = self.icon_paths_of_script
            # ウィンドウのアイコンを設定
            self.setWindowIcon(QIcon(icon_path_of_app))
        except:
            icon_path_of_app = None
            self.log_.error(traceback.format_exc())
        """ アイコンパスをログに出力 """
        # if icon_path:
        #     self.log_.info(icon_path)
        """"""

    def _init_instance_variables(self):
        """インスタンス変数の初期化"""
        # ******** インスタンス変数設定 ******** __instance__ __var__
        self.input_fobjs = []
        self.target_lineedit_for_text_dialog_list = None # テキストダイアログの対象となるLineEditオブジェクトのリスト
        self.main_data_ins = MainData()
        self.data_list = None
        self.target_lineedit_for_insert_char_list = None # F10, F11等の変換
        self.IS_REMOVE_NEWLINE_ON_EXPORT_CSV = False # CSV出力時に改行コードを削除するかどうかのフラグ
        self.on_check_lineedit = False
        self.is_pdfmode_to_read_image_file = False # PDFモードで画像ファイルを読み込むかどうかのフラグ
        self.is_single_pdf_mode = False # 1PDF1画像: True
        self.is_canceled_next_img = False
        self.is_img_listwidget_select_canceled = False
        self.previous_index_for_filepath_list = None
        self.next_index_for_filepath_list = None
        self.current_index_for_img_df = 0 # imgモードのカレントインデックス
        self.is_init_restart = False
        self.is_invalid_img = False
        self.current_index_for_pdf_df = 0
        self.is_pdfmode = None
        self.is_new1_no_edit = None
        self.total_pdf_page_count = None
        self.pdf_page_list = []
        self.file_type = 'img'
        self.delta_scale = 0.1
        self.current_index_for_rept_and_ver = 0
        self.pixmap_item_pos_on_collation_dialog = None
        self.is_show_collation_dialog_on_last_and_rept_after_collation = False
        self.focus_out_obj_for_collation = None
        self.focus_out_obj_for_list_check = None
        self.focused_obj_for_list_clicked = None
        self.list_widget_dd = None
        self.is_collation_daialog_canceled = False
        self.is_show_collation_dialog_on_last_and_rept_in_type_check = False
        self.is_show_type_error_for_rect = False
        self.focus_out_line_widget_obj_for_set_rect = None
        self.sep_of_line_widget_text = '  '
        self.last_executing_time_of_focus_in_event = 0
        self.last_executing_time_of_focus_out_event = 0
        self.last_executing_time_of_convertion_text = 0
        self.is_last_enter_pressed = False
        self.rept_col_indexes = None
        self.first_rept_line_widget_obj = None
        self.focus_in_line_widget_obj_buf_for_enter = None
        self.test_counter = 0
        self.focus_out_line_widget_obj_befoer_collation = None
        self.main_mode = None
        self.is_focus_out_allowed = False
        self.prevuous_list_widget_index = None
        self.ime_thread = None  # スレッドのインスタンス変数を作成
        self.new_list_item_text = None
        self.is_new_record_added = None
        self.is_rept_mode = False
        self.is_last_enter_canceled = False
        self.pixmap_item = None
        self.log_df = pd.DataFrame(columns=['timestamp', 'item', 'new1_user_name', 'ver1_user_name', 'new1_value', 'ver1_value', 'img_filename'])
        self.is_last_img_file_process_activated = False
        self.is_in_close_processing = False
        self.is_mouse_on_scroll_area = False
        self.is_tab_pressed = False
        self.is_focus_out = False
        self.is_enter_pressed = False
        self.is_left_button_clicked_and_so_on = False
        self.focus_in_line_widget_obj = None
        self.focus_in_line_widget_obj = None
        self.value_on_focus_in = ''
        self.current_event_filter = None
        self.is_initialaized = True
        self.is_next_img_change = False
        self.is_selected_list_widget = False # リストウィジェットが選択されたかどうかのフラグ
        self.is_executing_fx_editing_finished = False
        self.is_executing_fx_pressed_enter = False
        self.last_executing_time_of_check_and_verify = 0
        self.last_exexuting_time_of_ime_control = 0
        self.last_executing_time_of_helper_of_not_last_image_before_change = 0
        self.last_mouse_focusin_time = 0 # LineEditがクリックされたかどうかのフラグ
        self.previous_list_widget_index = 0 # 更新前のリストウィジェットのインデックス
        self.previous_list_widget_index_for_rept = 0
        self.verified_value = '' # ベリファイ後の値を保持するためのインスタンス変数
        self.line_edit_obj_dict = {} # {int: QtWidgets.QLineEdit} LineEditオブジェクトの辞書
        self.verification_log_list = [] # ベリファイモード、入力値変更時ログリスト
        self.previous_df = None
        self.previous_df_len = 0
        self.input_mode = 'new1'
        self.config_dict = None
        self.init_dialog = None
        self.last_input_line_widget = None
        self.user_name = ''
        self.img_dir_path = ''
        self.img_pobj_dict = None
        self.img_num = 0
        self.current_file_index = 0 # 現在のファイルインデックス
        self.current_angle = 0 # 回転角度を保持するためのインスタンス変数
        self.current_scale = 1.0 # 拡大率を保持するためのインスタンス変数
        self.config_path = './data/config.json'
        # エンコーディング辞書の取得
        self.name_to_encode_dict, self.encode_to_name_dict = _get_encode_dicts()

    def _init_mode_and_headers(self):
        """モード設定とヘッダー設定の初期化"""
        # ========== モード設定 (mode_config_managerから取得) ==========
        # リストウィジェット対応 (file_typeから自動設定)
        self.main_mode_to_listwidget_obj = {}
        self.mode_config_manager: "ModeConfigManager"
        for mode_id in self.mode_config_manager.modes.keys():
            file_type = self.mode_config_manager.get_file_type(mode_id)
            self.main_mode_to_listwidget_obj[mode_id] = self.listWidget_filepath if file_type == 'img' else self.listWidget_pdf

        self.filetype_to_hide_obj = {'img': self.frame_splitter_list, 'pdf': self.listWidget_filepath}
        self.extensions = ['.jpg', '.jpeg', '.png']

        # データリスト (互換性のため個別変数も保持)
        self.data_list_utane_sample = self.mode_config_manager.get_data_list('utane')
        self.data_list_card_sample = self.mode_config_manager.get_data_list('card')
        self.data_list_foreigner = self.mode_config_manager.get_data_list('foreigner')
        self.data_list_prevention = self.mode_config_manager.get_data_list('prevention')
        self.data_list_syuei = self.mode_config_manager.get_data_list('syuei')
        self.data_list_prevention_v2 = self.mode_config_manager.get_data_list('prevention2')
        self.data_list_factory = self.mode_config_manager.get_data_list('factory')
        self.data_list_payroll = self.mode_config_manager.get_data_list('payroll')

        self.data_lists = [
                self.data_list_utane_sample, self.data_list_card_sample, self.data_list_foreigner,
                self.data_list_prevention, self.data_list_syuei, self.data_list_prevention_v2,
                self.data_list_factory,
        ]

        # ヘッダー (mode_config_managerから取得)
        self.foreigner_headers = self.mode_config_manager.get_headers('foreigner')
        self.prevention_headers = self.mode_config_manager.get_headers('prevention')
        self.syuei_headers = self.mode_config_manager.get_headers('syuei')
        self.prevention_v2_headers = self.mode_config_manager.get_headers('prevention2')
        self.factory_headers = self.mode_config_manager.get_headers('factory')

        # ヘッダー辞書 (mode_config_managerから自動生成)
        self.headers_dict = {}
        for mode_id in self.mode_config_manager.modes.keys():
            config = self.mode_config_manager.get_mode(mode_id)
            self.headers_dict[mode_id] = {
                'has_header': config.has_header,
                'headers': config.headers
            }
            # factoryモードの場合、is_multi_pdfフラグを追加
            if mode_id == 'factory':
                self.headers_dict[mode_id]['is_multi_pdf'] = True

    def _init_config_and_dialog(self) -> bool:
        """設定ファイル初期化と初期設定ダイアログの表示

        Returns:
            bool: 初期化を継続する場合True、中断する場合False
        """
        # 初期設定辞書の取得
        self.init_config_dict = _get_init_config_dict()
        self.index_to_delta_scale_dict, self.delta_scale_to_index_dict = _get_delta_scale_dicts()
        self.config_keys = list(self.init_config_dict.keys())
        # ************************
        # 設定ファイルの初期化処理 #config
        # ConfigManagerのインスタンス作成
        self.config_manager = ConfigManager(self.config_path, self.init_config_dict)
        self.init_config()
        # ************************
        # 挿入文字をデータクラスに設定
        self.main_data_ins.insert_char_1 = self.config_dict['insert_char']
        self.main_data_ins.insert_char_2 = self.config_dict['insert_char2']
        self.main_data_ins.insert_char_3 = self.config_dict['insert_char3']
        # rect config frame の表示設定
        if not self.config_dict['is_show_rect_frame']: # ! 矩形設定フレームの表示非表示
            self.frame_rect_mode.hide()
        # /
        self.max_side_length = self.config_dict['max_side_length'] # 画像の最大辺の長さ
        self.encode_type = self.config_dict['encode_type'] # エンコードタイプを取得



        # *********** 初期設定ダイアログの表示 開始 ***********
        # WIP 20251108 initダイアログ前に定義
        self.data_list = self.mode_config_manager.get_data_list(self.main_mode_init)
        self.headers = [data['index'] for data in self.data_list] # ヘッダーを取得

        if self.mode_config_manager.get_need_df_transformed(self.main_mode_init):
            self.full_headers = self.mode_config_manager.get_headers(self.main_mode_init)
        else:
            self.full_headers = self.headers + [10000, 20000, 30000]

        if not self.is_debug: # デバッグモードでない場合
            self.is_show_init_dialog = True
            self.show_init_dialog() # 初期設定ダイアログを表示
            self.is_show_init_dialog = False
        if self.is_close_button_pressed: # 閉じるボタンが押された場合
            return False
        self.setWindowTitle(self.mode_config_manager.get_title_dict()[self.main_mode]) # ウィンドウタイトルの設定
        # *********** 初期設定ダイアログの表示 終了 ***********
        return True

    def _init_data_list_and_frames(self):
        """データリスト、フレーム、UIオブジェクトの設定"""
        self.is_multi_pdf_mode = self.headers_dict[self.main_mode].get('is_multi_pdf', False)

        # メインデータリスト設定 (mode_config_managerから取得)
        self.input_frames_data_list = self.mode_config_manager.get_frame_list(self.main_mode)
        self.file_type = self.mode_config_manager.get_file_type(self.main_mode)
        self.filetype_to_hide_obj[self.file_type].hide() # メインモードに応じたオブジェクトを非表示にする
        # ****** メインデータリスト設定 終了 ******
        # for handle in self.findChildren(QtWidgets.QSplitterHandle):
        #     handle.setStyleSheet("background: #ffffff;") # スプリッターハンドルの色を変更
        for frame_data in self.input_frames_data_list: # Frameの表示設定
            for frame in self.scrollArea_input.findChildren(QtWidgets.QFrame):
                if frame.objectName() == frame_data['frame_name']:
                    if frame_data['is_visible']:
                        frame.show()
                    else:
                        frame.hide()
                    frame_data['frame_obj'] = frame
        self.splitter_3.hide()
        if not self.is_test_button_show:
            self.label_angle_label.hide()
            self.lineEdit_angle.hide()
        self.obj_name_to_info_dict = {data['line_edit_name']: data['info'] for data in self.data_list} # ! メインデータの変換
        self.obj_name_to_display_name_dict = {data['line_edit_name']: data['display_name'] for data in self.data_list}
        self.obj_name_to_name_dict = {data['line_edit_name']: data['name'] for data in self.data_list}
        self.obj_name_lst = [x for x in self.obj_name_to_name_dict.values()]
        self.obj_idx_name_dct = {data['index']: data['name'] for data in self.data_list}
        self.obj_name_to_type_dict = {data['line_edit_name']: data['data_type'] for data in self.data_list}
        self.obj_name_to_index_dict = {data['line_edit_name']: data['index'] for data in self.data_list}
        self.obj_name_to_ime_dict = {data['line_edit_name']: data['ime_mode'] for data in self.data_list}
        self.label_name_to_type_dict = {data['name']: data['data_type'] for data in self.data_list}
        # is_lastが 1のデータを取得
        for data in self.data_list:
            if data['is_last'] == 1:
                self.last_data = data
        self.last_index_of_line_edit = self.last_data['index'] # LineEdit(is_last)の最大インデックス
        self.obj_name_to_conversion_text_dict = {data['line_edit_name']: data['text_conversion'] for data in self.data_list}
        self.line_edit_count = len(self.data_list) # LineEditの数
        # self.headers = [data['index'] for data in self.data_list] # ヘッダーを取得

        # 型情報辞書の設定と検証
        self._init_type_validation()

        self.rect_path = f'./data/rect.json'
        if not Path(self.rect_path).resolve().exists():
            self.rect_path = f'./data/rect_{self.main_mode}.json'

        self.rect_config_base = {'x': None, 'y': None, 'w': None, 'h': None, 'scale': None, 'angle': None}
        self.init_rect_config = {}
        self.rect_config = {}
        for i in range(len(self.data_list)):
            rect_config_base = self.rect_config_base.copy()
            self.init_rect_config[i] = rect_config_base
        # RectConfigManagerのインスタンス作成
        self.rect_config_manager = RectConfigManager(self.rect_path, self.init_rect_config)
        self.rect_config = self.rect_config_manager.initialize()
        # rect_configのチェック（データ数に応じて追加）
        is_rect_config_changed = False
        for i in range(len(self.data_list)):
            if i not in self.rect_config:
                self.rect_config[i] = self.rect_config_base.copy()
                is_rect_config_changed = True
        if is_rect_config_changed:
            self.rect_config_manager.write(self.rect_config)
        # ************* data_listにオブジェクトを追加 開始 ************
        for data in self.data_list:
            for line_edit_obj in self.scrollArea_input.findChildren(QtWidgets.QLineEdit):
                if data['line_edit_name'] == line_edit_obj.objectName():
                    data['line_edit_obj'] = line_edit_obj # lineEditオブジェクトを取得
                    if data['is_last'] == 1:
                        self.last_input_line_widget = line_edit_obj # 最後のLineEdit取得
                    elif data['is_last'] == -1:
                        self.first_input_line_widget = line_edit_obj # 最初のLineEdit取得
        for data in self.data_list:
            for line_edit_obj in self.scrollArea_input.findChildren(QtWidgets.QLabel):
                if data['label_name'] == line_edit_obj.objectName():
                    data['label_obj'] = line_edit_obj # Labelオブジェクトを取得
        for data in self.data_list:
            for frame_obj in self.scrollArea_input.findChildren(QtWidgets.QFrame):
                if data['frame_a_name'] == frame_obj.objectName():
                    data['frame_a_obj'] = frame_obj # Frameオブジェクトを取得
        for data in self.data_list:
            for frame_obj in self.frame_input_right.findChildren(QtWidgets.QFrame):
                if data['frame_b_name'] == frame_obj.objectName():
                    data['frame_b_obj'] = frame_obj
        for data in self.data_list:
            for layout_obj in self.scrollArea_input.findChildren(QtWidgets.QHBoxLayout):
                if data['layout_a_name'] == layout_obj.objectName():
                    data['layout_a_obj'] = layout_obj
        for data in self.data_list:
            for layout_obj in self.frame_input_right.findChildren(QtWidgets.QHBoxLayout):
                if data['layout_b_name'] == layout_obj.objectName():
                    data['layout_b_obj'] = layout_obj
        # if self.main_mode in ['factory']: # 工場見学の時
        #     self.target_lineedit_for_insert_char_list = (
        #         [data['line_edit_obj'] for data in self.data_list if 'insert-char-2-3' in data['remarks'].split('_')]
        #     )
        #     self.target_lineedit_for_text_dialog_list = (
        #         [data['line_edit_obj'] for data in self.data_list if 'text-dialog' in data['remarks'].split('_')]
        #     )
        # ************* data_listにオブジェクトを追加 終了 ************
        # is_showが Falseを非表示にする
        for line_edit_obj in self.scrollArea_input.findChildren(QtWidgets.QLineEdit):
            if line_edit_obj.objectName().endswith('_'):
                line_edit_obj.hide()
        for label_obj in self.scrollArea_input.findChildren(QtWidgets.QLabel):
            if label_obj.objectName().endswith('_'):
                label_obj.hide()
        for data in self.data_list:
            if data['is_show']:
                data['line_edit_obj'].show()
                data['label_obj'].show()
            else:
                data['line_edit_obj'].setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # 右側のフレーム内のフレームの非表示設定
        for data in self.data_list:
            if data['is_show']:
                data['frame_b_obj'].show()
            else:
                data['frame_b_obj'].hide()
        self.obj_name_to_list_item_dict = {data['line_edit_name']: data['list_item'] for data in self.data_list}
        self.obj_name_to_pn_auto_input_dict = {data['line_edit_name']: data['pn_auto_input'] for data in self.data_list}
        self.pn_auto_input_to_obj_dict = {data['pn_auto_input']: data['line_edit_obj'] for data in self.data_list} # 郵便番号用の辞書
        self.index_to_obj_dict = {data['index']: data['line_edit_obj'] for data in self.data_list}

    def _init_type_validation(self):
        """データ型情報辞書の設定と検証"""
        # 型辞書（現在は未使用）
        self.type_dict = {
                'str': '文字列', 'int': '整数', 'float': '数値', 'postnum': '郵便番号',
                'telnum': '電話番号', 'date': '日付', 'zenkaku': '全角', 'hankaku': '半角',
                'int_hankaku': '半角整数', 'float_hankaku': '半角数値'
        }

        # 型情報辞書（入力値の検証に使用）
        self.type_info_dict = {
                '': '文字列', 'str': '文字列', 'int': '整数', 'float': '数値', 'postnum': '例) 123-4567',
                'telnum': '例) 123-456-7890', 'date': '例) yyyy/mm/dd, yyyy-mm-dd',
                'zenkaku': '全角', 'hankaku': '半角', 'int_hankaku': '半角整数',
                'float_hankaku': '半角数値', 'float_hankaku_completer': '半角数値',
                'notempty': '空欄不可', 'int_notempty': '整数(空欄不可)',
                'int_hankaku_notempty': '半角整数(空欄不可)',
                'listonly': 'リスト内の値以外不可', 'list': '', 'conv': '', 'inli': '規定値以外不可',
                'int_hankaku_inli': '半角整数(規定値以外不可)', 'str_hankaku': '半角文字列',
                'int_hankaku_maxlen': '半角整数(文字数制限)', 'str_hankaku_maxlen': '半角文字列(文字数制限)',
                'int_hankaku_range': '半角整数(範囲指定)', 'hankaku_eisu_lenjust': '半角英数字(文字数指定)',
                'hankaku_eisu_lenrange': '半角英数字(文字数指定)', 'hankaku_eisu': '半角英数字', 'rematch': '指定された文字',
                'username_noedit': '', 'date_nover': '例) yyyy/mm/dd, yyyy-mm-dd',
                'hankaku_int_lenrange': '半角整数(文字数指定)', 'hankaku_int_lenjust': '半角整数(文字数指定)',
                'hankaku-eisu-kuromaru': '半角英数字', 'hankaku-eisu-kuromaru_lenjust': '半角英数字(文字数指定)', 'hankaku-eisu-kuromaru_lenrange': '半角英数字(文字数指定)',
                'hankaku-eisu-kuromaru_replace': '半角英数字', "z2h_digit_only": "全角数値を半角に変換",
                'str_replace': '文字列(置換)', 'hankaku-eisu-kuromaru_radd': '半角英数字', 'postnum-kuromaru': '郵便番号',
                'hankaku-kuromaru': '半角', 'zenkaku-katakana-kuromaru': '全角カタカナ', 'postnum-kuromaru_postauto': '郵便番号',
                'ischeck_nover': 'チェック用', 'listonly-kuromaru': 'リスト内の値と●以外不可', 'postauto': '', 'replace': '文字列(置換)',
                'hankaku-kuromaru_lenrange': '半角英数字(文字数指定)', 'hankaku_replace': '半角',
        } # ! タイプを増やした場合は追加

        # 型情報辞書の検証（全data_listの型が定義されているか確認）
        all_keys = []
        self.data_lists = [data_list for data_list in self.data_lists if data_list is not None]
        for data_list in self.data_lists: # ここにメインモード追加
            for data in data_list:
                all_keys.append(data['data_type'])
        all_keys = set(all_keys)
        info_keys = tuple(self.type_info_dict.keys())
        error_keys = []
        for key in all_keys:
            if key not in info_keys:
                error_keys.append(key)
        if error_keys != []:
            error_text = '\n'.join(error_keys)
            QMessageBox.warning(self, 'エラー', f'type_info_dictに {error_text} がありません')

    def _init_dataframe_and_paths(self):
        """DataFrame、色辞書、ファイルパス、グラフィックスビューの初期化"""

        if self.mode_config_manager.get_need_df_transformed(self.main_mode):
            self.full_headers = self.mode_config_manager.get_headers(self.main_mode)
        else:
            self.full_headers = self.headers + [10000, 20000, 30000] # DELETE
        self.current_df = pd.DataFrame(columns=self.full_headers) # 空のDataFrameを作成
        # グローバル色辞書の取得
        self.global_color_dict = _get_global_color_dict()
        self.line_dict = {}
        # 右側のラインの追加
        # def _set_max_height_to_frame_b():
        #     frame_b_list = [obj for obj in self.frame_input_right.findChildren(QtWidgets.QFrame) if obj.objectName().endswith('__')]
        #     for f in frame_b_list:
        #         print(f.objectName())
        #         f.setMaximumHeight(f.maximumHeight() + 10)
        # QTimer.singleShot(0, _set_max_height_to_frame_b) # 右側のフレーム群の高さを調整
        for i in range(len(self.data_list) - 1, -1, -1):
            line = QtWidgets.QFrame(self.tab_2)
            line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
            line.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
            line.setLineWidth(1)
            palette = line.palette()
            palette.setColor(QPalette.ColorRole.Foreground, QColor(0, 0, 111, 255))
            line.setPalette(palette)
            line.setObjectName(f"line__{i}__")
            if not self.data_list[i]['is_b_line_show']:
                line.hide()
            self.verticalLayout_input_right.insertWidget(i, line)
            self.line_dict[i] = line
        # ヘルププレーンテキストの設定
        for plain_text_edit in [self.plainTextEdit_explain, self.plainTextEdit_explain_2]:
            palette = plain_text_edit.palette()
            palette.setColor(QPalette.ColorRole.Base, QColor(233, 233, 233, 255))
            plain_text_edit.setPalette(palette)
        # テスト変数...
        if self.is_debug:
            self.input_mode = self.test_mode
            self.user_name = self.test_user_name
            self.img_dir_path = self.test_img_dir_path
            self.output_path = self.test_output_path
            self.is_rept_mode = self.test_is_rept_mode
        self.is_close_button_pressed = False
        self.is_show_init_dialog = False
        self.lineEdit_angle.setReadOnly(True)
        # ラベルの背景色を設定
        q_gray_color = QColor(244, 244, 244, 255)
        palette = self.lineEdit_angle.palette()
        palette.setColor(QPalette.ColorRole.Base, q_gray_color)
        self.lineEdit_angle.setPalette(palette)
        self.lineEdit_scale.setReadOnly(False)
        palette = self.label_username.palette()
        palette.setColor(QPalette.ColorRole.Base, q_gray_color)
        palette.setColor(QPalette.ColorRole.Foreground, QColor(50, 0, 0, 255))
        font = self.label_username.font()
        font.setBold(True)
        self.label_username.setFont(font)
        self.label_username.setPalette(palette)
        palette = self.label_input_mode.palette()
        palette.setColor(QPalette.ColorRole.Base, q_gray_color)
        if self.input_mode == 'new1':
            palette.setColor(QPalette.ColorRole.Foreground, Qt.GlobalColor.blue)
        elif self.input_mode == 'ver1':
            palette.setColor(QPalette.ColorRole.Foreground, Qt.GlobalColor.red)
        self.label_input_mode.setPalette(palette)
        palette = self.label_main_mode.palette()
        mode_jp = self.mode_config_manager.get_jp_name_dict()[self.main_mode]
        self.label_main_mode.setText(mode_jp)
        palette.setColor(QPalette.ColorRole.Foreground, Qt.GlobalColor.darkMagenta)
        self.label_main_mode.setPalette(palette)
        self.label_main_mode.hide()
        # ファイルパスの設定...
        self.img_dobj = Path(self.img_dir_path).absolute() # 画像ファイルのパスオブジェクト
        self.img_dir_name = self.img_dobj.name
        self.suffix_of_filename = '_NEW1.csv' if self.input_mode == 'new1' else '_VER1.csv'
        self.output_dobj = Path(self.output_path).absolute() # 出力フォルダのパスオブジェクト
        self.output_csv_filename = self.img_dir_name + self.suffix_of_filename
        self.output_csv_fobj = self.output_dobj / self.output_csv_filename
        self.output_log_filename = self.img_dir_name + f'_VER1_log.csv'
        self.output_log_fobj = Path(self.output_path) / self.output_log_filename # 出力ログファイルオブジェクト
        self.new1_csv_fobj = self.output_csv_fobj.parent.absolute() / (self.img_dir_name + '_NEW1.csv')
        self.new1_csv_filename = self.new1_csv_fobj.name
        self.insert_char = self.config_dict['insert_char'] # 挿入文字を取得 ●
        # 初期化処理...
        self.initializer_sub()
        self.img_pobj_dict = self.image_utils.get_image_filepath_obj_dict(self.img_dir_path) # 画像ファイルパスオブジェクトの辞書を取得
        # 画像ファイルかPDFか分岐
        if self.file_type == 'img':
            self.init_graphics_view() # グラフィックスビューの初期化
        elif self.file_type == 'pdf':
            self.init_graphics_view_pdf()

    def _init_data_loading_and_listwidgets(self):
        """既存データ読み込みとリストウィジェットの設定"""
        # ____メインデータ辞書を作成____main_data_dict 開始...
        self.main_data_dict = {data['line_edit_name']: data for data in self.data_list}
        # ____メインデータ辞書を作成____main_data_dict 終了
        # self.set_blank_to_line_edits() # 全てのLineEditを空白にする
        if os.path.exists(str(self.new1_csv_fobj)): # 既に入力データファイルが存在する場合の処理...
            has_header = self.headers_dict[self.main_mode]['has_header']
            # InitDialogで設定済みの場合はスキップ
            if self.previous_df is None:
                has_header = self.headers_dict[self.main_mode]['has_header']
                self.previous_df = DataIO.read_csv_with_header(
                    self,
                    self.new1_csv_fobj,
                    encoding=self.encode_type,
                    headers=self.full_headers,
                    has_header=has_header,
                )
            # WIP 列が多い場合は減らす
            if self.mode_config_manager.get_need_df_transformed(self.main_mode):
                self.previous_df = self.previous_df[self.obj_name_lst + [10000, 20000, 30000]]

            self.previous_df_len = len(self.previous_df) # 入力データの行数を取得 == 画像ファイル数
            if self.input_mode == 'new1': # new1の場合
                self.set_previous_data_to_line_edits() # 入力データをLineEditにセット
        # _____________ reptの場合のリストウィジェットの設定 _____________
        if self.is_rept_mode: # リピートモードの場合
            self.rept_col_indexes = [data['index'] for data in self.data_list if data['is_rept']]
            self.first_rept_line_widget_obj = self.index_to_obj_dict[self.rept_col_indexes[0]]
            if self.previous_df is None or self.input_mode == 'ver1': # 過去データが存在しない場合
                self.listWidget_filepath.addItem('新しいレコード')
            else: # 過去データが存在する場合
                for i in range(self.previous_df.shape[0]):
                    rept_texts = []
                    for j in self.rept_col_indexes:
                        rept_texts.append(self.previous_df.loc[i, j])
                    self.listWidget_filepath.addItem(f'{i + 1:05}{self.sep_of_line_widget_text}{self.sep_of_line_widget_text.join(rept_texts)}')
                self.listWidget_filepath.addItem('新しいレコード')
        # _____________ pdfmodeの場合のlistwidgetの処理 _____________
        if self.is_pdfmode:
            if self.previous_df is not None: # previous_dfが存在する場合
                for i in range(self.previous_df.shape[0]):
                    # if self.main_mode in ['prevention', 'syuei',]:
                    #     text = self.previous_df.iloc[i, 7] # 氏名
                    # elif self.main_mode in ['prevention2',]:
                    #     text = self.previous_df.iloc[i, 8] # 氏名
                    # elif self.main_mode in ['payroll',]:
                    #     text = self.previous_df.iloc[i, 1] # 指名
                    # else:
                    #     text = ''

                    idx_for_text = self.mode_config_manager.get_df_name_column_index((self.main_mode_init))
                    text = self.previous_df.iloc[i, idx_for_text] # 指名

                    item = QListWidgetItem(f'{i + 1:03}{self.sep_of_line_widget_text}{text}')
                    self.listWidget_pdf_record.addItem(item)
                if self.input_mode == 'new1':
                    # shingle mode かつ 画像数と過去データ数が同じ場合は作成しない
                    if self.listWidget_pdf.count() != self.previous_df.shape[0]:
                        item = QListWidgetItem('新しいレコード')
                        self.listWidget_pdf_record.addItem(item)
            elif self.previous_df is None: # previous_dfが存在しない場合
                item = QListWidgetItem('新しいレコード')
                self.listWidget_pdf_record.addItem(item)
            self.select_next_item_of_list_widget(0)
            self.listWidget_pdf_record.show()
            self.listWidget_pdf.setCurrentRow(0)
            # PDF single mode時 listWidget_pdfは選択しない
            if self.is_single_pdf_mode:
                self.listWidget_pdf.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        # _____________________________________________________
        # ________リストウィジェット index 0 を選択 選択の可、不可 設定
        self.listWidget_filepath.blockSignals(True)
        self.listWidget_filepath.setCurrentRow(0) # リストウィジェットの最初のアイテムを選択
        if self.input_mode == 'ver1':
            self.listWidget_filepath.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
            self.listWidget_pdf_record.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        elif self.input_mode == 'new1':
            self.listWidget_filepath.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.listWidget_pdf_record.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.listWidget_filepath.blockSignals(False)
        # ________ログファイルを新規作成、または空欄で上書きする処理________
        log_file_path = str(self.output_log_fobj.absolute())
        if self.input_mode == 'ver1':
                try:
                    with open(log_file_path, 'w', encoding=self.encode_type) as f: # ログファイルの初期化
                        f.write('')
                except PermissionError:
                    QMessageBox.warning(self, 'エラー', 'ログファイルの初期化に失敗しました\n\n'
                                        'ログファイルが開かれている可能性があります\n\n'
                                        f'ログファイルパス: {log_file_path}', QMessageBox.Ok)
                    self.restart_app(is_button_pressed=False)

    def _init_ui_settings(self) -> bool:
        """UI設定（イベント、シグナル、レイアウト、スタイル）

        Returns:
            bool: 初期化を継続する場合True、中断する場合False
        """
        # _____________________________________________________
        if self.is_test_button_show: # テストボタンを表示する場合
            self.frame_test_button.show()
        else:
            self.frame_test_button.hide()
        self.event_filter_dict = {}  # イベントフィルターを保持する辞書を初期化
        self.install_event_filter_to_all_line_edit() # 全てのLineEditのシグナルを設定
        self.installEventFilter(self) # メインウィンドウのイベントフィルターを設定
        if self.is_close_button_pressed:
            self.close()
            return False
        for widget, icon_path in zip(self.widgets_require_icon, self.icon_paths):
            try:
                widget.setIcon(QIcon(icon_path))
                widget.setIconSize(QSize(widget.width(), widget.height()))
            except:
                self.log_.error(f'アイコンの設定に失敗しました: {icon_path}\n{traceback.format_exc()}')
        # ラジオボタン初期設定...
        if self.config_dict['auto_move']:
            self.radioButton_automove_on.setChecked(True)
        else:
            self.radioButton_automove_off.setChecked(True)
        if self.config_dict['is_rect_show']:
            self.radioButton_rect_show.setChecked(True)
            self.frame_rect_select.show()
        else:
            self.radioButton_rect_hide.setChecked(True)
            self.frame_rect_select.hide()
        self.radioButton_rect_move.setChecked(True)
        # レイアウト設定...
        if self.config_dict['layout_type'] == 'v':
            self.radioButton_layout_vertival.setChecked(True)
            QTimer.singleShot(100, self.change_layout_vertical)
        else:
            self.radioButton_layout_horizontal.setChecked(True)
            QTimer.singleShot(400, self.change_layout_horizontal)
        # ボタンスプリッターサイズ設定...
        def _set_splitter_size():
            splitter_button_height = self.config_dict['splitter_5a_height']
            self.splitter_5.setSizes([
                    splitter_button_height, self.splitter_5.size().height() - splitter_button_height
            ])
            splitter_left_width = self.config_dict['splitter_6a_width']
            splitter_right_widht = self.config_dict['splitter_6b_width']
            self.splitter_6.setSizes([splitter_left_width, splitter_right_widht])
        QTimer.singleShot(600, _set_splitter_size )
        # 情報ボタンの表示設定...
        if self.config_dict['is_info_show']:
            self.radioButton_info_show.setChecked(True)
            self.info_label_show()
        else:
            self.radioButton_info_hide.setChecked(True)
            self.info_label_hide()
        font = self.label_infomation.font()
        font.setBold(True)
        self.label_infomation.setFont(font)
        font = self.label_infomation_right.font()
        font.setBold(True)
        self.label_infomation_right.setFont(font)
        palette = self.label_infomation.palette()
        palette.setColor(QPalette.ColorRole.Foreground, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Background, QColor(234,234,234,255))
        self.label_infomation.setPalette(palette)
        self.label_infomation.setAutoFillBackground(True)
        # label_infomation_right
        palette = self.label_infomation_right.palette()
        palette.setColor(QPalette.ColorRole.Foreground, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Background, QColor(234,234,234,255))
        self.label_infomation_right.setPalette(palette)
        self.label_infomation_right.setAutoFillBackground(True)
        # 下部のスクロールエリアの設定...
        def _set_scrollarea_size_1():
            line_widget_height = self.last_input_line_widget.height()
            data_frame_num =len(set([data['frame_a_obj'] for data in self.data_list]))
            # self.scrollAreaWidgetContents.setMaximumHeight(line_widget_height * (data_frame_num + 10)) # スクロールエリアの高さを設定
            self.scrollAreaWidgetContents.setMinimumHeight(line_widget_height * (data_frame_num + 6))
            self.gridLayout_bottom_scroll_area.setAlignment(Qt.AlignmentFlag.AlignTop)
        QTimer.singleShot(200, _set_scrollarea_size_1)
        # 右スクロールエリアの設定...
        def _set_scrollarea_size_2():
            # 右側のフレームの高さを設定...
            cnt = len(self.data_list)
            one_height = self.frame__0__.size().height()
            height = one_height * (cnt + 12)
            self.scrollAreaWidgetContents_2.setMinimumHeight(height)
            max_height = int(height * 10)
            self.frame_input_right.setMinimumHeight(int(max_height * 1.5)) # IMPORTANT ここを変更すると右側のフレーム群の詰まりが解消される
        QTimer.singleShot(200, _set_scrollarea_size_2)
        # タブオーダーの設定...
        objs_for_taborder = []
        for data in self.data_list:
            types = data['data_type'].split('_')
            if not 'noedit' in types: # noeditはnoEnable, noFocusにする
                objs_for_taborder.append(data['line_edit_obj'])
            else:
                if 'username' in types:
                    data['line_edit_obj'].setText(self.user_name) # ユーザー名ﾗﾍﾞﾙならユーザー名を設定
                data['line_edit_obj'].setEnabled(False)
                data['line_edit_obj'].setFocusPolicy(Qt.FocusPolicy.NoFocus)
        for i, data in enumerate(objs_for_taborder):
            if i == len(objs_for_taborder) - 1:
                break
            self.setTabOrder(objs_for_taborder[i], objs_for_taborder[i + 1])
        # 矩形設定エリアの設定...
        palette = self.frame_rect_show_hide.palette()
        palette.setColor(QPalette.ColorRole.Background, QColor(0, 244, 244, 30))
        self.frame_rect_show_hide.setPalette(palette)
        self.frame_rect_show_hide.setAutoFillBackground(True) # setAutoFillBackground
        palette = self.frame_rect_select.palette()
        palette.setColor(QPalette.ColorRole.Background, QColor(244, 244, 0, 30))
        self.frame_rect_select.setPalette(palette)
        self.frame_rect_select.setAutoFillBackground(True) # setAutoFillBackground
        # 最初のLineEdit の IMEモード設定...
        self.focus_in_line_widget_obj = self.first_input_line_widget
        # リピートモードの場合の設定...
        if self.is_rept_mode:
            # rept == Trueになる最初の Objを取得...
            self.first_rept_line_edit_obj = None
            for data in self.data_list:
                if data['is_rept']:
                    self.first_rept_line_edit_obj = data['line_edit_obj']
                    break
        self.is_not_set_sub_rect = False
        self.scrollAreaWidgetContents.installEventFilter(self) # scrollAreaWidgetContentsのイベントフィルターを設定
        self.scrollArea_input_right.installEventFilter(self)
        self.delta_scale = self.config_dict['delta_scale']
        self.delta_index = self.delta_scale_to_index_dict[self.delta_scale]
        self.comboBox_delta.setCurrentIndex(self.delta_index)
        # infomation...
        info = self.obj_name_to_info_dict[self.data_list[0]['line_edit_obj'].objectName()]
        self.label_infomation.setText(info.replace('\n', '')) # >> を空欄に変更
        self.label_infomation_right.setText(info)
        # スケールラインのイベントインストール...
        self.custom_event_filter_for_line_edit_scale = CustomEventFilterForLineEditScale(self)
        self.lineEdit_scale.installEventFilter(self.custom_event_filter_for_line_edit_scale)
        self.custom_event_filter_for_button = CustomEventFilterForButtonScrollArea(self)
        self.scrollArea_top.installEventFilter(self.custom_event_filter_for_button)
        if self.input_mode == 'new1':
            try:
                self.listWidget_pdf_record.disconnect(self.on_list_widget_selected_for_pdf_record)
            except TypeError:
                pass
            self.listWidget_pdf_record.currentItemChanged.connect(self.on_list_widget_selected_for_pdf_record) # リストウィジェットのアイテムが選択されたときの処理...
        self.is_connected = True
        dict_of_connected_objs = {
            # self.listWidget_filepath: [self.on_list_widget_selected, 'currentRowChanged'],
            self.listWidget_filepath: [self.on_list_widget_selected, 'currentItemChanged'],
            # self.listWidget_pdf: [self.on_list_widget_selected_for_pdf, 'currentItemChanged'],
            self.comboBox_delta: [self.change_delta_scale, 'currentIndexChanged'],
            self.pushButton_check_encode: lambda: self.check_encoding_line_edits(),
            self.pushButton_cw: lambda: self.rotate_image(90, is_button=True),
            self.pushButton_ccw: lambda: self.rotate_image(-90, is_button=True),
            self.pushButton_zoomin: lambda: self.scaling_image(self.delta_scale, is_button=True),
            self.pushButton_zoomout: lambda: self.scaling_image(-self.delta_scale, is_button=True),
            self.pushButton_reset_scale: lambda: self.scaling_image(0, is_reset=True, is_button=True),
            self.pushButton_fit_w: lambda: self.adjust_image('w', is_button=True),
            self.pushButton_fit_h: lambda: self.adjust_image('h', is_button=True),
            self.pushButton_select_folder: lambda: self.restart_app(is_button_pressed=True),
            self.pushButton_goto_tab_index_0: lambda: self.tabWidget.setCurrentIndex(0),
            self.pushButton_rect_get: lambda: self.pressed_get_rect(),
            self.pushButton_rect_set: lambda: self.pixmap_item.set_rect(),
            self.radioButton_rect_show: lambda: self.rect_area_show_or_hide(is_show=True),
            self.radioButton_rect_hide: lambda: self.rect_area_show_or_hide(is_show=False),
            self.radioButton_rect_select: lambda: self.change_rect_mode('select'),
            self.radioButton_rect_move: lambda: self.change_rect_mode('move'),
            self.radioButton_layout_horizontal: lambda: self.pressed_h_button(),
            self.radioButton_layout_vertival: lambda: self.pressed_v_button(),
            self.radioButton_info_show: lambda: self.info_label_show(),
            self.radioButton_info_hide: lambda: self.info_label_hide(),
            self.radioButton_automove_on: lambda: self.pressed_radioButton_automove_on(),
            self.pushButton_help: lambda: self.tabWidget.setCurrentIndex(1),
            self.pushButton_test: lambda: self.on_test_button_pressed(),
            self.pushButton_test_2: lambda: self.on_test_button_pressed_2(),
            self.pushButton_change_view_mode: self.set_screen_mode_toggle_full_or_max,
        }
        for obj, item in dict_of_connected_objs.items():
            if isinstance(item, list):
                func = item[0]
                mode = item[1]
            else:
                func = item
                mode = 'clicked'
            self.set_connect(obj, func, mode) # シグナルとスロットを設定 <--重要
        # ツールチップ設定...
        tool_tip_move_select = '画像ドラッグ時の挙動\n移動モード: 画像をつかんで移動\n選択モード: 自動ジャンプ用の矩形を選択'
        self.radioButton_rect_move.setToolTip(tool_tip_move_select)
        self.radioButton_rect_select.setToolTip(tool_tip_move_select)
        tool_tip_automove = '自動移動モード\nオン: テキストボックス移動時に設定した座標へジャンプ\nオフ: 通常モード'
        self.radioButton_automove_on.setToolTip(tool_tip_automove)
        self.radioButton_automove_off.setToolTip(tool_tip_automove)
        self.pushButton_select_folder.setToolTip('初期設定ダイアログに移動します(Ctrl + F)')
        self.pushButton_rect_get.setToolTip('選択した矩形の座標を自動ジャンプ用設定します(Ctrl + R)\n設定時は選択ラジオボタンをオンにしてください')
        self.pushButton_ccw.setToolTip('Ctrl + 1')
        self.pushButton_cw.setToolTip('Ctrl + 2')
        self.pushButton_zoomout.setToolTip('Ctrl + 3')
        self.pushButton_zoomin.setToolTip('Ctrl + 4')
        self.pushButton_fit_w.setToolTip('Ctrl + 5')
        self.pushButton_fit_h.setToolTip('Ctrl + 6')
        self.pushButton_reset_scale.setToolTip('Ctrl + 7')
        self.pushButton_change_view_mode.setToolTip('フルスクリーンと画面最大化の切り替え(F7)')
        self.pushButton_help.setToolTip('ヘルプページに移動します(Ctrl + Tab)')
        self.pushButton_check_encode.setToolTip('全てのテキストボックス内の文字列がエンコード可能かどうかを確認します(Alt + E)')
        # フォーカス設定...
        self.radioButton_automove_off.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.radioButton_automove_on.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.radioButton_rect_show.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.radioButton_rect_hide.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.radioButton_rect_select.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.radioButton_rect_move.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_rect_get.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # テストボタン...
        self.pushButton_rect_set.hide() # 移動ボタンを非表示
        # 自動移動モード, Ime, UpdatesEnabledの設定...
        def _set_rect_config():
            current_scale = self.config_dict['current_scale']
            if 0 < current_scale < 3:
                self.scaling_image(current_scale, is_absolute=True)
            else:
                self.scaling_image(1, is_absolute=True)
            if self.radioButton_automove_on.isChecked():
                self.pixmap_item.set_rect(is_first=True)
            ime_mode = self.obj_name_to_ime_dict[self.first_input_line_widget.objectName()]
            self.set_ime_from_ime_mode_text(ime_mode)
            self.graphicsView_main.setUpdatesEnabled(True)
            self.is_initialaized = False # 初期化中フラグをFalseに設定
        QTimer.singleShot(555, lambda: _set_rect_config())
        # ...
        def _set_true_to_is_focus_out_allowed():
            self.goto_first_visible_line_edit() # 最初のLineEditにフォーカスを移動
            self.is_focus_out_allowed = True
        QTimer.singleShot(1000, _set_true_to_is_focus_out_allowed)
        if not self.is_invalid_img:
            self.show()
        self.init_dialog = None
        time.sleep(0.505)
        return True

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

        # Phase 2: モード設定とヘッダー設定
        self._init_mode_and_headers()

        # Phase 3: 設定ファイル初期化とダイアログ
        if not self._init_config_and_dialog():
            return  # 初期化を中断

        # Phase 4: データリストとフレーム設定
        self._init_data_list_and_frames()

        # Phase 5: DataFrame、色辞書、ファイルパス設定
        self._init_dataframe_and_paths()

        # Phase 6: データ読み込みとリストウィジェット設定
        self._init_data_loading_and_listwidgets()

        # Phase 7: UI設定（イベント、シグナル、レイアウト、スタイル）
        if not self._init_ui_settings():
            return  # 初期化を中断

    def initializer_sub(self):
        # スプリッターのサイズを設定...
        self.splitter.setSizes([self.config_dict['splitter_1a_height'], self.config_dict['splitter_1b_height']])
        self.splitter_2.setSizes([self.config_dict['splitter_2a_width'], self.config_dict['splitter_2b_width']])
        self.current_angle = self.config_dict['current_angle'] # 回転角度と設定
        self.current_scale = self.config_dict['current_scale'] # 拡大率を設定
        self.show_angle_and_scale()
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        self.label_username.setText(self.user_name)
        self.index_to_line_edit_obj_dict = {data['index']: data['line_edit_obj'] for data in self.data_list} # define_dict
        if self.last_input_line_widget is None:
            self.log_.error('最後のLineEditが取得できませんでした')
            raise
        labels = self.scrollArea_input.findChildren(QtWidgets.QLabel)
        label_is_bold = self.mode_config_manager.get_label_font_is_bold()
        label_point = self.mode_config_manager.get_label_font_point()
        for label in labels: # 全てのラベル表示名を設定
            label_name = label.objectName()
            for data in self.data_list:
                if data['label_name'] == label_name:
                    label.setText(data['display_name'])
                    font = label.font()
                    font.setBold(label_is_bold)
                    font.setPointSize(int(label_point))
                    label.setFont(font)
        self.label_input_mode.setText(self.input_mode.upper()) # input_modeの表示
        self.statusBar().hide() # ステータスバーを非表示


