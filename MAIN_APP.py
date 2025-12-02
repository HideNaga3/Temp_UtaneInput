# venv : input_img, python version : 3.10.14
# ブロックなし ^(?!\s*#).*print.*
# ブロックあり ^.*#.*print.*

# PyQt5-stubs (型スタブファイル)

# TODO

# 標準モジュール
import traceback
from datetime import datetime
import time
import os
from pathlib import Path
import sys
# VSCodeデバッグコンソールでのトレースバック文字化け対策（UTF-8設定）
if not hasattr(sys, 'frozen'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import json
import re
import ctypes
from typing import List, TYPE_CHECKING
from dataclasses import dataclass
from collections import Counter
from pprint import pprint as pp

# 外部ライブラリ
import pandas as pd

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer, QSharedMemory, QSize, pyqtSignal, QObject, QEvent, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QGraphicsScene, \
    QDialog, QAbstractItemView, QShortcut, QSizePolicy, QMenu, QAction, QGraphicsView, QLineEdit, QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPalette, QColor, QTextCursor, QKeySequence, \
    QTextCharFormat, QBrush, QKeyEvent
from PyQt5 import sip

from main_app_ui import Ui_MainWindow
from _lib._create_logger import create_logger
from _lib._draggable_pixmap_item import DraggablePixmapItem
from _lib._init_dialog_main import InitDialog
from _lib._collation_dialog_main import CollationDialog
from _lib._ime_control import set_ime_mode_jp_or_en
from _lib._helper_classes import IMEThread, SingleApplication
from _lib._postnum_reader import PostNumReader
from _lib._collation_two_text import CollationTwoText
from _lib._sub_lib import SubLib, pri
from _lib._pdf_util import PdfImgReader
from _lib._create_data_list import create_data_list, create_frame_list
from _lib._text_edit_dialog import MyTextEditDialog
from _lib._mode_config import ModeConfigManager
from _lib._validators import InputValidator
from _lib._image_utils import ImageUtils
from _lib._data_io import DataIO
from _lib._config_manager import ConfigManager, RectConfigManager
from _lib._main_data import MainData
from _lib._event_filters import (
    CustomEventFilterForGraphicsView,
    CustomEventFilterForLineEditScale,
    CustomEventFilterForLineEdit,
    CustomEventFilterForPlaneTextEdit,
    CustomEventFilterForDD,
    CustomEventFilterForButtonScrollArea
)
from _lib._data_transform import DataTransformerFactory

SHORT_CUT_KEY_DD = Qt.Key.Key_unknown # ドロップダウンのショートカットキー


# ========================================
''' payroll, payroll2, utane2 '''
G_MAIN_MODE = 'utane2'  # ! exe 初期モード設定
# ========================================


# 定数取得関数をインポート
from _lib._constants import (
    _get_init_config_dict,
    _get_delta_scale_dicts,
    _get_encode_dicts,
    _get_global_color_dict
)

############################# メインウィンドウクラス 開始 #############################

# 初期化Mixin
from _lib.initializer_mixin import InitializerMixin


class MyMainWindow(QMainWindow, Ui_MainWindow, InitializerMixin):

    def __init__(self):

        super().__init__()
        # UIウィジェットのタイプヒント設定
        self._init_type_hints()
        if not os.path.exists('./data'):
            os.makedirs('./data')
        if not os.path.exists('./data/postnum'):
            os.makedirs('./data/postnum')
        self.main_mode_init = G_MAIN_MODE # ! exe 初期モード設定
        self.postnum_reader = PostNumReader(self)
        self.sublib = SubLib()
        # data_transformer はis_frozenが定義された後に初期化
        self.is_frozen = hasattr(sys, "frozen")

        # 新しいヘルパークラスの初期化
        self.mode_config_manager: ModeConfigManager = ModeConfigManager(create_data_list, create_frame_list)
        self.data_transformer = DataTransformerFactory(parent=self).get_transformer()
        self.validator = InputValidator(sublib=self.sublib, encode_type='cp932')
        self.image_utils = ImageUtils()

        if self.postnum_reader.conv_df is not  None:
            self.postnum_reader.conv_df = self.postnum_reader.conv_df.fillna('') # NaNを空文字に変換
            self.postnum_reader.conv_df = self.postnum_reader.conv_df.drop_duplicates()
        self.is_close_button_pressed = False
        self.is_restart_processing = False
        self.is_first_init = True
        try:
            self.initializer()
        finally:
            # 例外が発生しても必ずフラグをリセット
            self.is_first_init = False


        # ショートカットキー設定
        self._init_shortcut_keys()

    def on_test_button_pressed(self):
        print('\n\n##################################################################\n####################### test button pressed ######################\n##################################################################')
        print('splitter size:', self.splitter.size())
        splitter_above_height = self.config_dict['splitter_4a_height']
        splitter_below_height = self.config_dict['splitter_4b_height']
        print('splitter_4ab_height:', splitter_above_height, splitter_below_height)
        try:
            pp(self.previous_df.columns.to_list())
            pp(self.previous_df.iloc[:, -3:])
        except Exception as e:
            print('Error in on_test_button_pressed:', e)

    def on_test_button_pressed_2(self):
        pass
        print(self.scrollArea_input.isVisible(), self.scrollArea_input.verticalScrollBar().singleStep())
        print(self.scrollArea_input_right.isVisible(), self.scrollArea_input_right.verticalScrollBar().singleStep())

    def pr(self, *args, **kwargs):
        if not self.is_frozen:
            if args:
                print(args)
            if kwargs:
                print(kwargs)

    def set_value_to_scrollbar(self, orientation):
        if self.scrollArea_input.isVisible():
            scrollbar_obj = self.scrollArea_input.verticalScrollBar()
            step = scrollbar_obj.singleStep()
        elif self.scrollArea_input_right.isVisible():
            scrollbar_obj = self.scrollArea_input_right.verticalScrollBar()
            step = scrollbar_obj.singleStep()
        if orientation == 'up':
            step = -step
        scrollbar_obj.setValue(scrollbar_obj.value() + step * 5)

    # main function ( focus_out_eventから ) __focus_out_002
    def do_event_of_line_edit_focus_out(self):
        self.prevuous_list_widget_index = self.listWidget_filepath.currentRow()
        if not self.is_enter_pressed and not self.is_tab_pressed: # エンターキー、タブキーが押されなかった場合はマウスクリック
            self.is_left_button_clicked_and_so_on = True
        if self.focus_in_line_widget_obj is None:
            return
        line_edit_index = self.obj_name_to_index_dict[self.focus_in_line_widget_obj.objectName()]
                # next_line_edit_index = line_edit_index + 1 if line_edit_index < len(self.data_list) - 1 else None
        data_type = self.data_list[line_edit_index]['data_type']
        is_ver1 = True if self.input_mode == 'ver1' else False
        self.current_event_filter = self.event_filter_dict[self.focus_in_line_widget_obj.objectName()]
        self.conversion_inputted_text() # テキスト変換処理(半角/全角)
        # メイン処理へ...
        self.check_type_line_edit_and_verify_text(self.focus_in_line_widget_obj, line_edit_index, data_type, is_ver1) # メイン処理
        self.set_values_pref_city_and_town()

    # main function: ( do_event_of_line_edit_focus_out から ) __focus_out_003
    def check_type_line_edit_and_verify_text(self, line_edit_obj ,line_edit_index, data_type: str, is_ver1: bool): # editFinished時の処理
        if self.img_pobj_dict is None:
            return
        if self.is_initialaized:
            return
        current_value = line_edit_obj.text()
        current_line_edit_index = line_edit_index
        current_time = time.time()
        # リスタート中、または、連続起動の場合は何もしない
        if (self.is_restart_processing
                or current_time - self.last_executing_time_of_check_and_verify < 0.05):
            self.is_executing_fx_editing_finished = False
            self.is_executing_fx_pressed_enter = False
            return
        # ****************** ベリファイ処理開始 ******************
        # VER1モードかつfocus_out_line_edit_objがある場合はベリファイ, noverの場合はベリファイしない...
        if self.is_enter_pressed:
            pass
        if is_ver1 and self.focus_in_line_widget_obj \
                and not 'nover' in self.main_data_dict[self.focus_in_line_widget_obj.objectName()]['data_type'].split('_'):
            if not self.is_rept_mode: # リピートモードでない場合
                if self.is_pdfmode:
                    row_index = self.current_index_for_pdf_df
                else:
                    row_index = self.current_file_index
                if row_index > len(self.previous_df) - 1:
                    pre_value = ''
                else:
                    pre_value = self.previous_df.iloc[row_index, line_edit_index]
            else: # rept
                if self.input_mode == 'new1':
                    row_index = self.prevuous_list_widget_index
                elif self.input_mode == 'ver1':
                    row_index = self.current_index_for_rept_and_ver
                if row_index > len(self.previous_df) - 1:
                    pre_value = ''
                else:
                    pre_value = self.previous_df.iloc[row_index, line_edit_index]
            if self.is_pdfmode and is_ver1:
                if self.current_index_for_pdf_df > len(self.previous_df) - 1:
                    pre_value = '' # new1で入力していない場合は空欄にする
            if not current_value == pre_value: # 前回の入力内容と異なる場合
                # 終了ボタンが押されてる場合の処理...
                if self.is_close_button_pressed:
                    return
                # マウスがスクロールエリアにない場合かつ# エンターキー、タブキーが押されていない場合...
                if not self.is_mouse_on_scroll_area \
                        and not self.is_enter_pressed and not self.is_tab_pressed:
                    self.is_mouse_on_scroll_area = False
                    return # 何もしない
                else:
                    # ベリファイダイアログのインスタンスを作成準備...
                    self.focus_out_line_widget_obj_befoer_collation = self.focus_in_line_widget_obj
                    if line_edit_obj.objectName() == self.last_input_line_widget.objectName() and self.is_rept_mode == True:
                        self.is_show_collation_dialog_on_last_and_rept_in_type_check = True
                        pass
                    if self.focus_out_obj_for_collation is not None:
                        line_edit_obj_for_pdfmode = line_edit_obj
                        line_edit_obj = self.focus_out_obj_for_collation
                        current_value = line_edit_obj.text()
                        line_edit_index = self.obj_name_to_index_dict[line_edit_obj.objectName()]
                        line_edit_index_for_pdfmode = self.obj_name_to_index_dict[line_edit_obj_for_pdfmode.objectName()]
                        if not self.is_pdfmode and not self.is_rept_mode and row_index <= len(self.previous_df) - 1:
                            pre_value = self.previous_df.iloc[row_index, line_edit_index]
                        if self.is_pdfmode and not self.is_rept_mode and self.current_index_for_pdf_df <= len(self.previous_df) - 1:
                            pre_value = self.previous_df.iloc[self.current_index_for_pdf_df, line_edit_index_for_pdfmode]
                        elif self.is_rept_mode:
                            if row_index <= len(self.previous_df) - 1:
                                pre_value = self.previous_df.iloc[row_index, line_edit_index]
                            else:
                                pre_value = ''
                    if pre_value != current_value:
                        # スクロールエリアの更新する...
                        is_updates_enabled_scroll_area_input = self.scrollArea_input.updatesEnabled()
                        is_updates_enabled_scroll_area_input_right = self.scrollArea_input_right.updatesEnabled()
                        if not is_updates_enabled_scroll_area_input:
                            self.scrollArea_input.setUpdatesEnabled(True)
                        if not is_updates_enabled_scroll_area_input_right:
                            self.scrollArea_input_right.setUpdatesEnabled(True)
                        # ____
                        self.pixmap_item_pos_on_collation_dialog = self.pixmap_item.pos()
                        collation_dialog = CollationDialog(self, pre_value, current_value, line_edit_obj)
                        self.deactivate_all_event_filter()
                        collation_dialog.exec_() # ベリファイダイアログを表示 #collation <--- 重要
                        self.activate_all_event_filter()
                        # スクロールエリアの更新を停止する...
                        if not is_updates_enabled_scroll_area_input:
                            self.scrollArea_input.setUpdatesEnabled(False)
                        if not is_updates_enabled_scroll_area_input_right:
                            self.scrollArea_input_right.setUpdatesEnabled(False)
                        # ____
                        collation_line_edit_obj = collation_dialog.line_edit_obj
                        self.is_show_collation_dialog_on_last_and_rept_after_collation = True
                        current_value = self.verified_value # ベリファイ後の値を取得
                        if self.is_collation_daialog_canceled == True:
                            self.is_collation_daialog_canceled = False
                            self.is_show_collation_dialog_on_last_and_rept_in_type_check = False
                            self.is_show_collation_dialog_on_last_and_rept_after_collation = False
                            if self.is_last_enter_pressed:
                                # self.set_focus_ime_and_rect(self.focus_out_line_widget_obj_befoer_collation)
                                self.set_focus_ime_and_rect(collation_line_edit_obj)
                            return
                # self.next_line_edit(current_index) # 次のLineEditにフォーカスを移動
        # ****************** ベリファイ処理終了 ******************
        # ****************** タイプチェックと色の変更開始 *******************
        # 最後のline_edit以外...
        if self.previous_list_widget_index + 1 != len(self.data_list):
            is_valid = self.check_type_line_edit(current_value, data_type, current_obj=line_edit_obj) # 現在のline edit textの型チェック
            palette = line_edit_obj.palette() # パレット取得
            if not is_valid and current_value != '': # 空欄でない、または 型が違う場合は文字色を赤くする
                palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.red)
                line_edit_obj.setPalette(palette) # 文字色を赤くする
            else: # 型が正しい場合は文字色を黒にする
                palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
                line_edit_obj.setPalette(palette) # 文字色を黒くする
        # ****************** タイプチェックと色の変更終了 *******************
        # Enterキーが押された場合 ただしリスタート時はのぞく...
        if self.is_enter_pressed and not self.is_restart_processing:
            self.processing_enter_key_in_line_edit_after_check(current_line_edit_index) # Enterキー押下時の処理
        self.is_show_collation_dialog_on_last_and_rept_after_collation = False
        self.last_executing_time_of_check_and_verify = current_time # 最終実行時間を更新
        self.is_executing_fx_pressed_enter = False
        self.is_executing_fx_editing_finished = False
        def _set_var():
            self.pixmap_item_pos_on_collation_dialog = None
        QTimer.singleShot(70, _set_var)

    # main function( check_type_line_edit_and_verify_textから ) __focus_out_004 __in_branch
    def processing_enter_key_in_line_edit_after_check(self, current_line_edit_index):
        if self.is_initialaized:
            return
        # *********************** エンターキー押下時の処理 開始 ***********************
        self.previous_list_widget_index_for_rept = self.listWidget_filepath.currentRow() # リピートモード用のリストウィジェットインデックスを保存
        if self.is_restart_processing: # リスタート時は何もしない
            return
        is_last_line = False
        # >> チェック用のLineEditがある場合はその値を取得して次に進むか判定
        has_check_lineedit = False
        for data in self.data_list:
            if 'ischeck' in data['data_type'].split('_'):
                lineedit_for_check = data['line_edit_obj']
                has_check_lineedit = True
                check_char = str(data['remarks'])
                break
        if has_check_lineedit:
            is_checked = True if lineedit_for_check.text() == check_char else False
        else:
            is_checked = True
        # チェック用のLineEditがある場合はその値を取得して次に進むか判定 <<
        # >> 最後のLineEditの場合
        if (
            current_line_edit_index == self.last_index_of_line_edit and
            is_checked
        ):
            is_last_line = True
            # 最後のLineEditの場合...
            if (
                self.is_show_collation_dialog_on_last_and_rept_after_collation
                and self.is_rept_mode
                and self.input_mode == 'ver1' # モード NEW1
            ): # リピートモードでベリファイ画面が表示された場合
                if QMessageBox.question(self, '確認',
                    'データを保存して次のレコードへ進みますか？\n\n' +
                    '※このメッセージは最後の入力項目のベリファイウインドウ内でエンター確定したときに表示されるものです',
                    QMessageBox.Yes | QMessageBox.No
                ) == QMessageBox.No:
                    # 次の画像に移動しない場合...
                    last_line_edit_obj = self.index_to_obj_dict[self.last_index_of_line_edit]
                    QTimer.singleShot(65, lambda: self.set_focus_to_target_edit_for_timer(last_line_edit_obj))
                    def set_false_to_is_last_enter_pressed():
                        self.is_last_enter_pressed = False
                    QTimer.singleShot(0, set_false_to_is_last_enter_pressed)
                    self.is_show_collation_dialog_on_last_and_rept_after_collation = False
                    return
                else:
                    self.is_enter_pressed = True
            is_valids_names_and_types = self.check_type_all_line_edit() # 全てのLineEditの型チェック
            is_valid_all_value = all(is_valids_names_and_types[0]) # 全ての値が正しいかどうか
            if is_valid_all_value and self.is_enter_pressed: # 全ての値が正しい場合
                # 入力値に誤り無し vew1ならここでログファイルを保存する処理を行う
                # ************
                is_list_clicked = False
                result = None
                if self.file_type == 'img':
                    self.process_of_before_change_image(None, is_list_clicked=is_list_clicked)
                elif self.file_type == 'pdf':
                    result = self.process_of_before_change_image(None, is_list_clicked=is_list_clicked) # 画像変更ダイアログを表示 # Main Function
                next_record_index, is_end = None, None
                if result is not None:
                    if len(result) == 1:
                        next_record_index = result[0]
                    elif len(result) == 2:
                        next_record_index, is_end = result
                # ************
                if is_end != True:
                    if self.input_mode == 'ver1':
                        if self.file_type == 'img':
                            self.output_log()
                        elif self.file_type == 'pdf':
                            self.output_log_for_pdf()
                    if not is_list_clicked:
                        self.current_index_for_pdf_df += 1 # インデックスを更新 <--- 重要
                    else:
                        self.current_index_for_pdf_df = next_record_index # インデックスを更新 <--- 重要
                    # PDFシングルモード(ver1 mode)の場合、最後の画像のダイアログを表示...
                    is_updates_enabled_scroll_area_input = self.scrollArea_input.updatesEnabled()
                    is_updates_enabled_scroll_area_input_right = self.scrollArea_input_right.updatesEnabled()
                    if self.is_single_pdf_mode and self.input_mode == 'ver1':
                        if self.current_index_for_pdf_df > self.listWidget_pdf.count() - 1: # 最後の画像か？
                            # 最後の画像の場合の処理...
                            # スクロールエリア更新処理...
                            if not is_updates_enabled_scroll_area_input:
                                self.scrollArea_input.setUpdatesEnabled(True)
                            if not is_updates_enabled_scroll_area_input_right:
                                self.scrollArea_input_right.setUpdatesEnabled(True)
                            QMessageBox.information(self, '情報', 'ベリファイが完了しました\n\n初期設定ダイアログに戻ります', QMessageBox.Ok)
                            # スクロールエリア更新停止...
                            if not is_updates_enabled_scroll_area_input:
                                self.scrollArea_input.setUpdatesEnabled(False)
                            if not is_updates_enabled_scroll_area_input_right:
                                self.scrollArea_input_right.setUpdatesEnabled(False)
                            # ____
                            self.is_restart_processing = True
                            self.restart_app()
                            def _var_set():
                                self.is_restart_processing = False
                            QTimer.singleShot(0, _var_set)
                            self.is_last_img_file_process_activated = True
                        else: # 最後の画像でなければ画像を更新
                            # PDFシングル: ここで次の画像に移動する処理をおこなう
                            self.listWidget_pdf.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
                            self.listWidget_pdf.setCurrentRow(self.current_index_for_pdf_df) # <--- 重要 pdflistの選択を変更
                            self.listWidget_pdf.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
                            self.change_pdf_image(self.current_index_for_pdf_df)
                    elif self.is_single_pdf_mode and self.input_mode == 'new1': # Mode New1
                        if self.file_type == "pdf":
                            file_cnt = self.listWidget_pdf.count()
                        elif self.file_type == "img":
                            file_cnt = self.listWidget_filepath.count()
                        if self.current_index_for_pdf_df > file_cnt - 1: # 最後の画像か？
                            # スクロールエリア更新処理...
                            if not is_updates_enabled_scroll_area_input:
                                self.scrollArea_input.setUpdatesEnabled(True)
                            if not is_updates_enabled_scroll_area_input_right:
                                self.scrollArea_input_right.setUpdatesEnabled(True)
                            # ____
                            if QMessageBox.question(self, '確認',
                                '最後の画像です 画像フォルダ、または[NEW/VER]モードを変更しますか？\n\n'
                                'Yes: 初期設定ダイアログを開きます\n\n'
                                'No: この画面にとどまります'
                                , QMessageBox.Yes | QMessageBox.No
                                ) == QMessageBox.No:
                                # スクロールエリア更新停止...
                                if not is_updates_enabled_scroll_area_input:
                                    self.scrollArea_input.setUpdatesEnabled(False)
                                if not is_updates_enabled_scroll_area_input_right:
                                    self.scrollArea_input_right.setUpdatesEnabled(False)
                                # ____
                                # ノー とどまる場合は idx を戻し、listWidget_pdf_recordの選択も戻す
                                self.current_index_for_pdf_df -= 1
                                selection_mode = self.listWidget_pdf_record.selectionMode()
                                self.listWidget_pdf_record.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
                                self.listWidget_pdf_record.setCurrentRow(self.current_index_for_pdf_df)
                                self.listWidget_pdf_record.setSelectionMode(selection_mode)
                                return
                            else: # イエス 初期設定ダイアログを開く
                                # スクロールエリア更新停止...
                                if not is_updates_enabled_scroll_area_input:
                                    self.scrollArea_input.setUpdatesEnabled(False)
                                if not is_updates_enabled_scroll_area_input_right:
                                    self.scrollArea_input_right.setUpdatesEnabled(False)
                                # ____
                                self.is_restart_processing = True
                                self.restart_app() # リスタート処理
                                def _var_set():
                                    self.is_restart_processing = False
                                QTimer.singleShot(0, _var_set)
                                self.is_last_img_file_process_activated = True
                        else: # 最後の画像でなければ画像を更新
                            # PDFシングル: ここで次の画像に移動する処理をおこなう
                            self.listWidget_pdf.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
                            self.listWidget_pdf.setCurrentRow(self.current_index_for_pdf_df) # <--- 重要 pdflistの選択を変更
                            self.listWidget_pdf.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
                            self.change_pdf_image(self.current_index_for_pdf_df)
                if not self.is_canceled_next_img and is_last_line and not self.is_restart_processing:
                    self.current_index_for_img_df += 1 # インデックスを更新 <--- 重要
                self.is_canceled_next_img = False
            else: # 入力値に誤りがある場合
                error_info = self.get_error_info(is_valids_names_and_types)
                self.is_show_type_error_for_rect = True
                self.deactivate_all_event_filter()
                # スクロールエリア更新処理...
                is_updates_enabled_scroll_area_input = self.scrollArea_input.updatesEnabled()
                is_updates_enabled_scroll_area_input_right = self.scrollArea_input_right.updatesEnabled()
                if not is_updates_enabled_scroll_area_input:
                    self.scrollArea_input.setUpdatesEnabled(True)
                if not is_updates_enabled_scroll_area_input_right:
                    self.scrollArea_input_right.setUpdatesEnabled(True)
                QMessageBox.warning(self, 'エラー', '不正な入力値\nまたはエンコードできない特殊な文字があります\n\n' + error_info, QMessageBox.Ok)
                if not is_updates_enabled_scroll_area_input:
                    self.scrollArea_input.setUpdatesEnabled(False)
                if not is_updates_enabled_scroll_area_input_right:
                    self.scrollArea_input_right.setUpdatesEnabled(False)
                self.activate_all_event_filter()
                def _set_true_to_var():
                    self.is_show_type_error_for_rect = False
                QTimer.singleShot(80, _set_true_to_var)
                self.is_last_enter_canceled = True
                if self.focus_in_line_widget_obj is None and self.focus_out_line_widget_obj_befoer_collation is not None:
                    self.focus_in_line_widget_obj = self.focus_out_line_widget_obj_befoer_collation
                if current_line_edit_index == len(self.data_list) - 1:
                    QTimer.singleShot(50, self.on_line_edit_canceled)
                self.is_executing_fx_pressed_enter = False
                return
        # 最後のLineEditの場合 <<
        elif current_line_edit_index == self.last_index_of_line_edit and not is_checked:
            # QTimer.singleShot(500, lambda: self.pixmap_item.set_rect(lineedit_for_check))
            pass
        else: # >> 最後のLineEditでない場合
            self.next_line_edit(current_line_edit_index) # 次のLineEditにフォーカスを移動
        self.is_executing_fx_pressed_enter = False
        self.is_img_listwidget_select_canceled = False
        # 最後のLineEditでない場合 <<
        # *********************** エンターキー押下時の処理 終了 ***********************

    def change_pdf_image(self, file_index):
        if self.file_type == "pdf":
            next_item = self.listWidget_pdf.item(file_index)
        elif self.file_type == "img":
            next_item = self.listWidget_filepath.item(file_index)
        if next_item is None:
            QMessageBox.warning(self, 'エラー', '画像が見つかりませんでした\n\n最初の画面に戻ります', QMessageBox.Ok)
            self.restart_app(is_button_pressed=False)
            return
        if self.file_type == "pdf":
            next_record = next_item.data(100)
            next_pdf_fobj = next_record['pdf_obj'] if not self.is_pdfmode_to_read_image_file else next_record['img_obj']
            if not os.path.exists(str(next_pdf_fobj)):
                ans_num = self.create_multi_button_msg(self, 'エラー', f'PDFファイルが見つかりませんでした\n\n対象ファイル名:\n{next_pdf_fobj.name}', ['リトライ', '再起動'], 0, 'warning')
                if ans_num == 0:
                    while True:
                        if not os.path.exists(str(next_pdf_fobj)):
                            ans_num = self.create_multi_button_msg(self, 'エラー', f'PDFファイルが見つかりませんでした\n\n対象ファイル名:\n{next_pdf_fobj.name}', ['リトライ', '再起動'], 0, 'warning')
                            if ans_num == 1:
                                self.restart_app(is_button_pressed=False)
                                return
                        else:
                            QMessageBox.information(self, '情報', 'PDFファイルが見つかりました', QMessageBox.Ok)
                            break
                elif ans_num == 1:
                    self.restart_app(is_button_pressed=False)
                    return
            next_main_index = next_record['main_index']
            self.label_pdf.setText(f'{next_main_index + 1:03} / {self.total_pdf_page_count:03}    ') # Labelにページ総数とページ番号を表示
        elif self.file_type == "img":
            fp_img: str = next_item.text()
            fp_img = fp_img.strip()

        if not self.is_pdfmode_to_read_image_file: # PDFモードでPDFを読み込む場合
            self.pixmap = self.pdf_img_reader.get_img_from_pdf(next_record['file_name'], next_record['page_index'])
            self.set_image_from_pixmap(is_list_clicked=True)
        elif self.is_pdfmode_to_read_image_file:
            file_obj = next_record['img_obj']
            self.pixmap = QPixmap(str(file_obj)) # pixmap更新
            self.set_image_from_pixmap(is_list_clicked=True, filepath=str(file_obj.resolve())) # 角度取得用filepath付き
        elif self.file_type == "img" : # PDFモードで画像ファイルを読み込む場合
            self.pixmap = QPixmap(fp_img) # pixmap更新
            file_obj = Path(fp_img).resolve()
            if file_obj:
                print('next_file:', str(file_obj))
            self.set_image_from_pixmap(is_list_clicked=True, filepath=str(file_obj.resolve())) # 角度取得用filepath付き

    # main function
    # 画像が変わる前のダイアログや、タイプチェック処理 __branch_001
    def process_of_before_change_image(self, next_file_index = None, is_list_clicked = True): # 画像変更時のダイアログ表示
        if self.file_type == 'img':
            if is_list_clicked == False: # エンターキーでの変更の場合
                message =  'データを保存して画像を変更しますか？'
                is_enterkey_pressed = True
            else: # リストアイテムクリックでの変更の場合
                message = 'データを保存して次の画像に進みますか？'
                is_enterkey_pressed = False
                next_file_index = self.next_index_for_filepath_list
            if not self.is_rept_mode: # リピートモードでない場合
                if is_enterkey_pressed and self.current_file_index + 1 == len(self.img_pobj_dict):
                    # 最後の画像の場合の処理...
                    self.helper_of_last_image_before_change()
                else:
                    # 最後の画像でない場合の処理...
                    self.helper_of_not_last_image_before_change(message, next_file_index, is_enterkey_pressed, is_list_clicked)
            elif self.is_rept_mode: # リピートモードの場合 rept_True
                self.helper_of_not_last_image_before_change(message, next_file_index, is_enterkey_pressed, is_list_clicked)
            def _set_true_to_var():
                self.is_last_enter_canceled = False
            QTimer.singleShot(60, _set_true_to_var)
        elif self.file_type == 'pdf': # PDFの場合
            is_enterkey_pressed = True
            next_file_index = self.current_index_for_pdf_df + 1
            is_list_clicked = False
            self.is_last_img_file_process_activated = True
            flag_dict = self.helper_of_before_change_for_pdf(next_file_index, is_list_clicked)
            if flag_dict is None:
                flag_dict = {}
            is_end = True if flag_dict.get('is_canceled', False) or flag_dict.get('is_not_valid', False) or flag_dict.get('is_output_error', False) else False
            self.is_last_img_file_process_activated = False
            return next_file_index, is_end

    # main function PDF
    # PDFの場合の画像変更前の処理 __branch_002_pdf
    def helper_of_before_change_for_pdf(
            self, next_record_index, is_list_clicked = False, pre_index=None, pre_item=None, pre_text=None
    ):
        current_time = time.time()
        current_filename = None
        if pre_item is not None and pre_item.data(100) is not None:
            if pre_item.data(100) is not None:
                current_filename = pre_item.data(100)['file_name']
        else:
            if not self.is_single_pdf_mode:
                item = self.listWidget_pdf.currentItem()
            else: # pdfシングルモードの時の画像名
                item = self.listWidget_pdf.item(self.current_index_for_pdf_df)
            if item.data(100) is not None:
                current_filename = item.data(100)['file_name']
        if (
            int(self.last_executing_time_of_helper_of_not_last_image_before_change) != int(0)
            and current_time - self.last_executing_time_of_helper_of_not_last_image_before_change < 0.2
        ):
            print('helper_of_before_change_for_pdf: 連続実行防止')
            return
        self.last_executing_time_of_helper_of_not_last_image_before_change = current_time
        # ********************** 最後でない画像の処理開始 ***********************
        if not self.pdf_page_list and not self.is_pdfmode_to_read_image_file: # 追加
            return
        # is_return = (
        #     self.is_last_img_file_process_activated and
        #     self.current_file_index + 1 == len(self.img_pobj_dict) and
        #     not is_list_clicked
        # )
        # if is_return:
        #     self.is_last_img_file_process_activated = False
        #     return # IMPORTANT # DELETE
        # リスタート時と最後のエンター時は何もしない
        if self.is_restart_processing:
            return
        # if pre_item and pre_text == '新しいレコード' and is_list_clicked:
        is_all_blanks = []
        for data in self.data_list:
            if data['line_edit_obj'].text() == '':
                is_all_blanks.append(True)
            else:
                is_all_blanks.append(False)
        # pre_item あり and リストクリック and 新しいレコード and すべてのlineの値が空欄なら -> データが同じなら保存しない
        is_update_enabled_scroll_area_input = self.scrollArea_input.updatesEnabled()
        is_update_enabled_scroll_area_input_right = self.scrollArea_input_right.updatesEnabled()
        if all(is_all_blanks) and pre_item and pre_text == '新しいレコード' and is_list_clicked:
            pass
        else:
            # スクロールエリアのアップデートを有効にする...
            if not is_update_enabled_scroll_area_input:
                self.scrollArea_input.setUpdatesEnabled(True)
            if not is_update_enabled_scroll_area_input_right:
                self.scrollArea_input_right.setUpdatesEnabled(True)
            # ____
            if not is_list_clicked:
                message = f'{self.current_index_for_pdf_df + 1} 人目のデータをCSVに保存しますか？\n\nCSVに保存されるファイル名: {current_filename}'
            else: # リストクリック時
                if pre_item and pre_text == '新しいレコード':
                    message = (
                        '編集対象を変更しますか？\n\n※新しいレコードでリストクリックの場合はデータは保存されません\n\n'
                        '※保存する場合は一番下のテキストボックス内でエンターキーを押してください'
                    )
                else:
                    message = (
                        f'{self.current_index_for_pdf_df + 1} 人目のデータをCSVに保存して編集対象を変更しますか？\n\n'
                        f'CSVに保存されるファイル名: {current_filename}'
                    )
            if QMessageBox.question(
                    self, '確認', f'{message}',
                    QMessageBox.Yes | QMessageBox.No
            ) == QMessageBox.No: # ノーの場合
                # スクロールエリアのアップデートを無効にする...
                if not is_update_enabled_scroll_area_input:
                    self.scrollArea_input.setUpdatesEnabled(False)
                if not is_update_enabled_scroll_area_input_right:
                    self.scrollArea_input_right.setUpdatesEnabled(False)
                # ____
                self.is_not_set_sub_rect = True
                self.is_last_enter_canceled = True
                if not is_list_clicked:
                    self.deactivate_all_event_filter()
                    self.last_input_line_widget.setFocus() # 最後のLineEditにフォーカスを移動
                    self.activate_all_event_filter()
                # 次の画像に移動しない場合...
                last_line_edit_obj = self.index_to_obj_dict[self.last_index_of_line_edit]
                if not is_list_clicked:
                    QTimer.singleShot(55, lambda: self.set_focus_to_target_edit_for_timer(last_line_edit_obj))
                def _next_row_select():
                    self.is_last_enter_pressed = False
                    if is_list_clicked:
                        self.listWidget_pdf_record.blockSignals(True)
                        self.select_next_item_of_list_widget(pre_index)
                        self.listWidget_pdf_record.blockSignals(False)
                def _set_last_obj(): # ここを変更
                    self.focus_in_line_widget_obj = self.data_list[-1]['line_edit_obj']
                QTimer.singleShot(100, _set_last_obj) # ここを変更
                QTimer.singleShot(0, _next_row_select)
                return {'is_canceled': True}
        # Yes: 次の画像に移動する場合... <- 画像の変更処理 最初のラインエディットにフォーカスを移動, リピートモードはこっちのみ
        # ____ 型チェック____
        # スクロールエリアのアップデートを無効にする...
        if not is_update_enabled_scroll_area_input:
            self.scrollArea_input.setUpdatesEnabled(False)
        if not is_update_enabled_scroll_area_input_right:
            self.scrollArea_input_right.setUpdatesEnabled(False)
        # ____
        is_valids_names_and_types = self.check_type_all_line_edit() # 全てのLineEditの型チェック
        is_valid_all_value = all(is_valids_names_and_types[0]) # 全ての値が正しいかどうか
        if not is_valid_all_value:
            # 入力値に誤りがある場合...
            error_info = self.get_error_info(is_valids_names_and_types)
            self.is_show_type_error_for_rect = True
            is_updates_enabled_scroll_area_input = self.scrollArea_input.updatesEnabled()
            is_updates_enabled_scroll_area_input_right = self.scrollArea_input_right.updatesEnabled()
            if not is_updates_enabled_scroll_area_input:
                self.scrollArea_input.setUpdatesEnabled(True)
            if not is_updates_enabled_scroll_area_input_right:
                self.scrollArea_input_right.setUpdatesEnabled(True)
            QMessageBox.warning(self, 'エラー', '不正な入力値\nまたはエンコードできない特殊な文字があります\n\n' + error_info, QMessageBox.Ok)
            if not is_updates_enabled_scroll_area_input:
                self.scrollArea_input.setUpdatesEnabled(False)
            if not is_updates_enabled_scroll_area_input_right:
                self.scrollArea_input_right.setUpdatesEnabled(False)
            def fx():
                self.is_show_type_error_for_rect = False
                if is_list_clicked:
                    self.listWidget_pdf_record.blockSignals(True)
                    self.select_next_item_of_list_widget(pre_index)
                    self.listWidget_pdf_record.blockSignals(False)
            QTimer.singleShot(80, fx)
            self.is_last_enter_canceled = True
            return {'is_not_valid': True}

        # ヘッダーが多い場合は減らす
        if self.mode_config_manager.get_need_df_transformed((self.main_mode)):
            valid_headers = self.obj_name_lst
            self.current_df = self.current_df[valid_headers + [10000, 20000, 30000]]
        self.current_df = self.current_df.fillna('') # NaNを空文字に変換
        self.current_df = self.current_df.astype(str) # 全てのデータを文字列に変換
        if pre_item and pre_text == '新しいレコード' and is_list_clicked: # 新しいレコード and リストクリック
            pass
        else:
            # ************
            is_error = self.add_record_for_pdf() # dfにレコード追加 <----------- 重要
            # ************
            if is_error:
                return {'is_output_error': True}
        if next_record_index in self.current_df.index:
            # dfに次のレコードが存在する場合は 入力欄にテキストをセット
            value_list = self.current_df.loc[next_record_index].to_list()
            self.set_new_text_to_line_edits(value_list) # dfに次のレコードが存在する場合は 入力欄にテキストをセット
            # 型が違う場合は文字色を赤くする処理...
            self.change_color_black_or_red(is_ignore_empty=True)
        elif not (self.is_single_pdf_mode and self.current_index_for_pdf_df == self.listWidget_pdf.count() - 1):
            self.deactivate_all_event_filter()
            self.set_blank_to_line_edits() # dfに次のレコードが存在しない場合は ---------> 入力欄を全て空欄にする
            self.change_color_of_all_line_edits('black') # 全てのLineEditの文字色を黒にする
            self.deactivate_all_event_filter()
        self.deactivate_all_event_filter()
        self.lineEdit_0_.setFocus()
        self.first_input_line_widget.setFocus() # 最初のLineEditにフォーカスを移動
        ime_mode = self.obj_name_to_ime_dict[self.first_input_line_widget.objectName()]
        self.activate_all_event_filter()
        self.set_ime_from_ime_mode_text(ime_mode) # IMEの設定 <----------- 重要
        # self.change_image(next_file_index) # 画像の変更処理 <----------- 重要
        if self.radioButton_automove_on.isChecked() and self.is_last_enter_pressed == False:
            def set_rect_last_edit():
                self.pixmap_item.set_rect(is_first=True)
            QTimer.singleShot(30, lambda: set_rect_last_edit()) # 移動モードの場合最初の矩形に移動
        time.sleep(0.1)
        if self.input_mode == 'ver1' and self.current_index_for_pdf_df + 1 == self.previous_df.shape[0]:
            # スクロールエリア更新処理...
            is_updates_enabled_scroll_area_input = self.scrollArea_input.updatesEnabled()
            is_updates_enabled_scroll_area_input_right = self.scrollArea_input_right.updatesEnabled()
            if not is_updates_enabled_scroll_area_input:
                self.scrollArea_input.setUpdatesEnabled(True)
            if not is_updates_enabled_scroll_area_input_right:
                self.scrollArea_input_right.setUpdatesEnabled(True)
            # ____
            if not self.is_single_pdf_mode:
                QMessageBox.information(self, '情報', 'New1にある全てのデータをベリファイしました'
                        , QMessageBox.Ok
                )
            # スクロールエリア更新停止...
            if not is_updates_enabled_scroll_area_input:
                self.scrollArea_input.setUpdatesEnabled(False)
            if not is_updates_enabled_scroll_area_input_right:
                self.scrollArea_input_right.setUpdatesEnabled(False)
            # ____
        # リストのアイテム処理...
        if pre_item and pre_text == '新しいレコード' and is_list_clicked:
            new_list_widget_index = next_record_index
        else:
            name = self.mode_config_manager.get_name_from_df(
                self.main_mode,
                self.current_df,
                self.current_index_for_pdf_df
            ) # listWidget_pdf_recordに表示する名前を取得 # WIP
            if not name:
                name = ""
            # if not self.is_pdfmode_to_read_image_file:
            item = self.listWidget_pdf_record.item(self.current_index_for_pdf_df)
            item.setText(f'{self.current_index_for_pdf_df + 1:03}{self.sep_of_line_widget_text}{name}')
            # エンターかつ最後の画像の場合は新しいレコードを追加
            if not is_list_clicked and self.current_index_for_pdf_df == self.listWidget_pdf_record.count() - 1:
                # PDF single mode かつ 最後の画像の場合は 新しいレコード は追加しない
                if self.is_single_pdf_mode and self.current_index_for_pdf_df != self.listWidget_pdf.count() - 1:
                    item = QListWidgetItem('新しいレコード')
                    self.listWidget_pdf_record.addItem(item)
            if not is_list_clicked:
                new_list_widget_index = self.current_index_for_pdf_df + 1
            else:
                new_list_widget_index = next_record_index
        self.listWidget_pdf_record.blockSignals(True)
        self.select_next_item_of_list_widget(new_list_widget_index)
        self.listWidget_pdf_record.blockSignals(False)

    def add_record_for_pdf(self): # レコード追加処理 __branch_003_pdf
        if self.mode_config_manager.get_need_df_transformed(self.main_mode):
            record_dict = {data['name']: data['line_edit_obj'].text() for data in self.data_list} # 全ての入力項目を取得
        else:
            record_dict = {data['index']: data['line_edit_obj'].text() for data in self.data_list} # 全ての入力項目を取得
        timestamp = self.get_timestamp()
        if not self.is_single_pdf_mode:
            current_list_item = self.listWidget_pdf.currentItem()
        else: # pdfシングルモードの時の画像名
            current_list_item = self.listWidget_pdf.item(self.current_index_for_pdf_df)
        # 10000, 20000, 30000 列に代入
        current_file_name = current_list_item.data(100)['file_name']
        file_info_text = f'{current_file_name}' # ファイル情報テキスト # ページ番号無し
        record_dict.update({10000: file_info_text, 20000: self.user_name, 30000: timestamp})
        record_df = pd.DataFrame(record_dict, index=[self.current_index_for_pdf_df]) # 辞書から1レコードDataFrameを作成(インデックスはファイルインデックス)
        record_df = record_df.reset_index(drop=True)
        if self.is_new1_no_edit and self.current_index_for_pdf_df in self.current_df.index: # no edit レコードが存在する場合
            raise Exception('編集不可モードではレコードが存在する場合の処理は未実装です')
        elif not self.is_new1_no_edit and self.current_index_for_pdf_df in self.current_df.index: # edit可
            self.current_df.loc[self.current_index_for_pdf_df] = record_df.loc[0] # レコードを更新
        else: # レコードが存在しない場合
            self.current_df = pd.concat([self.current_df, record_df], axis=0, ignore_index=True) # レコードを追加
        is_error = self.output_csv() # CSV保存処理 <--- ここで保存
        return is_error # csv保存処理が失敗した場合はTrueを返す

    def output_log_for_pdf(self): # ログファイルを出力する処理 __branch_004_pdf
        if self.is_restart_processing or self.input_mode == 'new1': # リスタート時, new1時 は何もしない
            return
        self.previous_df = self.previous_df.astype(str)
        self.previous_df = self.previous_df.fillna('')
        # self.previous_df = self.previous_df.sort_index(axis=1)
        self.previous_df = self.previous_df.sort_index(axis=0)
        values = []
        try:
            values = self.current_df.iloc[self.current_index_for_pdf_df].to_list()
        except:
            return
        # values = [株式会社..., 部長, 田中太郎...]
        pre_values = []
        timestamp = self.get_timestamp()
        # current_dfの行数がprevious_dfの行数より多くなったらprevious_dfに空欄行を追加...(rept_line_editのみ空欄の行にする)


        for i in range(self.line_edit_count):
            if self.previous_df.shape[0] - 1 < self.current_index_for_pdf_df:
                pre_value = ''
            else:
                pre_value = self.previous_df.iloc[self.current_index_for_pdf_df, i]
            pre_values.append(pre_value)
        if self.previous_df.shape[0] - 1 < self.current_index_for_pdf_df:
            new1_user_name = self.previous_df.loc[0, 20000]
        else:
            new1_user_name = self.previous_df.loc[self.current_index_for_pdf_df, 20000]
        is_write_log_needed = False
        columns=['timestamp', 'item', 'new1_user_name', 'ver1_user_name', 'new1_value', 'ver1_value', 'page_filename']
        empty_record = pd.DataFrame(columns=columns)
        one_record_log_df = empty_record.copy()
        another_logs = []
        for i, (pre, next) in enumerate(zip(pre_values, values)):
            if pre != next:
                # ログの内容を作成...
                record_df = empty_record.copy()
                list_index = self.listWidget_pdf.currentRow()
                meta_record = self.listWidget_pdf.item(list_index).data(100)
                file_name = meta_record["file_name"]
                if not self.is_pdfmode_to_read_image_file:
                    page = f'P{meta_record["page_index"] + 1:03}'
                    num = f'{self.current_index_for_pdf_df + 1}人目'
                    file_info = f'{num}_{page}:{file_name}'
                else:
                    file_info = file_name
                current_item = self.data_list[i]['name']
                another_logs.extend([file_info, current_item, f'New:{pre}', f'Ver:{next}'])
                if pre != next: # 前回の入力内容と異なる場合はログに記録
                    record_df.loc[0] = [
                            timestamp, current_item, new1_user_name,
                            self.user_name, pre, next, file_info
                    ]
                one_record_log_df = pd.concat([one_record_log_df, record_df], axis=0)
        is_write_log_needed = True
        self.log_df = pd.concat([self.log_df, one_record_log_df], axis=0)
        keep = 'last' if self.is_rept_mode else 'first'
        subset = ['item', 'new1_user_name', 'ver1_user_name', 'new1_value', 'ver1_value' ,'page_filename']
        self.log_df = self.log_df.drop_duplicates(subset=subset, keep=keep) # 重複削除
        self.log_df = self.log_df.fillna('')
        self.log_df = self.log_df.reset_index(drop=True)
        new_columns = ['timestamp', 'item', 'new1_value', 'ver1_value', 'new1_user_name', 'ver1_user_name', 'page_filename']
        self.log_df = self.log_df[new_columns]
        new_export_columns = ['確定日時', '属性', '値_new1', '値_ver1', 'ユーザー_new1', 'ユーザー_ver1', 'ファイル名']
        export_log_df = self.log_df.copy()
        export_log_df.columns = new_export_columns
        # ログファイルを出力...
        try:
            DataIO.write_csv_with_header(
                self ,export_log_df, self.output_log_fobj, encoding=self.encode_type, has_header=True
            )
        except PermissionError:
            QMessageBox.warning(self, 'エラー', 'ログファイルの書き込みに失敗しました', QMessageBox.Ok)
        if is_write_log_needed:
            log_file_path = str(self.output_log_fobj)
            try:
                if not os.path.exists(log_file_path): # ログファイルが存在しない場合作成する
                    with open(log_file_path, 'w', encoding=self.encode_type) as f:
                        f.write('')
                with open(log_file_path, 'a', encoding=self.encode_type) as f:
                    f.write('')
            except PermissionError:
                QMessageBox.warning(self, 'エラー', 'ログファイルの書き込みに失敗しました', QMessageBox.Ok)

    # main function last
    def helper_of_last_image_before_change(self): # __branch_002_img not last
        # ********************** 最後の画像の場合の処理開始 ***********************
        # 最後の画像の場合の処理、かつ、エンター押下時...
        self.is_last_img_file_process_activated = True
        if QMessageBox.question(self, '確認',
                    '最後の画像です 画像フォルダ、または[NEW/VER]モードを変更しますか？\n\n'
                    'Yes: データをCSVに保存後、初期設定ダイアログを開きます\n\n'
                    'No: データをCSVに保存後、この画面にとどまります'
                    , QMessageBox.Yes | QMessageBox.No
                    ) == QMessageBox.No:
            # ノー:
            self.is_canceled_next_img = True
            self.is_not_set_sub_rect = True
            self.is_last_enter_canceled = True
            _ = self.add_record() # Noの場合はCSVを保存して元の画面に戻る
            last_line_edit_obj = self.index_to_obj_dict[self.last_index_of_line_edit]
            QTimer.singleShot(55, lambda: self.set_focus_to_target_edit_for_timer(last_line_edit_obj))
            def _set_false_to_is_last_enter_pressed_1():
                self.is_last_enter_pressed = False
            QTimer.singleShot(0, _set_false_to_is_last_enter_pressed_1)
        else: # イエス: CSV保存後 アプリ初期化 フォルダ設定画面に移動
            is_error = self.add_record()
            if is_error:
                last_line_edit_obj = self.index_to_obj_dict[self.last_index_of_line_edit]
                QTimer.singleShot(55, lambda: self.set_focus_to_target_edit_for_timer(last_line_edit_obj))
                def _set_false_to_is_last_enter_pressed_2():
                    self.is_last_enter_pressed = False
                QTimer.singleShot(0, _set_false_to_is_last_enter_pressed_2)
                self.is_canceled_next_img = True
                return
            self.output_log()
            self.is_restart_processing = True
            self.restart_app()
            def _var_set():
                self.is_restart_processing = False
            QTimer.singleShot(0, _var_set)
        self.is_last_img_file_process_activated = True
        # ********************** 最後の画像の場合の処理終了 ***********************

    # main function not last
    # 最後でない画像の処理関数  # __branch_002_img last
    def helper_of_not_last_image_before_change(self, message, next_file_index, is_enterkey_pressed, is_list_clicked):
        current_time = time.time()
        if current_time - self.last_executing_time_of_helper_of_not_last_image_before_change < 0.2:
            return
        self.last_executing_time_of_helper_of_not_last_image_before_change = current_time
        # ********************** 最後でない画像の処理開始 ***********************
        if not self.img_pobj_dict:
            return
        if self.is_last_img_file_process_activated and self.current_file_index + 1 == len(self.img_pobj_dict) and not is_list_clicked:
            self.is_last_img_file_process_activated = False
            return
        # リスタート時と最後のエンター時は何もしない
        if self.is_restart_processing:
            return
        if next_file_index is None:
            if not self.is_rept_mode:
                next_file_index = self.current_file_index + 1
            else: # リピートモードの場合
                next_file_index = self.listWidget_filepath.currentRow() + 1
        try: # リストクリックの場合はシグナルを切断
            self.listWidget_filepath.currentItemChanged.disconnect(self.on_list_widget_selected)
        except:
            pass
        # message = 'データを保存して次の画像に進みますか？' or 'データを保存して画像を変更しますか？' リストクリックかどうか？
        if not self.is_rept_mode: # リピートモードでない場合
            if QMessageBox.question(self, '確認', message, QMessageBox.Yes | QMessageBox.No
                    ) == QMessageBox.No:
                self.is_canceled_next_img = True
                self.is_not_set_sub_rect = True
                self.is_last_enter_canceled = True
                is_executed_cancel_event = False
                if not is_list_clicked:
                    self.deactivate_all_event_filter()
                    self.last_input_line_widget.setFocus() # 最後のLineEditにフォーカスを移動
                    self.activate_all_event_filter()
                else: # リストクリックの場合
                    QTimer.singleShot(0, lambda: self.on_line_edit_canceled_for_listwidget())
                    is_executed_cancel_event = True
                # 次の画像に移動しない場合...
                last_line_edit_obj = self.index_to_obj_dict[self.last_index_of_line_edit]
                if not is_list_clicked:
                    QTimer.singleShot(55, lambda: self.set_focus_to_target_edit_for_timer(last_line_edit_obj))
                else:
                    if is_executed_cancel_event == False:
                        QTimer.singleShot(45, lambda: self.on_line_edit_canceled_for_listwidget())
                self.is_img_listwidget_select_canceled = True
                QTimer.singleShot(110, lambda: self.listWidget_filepath.currentItemChanged.connect(self.on_list_widget_selected)) # シグナルを復元)
                def _set_false_to_is_last_enter_pressed():
                    self.is_last_enter_pressed = False
                QTimer.singleShot(0, _set_false_to_is_last_enter_pressed)
                return
        # Yes: 次の画像に移動する場合... <- 画像の変更処理 最初のラインエディットにフォーカスを移動, リピートモードはこっちのみ
        # 型チェック...
        is_valids_names_and_types = self.check_type_all_line_edit() # 全てのLineEditの型チェック
        is_valid_all_value = all(is_valids_names_and_types[0]) # 全ての値が正しいかどうか
        if not is_valid_all_value:
            # 入力値に誤りがある場合...
            error_info = self.get_error_info(is_valids_names_and_types)
            self.is_show_type_error_for_rect = True
            self.deactivate_all_event_filter()
            is_updates_enabled_scroll_area_input = self.scrollArea_input.updatesEnabled()
            is_updates_enabled_scroll_area_input_right = self.scrollArea_input_right.updatesEnabled()
            if not is_updates_enabled_scroll_area_input:
                self.scrollArea_input.setUpdatesEnabled(True)
            if not is_updates_enabled_scroll_area_input_right:
                self.scrollArea_input_right.setUpdatesEnabled(True)
            QMessageBox.warning(self, 'エラー', '不正な入力値\nまたはエンコードできない特殊な文字があります\n\n' + error_info, QMessageBox.Ok)
            if not is_updates_enabled_scroll_area_input:
                self.scrollArea_input.setUpdatesEnabled(False)
            if not is_updates_enabled_scroll_area_input_right:
                self.scrollArea_input_right.setUpdatesEnabled(False)
            self.activate_all_event_filter()
            def _set_value_for_rect_var():
                self.is_show_type_error_for_rect = False
            QTimer.singleShot(80, _set_value_for_rect_var)
            self.is_last_enter_canceled = True
            if (self.focus_in_line_widget_obj
                    and self.obj_name_to_index_dict[self.focus_in_line_widget_obj.objectName()] == len(self.data_list) - 1):
                if not is_list_clicked:
                    QTimer.singleShot(50, self.on_line_edit_canceled)
                else:
                    QTimer.singleShot(50, lambda: self.on_line_edit_canceled_for_listwidget())
            self.is_img_listwidget_select_canceled = True
            QTimer.singleShot(110, lambda: self.listWidget_filepath.currentItemChanged.connect(self.on_list_widget_selected)) # シグナルを復元
            self.is_canceled_next_img = True
            return
        # データフレーム処理にレコード追加...  # 全ての値が正しい場合
        self.current_df = self.current_df.fillna('') # NaNを空文字に変換
        self.current_df = self.current_df.astype(str) # 全てのデータを文字列に変換
        is_error = self.add_record() # レコード追加処理関数 <----------- 重要
        if is_error:
            self.is_img_listwidget_select_canceled = True
            QTimer.singleShot(110, lambda: self.listWidget_filepath.currentItemChanged.connect(self.on_list_widget_selected)) # シグナルを復元
            self.is_canceled_next_img = True
            return
        if next_file_index in self.current_df.index: # dfに次のレコードが存在する場合
            value_list = self.current_df.loc[next_file_index].to_list()
            self.set_new_text_to_line_edits(value_list) # dfに次のレコードが存在する場合は 入力欄にテキストをセット
            # 型が違う場合は文字色を赤くする処理...
            self.change_color_black_or_red(is_ignore_empty=True)
        else:
            self.deactivate_all_event_filter()
            self.set_blank_to_line_edits() # dfに次のレコードが存在しない場合は ---------> 入力欄をクリア
            self.change_color_of_all_line_edits('black') # 全てのLineEditの文字色を黒にする
            self.deactivate_all_event_filter()
        if not self.is_rept_mode: # リピートモードでない場合
            self.deactivate_all_event_filter()
            self.lineEdit_0_.setFocus()
            self.first_input_line_widget.setFocus() # 最初のLineEditにフォーカスを移動
            ime_mode = self.obj_name_to_ime_dict[self.first_input_line_widget.objectName()]
            self.activate_all_event_filter()
        else: # リピートモードの場合 <--- 最初の REPT_line_editにフォーカスを移動
            ime_mode = self.obj_name_to_ime_dict[self.first_rept_line_edit_obj.objectName()]
            last_line_edit_obj = self.first_rept_line_edit_obj
            def fx(last_line_edit_obj):
                self.deactivate_all_event_filter()
                self.set_focus_to_target_edit_for_timer(last_line_edit_obj)
                self.activate_all_event_filter()
            QTimer.singleShot(55, lambda: fx(last_line_edit_obj))
        self.set_ime_from_ime_mode_text(ime_mode) # IMEの設定 <----------- 重要
        if not self.is_rept_mode: # リピートモードでない場合
            # 画像の変更処理...
            self.change_image(next_file_index) # 画像の変更処理 <----------- 重要
        else: # リピートモードの場合
            # if self.input_mode == 'new1':
            self.create_new_list_item_on_rept()
            self.current_file_index += 1
        if self.radioButton_automove_on.isChecked() and self.is_last_enter_pressed == False:
            def _set_rect_last_edit():
                self.pixmap_item.set_rect(is_first=True)
            QTimer.singleShot(30, lambda: _set_rect_last_edit()) # 移動モードの場合最初の矩形に移動
        if is_enterkey_pressed:
            QTimer.singleShot(0, lambda: self.select_next_item_of_list_widget(next_file_index)) # リストウィジェットの選択を変更
        QTimer.singleShot(110, lambda: self.listWidget_filepath.currentItemChanged.connect(self.on_list_widget_selected)) # シグナルを復元
        time.sleep(0.1)

    def set_focus_to_target_edit_for_timer(self, last_line_edit_obj):
        self.deactivate_all_event_filter()
        self.lineEdit_0_.setFocus()
        last_line_edit_obj.setFocus() # 最後のLineEditにフォーカスを移動
        if self.radioButton_automove_on.isChecked():
            self.pixmap_item.set_rect(current_focus_in_obj=last_line_edit_obj)
        ime_mode = self.obj_name_to_ime_dict[last_line_edit_obj.objectName()]
        self.set_ime_from_ime_mode_text(ime_mode)
        self.activate_all_event_filter()

    def on_line_edit_canceled(self):
        self.deactivate_all_event_filter()
        self.last_input_line_widget.setFocus()
        self.activate_all_event_filter()
        if self.radioButton_automove_on.isChecked():
            self.pixmap_item.set_rect(current_focus_in_obj=self.last_input_line_widget)
        ime_mode = self.obj_name_to_ime_dict[self.last_input_line_widget.objectName()]
        self.set_ime_from_ime_mode_text(ime_mode)

    def set_focus_ime_and_rect(self, target_obj):
        def _set_focus():
            self.deactivate_all_event_filter()
            target_obj.setFocus()
            self.activate_all_event_filter()
            if self.radioButton_automove_on.isChecked():
                self.pixmap_item.set_rect(current_focus_in_obj=target_obj)
            ime_mode = self.obj_name_to_ime_dict[target_obj.objectName()]
            self.set_ime_from_ime_mode_text(ime_mode)
        QTimer.singleShot(66, _set_focus)

    def on_line_edit_canceled_for_listwidget(self):
        self.deactivate_all_event_filter()
        if self.focused_obj_for_list_clicked is None:
            return
        self.focused_obj_for_list_clicked.setFocus()
        self.activate_all_event_filter()
        if self.radioButton_automove_on.isChecked():
            self.pixmap_item.set_rect(current_focus_in_obj=self.focused_obj_for_list_clicked)
        ime_mode = self.obj_name_to_ime_dict[self.focused_obj_for_list_clicked.objectName()]
        self.set_ime_from_ime_mode_text(ime_mode)
        self.is_last_enter_canceled = False

    # pdf_record リストウィジェットのアイテムが選択された時の処理
    def on_list_widget_selected_for_pdf_record(self, next_item, pre_item):
        self.focused_obj_for_list_clicked = self.get_focused_line_edit_obj()
        if next_item is None or pre_item is None:
            print('MY_ERROR: lidtwidget_pdf_record: next_item or pre_item IS None')
            print('current_ind', self.current_index_for_pdf_df)
            return
            # raise
        try:
            self.list_widget_dd.close()
            self.list_widget_dd = None
        except:
            pass
        next_index = self.listWidget_pdf_record.row(next_item) # 次のインデックス
        pre_index = self.listWidget_pdf_record.row(pre_item) # 選択前のインデックス
        pre_text = pre_item.text()
        self.listWidget_pdf_record.setUpdatesEnabled(False)
        flag_dict = self.helper_of_before_change_for_pdf( # WIP
            next_index, is_list_clicked=True, pre_index=pre_index, pre_item=pre_item, pre_text=pre_text
        )
        if flag_dict is None:
            flag_dict = {}
        is_end = True if flag_dict.get('is_canceled', False) or flag_dict.get('is_not_valid', False) or flag_dict.get('is_output_error', False) else False
        if not is_end: # 次のレコード
            self.current_index_for_pdf_df = next_index # レコード書き込みが完了した場合は次のレコードのインデックスをセット
            if self.is_single_pdf_mode: # single PDF の場合は画像も変更
                self.change_pdf_image(self.current_index_for_pdf_df)
                def _select_pre_item(next_index):
                    self.listWidget_pdf.blockSignals(True)
                    self.listWidget_pdf.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
                    self.listWidget_pdf.setCurrentRow(next_index) # 次のアイテムを選択
                    self.listWidget_pdf.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
                    self.listWidget_pdf.blockSignals(False)
                QTimer.singleShot(0, lambda: _select_pre_item(next_index))
        else:
            def _select_pre_item(pre_index):
                self.listWidget_pdf_record.blockSignals(True)
                self.listWidget_pdf_record.setCurrentRow(pre_index) # 失敗した場合は前のアイテムを選択
                self.listWidget_pdf_record.blockSignals(False)
            QTimer.singleShot(0, lambda: _select_pre_item(pre_index))
        QTimer.singleShot(100, lambda: self.listWidget_pdf_record.setUpdatesEnabled(True))

    def create_new_list_item_on_rept(self): # rept専用
        # add_record()と関連
        list_widget_texts = self.create_rept_list_texts()
        self.listWidget_filepath.clear()
        self.set_items_to_list_widget(list_widget_texts)

    def add_record(self): # img専用
        record_dict = {data['index']: data['line_edit_obj'].text() for data in self.data_list} # 全ての入力項目を取得
        timestamp = self.get_timestamp()
        if not self.is_rept_mode:
            record_dict.update({10000: self.img_pobj_dict[self.current_index_for_img_df].name, 20000: self.user_name, 30000: timestamp})
        else:
            record_dict.update({10000: self.img_pobj_dict[0].name, 20000: self.user_name, 30000: timestamp})
        record_df = pd.DataFrame(record_dict, index=[self.current_index_for_img_df]) # 辞書から1レコードDataFrameを作成(インデックスはファイルインデックス)
        record_df = record_df.reset_index(drop=True)
        if not self.is_rept_mode: # reptでない場合
            if self.current_index_for_img_df in self.current_df.index: # レコードが存在する場合
                self.current_df.loc[self.current_index_for_img_df] = record_df.loc[0] # レコードを更新
            else: # レコードが存在しない場合
                self.current_df = pd.concat([self.current_df, record_df], axis=0, ignore_index=True) # レコードを追加
        elif self.is_rept_mode: # reptの場合
            # レコードが存在している場合
            if self.listWidget_filepath.currentRow() in self.current_df.index:
                self.current_df.loc[self.listWidget_filepath.currentRow()] = record_df.loc[0] # レコードを更新
                self.is_new_record_added = False
            else: # レコードが存在しない場合
                self.current_df = pd.concat([self.current_df, record_df], axis=0, ignore_index=True) # レコードを追加
                self.is_new_record_added = True
        is_error = self.output_csv() # CSV保存処理 <--- ここで保存
        return is_error # csv保存処理が失敗した場合はTrueを返す

    def output_log(self): # img専用
        if self.is_restart_processing or self.input_mode == 'new1': # リスタート時は何もしない
            return
        self.previous_df = self.previous_df.astype(str)
        self.previous_df = self.previous_df.fillna('')
        self.previous_df = self.previous_df.sort_index(axis=0)
        # self.previous_df = self.previous_df.sort_index(axis=1)
        values = []
        if self.is_rept_mode:
            self.current_file_index = self.previous_list_widget_index_for_rept
        try:
            values = self.current_df.iloc[self.current_file_index].to_list()
        except:
            return
        # values = [株式会社..., 部長, 田中太郎...]
        pre_values = []
        timestamp = self.get_timestamp()
        # current_dfの行数がprevious_dfの行数より多くなったらprevious_dfに空欄行を追加...(rept_line_editのみ空欄の行にする)
        if self.is_rept_mode:
            rept_col_names = [data['name'] for data in self.data_list if data['is_rept'] and data['is_show']]
            rept_indexes = [data['index'] for data in self.data_list if data['is_rept'] and data['is_show']]
            if self.current_df.shape[0] > self.previous_df.shape[0]:
                new_row = {col: '' for col in self.previous_df.columns}
                new_row = self.previous_df.iloc[0].to_dict()
                for rept_index in rept_indexes:
                    new_row[rept_index] = ''
                for _ in range(self.current_df.shape[0] - self.previous_df.shape[0]):
                    self.previous_df.loc[len(self.previous_df)] = new_row
        for i in range(self.line_edit_count):
            pre_value = self.previous_df.iloc[self.current_file_index, i]
            pre_values.append(pre_value)
        new1_user_name = self.previous_df.loc[self.current_file_index, 20000]
        is_write_log_needed = False
        columns=[
            'timestamp', 'item', 'new1_user_name', 'ver1_user_name', 'new1_value', 'ver1_value', 'img_filename'
        ]
        empty_record = pd.DataFrame(columns=columns)
        one_record_log_df = empty_record.copy()
        buf_items, buf_pres, buf_nexts, new_rept_item_names = [], [], [], []
        another_logs = []
        for i, (pre, next) in enumerate(zip(pre_values, values)):
            if pre != next:
                # ログの内容を作成...
                record_df = empty_record.copy()
                file_name = self.img_pobj_dict[self.current_file_index].name if not self.is_rept_mode else self.img_pobj_dict[0].name
                # file_name = self.img_pobj_dict[self.current_file_index].name if not self.is_rept_mode else self.output_dobj.name
                current_item = self.data_list[i]['name']
                types = self.label_name_to_type_dict[current_item].split('_')
                if 'nover' in types or 'noedit' in types:
                    continue
                another_logs.extend([file_name, current_item, f'New:{pre}', f'Ver:{next}'])
                if not self.is_rept_mode or not current_item in rept_col_names: # not_rept or in_rept_display_name
                    if pre != next: # 前回の入力内容と異なる場合はログに記録
                        record_df.loc[0] = [
                                timestamp, current_item, new1_user_name,
                                self.user_name, pre, next, file_name
                        ]
                else:
                    buf_items.append(current_item)
                    buf_pres.append(pre)
                    buf_nexts.append(next)
                    if len(buf_items) == len(rept_col_names):
                        item_text = ' / '.join(buf_items)
                        pre_text = ' / '.join(buf_pres)
                        next_text = ' / '.join(buf_nexts)
                        if pre_text != next_text:
                            record_df.loc[0] = [
                                    timestamp, item_text, new1_user_name,
                                    self.user_name, pre_text, next_text, file_name
                            ]
                            new_rept_item_names.append(item_text)
                one_record_log_df = pd.concat([one_record_log_df, record_df], axis=0)
        is_write_log_needed = True
        self.log_df = pd.concat([self.log_df, one_record_log_df], axis=0)
        keep = 'last' if self.is_rept_mode else 'first'
        subset = ['item', 'new1_user_name', 'ver1_user_name', 'new1_value', 'ver1_value' ,'img_filename']
        self.log_df = self.log_df.drop_duplicates(subset=subset, keep=keep) # 重複削除
        self.log_df = self.log_df.fillna('')
        if self.is_rept_mode: # rept
            filtered_df = self.log_df[self.log_df['item'].isin(new_rept_item_names)]
            other_df = self.log_df[~self.log_df['item'].isin(new_rept_item_names)]
            subset = ['item', 'new1_user_name', 'ver1_user_name', 'img_filename']
            other_df = other_df.drop_duplicates(subset=subset, keep='last')
            self.log_df = pd.concat([other_df, filtered_df], axis=0)
        self.log_df = self.log_df.reset_index(drop=True)
        noew_columns=[
            'timestamp', 'item', 'new1_value', 'ver1_value', 'new1_user_name', 'ver1_user_name', 'img_filename'
        ]
        self.log_df = self.log_df[noew_columns]
        # ログファイルを出力...
        try:
            DataIO.write_csv_with_header(
                self, self.log_df, self.output_log_fobj, encoding=self.encode_type, has_header=False
            )
        except PermissionError:
            QMessageBox.warning(self, 'エラー', 'ログファイルの書き込みに失敗しました', QMessageBox.Ok)
        if is_write_log_needed:
            log_file_path = str(self.output_log_fobj)
            try:
                if not os.path.exists(log_file_path): # ログファイルが存在しない場合作成する
                    with open(log_file_path, 'w', encoding=self.encode_type) as f:
                        f.write('')
                with open(log_file_path, 'a', encoding=self.encode_type) as f:
                    f.write('')
            except PermissionError:
                QMessageBox.warning(self, 'エラー', 'ログファイルの書き込みに失敗しました', QMessageBox.Ok)

    def create_another_log(self, log_df): # 念のため旧バージョンのログを作成
        another_log = []
        for row in range(log_df.shape[0]):
            item = log_df.loc[row, 'item']
            new = log_df.loc[row, 'new1_value']
            ver = log_df.loc[row, 'ver1_value']
            filename = log_df.loc[row, 'img_filename']
            another_log.extend([filename, item, f'New:{new}', f'Ver:{ver}'])
        return another_log

    def set_screen_mode_toggle(self): # 表示モード変更 3種トグル
        if self.isMaximized():
            self.showFullScreen()
        elif self.isFullScreen():
            self.showNormal()
        else:
            self.showMaximized()

    def set_screen_mode_toggle_full_or_max(self): # 表示モード変更 2種トグル
        if self.isMaximized():
            self.showFullScreen()
        else:
            self.setUpdatesEnabled(False)
            self.showNormal()
            QTimer.singleShot(0, lambda: self.showMaximized())
            self.setUpdatesEnabled(True)


    def set_connect(self, obj, func, mode=None):
        if mode == 'clicked':
            try:
                obj.clicked.disconnect(func)
                print('____disconnect >>', obj.objectName())
            except TypeError:
                pass
        elif mode == 'currentRowChanged':
            try:
                obj.currentRowChanged.disconnect(func)
                print('____disconnect >>', obj.objectName())
            except TypeError:
                pass
        elif mode == 'currentIndexChanged':
            try:
                obj.currentIndexChanged.disconnect(func)
                print('____disconnect >>', obj.objectName())
            except TypeError:
                pass
        elif mode == 'currentItemChanged':
            try:
                obj.currentItemChanged.disconnect(func)
                print('____disconnect >>', obj.objectName())
            except TypeError:
                pass
        if mode == 'clicked':
            obj.clicked.connect(func)
        elif mode == 'currentRowChanged':
            obj.currentRowChanged.connect(func)
        elif mode == 'currentIndexChanged':
            obj.currentIndexChanged.connect(func)
        elif mode == 'currentItemChanged':
            obj.currentItemChanged.connect(func)

    def get_focused_line_edit_obj(self):
        if not hasattr(self, 'data_list') or not self.data_list:
            return None
        focused_line_edit_objs = []
        for data in self.data_list:
            line_edit_obj = data['line_edit_obj']
            if line_edit_obj is None:
                continue
            if sip.isdeleted(line_edit_obj):
                continue
            if line_edit_obj.hasFocus():
                focused_line_edit_objs.append(line_edit_obj)
        if focused_line_edit_objs:
            # print('フォーカスオブジェ >>', focused_line_edit_objs[0].objectName())
            return focused_line_edit_objs[0]
        else:
            return None

    def show_dd_list_widget(self, focused_line_edit_obj: QLineEdit): # ドロップダウンリストを表示
        if focused_line_edit_obj is None:
            return
        line_type = self.obj_name_to_type_dict[focused_line_edit_obj.objectName()]
        if not 'list' in line_type:
            return
        current_text = focused_line_edit_obj.text()
        if self.radioButton_layout_vertival.isChecked():
            parent_scroll_area = self.scrollAreaWidgetContents
        else:
            parent_scroll_area = self.scrollAreaWidgetContents_2
        if self.list_widget_dd is not None:
            self.list_widget_dd.clear()
            self.list_widget_dd.close()
            self.list_widget_dd = None
        self.list_widget_dd = QtWidgets.QListWidget(parent_scroll_area) # ドロップダウンリスト作成
        self.event_filter_for_dd = CustomEventFilterForDD(self, self.list_widget_dd, focused_line_edit_obj)
        self.list_widget_dd.installEventFilter(self.event_filter_for_dd)
        font = self.list_widget_dd.font()
        font.setPointSize(11)
        font.setFamily("BIZ UDゴシック")
        self.list_widget_dd.setFont(font) # フォント
        self.focused_line_edit_obj_for_dd = None
        self.list_widget_dd.itemClicked.connect(self.activated_dd_list_widget) # connect
        self.list_widget_dd.itemActivated.connect(self.activated_dd_list_widget) # connect
        converted_pos = focused_line_edit_obj.mapTo(parent_scroll_area, focused_line_edit_obj.rect().topLeft()) # スクロールエリアの座標に変換
        x = converted_pos.x()
        y = converted_pos.y()
        line_width = focused_line_edit_obj.width()
        line_height = focused_line_edit_obj.height()
        self.list_widget_dd.clear()
        dd_items = self.obj_name_to_list_item_dict[focused_line_edit_obj.objectName()].copy()
        init_index = dd_items.index(current_text) if current_text in dd_items else 0
        dd_items.append('空欄')
        dd_items.append('キャンセル')
        self.list_widget_dd.addItems(dd_items)
        item = self.list_widget_dd.item(0)
        item_height = item.sizeHint().height()
        self.focused_line_edit_obj_for_dd = focused_line_edit_obj
        self.list_widget_dd.show() # ドロップダウンリストを表示
        self.deactivate_all_event_filter()
        self.list_widget_dd.setFocus()
        self.list_widget_dd.setCurrentRow(init_index) # ドロップダウンリストのアイテムを選択
        self.activate_all_event_filter()
        item_height = self.list_widget_dd.sizeHintForRow(0)
        row_count = self.list_widget_dd.count()
        self.list_widget_dd.setGeometry(x, y + line_height, line_width, int(item_height * (row_count + 1)))

    def activated_dd_list_widget(self, item): # ドロップダウンリストのアイテムが選択されたときの処理
        self.deactivate_all_event_filter()
        row = self.list_widget_dd.row(item)
        if row == self.list_widget_dd.count() - 2:
            self.focused_line_edit_obj_for_dd.setText('')
        elif row == self.list_widget_dd.count() - 1:
            pass
        else:
            self.focused_line_edit_obj_for_dd.setText(item.text())
        self.list_widget_dd.close()
        self.focused_line_edit_obj_for_dd.setFocus()
        self.list_widget_dd = None
        self.activate_all_event_filter()

    def change_delta_scale(self, index):
        self.delta_scale = self.index_to_delta_scale_dict[index]
        self.config_dict['delta_scale'] = self.delta_scale

    def set_focus_to_first_line_edit(self):
        def _set_focus_to_first_line_edit():
            self.deactivate_all_event_filter()
            self.first_input_line_widget.blockSignals(True)
            self.first_input_line_widget.setFocus() # 最初のLineEditにフォーカスを移動
            self.first_input_line_widget.blockSignals(False)
            self.activate_all_event_filter()
        QTimer.singleShot(10, _set_focus_to_first_line_edit)

    def pressed_h_button(self):
        if self.config_dict['layout_type'] == 'h':
            return
        self.change_layout_horizontal()

    def pressed_v_button(self):
        if self.config_dict['layout_type'] == 'v':
            return
        self.change_layout_vertical()

    def change_layout_vertical(self):
        self.config_dict['layout_type'] = 'v'
        self.config_dict['splitter_3a_width'] = int(self.splitter.size().width())
        self.config_dict['splitter_3b_width'] = int(self.splitter_3.size().width())
        self.config_dict['splitter_4a_height'] = int(self.frame_input_right.size().height())
        self.config_dict['splitter_4b_height'] = int(self.frame_for_right_list.size().height())
        self.splitter_3.hide()
        self.frame_splitter_below.show()
        for data in self.data_list:
            current_line_edit_obj = data['line_edit_obj']
            current_label_obj = data['label_obj']
            next_hlayout_obj = data['layout_a_obj']
            current_hlayout_obj = data['layout_b_obj']
            current_hlayout_obj.removeWidget(current_line_edit_obj)
            current_hlayout_obj.removeWidget(current_label_obj)
            next_hlayout_obj.addWidget(current_label_obj)
            next_hlayout_obj.addWidget(current_line_edit_obj)
        for frames_dict in self.input_frames_data_list:
            frame_obj = frames_dict['frame_obj']
            stretchs = frames_dict['stretch']
            layout = frame_obj.layout()
            for i, stretch in enumerate(stretchs):
                layout.setStretch(i, stretch)
        splitter_below_height = self.config_dict['splitter_1b_height']
        splitter_above_height = self.config_dict['splitter_1a_height']
        self.splitter.setSizes([splitter_above_height, splitter_below_height]) # メイン左スプリッター
        self.horizontalLayout_for_right_list.removeWidget(self.listWidget_filepath)
        self.horizontalLayout_for_left_list.addWidget(self.listWidget_filepath)
        self.horizontalLayout_for_right_list.removeWidget(self.frame_splitter_list)
        self.horizontalLayout_for_left_list.addWidget(self.frame_splitter_list)
        self.set_focus_to_first_line_edit()
        self.show_info_to_two_labels(self.data_list[0]['line_edit_obj'])


    def show_info_to_two_labels(self, focus_in_obj):
        try:
            if focus_in_obj is not None:
                info = self.obj_name_to_info_dict.get(focus_in_obj.objectName(), None)
                if not info:
                    return
                self.label_infomation.setText(info.replace('\n', ', ')) # >> を空欄に変更
                self.label_infomation_right.setText(info)
        except Exception as e:
            print('MyError_show_info_to_two_labels:', e)


    def change_layout_horizontal(self):
        self.config_dict['layout_type'] = 'h'
        self.config_dict['splitter_1a_height'] = int(self.graphicsView_main.size().height())
        self.config_dict['splitter_1b_height'] = int(self.frame_splitter_below.size().height())
        self.config_dict['splitter_2a_width'] = int(self.scrollArea_input.size().width())
        self.config_dict['splitter_2b_width'] = int(self.frame_splitter_after.size().width())
        self.splitter_3.show()
        self.frame_splitter_below.hide()
        for data in self.data_list:
            current_line_edit_obj = data['line_edit_obj']
            current_label_obj = data['label_obj']
            current_hlayout_obj = data['layout_a_obj']
            next_hlayout_obj = data['layout_b_obj']
            current_hlayout_obj.removeWidget(current_line_edit_obj)
            current_hlayout_obj.removeWidget(current_label_obj)
            next_hlayout_obj.insertWidget(0, current_label_obj)
            next_hlayout_obj.insertWidget(1, current_line_edit_obj)
            next_hlayout_obj.setStretch(0, 0)  # ラベルはストレッチしない
            next_hlayout_obj.setStretch(1, 1)  # QLineEdit が最大限に広がるようにストレッチ
            current_label_obj.adjustSize()
            current_line_edit_obj.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            current_line_edit_obj.setMinimumWidth(0)
            current_line_edit_obj.setMaximumWidth(16777215)
        splitter_below_hight = 200
        self.splitter_3.setSizes([self.splitter_3.height() - splitter_below_hight, splitter_below_hight])
        self.horizontalLayout_for_left_list.removeWidget(self.listWidget_filepath)
        self.horizontalLayout_for_right_list.addWidget(self.listWidget_filepath)
        self.horizontalLayout_for_left_list.removeWidget(self.frame_splitter_list)
        self.horizontalLayout_for_right_list.addWidget(self.frame_splitter_list)
        splitter_left_width = self.config_dict['splitter_3b_width']
        splitter_right_width = self.config_dict['splitter_3a_width']
        self.splitter_4.setSizes([splitter_right_width, splitter_left_width])
        self.set_focus_to_first_line_edit()
        self.show_info_to_two_labels(self.data_list[0]['line_edit_obj'])

    def pressed_radioButton_automove_on(self):
        self.radioButton_rect_move.setChecked(True)
        self.pixmap_item.mode = 'move'

    def pressed_get_rect(self):
        if self.pixmap_item.mode != 'select':
            QMessageBox.warning(self, '警告', '選択モードでないと矩形を取得できません。', QMessageBox.Ok)
            return
        elif self.radioButton_automove_on.isChecked():
            QMessageBox.warning(self, '警告', '自動移動モード中は矩形を取得できません。', QMessageBox.Ok)
            return
        forcus_in_line_widget_obj_buf = self.focus_in_line_widget_obj
        col_name = self.obj_name_to_name_dict[forcus_in_line_widget_obj_buf.objectName()]
        if self.pixmap_item.current_rect_item is None \
                or self.pixmap_item.current_rect_item.boundingRect().width() <= 5 \
                or self.pixmap_item.current_rect_item.boundingRect().height() <= 5:
            QMessageBox.information(self, '情報', f'{col_name}の矩形設定を解除しました。', QMessageBox.Ok)
            current_focus_in_obj = self.focus_in_line_widget_obj
            current_index = self.obj_name_to_index_dict[current_focus_in_obj.objectName()]
            self.rect_config[current_index]['w'] = None
            self.rect_config[current_index]['h'] = None
            self.rect_config[current_index]['x'] = None
            self.rect_config[current_index]['y'] = None
            self.rect_config[current_index]['angle'] = None
            self.rect_config[current_index]['scale'] = None
            self.write_rect_config(self.rect_config)
            if current_index == len(self.data_list) - 1:
                next_obj = self.index_to_obj_dict[0]
            else:
                next_obj = self.index_to_obj_dict[current_index + 1]
            self.deactivate_all_event_filter()
            next_obj.setFocus()
            self.focus_in_line_widget_obj = next_obj
            self.activate_all_event_filter()
            return
        self.pixmap_item.get_rect()
        QMessageBox.information(self, '情報', f'{col_name}の矩形を設定しました。', QMessageBox.Ok)

    def copy_rect_from_previous(self):
        """前のデータ（上のデータ）の矩形設定を現在のフィールドにコピー

        Ctrl+Shift+R のショートカットで呼び出されます。
        現在フォーカスされているフィールドのインデックスから、
        1つ前（上）のデータの矩形設定をコピーします。
        """
        # 選択モードでないと矩形をコピーできない
        if self.pixmap_item.mode != 'select':
            QMessageBox.warning(self, '警告', '選択モードでないと矩形をコピーできません。', QMessageBox.Ok)
            return
        elif self.radioButton_automove_on.isChecked():
            QMessageBox.warning(self, '警告', '自動移動モード中は矩形をコピーできません。', QMessageBox.Ok)
            return

        # 現在フォーカスされているフィールドのインデックスを取得
        current_focus_in_obj = self.focus_in_line_widget_obj
        current_index = self.obj_name_to_index_dict[current_focus_in_obj.objectName()]
        col_name = self.obj_name_to_name_dict[current_focus_in_obj.objectName()]

        # 最初のフィールド（インデックス0）の場合はコピー元がない
        if current_index == 0:
            QMessageBox.warning(self, '警告', '最初のフィールドには前のデータがありません。', QMessageBox.Ok)
            return

        # 1つ前のインデックスの矩形設定を取得
        previous_index = current_index - 1
        previous_rect = self.rect_config.get(previous_index)

        # 前のデータに矩形設定がない場合
        if not previous_rect or previous_rect.get('w') is None:
            QMessageBox.warning(self, '警告', '前のフィールドに矩形設定がありません。', QMessageBox.Ok)
            return

        # 矩形設定をコピー
        self.rect_config[current_index]['w'] = previous_rect['w']
        self.rect_config[current_index]['h'] = previous_rect['h']
        self.rect_config[current_index]['x'] = previous_rect['x']
        self.rect_config[current_index]['y'] = previous_rect['y']
        self.rect_config[current_index]['angle'] = previous_rect.get('angle')
        self.rect_config[current_index]['scale'] = previous_rect.get('scale')

        # JSONファイルに保存
        self.write_rect_config(self.rect_config)

        QMessageBox.information(self, '情報', f'{col_name}に前のデータの矩形設定をコピーしました。', QMessageBox.Ok)

        # 次のフィールドにフォーカスを移動
        if current_index == len(self.data_list) - 1:
            next_obj = self.index_to_obj_dict[0]
        else:
            next_obj = self.index_to_obj_dict[current_index + 1]
        self.deactivate_all_event_filter()
        next_obj.setFocus()
        self.focus_in_line_widget_obj = next_obj
        self.activate_all_event_filter()

    def fill_rect_json_null_with_previous(self):
        """nullを上のデータで埋める（Excelのフィル機能）

        rect.json内のnull値（矩形未設定）を、直前の有効な矩形設定で埋めます。
        pressed_get_rectと同様の外部から持ってきた関数として動作します。

        - 選択モード、非自動移動モードでのみ実行可能
        - 確認ダイアログで実行を確認
        - rect.jsonに直接保存（returnなし）
        - 引数はselfのみ
        """
        # 選択モードでないと矩形をコピーできない
        if self.pixmap_item.mode != 'select':
            QMessageBox.warning(self, '警告', '選択モードでないと矩形をコピーできません。', QMessageBox.Ok)
            return
        elif self.radioButton_automove_on.isChecked():
            QMessageBox.warning(self, '警告', '自動移動モード中は矩形をコピーできません。', QMessageBox.Ok)
            return
        # 実行確認ダイアログ
        reply = QMessageBox.question(
            self,
            '確認',
            'rect.json内のnull値を前のデータで埋めますか？\n\nこの操作は元に戻せません。',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # rect.jsonから最新データを読み込み
        rect_data = self.read_rect_config()

        # 現在のrect_configを処理
        filled_data = {}
        previous_rect = None
        fill_count = 0

        # インデックスの数値順にソート
        sorted_keys = sorted(rect_data.keys(), key=lambda x: int(x))

        for key in sorted_keys:
            rect = rect_data[key]

            # すべての値がnullかチェック
            all_null = all(rect[field] is None for field in ['x', 'y', 'w', 'h', 'scale', 'angle'])

            if all_null and previous_rect is not None:
                # すべてnullの場合、前のデータをコピー
                filled_data[key] = previous_rect.copy()
                fill_count += 1
                print(f"  [{key}] nullを前のデータで埋めました: x={filled_data[key]['x']}, y={filled_data[key]['y']}")
            else:
                # nullでない場合、そのまま使用
                filled_data[key] = rect.copy()
                # 次の反復のために保存（nullでない場合のみ）
                if not all_null:
                    previous_rect = rect.copy()

        # rect_configを更新
        self.rect_config = filled_data

        # JSONファイルに保存
        self.write_rect_config(self.rect_config)

        # 完了ダイアログ
        QMessageBox.information(
            self,
            '完了',
            f'{fill_count}個のnull値を前のデータで埋めました。',
            QMessageBox.Ok
        )

    def reset_rect_json_to_null(self):
        """すべての矩形データをnullにリセット

        rect.json内のすべての矩形設定['x', 'y', 'w', 'h', 'scale', 'angle']をnullにリセットします。
        fill_rect_json_null_with_previousの逆機能として動作します。

        - 選択モード、非自動移動モードでのみ実行可能
        - 確認ダイアログで実行を確認
        - rect.jsonに直接保存（returnなし）
        - 引数はselfのみ
        """
        # 選択モードでないと実行できない
        if self.pixmap_item.mode != 'select':
            QMessageBox.warning(self, '警告', '選択モードでないと矩形をリセットできません。', QMessageBox.Ok)
            return
        elif self.radioButton_automove_on.isChecked():
            QMessageBox.warning(self, '警告', '自動移動モード中は矩形をリセットできません。', QMessageBox.Ok)
            return

        # 実行確認ダイアログ
        reply = QMessageBox.question(
            self,
            '確認',
            'rect.json内のすべての矩形データをnullにリセットしますか?\n\nこの操作は元に戻せません。',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # rect.jsonから最新データを読み込み
        rect_data = self.read_rect_config()

        # すべての矩形データをnullにリセット
        reset_data = {}
        reset_count = 0

        # インデックスの数値順にソート
        sorted_keys = sorted(rect_data.keys(), key=lambda x: int(x))

        for key in sorted_keys:
            rect = rect_data[key]

            # すべての値がnullかチェック
            all_null = all(rect[field] is None for field in ['x', 'y', 'w', 'h', 'scale', 'angle'])

            if not all_null:
                # null以外の値がある場合、nullにリセット
                reset_data[key] = {
                    'x': None,
                    'y': None,
                    'w': None,
                    'h': None,
                    'scale': None,
                    'angle': None
                }
                reset_count += 1
                print(f"  [{key}] 矩形データをnullにリセットしました")
            else:
                # 既にnullの場合、そのまま使用
                reset_data[key] = rect.copy()

        # rect_configを更新
        self.rect_config = reset_data

        # JSONファイルに保存
        self.write_rect_config(self.rect_config)

        # 完了ダイアログ
        QMessageBox.information(
            self,
            '完了',
            f'{reset_count}個の矩形データをnullにリセットしました。',
            QMessageBox.Ok
        )

    def scroll_to_position(self, view_obj, orientation: str):
        # 水平方向のスクロールバー
        scale = 8
        left_scale = 1 / scale
        right_scale = 1 - left_scale
        up_scale = left_scale
        down_scale = 1 - up_scale
        if orientation == 'left' or orientation == 'right':
            h_scrollbar = view_obj.horizontalScrollBar()
            if h_scrollbar:
                # 全体の1/4のスクロール量を計算
                h_range = h_scrollbar.maximum() - h_scrollbar.minimum()
                current_h_value = h_scrollbar.value() - h_scrollbar.minimum()
                if current_h_value >= right_scale * h_range and orientation == 'right':
                    h_scrollbar.setValue(h_scrollbar.maximum())
                elif current_h_value  <= left_scale * h_range and orientation == 'left':
                    h_scrollbar.setValue(h_scrollbar.minimum())
                else:
                    h_scroll_amount = h_range // scale  # 1/4のスクロール
                    h_scroll_amount = -h_scroll_amount if orientation == 'left' else h_scroll_amount
                    h_scrollbar.setValue(h_scrollbar.value() + h_scroll_amount)
        elif orientation == 'up' or orientation == 'down':
            # 垂直方向のスクロールバー
            v_scrollbar = view_obj.verticalScrollBar()
            if v_scrollbar:
                # 全体の1/4のスクロール量を計算
                v_range = v_scrollbar.maximum() - v_scrollbar.minimum()
                current_v_value = v_scrollbar.value() - v_scrollbar.minimum()
                if current_v_value >= down_scale * v_range and orientation == 'down':
                    v_scrollbar.setValue(v_scrollbar.maximum())
                elif current_v_value <= up_scale * v_range and orientation == 'up':
                    v_scrollbar.setValue(v_scrollbar.minimum())
                else:
                    v_scroll_amount = v_range // scale  # 1/4のスクロール
                    v_scroll_amount = -v_scroll_amount if orientation == 'up' else v_scroll_amount
                    v_scrollbar.setValue(v_scrollbar.value() + v_scroll_amount)

    def info_label_show(self):
        self.frame_infomation.show()
        self.frame_infomation_right.show()
        self.config_dict['is_info_show'] = True

    def info_label_hide(self):
        self.frame_infomation.hide()
        self.frame_infomation_right.hide()
        self.config_dict['is_info_show'] = False

    def rect_area_show_or_hide(self, is_show: bool):
        if is_show:
            self.frame_rect_select.show()
        else:
            if self.radioButton_rect_select.isChecked:
                self.radioButton_rect_move.setChecked(True)
                self.change_rect_mode('move')
            self.frame_rect_select.hide()

    def change_rect_mode(self, pixmap_item_mode):
        self.pixmap_item.delete_sub_rect()
        if pixmap_item_mode == 'move':
            self.pixmap_item.mode = 'move'
        elif pixmap_item_mode == 'select':
            self.pixmap_item.mode = 'select'
            self.radioButton_automove_off.setChecked(True)

    def set_ime_from_ime_mode_text(self, ime_mode :str):
        if time.time() - self.last_exexuting_time_of_ime_control < 0.05:
            return
        if ime_mode == 'jp':
            self.set_ime_on_jp()
        elif ime_mode == 'en':
            self.set_ime_on_en()
        self.last_exexuting_time_of_ime_control = time.time()

    def set_ime_on_jp(self):
        # 新しいスレッドを作成してIMEを日本語に設定
        self.ime_thread = IMEThread('jp')
        self.ime_thread.finished.connect(self.on_thread_finished)
        self.ime_thread.finished.connect(self.clean_up_thread)  # スレッド終了後に削除
        self.ime_thread.start()

    def set_ime_on_en(self):
        # 新しいスレッドを作成してIMEをオフに設定
        self.ime_thread = IMEThread('en')
        self.ime_thread.finished.connect(self.on_thread_finished)
        self.ime_thread.finished.connect(self.clean_up_thread)  # スレッド終了後に削除
        self.ime_thread.start()

    def on_thread_finished(self, message):
        # print(message)
        pass

    def clean_up_thread(self):
        try:
            if self.ime_thread.isRunning():
                # print('スレッドがまだ動作中です。終了を待ちます...')
                if not self.ime_thread.wait(200):  # 0.2秒以内に終了しない場合
                    # print("スレッドがタイムアウトしました。強制終了します。")
                    self.ime_thread.terminate()  # 強制終了
                    self.ime_thread.wait()  # 完全終了を待機
            else:
                # print('スレッドが正常に終了しました。')
                pass
            self.ime_thread.deleteLater()  # スレッドオブジェクトを削除
        except Exception as e:
            # print(f'clean_up_threadでエラー発生: {e}')
            pass

    def install_event_filter_to_all_line_edit(self):  # 全てのLineEditにイベントフィルターを設定
        for data in self.data_list:  # 全てのLineEditにEnterキー押下時の処理を設定
            custom_event_filter = CustomEventFilterForLineEdit(self, data['line_edit_obj'])  # イベントフィルターのインスタンスを作成
            data['line_edit_obj'].installEventFilter(custom_event_filter)  # イベントフィルターをインストール
            self.event_filter_dict[data['line_edit_name']] = custom_event_filter  # イベントフィルターを辞書に保持

    def remove_event_filter_to_all_line_edit(self):  # 全てのLineEditに設定されたイベントフィルターを削除
        for data in self.data_list:
            data['line_edit_obj'].removeEventFilter(self.event_filter_dict[data['line_edit_name']])
        self.event_filter_dict = {}

    def get_error_info(self, is_valids_names_and_types): # 表示用エラー情報を取得
        error_names_and_types = []
        for obj_name, jp_type in zip(is_valids_names_and_types[1], is_valids_names_and_types[2]):
            if obj_name:
                col_name = self.obj_name_to_name_dict[obj_name]
                error_names_and_types.append(f'{col_name}: {jp_type}')
        error_info = '\n'.join(error_names_and_types)
        return error_info

    def next_line_edit(self, index): # 次のLineEditにフォーカスを移動
        current_time = time.time()
        if self.is_next_img_change or current_time - self.last_mouse_focusin_time < 0.01:  # 0.01秒以内に実行された場合
            return
        if self.data_list[index]['is_last'] == 1:
            return
        self.deactivate_all_event_filter()  # イベントフィルターを無効化
        next_index = index + 1
        count_for_error = 0
        while True:
            count_for_error += 1
            if count_for_error > 100:
                pass
                raise ValueError('次のLineEditが見つかりませんでした')
            # 次のLineEditオブジェクトを探す
            found = False
            for data in self.data_list:
                if data['index'] == next_index:
                    # LineEditが表示されている場合のみフォーカスを移動
                    types = self.main_data_dict[data['line_edit_obj'].objectName()]['data_type']
                    if data['line_edit_obj'].isVisible() and not 'noedit' in types:
                        data['line_edit_obj'].setFocus()  # ここでフォーカスイベントが発生
                        found = True
                        break
                    else:
                        # 非表示なら次のLineEditを探す
                        next_index += 1

            # 見つからなければループを抜ける
            if found:
                break

        self.activate_all_event_filter()  # イベントフィルターを有効化

    def set_previous_data_to_line_edits(self):
        self.current_df = self.previous_df

        # previous_dfが空でないか、インデックス0が存在するかチェック
        if self.previous_df.empty or 0 not in self.previous_df.index:
            return  # データがない場合は何もしない

        init_value_list = self.previous_df.loc[0].to_list()
        self.set_new_text_to_line_edits(init_value_list) # dfの最初のレコードを入力欄にセット
        self.change_color_black_or_red(is_ignore_empty=True) # 型が違う場合は文字色を赤くする処理

    def set_blank_to_line_edits(self, is_force=False):
        self.deactivate_all_event_filter()
        if not self.is_rept_mode or is_force:
            for data in self.data_list:
                line_edit_obj = data['line_edit_obj']
                types = self.main_data_dict[line_edit_obj.objectName()]['data_type']
                line_edit_obj.blockSignals(True)
                if 'username' in types:
                    line_edit_obj.setText(self.user_name)
                else:
                    line_edit_obj.setText('')
                line_edit_obj.blockSignals(False)
        else:
            is_rept_list = [data['is_rept'] for data in self.data_list]
            for data, is_rept in zip(self.data_list, is_rept_list):
                if is_rept: # リピートモードの場合 is_reptがTrue -> 空欄にする
                    line_edit_obj = data['line_edit_obj']
                    types = self.main_data_dict[line_edit_obj.objectName()]['data_type']
                    line_edit_obj.blockSignals(True)
                    if 'username' in types:
                        line_edit_obj.setText(self.user_name)
                    else:
                        line_edit_obj.setText('')
                    line_edit_obj.blockSignals(False)
        self.activate_all_event_filter()

    def restart_app(self, is_button_pressed=False, is_not_save_config=False): # アプリケーションの再起動
        if is_button_pressed:
            if self.is_initialaized:
                return
            if QMessageBox.question(self, '確認', '現在の作業を終了して新しく画像フォルダを選択しますか？',
                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
                return
            else: # ボタンでリスタートの場合
                self.close_event_processing()
                self.current_file_index = 0 # 現在のファイルインデックスをリセット
                self.previous_list_widget_index = 0 # 前回のリストウィジェットのインデックスをリセット
        self.is_initialaized = True
        # 全てのLineEditのシグナルをブロックする
        for data in self.data_list:
            data['line_edit_obj'].blockSignals(True)
        self.listWidget_filepath.blockSignals(True) # リストウィジェットのシグナルをブロック
        self.set_blank_to_line_edits(is_force=True) # 全てのLineEditを空白にする
        self.listWidget_filepath.clear()
        if not is_not_save_config:
            self.close_event_processing()
        self.initializer() # _________________初期化処理
        if self.is_close_button_pressed:
            return # 再起動時のダイアログでキャンセルボタンが押された場合はシグナルは設定されていない
        # 全てのLineEditのシグナルを復元する...
        for data in self.data_list:
            data['line_edit_obj'].blockSignals(False)
        self.listWidget_filepath.setCurrentRow(0)
        self.listWidget_filepath.blockSignals(False) # リストウィジェットのシグナルを復元

    def create_multi_button_msg(self, parent, title: str, message: str, button_list: list[str], default_index: int, icon_type: str = 'question') -> int:
        msg = QMessageBox(parent)
        msg.setWindowTitle(title)
        msg.setText(message)
        if icon_type == 'question':
            msg.setIcon(QMessageBox.Question)
        elif icon_type == 'warning':
            msg.setIcon(QMessageBox.Warning)
        elif icon_type == 'information':
            msg.setIcon(QMessageBox.Information)
        elif icon_type == 'critical':
            msg.setIcon(QMessageBox.Critical)
        buttons = []
        for i in range(len(button_list)):
            buf_button = QtWidgets.QPushButton(button_list[i], msg)
            msg.addButton(buf_button, QMessageBox.ButtonRole.ActionRole)
            buttons.append(buf_button)
        buttons[default_index].setDefault(True)
        msg.exec_()
        clicked_button = msg.clickedButton()
        for button in buttons:
            if clicked_button == button:
                return buttons.index(button)

    def init_config(self):
        # 設定ファイルの読み込みと初期化処理...
        self.config_dict = self.config_manager.initialize()

    def set_items_to_list_widget(self, items):
        self.listWidget_filepath.blockSignals(True)
        self.listWidget_filepath.addItems(items) # リストウィジェットにアイテムを追加
        self.listWidget_filepath.blockSignals(False)

    def set_item_to_list_widget(self, item):
        self.listWidget_filepath.blockSignals(True)
        self.listWidget_filepath.addItem(item)
        self.listWidget_filepath.blockSignals(False)

    def change_text_of_list_widget(self, index, text):
        self.listWidget_filepath.blockSignals(True)
        self.listWidget_filepath.item(index).setText(text)
        self.listWidget_filepath.blockSignals(False)

    def init_graphics_view(self):
        if not self.is_rept_mode: # リピートモードでない場合ファイル名を表示
            filename_list = [f'{i:05}: ' + p.name for i, p in enumerate(self.img_pobj_dict.values())]
            self.listWidget_filepath.clear()
            self.set_items_to_list_widget(filename_list) # リストウィジェットにファイル名を追加 <----------- 重要
            self.listWidget_filepath.setCurrentRow(0)
        if not self.img_pobj_dict: # リピートモードでない場合は何も表示しない
            return
        first_img_path = str(self.img_pobj_dict[0].absolute()) # 最初のファイルパス
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(QColor(222, 222, 222)))
        self.pixmap = QPixmap(first_img_path) # pixmap更新
        self.set_image_from_pixmap()

    def init_graphics_view_pdf(self):
        first_file_path = None
        if not self.is_pdfmode_to_read_image_file: # PDFモードの場合
            self.pdf_img_reader = PdfImgReader(self.img_dobj, self.config_dict['matrix'])
            self.pdf_page_list = self.pdf_img_reader.get_page_list()
            self.total_pdf_page_count = self.pdf_img_reader.get_total_page_count()
            for record in self.pdf_page_list:
                text = str((record['main_index']) + 1).zfill(3) + self.sep_of_line_widget_text + 'P' + str((record['page_index']) + 1).zfill(3) + self.sep_of_line_widget_text + record['file_name']
                item = QListWidgetItem(text)
                item.setData(100, record) # メタデータをセット
                self.listWidget_pdf.addItem(item) # listwidgetにページ番号とファイル名を表示
            self.label_pdf.setText(f'001 / {self.total_pdf_page_count:03}    ') # Labelにページ総数とページ番号を表示
            # 最初のqpixmapを取得
            first_file_name = self.pdf_page_list[0]['file_name']
            self.pixmap = self.pdf_img_reader.get_img_from_pdf(first_file_name, 0) # pixmap更新
        else: # PDFモードでない場合
            self.total_pdf_page_count = 0
            fobjs = [fobj.resolve() for fobj in self.img_dobj.iterdir() if fobj.suffix.lower() in self.extensions and fobj.is_file()]
            fobjs = sorted(fobjs, key=lambda x: x.name)
            first_file_path = str(fobjs[0])
            self.pixmap = QPixmap(first_file_path) # pixmap更新
            for i, fobj in enumerate(fobjs):
                text = text = str(i + 1).zfill(3) + self.sep_of_line_widget_text + fobj.name
                item = QListWidgetItem(text)
                item.setData(100, {'img_obj': fobj, 'main_index': i, 'file_name': fobj.name})
                self.listWidget_pdf.addItem(item)
                self.total_pdf_page_count += 1
            self.label_pdf.setText(f'001 / {self.total_pdf_page_count:03}    ') # Labelにページ総数とページ番号を表示
        def fx():
            self.listWidget_pdf.blockSignals(True)
            self.listWidget_pdf.setCurrentRow(0)
            self.listWidget_pdf.blockSignals(False)
        QTimer.singleShot(500, fx)
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(QColor(222, 222, 222)))
        if first_file_path:
            self.set_image_from_pixmap(filepath=first_file_path)
        else:
            self.set_image_from_pixmap()

    def close_after_dialog(self):
        QTimer.singleShot(10, self.close)

    def show_init_dialog(self):
        self.init_dialog = InitDialog(self)
        self.init_dialog.close_parent.connect(self.close_after_dialog)
        self.init_dialog.exec_()

    def change_image(self, next_file_index): # 画像の変更処理メイン
        if (self.current_file_index + 1 == len(self.img_pobj_dict)
                and not self.is_selected_list_widget): # 最後の画像の場合
            return
        self.scene.removeItem(self.pixmap_item)
        def set_new_file_index():
            self.current_file_index = next_file_index # current_file_indexを更新
        QTimer.singleShot(0, set_new_file_index) # current_file_index更新を遅らせる
        current_pobj = self.img_pobj_dict[next_file_index]
        if not current_pobj.exists():
            ans_num = self.create_multi_button_msg(self, 'エラー', f'画像ファイルが見つかりませんでした\n\n対象ファイル名:\n{current_pobj.name}', ['リトライ', '再起動'], 0, 'warning')
            if ans_num == 0:
                while True:
                    if not current_pobj.exists():
                        ans_num = self.create_multi_button_msg(self, 'エラー', f'画像ファイルが見つかりませんでした\n\n対象ファイル名:\n{current_pobj.name}', ['リトライ', '再起動'], 0, 'warning')
                        if ans_num == 1:
                            self.restart_app(is_button_pressed=False)
                            return
                    else:
                        QMessageBox.information(self, '情報', '画像ファイルが見つかりました', QMessageBox.Ok)
                        break
            elif ans_num == 1:
                self.restart_app(is_button_pressed=False)
                return
        self.pixmap = QPixmap(str(current_pobj.absolute())) # pixmap更新
        self.original_pixmap = self.pixmap.copy()  # 回転やズーム前の画像を保存 # original_pixmap更新
        self.set_image_from_pixmap()

    def on_list_widget_selected_for_pdf(self, next_item, pre_item):
        next_record = next_item.data(100)
        next_pdf_fobj = next_record['pdf_obj']
        if not os.path.exists(str(next_pdf_fobj)):
            ans_num = self.create_multi_button_msg(self, 'エラー', f'PDFファイルが見つかりませんでした\n\n対象ファイル名:\n{next_pdf_fobj.name}', ['リトライ', '再起動'], 0, 'warning')
            if ans_num == 0:
                while True:
                    if not os.path.exists(str(next_pdf_fobj)):
                        ans_num = self.create_multi_button_msg(self, 'エラー', f'PDFファイルが見つかりませんでした\n\n対象ファイル名:\n{next_pdf_fobj.name}', ['リトライ', '再起動'], 0, 'warning')
                        if ans_num == 1:
                            self.restart_app(is_button_pressed=False)
                            return
                    else:
                        QMessageBox.information(self, '情報', 'PDFファイルが見つかりました', QMessageBox.Ok)
                        break
            elif ans_num == 1:
                self.restart_app(is_button_pressed=False)
                return
        next_main_index = next_record['main_index']
        self.label_pdf.setText(f'{next_main_index + 1:03} / {self.total_pdf_page_count:03}    ') # Labelにページ総数とページ番号を表示
        self.pixmap = self.pdf_img_reader.get_img_from_pdf(next_record['file_name'], next_record['page_index']) # pixmap更新
        self.set_image_from_pixmap(is_list_clicked=True)

    def select_item_for_list_widget_for_pdf(self, num: int = 1):
        if not self.is_pdfmode:
            return
        current_row = self.listWidget_pdf.currentRow()
        if num == -1 and current_row == 0:
            return
        elif num == 1 and current_row == self.total_pdf_page_count - 1:
            return
        next_row = current_row + num
        self.listWidget_pdf.setCurrentRow(next_row)

    def set_today_text(self):
        focused_obj = self.get_focused_line_edit_obj()
        type_text = self.obj_name_to_type_dict[focused_obj.objectName()]
        types = type_text.split('_')
        if 'date' in types:
            current_text = focused_obj.text()
            today_text = datetime.now().strftime('%Y/%#m/%#d')
            focused_obj.setText(current_text + today_text)

    def goto_first_or_last_line_edit(self, mode='last'):
        if mode == 'last':
            for data in reversed(self.data_list):
                if data['line_edit_obj'].isVisible():
                    data['line_edit_obj'].setFocus()
                    break
        elif mode == 'first':
            for data in self.data_list:
                if data['line_edit_obj'].isVisible():
                    data['line_edit_obj'].setFocus()
                    break

    def goto_first_visible_line_edit(self):
        for data in self.data_list:
            if data['line_edit_obj'].isVisible():
                data['line_edit_obj'].setFocus()
                break

    def on_list_widget_selected(self, next_item, previous_item=None): # リストウィジェットのアイテムが選択された時の処理
        if previous_item is None:
            pass
        self.next_index_for_filepath_list = self.listWidget_filepath.row(next_item)
        self.previous_index_for_filepath_list = self.listWidget_filepath.row(previous_item)
        self.focused_obj_for_list_clicked = self.get_focused_line_edit_obj()
        try:
            self.list_widget_dd.close()
            self.list_widget_dd = None
        except:
            pass
        self.is_selected_list_widget = True
        if self.input_mode == 'new1' and not self.is_enter_pressed: # newである, enterでない場合
            if not self.is_rept_mode: # reptでない場合
                self.is_next_img_change = True
                self.process_of_before_change_image(next_file_index=self.listWidget_filepath.currentRow(),
                        is_list_clicked=True)
                self.is_next_img_change = False
            else: # reptの場合
                clicked_index = self.listWidget_filepath.currentRow()
                if clicked_index in self.current_df.index: # dfにレコードが存在する場合
                    value_list = self.current_df.loc[clicked_index].to_list()
                    self.set_new_text_to_line_edits(value_list) # dfに次のレコードが存在する場合は 入力欄にテキストをセット
                    def _set_curent_index():
                        self.current_file_index = clicked_index
                    QTimer.singleShot(0, _set_curent_index) # current_file_indexを遅延更新
                else: # rept時、dfにレコードが存在しない場合
                    # reptLineEditsを空白にする処理...
                    self.set_blank_to_line_edits()
        self.current_index_for_img_df = self.next_index_for_filepath_list
        if self.is_img_listwidget_select_canceled:
            def _select_listwidget():
                self.listWidget_filepath.blockSignals(True)
                self.listWidget_filepath.setCurrentRow(self.previous_index_for_filepath_list) # キャンセル時は前のアイテム選択
                self.listWidget_filepath.blockSignals(False)
            QTimer.singleShot(0, _select_listwidget)
        self.is_img_listwidget_select_canceled = False
        self.is_selected_list_widget = False

    def select_next_item_of_list_widget(self, next_file_index):
        if not self.is_pdfmode:
            if self.input_mode == 'ver1':
                self.listWidget_filepath.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.listWidget_filepath.blockSignals(True)
            self.listWidget_filepath.setCurrentRow(next_file_index)
            self.listWidget_filepath.blockSignals(False)
            if self.input_mode == 'ver1':
                self.listWidget_filepath.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        else: # pdfmode
            if self.input_mode == 'ver1':
                self.listWidget_pdf_record.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.listWidget_pdf_record.setCurrentRow(next_file_index)
            if self.input_mode == 'ver1':
                self.listWidget_pdf_record.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    def change_color_of_all_line_edits(self, color: str): # 全てのLineEditの文字色を変更
        for data in self.data_list:
            global_color = self.global_color_dict[color]
            palette = data['line_edit_obj'].palette()
            palette.setColor(QPalette.ColorRole.Text, global_color)
            data['line_edit_obj'].setPalette(palette)

    def change_color_of_line_edit(self, line_edit_obj, color: str): # LineEditの文字色を変更
        global_color = self.global_color_dict[color]
        palette = line_edit_obj.palette()
        palette.setColor(QPalette.ColorRole.Text, global_color)
        line_edit_obj.setPalette(palette)

    def change_color_black_or_red(self, is_ignore_empty: bool = False):
        # 型が違う場合は文字色を赤くする処理...
        for data in self.data_list:
            current_obj = data['line_edit_obj']
            current_value = data['line_edit_obj'].text()
            if is_ignore_empty and not current_value: # NEW1次の画像時 空白の場合
                self.change_color_of_line_edit(data['line_edit_obj'], 'black') # 黒
            else:
                if current_value == '中学':
                    pass
                is_valid = self.check_type_line_edit(current_value, data['data_type'], current_obj)
                if not is_valid and current_value: # 空白でなく、エラーの場合
                    self.change_color_of_line_edit(data['line_edit_obj'], 'red')
                else: # エラーでない場合、空白の場合
                    self.change_color_of_line_edit(data['line_edit_obj'], 'black')

    def create_rept_list_texts(self): # rept専用
        rept_indexes = [data['index'] for data in self.data_list if data['is_rept'] == True]
        list_widget_texts = []
        df_rows_count = self.current_df.shape[0]
        for i in range(df_rows_count):
            one_lines = []
            one_text = ''
            for rept_index in rept_indexes:
                one_lines.append(self.current_df.at[i, rept_index])
                one_text = self.sep_of_line_widget_text.join(one_lines)
            list_widget_texts.append(f'{i + 1:05}{self.sep_of_line_widget_text}' + one_text)
        list_widget_texts.append('新しいレコード')
        # list_widget_texts.append(f'{df_rows_count:05}{self.sep_of_line_widget_text}新しいレコード')
        return list_widget_texts

    def output_csv(self) -> bool:
        pd.set_option('future.no_silent_downcasting', True) # 警告無効
        self.current_df = self.current_df.fillna('') # NaNを空文字に変換
        self.current_df = self.current_df.astype(str) # 全てのデータを文字列に変換
        self.current_df = self.current_df.sort_index(axis=0)
        # self.current_df = self.current_df.sort_index(axis=1) # DELETE 列の順番をソート
        pd.set_option('future.no_silent_downcasting', False) # 警告有効
        buf_df = self.current_df.copy()
        # if self.main_mode in ['foreigner', 'prevention']:
        if self.headers_dict[self.main_mode]['has_header']: # ヘッダーありの場合
            cols_count = self.current_df.shape[1]
            another_headers = self.headers_dict[self.main_mode]['headers'][:cols_count - 3]
            another_headers.extend([10000, 20000, 30000])

            # WIP ここで _data_transform.py の処理
            if self.mode_config_manager.get_need_df_transformed(self.main_mode): # need_df_transformed が True の場合
                self.current_df = self.data_transformer.transform_output_df(self.current_df) # データ変換処理
            else:
                rename_dict = {old: new for old, new in zip(self.current_df.columns ,another_headers)} # デフォルトの列を設定
                self.current_df = self.current_df.rename(columns=rename_dict)
        try:
            if self.current_df.astype('string').apply(lambda row_series: row_series.str.contains(r'[\r\n\t]', na=False)).any().any():
                self.current_df = self.current_df.replace(
                    {
                        r'\n': r'\\n',
                        r'\r': r'\\r',
                        r'\t': r'\\t',
                    },
                    regex=True
                )
        except Exception as e:
            print('OUTPUT_CSV replace new line error:', e)
        if self.is_multi_pdf_mode: # ! マルチPDFモードの場合 ページ番号をファイル名に追加
            # マルチPDFモードの場合 ファイル名にページ番号を付与
            self.current_df['stem'] = self.current_df[10000].astype(str).str.rsplit('.', n=1).str[0]
            self.current_df['ext'] = '.' + self.current_df[10000].astype(str).str.rsplit('.', n=1).str[1]
            self.current_df['page'] = (self.current_df.groupby(10000).cumcount() + 1).astype(str).str.zfill(4)
            self.current_df[10000] = self.current_df['stem'] + '_' + self.current_df['page'] + self.current_df['ext']
            self.current_df = self.current_df.drop(columns=['stem', 'ext', 'page'])
            if self.main_mode == 'factory':
                self.current_df = self.current_df.rename(columns={10000: '画像データ'})
        try:
            has_header = self.headers_dict[self.main_mode]['has_header']
            DataIO.write_csv_with_header(
                self,
                self.current_df,
                self.output_csv_fobj,
                encoding=self.encode_type,
                has_header=has_header
            ) # IMPORTANT <-- エンター時CSV出力処理
            if self.is_rept_mode:
                self.current_index_for_rept_and_ver += 1

            return False # is_error
        except PermissionError:
            # スクロールエリアの更新する...
            is_updates_enabled_scroll_area_input = self.scrollArea_input.updatesEnabled()
            is_updates_enabled_scroll_area_input_right = self.scrollArea_input_right.updatesEnabled()
            if not is_updates_enabled_scroll_area_input:
                self.scrollArea_input.setUpdatesEnabled(True)
            if not is_updates_enabled_scroll_area_input_right:
                self.scrollArea_input_right.setUpdatesEnabled(True)
            # /
            QMessageBox.critical(self, 'エラー', 'CSVファイルの保存に失敗しました\n\n' + 'ファイルが開かれていて保存できない可能性があります\n\n' +
                    f'対象ファイルパス；{str(self.output_csv_fobj)}')
            # スクロールエリアの更新を停止する...
            if not is_updates_enabled_scroll_area_input:
                self.scrollArea_input.setUpdatesEnabled(True)
            if not is_updates_enabled_scroll_area_input_right:
                self.scrollArea_input_right.setUpdatesEnabled(True)
            # /
            return True # is_error
        finally:
            self.current_df = buf_df.copy()

    def set_new_text_to_line_edits(self, value_list):
        if not self.is_initialaized:
            self.deactivate_all_event_filter()
        for i, value in enumerate(value_list):
            if i < len(self.data_list):
                if self.data_list[i]['is_show'] == False:
                    continue
                target_line_edit_obj = self.data_list[i]['line_edit_obj']
                target_line_edit_obj.blockSignals(True)
                target_line_edit_obj.setText(str(value))
                target_line_edit_obj.blockSignals(False)
        if not self.is_initialaized:
            self.activate_all_event_filter()

    def get_timestamp(self, for_filename=False):
        if for_filename:
            return datetime.now().strftime('%Y%m%d_%H%M_%S') # ロブファイル名用のタイムスタンプ
        else:
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def set_image_from_pixmap(self, is_list_clicked=False, filepath=None):
        is_pre_pos_valid = False
        # if hasattr(self, 'pixmap_item') and self.pixmap_item is not None and not sip.isdeleted(self.pixmap_item):
        if hasattr(self, 'pixmap_item') and self.pixmap_item is not None:
            # ******
            # 画像変更前の画像とスクロールバーの位置を取得
            pre_scroll_x = self.graphicsView_main.horizontalScrollBar().value()
            pre_scroll_y = self.graphicsView_main.verticalScrollBar().value()
            pre_scroll_x_max = self.graphicsView_main.horizontalScrollBar().maximum()
            pre_scroll_x_min = self.graphicsView_main.horizontalScrollBar().minimum()
            pre_scroll_y_max = self.graphicsView_main.verticalScrollBar().maximum()
            pre_scroll_y_min = self.graphicsView_main.verticalScrollBar().minimum()
            self.graphicsView_main.horizontalScrollBar().setValue(0)
            self.graphicsView_main.verticalScrollBar().setValue(0)
            pre_pos = self.graphicsView_main.mapFromScene(self.pixmap_item.scenePos())
            self.graphicsView_main.viewport().setUpdatesEnabled(False)
            is_pre_pos_valid = True
            if self.pixmap_item in self.scene.items():
                self.scene.removeItem(self.pixmap_item)
            # 画像変更前の画像とスクロールバーの位置を取得
            # ******
        if filepath:
            try:
                rotate_exif = self.image_utils.get_rotate_exif(filepath)
                tranform = QTransform().rotate(rotate_exif)
                self.pixmap = self.pixmap.transformed(tranform, mode=Qt.TransformationMode.SmoothTransformation)
            except Exception as e:
                print('回転処理エラー(exif):', e)

        self.original_pixmap = self.pixmap.copy()  # 回転やズーム前の画像を保存 # original_pixmap更新
        self.pixmap_item = DraggablePixmapItem(self, self.pixmap) # ドラッグ可能ピクスマップアイテムインスタンス作成
        self.pixmap_item.setTransformOriginPoint(0, 0)  # 回転の原点を中心に設定
        self.rotate_image(0)
        # self.scaling_image(0)
        self.scene.addItem(self.pixmap_item)
        self.graphicsView_main.setScene(self.scene)
        self.graphicsView_main.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        if is_list_clicked:
            self.reset_scroll_and_align_item()
        if hasattr(self, 'pixmap_item') and self.pixmap_item is not None and is_pre_pos_valid:
            # ******
            # 画像変更前の画像とスクロールバーの位置を復元
            self.pixmap_item.setPos(pre_pos)
            self.graphicsView_main.horizontalScrollBar().setMaximum(pre_scroll_x_max)
            self.graphicsView_main.horizontalScrollBar().setMinimum(pre_scroll_x_min)
            self.graphicsView_main.verticalScrollBar().setMaximum(pre_scroll_y_max)
            self.graphicsView_main.verticalScrollBar().setMinimum(pre_scroll_y_min)
            self.graphicsView_main.horizontalScrollBar().setValue(pre_scroll_x)
            self.graphicsView_main.verticalScrollBar().setValue(pre_scroll_y)
            self.graphicsView_main.viewport().setUpdatesEnabled(True)
            # 画像変更前の画像とスクロールバーの位置を復元
            # ******
        if self.radioButton_rect_select.isChecked():
            self.change_rect_mode('select')

    def adjust_image(self, mode: str = 'w', is_button=False): # GraphicsViewの高さ、幅を取得して画像をフィットさせる
        view_width = self.graphicsView_main.width()
        view_height = self.graphicsView_main.height()
        original_width = self.original_pixmap.width()
        original_height = self.original_pixmap.height()
        vertical_scrollbar_width = self.graphicsView_main.verticalScrollBar().width()
        horizontal_scrollbar_height = self.graphicsView_main.horizontalScrollBar().height()
        transform = QTransform().rotate(self.current_angle) # pixmapをcurrent_angleの角度で回転
        self.pixmap = self.original_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        if mode == 'w':
            new_width = view_width
            new_width_without_scroll_var = new_width - vertical_scrollbar_width # スクロールバーの幅を除外
            if self.current_angle in [90, 270]: # 90度または270度の場合は幅と高さを入れ替える
                original_width, original_height = original_height, original_width
            scale_factor = new_width_without_scroll_var / original_width
            new_height = int(original_height * scale_factor)
            self.pixmap = self.pixmap.scaled(new_width_without_scroll_var, new_height, # リサイズした画像を新しいPixmapに設定
                    Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        elif mode == 'h':
            new_height = view_height
            new_height_without_scroll_var = new_height - horizontal_scrollbar_height
            if self.current_angle in [90, 270]: # 90度または270度の場合は幅と高さを入れ替える
                original_width, original_height = original_height, original_width
            scale_factor = new_height_without_scroll_var / original_height
            new_width = int(original_width * scale_factor)
            self.pixmap = self.pixmap.scaled(new_width, new_height_without_scroll_var, # リサイズした画像を新しいPixmapに設定
                    Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.pixmap_item.setPixmap(self.pixmap)  # 既存のpixmap_itemに新しいpixmapをセット
        self.pixmap_item.setPos(0, 0)  # アイテムの位置を初期化
        self.scene.setSceneRect(self.pixmap_item.boundingRect()) # シーンのサイズを画像のサイズに合わせる
        if self.current_angle in [0, 180]:
            self.current_scale = new_width / original_width
            # self.current_scale = round(new_width / original_width, 1)
        elif self.current_angle in [90, 270]:
            self.current_scale = new_height / original_height
            # self.current_scale = round(new_height / original_height, 1)
        self.show_angle_and_scale()
        if is_button:
            self.reset_scroll_and_align_item()

    def rotate_image(self, angle: int, is_absolute = False, is_button=False): # 画像を回転させる
        if is_absolute:
            next_angle = angle
        else:
            next_angle = self.current_angle + angle
        transform = QTransform().rotate(next_angle) # 回転の角度transformを設定
        rotated_pixmap = self.original_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation) # 回転後のpixmapを取得
        if self.current_scale != 1.0: # 拡大処理が必要な場合
            new_width = int(rotated_pixmap.width() * self.current_scale)
            new_height = int(rotated_pixmap.height() * self.current_scale)
            rotated_pixmap = rotated_pixmap.scaled(
                    new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.pixmap_item.setPixmap(rotated_pixmap) # 回転後のpixmapをpixmap_itemにセット
        self.pixmap_item.setPos(0, 0) # アイテムの位置を左上に設定
        self.scene.setSceneRect(self.pixmap_item.boundingRect()) # シーンのサイズを画像のサイズに合わせる
        self.current_angle = int(next_angle % 360)
        self.show_angle_and_scale()
        if is_button:
            self.reset_scroll_and_align_item()

    def scaling_image(self, scale: float = 0, is_reset: bool = False, is_absolute: bool = False, is_button=False): # 画像を拡大縮小する
        if is_reset and is_absolute:
            raise ValueError('is_resetとis_absoluteは同時にTrueにできません')
        if is_reset or is_button == False:
            self.graphicsView_main.horizontalScrollBar().setValue(0)
            self.graphicsView_main.verticalScrollBar().setValue(0)
        # view中央に向けて拡大縮小するための設定
        if self.pixmap_item and is_button and not self.is_initialaized:
            view_w_harf, view_h_harf = int(self.graphicsView_main.geometry().width() / 2), int(self.graphicsView_main.geometry().height() / 2)
            view_center_in_scene = self.graphicsView_main.mapToScene(view_w_harf, view_h_harf)
            center_in_item = self.pixmap_item.mapFromScene(view_center_in_scene)
            item_x = center_in_item.x()
            item_y = center_in_item.y()
            item_w = self.pixmap_item.pixmap().width()
            item_h = self.pixmap_item.pixmap().height()
            x_per_w = item_x / item_w
            y_per_h = item_y / item_h
        next_scale = self.current_scale + scale
        if next_scale < 0.1:
            next_scale = 0.1
        if is_reset:
            next_scale = 1.0
        elif is_absolute:
            next_scale = scale
        # if self.is_initialaized:
        #     next_scale = 1.0
        new_width = int(self.original_pixmap.width() * next_scale)
        new_height = int(self.original_pixmap.height() * next_scale)
        scaled_pixmap = self.original_pixmap.scaled(
                new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        if self.pixmap_item.boundingRect().width() > self.max_side_length or self.pixmap_item.boundingRect().height() > self.max_side_length:
            if next_scale > 1 and is_absolute:
                self.show_angle_and_scale()
                return
            if scale > 0 and not is_absolute:
                self.show_angle_and_scale()
                return
        self.pixmap_item.setPixmap(scaled_pixmap)
        self.pixmap_item.setPos(0, 0)
        self.scene.setSceneRect(self.pixmap_item.boundingRect()) # シーンのサイズを画像のサイズに合わせる
        self.current_scale = next_scale
        if self.current_angle != 0:
            transform = QTransform().rotate(self.current_angle)
            rotated_pixmap = scaled_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
            self.pixmap_item.setPixmap(rotated_pixmap)
            self.pixmap_item.setPos(0, 0)
            self.scene.setSceneRect(self.pixmap_item.boundingRect())
            self.current_scale = next_scale
        self.show_angle_and_scale()
        if is_button:
            self.reset_scroll_and_align_item()
        if self.pixmap_item and is_button and not self.is_initialaized and not is_reset:
            delta_x = x_per_w * self.pixmap_item.pixmap().width()
            delta_y = y_per_h * self.pixmap_item.pixmap().height()
            self.pixmap_item.setPos(-delta_x + view_w_harf, -delta_y + view_h_harf)
            self.scene.setSceneRect(self.pixmap_item.sceneBoundingRect())
            self.pixmap_item.adjust_scene_to_fit_item()

    def change_scale_on_line_edit(self):
        original_pixmap = self.original_pixmap
        try:
            scale = float(self.lineEdit_scale.text()) / 100
        except ValueError:
            QMessageBox.critical(self, 'エラー', '拡大率は数値で入力してください')
            scale = self.current_scale
            try:
                self.lineEdit_scale.setText(str(round(self.current_scale * 100, 1)))
            finally:
                return
        w_for_check = original_pixmap.width() * scale
        h_for_chedk = original_pixmap.height() * scale
        if w_for_check > self.max_side_length or h_for_chedk > self.max_side_length:
            scale = min(self.max_side_length / original_pixmap.width(), self.max_side_length / original_pixmap.height())
        if scale < 0.1:
            scale = 0.1
            self.lineEdit_scale.setText('10.0')
        if scale and self.is_float(scale): # 空白でない、かつ、フロート場合
            self.scaling_image(scale, is_absolute=True)

    def reset_scroll_and_align_item(self):
        self.pixmap_item.setPos(0, 0) # アイテムの位置をシーンの左上 (0, 0) に合わせる
        item_rect = self.pixmap_item.sceneBoundingRect() # アイテムのシーン内でのバウンディングボックスを取得
        self.graphicsView_main.setSceneRect(item_rect) # シーンのサイズをアイテムのサイズに合わせて設定
        self.graphicsView_main.horizontalScrollBar().blockSignals(True)
        self.graphicsView_main.verticalScrollBar().blockSignals(True)
        self.graphicsView_main.horizontalScrollBar().setValue(0)
        self.graphicsView_main.verticalScrollBar().setValue(0)
        self.graphicsView_main.horizontalScrollBar().blockSignals(False)
        self.graphicsView_main.verticalScrollBar().blockSignals(False)
        self.graphicsView_main.viewport().update() # 最終的にビューを更新して変更を反映

    def align_image_to_top_left(self): # 画像を左上に合わせる 今は使っていない
        bounding_rect = self.pixmap_item.boundingRect()# バウンディングボックスを取得
        self.pixmap_item.setPos(-bounding_rect.width() / 2, -bounding_rect.height() / 2)# 左上に位置を調整
        self.scene.setSceneRect(self.pixmap_item.sceneBoundingRect())

    def show_angle_and_scale(self): # 回転角度と拡大率をラベルに表示
        self.lineEdit_angle.blockSignals(True)
        if self.pixmap_item is not None:
            self.pixmap_item.delete_sub_rect() # 黄色い四角を削除
        self.lineEdit_angle.setText(str(self.current_angle))
        self.lineEdit_scale.setText(str(round(self.current_scale * 100, 1)))
        self.lineEdit_angle.blockSignals(False)

    def check_config(self):
        # ConfigManagerに処理を委譲
        self.config_manager.config = self.config_dict
        self.config_manager.check_and_fix()
        self.config_dict = self.config_manager.config

    def write_config(self, config_dict: dict): # 設定dictを渡して設定ファイルに書き込む
        # ConfigManagerに処理を委譲
        self.config_manager.write(config_dict)

    def read_config(self) -> dict:
        # ConfigManagerに処理を委譲
        self.config_dict = self.config_manager.read()
        return self.config_dict

    def write_rect_config(self, rect_dict: dict): # 設定dictを渡して設定ファイルに書き込む
        # RectConfigManagerに処理を委譲
        self.rect_config_manager.write(rect_dict)

    def read_rect_config(self) -> dict:
        # RectConfigManagerに処理を委譲
        self.rect_dict = self.rect_config_manager.read()
        return self.rect_dict

    def eventFilter(self, obj, event):
        # MainWindowのイベントフィルターを処理...
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Escape:
                return True  # イベントを無効化してデフォルトの処理を防ぐ
            elif event.key() == Qt.Key.Key_F4 and event.modifiers() == Qt.AltModifier:
                return True  # イベントを無効化してデフォルトの処理を防ぐ !!!動作不良!!!
            elif event.key() == Qt.Key.Key_PageUp:
                self.select_item_for_list_widget_for_pdf(-1)
                return True
            elif event.key() == Qt.Key.Key_PageDown:
                self.select_item_for_list_widget_for_pdf(1)
                return True
        # scrollAreaWidgetContentsの上にマウスがあるかどうかを判定...
        if obj == self.scrollAreaWidgetContents or obj == self.scrollArea_input_right:
            if event.type() == QEvent.Enter:
                self.is_mouse_on_scroll_area = True
            elif event.type() == QEvent.Leave:
                self.is_mouse_on_scroll_area = False
        return super().eventFilter(obj, event)

    def showEvent(self, event): # ウィジェット初期化後処理
        if self.is_in_close_processing:
            return
        super().showEvent(event)
        if self.config_dict['splitter_1b_height'] > 100:
            sp_b1_h = self.config_dict['splitter_1b_height']
        else:
            sp_b1_h = 200
        self.splitter.setSizes([self.config_dict['splitter_1a_height'], sp_b1_h])
        self.splitter_2.setSizes([self.config_dict['splitter_2a_width'], self.config_dict['splitter_2b_width']])
            # スプリッターのサイズを設定...
        self.current_angle = self.config_dict['current_angle'] # 回転角度と設定
        self.current_scale = self.config_dict['current_scale'] # 拡大率を設定
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 0)
        self.splitter_2.setStretchFactor(0, 1)
        self.splitter_2.setStretchFactor(1, 0)
        # if not self.is_show_init_dialog and not self.is_close_button_pressed:
        if self.config_dict['is_maximized_screen']: # メインウィンドウのサイズを設定
            if self.is_first_init:
                self.showMaximized()
            else:
                QTimer.singleShot(10, self.showFullScreen)
                QTimer.singleShot(30, self.showMaximized)
        else:
            self.resize(self.config_dict['window_width'], self.config_dict['window_height'])
        # QTimer.singleShot(100, lambda: self.adjust_image('h')) # 画像を幅に合わせる)

    def closeEvent(self, event): # 終了前処理
        if self.is_in_close_processing:
            return
        if QMessageBox.question(self, '確認', '終了しますか？', QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            event.ignore()
            return
        if not self.is_in_close_processing:
            self.close_event_processing()
        return super().closeEvent(event)

    def close_event_processing(self):
        if self.list_widget_dd is not None:
            self.list_widget_dd.close()
            self.list_widget_dd = None
        try:
            self.clean_up_thread()
            # self.ime_thread.deleteLater()
        except:
            pass
        self.config_dict['splitter_5a_height'] = int(self.scrollArea_top.size().height())
        self.config_dict['splitter_5b_height'] = int(self.splitter_4.size().height())
        self.config_dict['splitter_6a_width'] = int(self.frame_pdf.size().width())
        self.config_dict['splitter_6b_width'] = int(self.listWidget_pdf_record.size().width())
        if self.config_dict['layout_type'] == 'v':
            self.config_dict['splitter_1a_height'] = int(self.graphicsView_main.size().height())
            self.config_dict['splitter_1b_height'] = int(self.frame_splitter_below.size().height())
            self.config_dict['splitter_2a_width'] = int(self.frame_of_below_scrollarea.size().width())
            self.config_dict['splitter_2b_width'] = int(self.frame_splitter_after.size().width())
        else:
            self.config_dict['splitter_3a_width'] = int(self.splitter.size().width())
            self.config_dict['splitter_3b_width'] = int(self.splitter_3.size().width())
            self.config_dict['splitter_4a_height'] = int(self.frame_for_right_top_sp.size().height())
            self.config_dict['splitter_4b_height'] = int(self.frame_for_right_list.size().height())
        if self.windowState() == Qt.WindowState.WindowMaximized:
            self.config_dict['is_maximized_screen'] = True
        else:
            self.config_dict['is_maximized_screen'] = False
            self.config_dict['window_width'] = self.width()
            self.config_dict['window_height'] = self.height()
        self.config_dict['current_angle'] = self.current_angle
        self.config_dict['current_scale'] = round(self.current_scale, 4)
        self.config_dict['auto_move'] = True if self.radioButton_automove_on.isChecked() else False
        self.config_dict['is_rect_show'] = True if self.radioButton_rect_show.isChecked() else False
        self.config_dict['auto_move'] = True if self.radioButton_automove_on.isChecked() else False
        # self.config_dict = sorted(self.config_dict)
        self.write_config(self.config_dict) # 設定ファイルに書き込む

    def check_encoding_line_edits(self):
        errors = []
        for data in self.data_list:
            current_obj = data['line_edit_obj']
            current_label = data['name']
            current_value = current_obj.text()
            if current_value == '':
                continue
            result = self.validator.is_encodable(s=current_value, enable_return=True)
            if isinstance(result, bool): # Trueの場合はエンコード可能
                continue
            else: # タプルの場合はエンコード不可能
                char, start_num = result[0], result[1]
            errors.append(f'[{current_label}] {start_num}文字目：{char}')
        if errors == []:
            QMessageBox.information(self, '確認', '全てのテキストボックスの文字はエンコード可能です')
        else:
            QMessageBox.warning(self, '警告', '以下の文字は特殊なためエンコードできません\n\n' + '\n'.join(errors))

    def check_type_line_edit(self, current_value, data_type, current_obj=None) -> bool:
        # current_objから必要なパラメータを抽出
        list_items = None
        max_length = None
        min_val = None
        max_val = None
        min_len = None
        max_len = None
        length = None
        pattern = None
        escape_pattern = False

        if current_obj is not None:
            obj_name = current_obj.objectName()
            if obj_name in self.main_data_dict:
                data_dict = self.main_data_dict[obj_name]
                max_length = data_dict.get('max_length')
                min_max = data_dict.get('min_max')
                if min_max:
                    min_val, max_val = min_max[0], min_max[1]
                length_val = data_dict.get('length')
                if isinstance(length_val, list) and len(length_val) == 2:
                    min_len, max_len = int(length_val[0]), int(length_val[1])
                elif isinstance(length_val, int):
                    length = length_val
                pattern = data_dict.get('re')
                escape_pattern = data_dict.get('escape_pattern', False)
            if obj_name in self.obj_name_to_list_item_dict:
                list_items = self.obj_name_to_list_item_dict[obj_name]

        # validatorのcheck_typeメソッドを使用
        return self.validator.check_type(
            current_value, data_type,
            list_items=list_items,
            max_length=max_length,
            min_val=min_val,
            max_val=max_val,
            min_len=min_len,
            max_len=max_len,
            length=length,
            pattern=pattern,
            escape_pattern=escape_pattern
        )

    def check_type_all_line_edit(self) -> list:
        is_valids_and_names_types = [[], [], []] # [0]はbool, [1]はLineEditの名前, [2]は日本語の型名
        for data in self.data_list:
            current_value = data['line_edit_obj'].text()
            if 'listonly' in data['data_type'] or 'inli' in data['data_type']:
                self.focus_out_obj_for_list_check = data['line_edit_obj']
            is_valid = self.check_type_line_edit(current_value, data['data_type'], current_obj=data['line_edit_obj'])
            is_valids_and_names_types[0].append(is_valid)
            if not is_valid:
                obj_name = data['line_edit_obj'].objectName()
                is_valids_and_names_types[1].append(obj_name)
                data_type = self.obj_name_to_type_dict[obj_name]
                jp_type = self.type_info_dict[data_type]
                is_valids_and_names_types[2].append(jp_type)
            else:
                is_valids_and_names_types[1].append('')
                is_valids_and_names_types[2].append('') # jp_type
        return is_valids_and_names_types

    def set_values_pref_city_and_town(self):
        '''
        郵便番号による住所自動入力
        '''
        self.pn_auto_input_to_obj_dict: dict[str, QtWidgets.QLineEdit]
        postnum_obj = self.pn_auto_input_to_obj_dict.get('postnum', None)
        postnum_obj: QtWidgets.QLineEdit
        if postnum_obj is None or self.focus_in_line_widget_obj is None:
            return
        if not (postnum_obj != '' and postnum_obj.objectName() == self.focus_in_line_widget_obj.objectName()):
            return
        postnum = postnum_obj.text()
        pn_df = self.postnum_reader.conv_df
        if not self.postnum_reader.is_valid_pkl or pn_df is None:
            return
        pref_obj = self.pn_auto_input_to_obj_dict.get('pref', None)
        city_obj = self.pn_auto_input_to_obj_dict.get('city', None)
        town_obj = self.pn_auto_input_to_obj_dict.get('town', None)
        pref_city_town_obj = self.pn_auto_input_to_obj_dict.get('pref-city-town', None)
        city_town_obj = self.pn_auto_input_to_obj_dict.get('city-town', None)
        self.pref_city_town_dict = self.postnum_reader.get_city_and_town_from_postnum(postnum)
        if self.pref_city_town_dict is None:
            return
        pref = self.pref_city_town_dict.get('pref', '')
        city = self.pref_city_town_dict.get('city', '')
        town = self.pref_city_town_dict.get('town', '')
        if pref_obj is not None:
            pre_pref = pref_obj.text()
            if pref != '' and not pre_pref.startswith(pref):
                pref_obj.setText(pref)
        if city_obj is not None:
            pre_city = city_obj.text()
            if city != '' and not pre_city.startswith(city):
                city_obj.setText(city)
        if town_obj is not None:
            pre_town = town_obj.text()
            if town != '' and not pre_town.startswith(town):
                town_obj.setText(town)
        if pref_city_town_obj is not None:
            pref_city_town = f'{pref}{city}{town}'
            pre_pref_city_town = pref_city_town_obj.text()
            if pref_city_town != '' and not pre_pref_city_town.startswith(pref_city_town):
                pref_city_town_obj.setText(pref_city_town)
        elif city_town_obj is not None:
            city_town = f'{city}{town}'
            pre_city_town = city_town_obj.text()
            if city_town != '' and not pre_city_town.startswith(city_town):
                city_town_obj.setText(city_town)

    def conversion_inputted_text(self, collation_line_obj=None, verified_text=None): # テキスト変換ヘルパ replaceとconvert
        current_time = time.time()
        if current_time - self.last_executing_time_of_convertion_text < 0.1: # 0.1秒以内に最実行された場合
            return
        is_collation = True if collation_line_obj is not None else False
        self.last_executing_time_of_convertion_text = current_time # 最終実行時間を更新
        if not is_collation: # ! ベリファイダイアログでない場合
            if self.is_enter_pressed:
                self.focus_in_line_widget_obj = self.focus_in_line_widget_obj_buf_for_enter
            if self.focus_in_line_widget_obj is None: # フォーカスインlineがない場合
                return
            focus_in_line_obj = self.focus_in_line_widget_obj
            focus_in_line_obj: QtWidgets.QLineEdit
            pre_text = focus_in_line_obj.text()
            if pre_text == '':
                return
            conversion_text_type = self.obj_name_to_conversion_text_dict[focus_in_line_obj.objectName()]
            types = self.main_data_dict[focus_in_line_obj.objectName()]['data_type'].split('_')
            if conversion_text_type != '':
                if conversion_text_type == 'zen':
                    focus_in_line_obj.setText(self.sublib.h2z(pre_text))
                elif conversion_text_type == 'zen-kana-digit':
                    focus_in_line_obj.setText(self.sublib.h2z_kana_digit(pre_text)) # NEW
                elif conversion_text_type == 'zen-an':
                    focus_in_line_obj.setText(self.sublib.h2z_an(pre_text))
                elif conversion_text_type == 'zen-ans':
                    focus_in_line_obj.setText(self.sublib.h2z_ans(pre_text))
                elif conversion_text_type == 'han':
                    focus_in_line_obj.setText(self.sublib.z2h(pre_text))
                elif conversion_text_type == 'han-ans':
                    focus_in_line_obj.setText(self.sublib.z2h_ans(pre_text))
                elif conversion_text_type == 'zen-katakana':
                    focus_in_line_obj.setText(self.sublib.h2z_hira2kata(pre_text))

                if conversion_text_type == 'upper':
                    focus_in_line_obj.setText(pre_text.upper())
                elif conversion_text_type == 'lower':
                    focus_in_line_obj.setText(pre_text.lower())
                elif conversion_text_type == 'z2h-digit-only':
                    focus_in_line_obj.setText(self.sublib.z2h_digit_only(pre_text))

                if conversion_text_type == 'radd-str': # 右詰めの場合
                    target_text = focus_in_line_obj.text()
                    add_text = self.main_data_dict[focus_in_line_obj.objectName()]['remarks']
                    add_text = str(add_text)
                    if not target_text.endswith(add_text) and not target_text == '': # 既にサフィックスがある または空欄 の場合追加しない
                        target_text += add_text
                        focus_in_line_obj.setText(target_text)

                if conversion_text_type == 'current-ym':
                    if re.fullmatch(r'[0-9]{1,2}', pre_text):
                        y = datetime.now().strftime('%Y')
                        m = pre_text.zfill(2)
                        if m in ['10', '11', '12']:
                            y = str(int(y) - 1)
                        focus_in_line_obj.setText(f'{y}{m}')

                if conversion_text_type == "zerofill" and pre_text != '':
                    width = self.main_data_dict[focus_in_line_obj.objectName()]['length']
                    focus_in_line_obj.setText(self.sublib.zerofill(pre_text, width))
            if 'replace' in types: # ここら一体は下の collation も同じように設定するように
                pre_li = self.main_data_dict[focus_in_line_obj.objectName()]['replace_keys']
                next_li = self.main_data_dict[focus_in_line_obj.objectName()]['replace_values']
                target_text = focus_in_line_obj.text()
                try:
                    for pre, next in zip(pre_li, next_li):
                        if target_text == pre:
                            focus_in_line_obj.setText(next)
                            break
                except TypeError as e:
                    raise TypeError(f'replace_keys({pre}) または replace_values({next}) の設定が不正です') from e
            if 'radd' in types: # 右詰めの場合
                target_text = focus_in_line_obj.text()
                items = self.main_data_dict[focus_in_line_obj.objectName()]['length']
                if not(isinstance(items, list) and len(items) == 2):
                    raise ValueError('lengthの設定が不正です')
                add_text = items[1] * items[0]
                if not target_text.endswith(add_text) and not target_text == '': # 既にサフィックスがある または空欄 の場合追加しない
                    target_text += add_text
                    focus_in_line_obj.setText(target_text)

            if 'postauto' in types:
                target_text = focus_in_line_obj.text()
                if re.match(r'^\d{7}$', target_text):
                    target_text = f'{target_text[:3]}-{target_text[3:]}'
                    focus_in_line_obj.setText(target_text)
        elif is_collation: # ! ベリファイダイアログの場合
            focus_in_line_obj = collation_line_obj
            conversion_text_type = self.obj_name_to_conversion_text_dict[focus_in_line_obj.objectName()]
            types = self.main_data_dict[focus_in_line_obj.objectName()]['data_type'].split('_')
            if conversion_text_type != '':
                if conversion_text_type == 'zen':
                    verified_text = self.sublib.h2z(verified_text) # verified_text = なので注意
                elif conversion_text_type == 'zen-kana-digit':
                    verified_text = self.sublib.h2z_kana_digit(verified_text) # NEW
                elif conversion_text_type == 'zen-an':
                    verified_text = self.sublib.h2z_an(verified_text)
                elif conversion_text_type == 'zen-ans':
                    verified_text = self.sublib.h2z_ans(verified_text)
                elif conversion_text_type == 'han':
                    verified_text = self.sublib.z2h(verified_text)
                elif conversion_text_type == 'han-ans':
                    verified_text = self.sublib.z2h_ans(verified_text)
                elif conversion_text_type == 'zen-katakana':
                    verified_text = self.sublib.h2z_hira2kata(verified_text)

                if conversion_text_type == 'upper':
                    verified_text = verified_text.upper()
                elif conversion_text_type == 'lower':
                    verified_text = verified_text.lower()
                elif conversion_text_type == 'z2h-digit-only':
                    verified_text = self.sublib.z2h_digit_only(verified_text)

                elif conversion_text_type == 'radd-str': # 右詰めの場合
                    target_text = focus_in_line_obj.text()
                    add_text = self.main_data_dict[focus_in_line_obj.objectName()]['remarks']
                    add_text = str(add_text)
                    if not verified_text.endswith(add_text) and not verified_text == '': # 既にサフィックスがある または空欄 の場合追加しない
                        verified_text += add_text
                        verified_text = verified_text

                if conversion_text_type == 'current-ym':
                    if re.fullmatch(r'[0-9]{1,2}', verified_text):
                        y = datetime.now().strftime('%Y')
                        m = verified_text.zfill(2)
                        if m in ['10', '11', '12']:
                            y = str(int(y) - 1)
                        verified_text.setText(f'{y}{m}')

                if conversion_text_type == "zerofill" and verified_text != '':
                    width = self.main_data_dict[focus_in_line_obj.objectName()]['length']
                    verified_text = self.sublib.zerofill(verified_text, width)
            if 'replace' in types:
                pre_li = self.main_data_dict[focus_in_line_obj.objectName()]['replace_keys']
                next_li = self.main_data_dict[focus_in_line_obj.objectName()]['replace_values']
                target_text = verified_text
                for pre, next in zip(pre_li, next_li):
                    if target_text == pre:
                        verified_text = next
            if 'radd' in types: # 右詰めの場合
                target_text = focus_in_line_obj.text()
                items = self.main_data_dict[focus_in_line_obj.objectName()]['length']
                if not(isinstance(items, list) and len(items) == 2):
                    raise ValueError('lengthの設定が不正です')

                add_text = items[1] * items[0]
                if not verified_text.endswith(add_text) and not verified_text == '': # 既にサフィックスがある または空欄 の場合追加しない
                    verified_text += add_text
                    verified_text = verified_text

            if 'postauto' in types:
                if re.match(r'^\d{7}$', verified_text):
                    verified_text = f'{verified_text[:3]}-{verified_text[3:]}'
            return verified_text

    def activate_all_event_filter(self):
        if not hasattr(self, 'event_filter_dict'):
            return
        for event_filter in self.event_filter_dict.values():
            event_filter.is_event_filter_activated = True

    def deactivate_all_event_filter(self):
        if not hasattr(self, 'event_filter_dict'):
            return
        for event_filter in self.event_filter_dict.values():
            event_filter.is_event_filter_activated = False

    ############################## カスタムイベントフォーカスアウト時の処理 終了 #############################
################################## MainWindowクラス 終了 ##################################

############################ Cls CustomEventFilter開始（分離済み） ############################
# CustomEventFilterクラス群は _lib/_event_filters.py に移動されました
# - CustomEventFilterForGraphicsView
# - CustomEventFilterForLineEditScale
# - CustomEventFilterForLineEdit
# - CustomEventFilterForPlaneTextEdit
# - CustomEventFilterForDD
# - CustomEventFilterForButtonScrollArea
############################ Cls CustomEventFilter終了 ############################
############################ Cls SingleApplication 終了############################
############################## Cls EventFilter 終了 #############################
if __name__ == '__main__':
    # windowedモードのための遅延処理
    if getattr(sys, '_MEIPASS', None):
        data_dir = os.path.join(sys._MEIPASS, 'data')
        for _ in range(10):  # 最大1秒程度待つ
            if os.path.exists(data_dir):
                break
            time.sleep(0.1)
    try:
        mutex_name = "my_unique_singleton_mutex"
        mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)

        # GetLastErrorを使ってミューテックスがすでに存在するかを確認
        if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
            # print("アプリケーションはすでに実行されています。")
            sys.exit(0)
        # app = SingleApplication(sys.argv)
        app = QApplication(sys.argv)
        window = MyMainWindow()
        window.show()
        sys.exit(app.exec_())

    except Exception as e:
        if hasattr(sys, 'frozen'): # PyInstallerで実行されている場合
            error_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'error.log')
            log_ = create_logger(error_log_path)
            error_info = traceback.format_exc()
            log_.error(error_info)
        else:
            raise
