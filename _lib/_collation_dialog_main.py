# _collation_dialog_main.py
# CollationDialogクラス - データ照合ダイアログ
# MAIN_APP.pyから分離
#
# 作成日: 2025-10-25
# Phase B (続き): CollationDialogの分離

import os
import sys
import re
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPalette, QColor, QTextCursor, QTextCharFormat

from _collation_dialog_ui import Ui_CollationDialog
from _lib._sub_lib import SubLib
from _lib._collation_two_text import CollationTwoText


# CustomEventFilterForPlaneTextEditのインポートは循環参照を避けるため動的に行う
# from MAIN_APP import CustomEventFilterForPlaneTextEdit


class CollationDialog(QDialog, Ui_CollationDialog):
    def __init__(self, parent, pre_value: str, current_value: str, line_edit_obj: QtWidgets.QLineEdit):
        super().__init__()
        self.setupUi(self)
        try:
            if getattr(sys, 'frozen', False): # 実行ファイルの場合
                application_path = sys._MEIPASS # 実行ファイルのパス
                icon_path = os.path.join(application_path, 'icon.ico')
            else: # スクリプトファイルの場合
                application_path = os.path.dirname(__file__)
                icon_path = os.path.join(application_path, '_icon', 'icon.ico')
            self.setWindowIcon(QIcon(icon_path)) # ウィンドウのアイコンを設定
        except:
            icon_path = None
        self.plainTextEdit_new: QtWidgets.QTextEdit
        self.plainTextEdit_ver: QtWidgets.QTextEdit
        self.gridLayout: QtWidgets.QGridLayout
        self.label_item_name: QtWidgets.QLabel
        self.pushButton_show_deff: QtWidgets.QPushButton
        self.pushButton_set_color: QtWidgets.QPushButton
        self.is_show_dd = False
        self.sublib = SubLib()
        self.line_edit_obj = line_edit_obj
        self.plainTextEdit_new.setReadOnly(True)
        self.main_window = parent
        # self.main_window: MyMainWindow  # 型ヒントはコメントアウト（循環インポート回避）

        # 循環参照を避けるため、CustomEventFilterForPlaneTextEditを動的にインポート
        from MAIN_APP import CustomEventFilterForPlaneTextEdit
        self.custom_event_filter = CustomEventFilterForPlaneTextEdit(self, self.main_window) # イベントフィルタをインスタンス化
        self.plainTextEdit_ver.installEventFilter(self.custom_event_filter) # イベントフィルタをインストール
        self.new_value = pre_value
        self.ver_value = current_value
        col_name = self.main_window.obj_name_to_name_dict[self.line_edit_obj.objectName()]
        self.label_item_name.setText(col_name)
        font = self.label_item_name.font()
        font.setBold(True)
        palette = self.label_item_name.palette()
        palette.setColor(QPalette.ColorRole.Foreground, QColor('red'))
        self.label_item_name.setPalette(palette)
        self.label_item_name.setFont(font)
        self.plainTextEdit_new.setPlainText(self.new_value)
        self.plainTextEdit_ver.setPlainText(self.ver_value)
        self.plainTextEdit_ver.setFocus()
        self.plainTextEdit_ver.moveCursor(QTextCursor.MoveOperation.End) # カーソルを先頭に移動
        # self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint) # クローズボタンを非表示にする
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        x = int(self.main_window.config_dict['collation_dialog_width'])
        y = int(self.main_window.config_dict['collation_dialog_height'])
        self.resize(x, y)
        self.is_close = False
        self.is_not_canceled = False
        self.collation_two_text = CollationTwoText()
        # self.pushButton_set_color.setAutoDefault(False)
        self.plainTextEdit_ver.setFocus()
        self.is_enter_pressed = self.main_window.is_enter_pressed
        self.pushButton_set_color.clicked.connect(self.set_color_to_diff_char)
        self.plainTextEdit_ver.textChanged.connect(self.plaintextedit_changed)

    def set_verified_text_to_line_edit(self): # エンターで確定時の処理
        self.is_not_canceled = True
        # current_text = self.plainTextEdit_new.toPlainText()
        verified_text = self.plainTextEdit_ver.toPlainText()
        # 全角半角変換...
        verified_text = self.main_window.conversion_inputted_text(self.line_edit_obj, verified_text)
        self.main_window.is_enter_pressed = self.is_enter_pressed
        self.main_window.verified_value = verified_text
        # self.line_edit_obj.blockSignals(True)
        self.main_window.deactivate_all_event_filter()
        if self.main_window.radioButton_automove_on.isChecked():
            self.main_window.scrollArea_input_right.setUpdatesEnabled(False)
            self.main_window.scrollArea_input.setUpdatesEnabled(False)
        self.line_edit_obj.setText(verified_text) # ラインエディットに確定値をセット
        if self.main_window.radioButton_automove_on.isChecked():
            QTimer.singleShot(20, lambda: self.main_window.scrollArea_input_right.setUpdatesEnabled(True))
            QTimer.singleShot(20, lambda: self.main_window.scrollArea_input.setUpdatesEnabled(True))
        self.main_window.set_values_pref_city_and_town()
        self.main_window.activate_all_event_filter()
        # self.line_edit_obj.blockSignals(False)
        h = int(self.height())
        w = int(self.width())
        if (int(self.main_window.config_dict['collation_dialog_width']) != w or
                int(self.main_window.config_dict['collation_dialog_height']) != h):
            self.main_window.config_dict['collation_dialog_width'] = w
            self.main_window.config_dict['collation_dialog_height'] = h
            self.main_window.write_config(self.main_window.config_dict)
        self.is_close = True
        self.close()

    def plaintextedit_changed(self): # 色リセットドライバ
        self.plainTextEdit_ver.blockSignals(True)
        self.reset_color_from_char([self.plainTextEdit_ver, self.plainTextEdit_new])
        self.plainTextEdit_ver.blockSignals(False)

    def set_color_to_diff_char(self): # 色セットドライバ
        if self.is_show_dd:
            return
        self.plainTextEdit_ver.blockSignals(True)
        # 別モジュールからの呼び出し...
        new_text = self.plainTextEdit_new.toPlainText()
        ver_text = self.plainTextEdit_ver.toPlainText()
        result_dict = self.collation_two_text.collation_two_text(new_text, ver_text)
        self.reset_color_from_char([self.plainTextEdit_new, self.plainTextEdit_ver]) # 色をリセット
        if not new_text or not ver_text:
            QMessageBox.information(self, '情報', '一次入力、またはベリファイ入力がありません')
            return
        elif new_text == ver_text:
            QMessageBox.information(self, '情報', 'テキストは一致しています')
            return
        else:
            if result_dict is None:
                QMessageBox.information(self, '情報', 'テキストは一致しています')
                return
            original_cursor = self.plainTextEdit_ver.textCursor()
            original_position = original_cursor.position()
            new_indexes = []
            ver_indexes = []
            new_diff = result_dict['new_diff']
            ver_diff = result_dict['ver_diff']
            for new_char in new_diff:
                indexes = [m.start() for m in re.finditer(re.escape(new_char), self.plainTextEdit_ver.toPlainText())]
                for index in indexes:
                    self.set_color_to_char(self.plainTextEdit_ver, index)
            for ver_char in ver_diff:
                indexes = [m.start() for m in re.finditer(re.escape(ver_char), self.plainTextEdit_new.toPlainText())]
                for index in indexes:
                    self.set_color_to_char(self.plainTextEdit_new, index)
            for item in result_dict['normal_and_rev']:
                new_indexes.append(item['new']['index'])
                ver_indexes.append(item['ver']['index'])
            for i, new_index in enumerate(new_indexes):
                self.set_color_to_char(self.plainTextEdit_new, new_index, color_index=i)
            for i, ver_index in enumerate(ver_indexes):
                self.set_color_to_char(self.plainTextEdit_ver, ver_index, color_index=i)
            original_cursor.setPosition(original_position)
            self.plainTextEdit_ver.setTextCursor(original_cursor)
        self.plainTextEdit_new.clearFocus()
        self.plainTextEdit_ver.setFocus()
        self.plainTextEdit_ver.blockSignals(False)

    def set_color_to_char(self, plain_obj, indexes, color_index: int = 2): # 色セットヘルパ
        if indexes is None:
            return
        cursor = plain_obj.textCursor()
        cursor.setPosition(indexes)
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)
        char_format = QTextCharFormat()
        if color_index == 0:
            char_format.setBackground(QColor(255, 0, 0, 70))
        elif color_index == 1:
            char_format.setBackground(QColor(0, 0, 255, 70))
        elif color_index == 2:
            char_format.setBackground(QColor(0, 255, 0, 70))
        cursor.setCharFormat(char_format)
        cursor.clearSelection()

    def reset_color_from_char(self, plain_objs: list): # 色リセットヘルパ
        for plain_obj in plain_objs:
            cursol = plain_obj.textCursor()
            cursol.select(QTextCursor.Document)
            char_format = QTextCharFormat()
            char_format.clearBackground()
            cursol.setCharFormat(char_format)

    def event(self, event):
        # キー押下イベントを処理
        if event.type() == event.KeyPress:
            if event.key() == Qt.Key_Escape:
                # return True  # イベントのデフォルト処理を防ぐ
                pass
            elif event.modifiers() & Qt.KeyboardModifier.AltModifier:
                if event.key() == Qt.Key_F4:
                    pass
        # 他のイベントはデフォルトのイベント処理を行う
        return super().event(event)

    def closeEvent(self, event):
        super().closeEvent(event)

    def reject(self):
        if not self.is_not_canceled:
            self.main_window.is_collation_daialog_canceled = True
        super().reject()
