# _event_filters.py
# CustomEventFilterクラス群
# MAIN_APP.pyから分離
#
# 作成日: 2025-10-25
# Phase: CustomEventFilterクラス群の分離（572行）

import time
from typing import List

from PyQt5.QtCore import QObject, QEvent, QTimer, Qt, QPoint
from PyQt5.QtWidgets import QLineEdit, QMenu, QListWidget, QAction
from PyQt5 import QtWidgets, QtCore

from _lib._text_edit_dialog import MyTextEditDialog

# ドロップダウンのショートカットキー
# MAIN_APP.pyと同じ値を使用（循環インポート回避のため再定義）
SHORT_CUT_KEY_DD = Qt.Key.Key_unknown


class CustomEventFilterForGraphicsView(QObject):
    """GraphicsViewのマウスホイールイベントフィルタ

    Ctrl+ホイールで画像のズーム処理を実行します。
    """

    def __init__(self, parent):
        """初期化

        Args:
            parent: MyMainWindowインスタンス
        """
        super().__init__()
        self.main_window = parent

    def eventFilter(self, obj, event):
        """イベントフィルタ

        Ctrl+ホイールイベントをキャプチャしてズーム処理を実行します。
        """
        # ホイールイベントをキャプチャ
        if event.type() == QEvent.Type.Wheel:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                # Ctrl+ホイール操作時はズーム処理を実行
                self.wheelEvent(event)
                return True
        return super().eventFilter(obj, event)

    def wheelEvent(self, event):
        """マウスホイールイベント

        ホイールの方向に応じて画像を拡大・縮小します。
        """
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.main_window.scaling_image(self.main_window.delta_scale, is_button=True)
            else:
                self.main_window.scaling_image(-self.main_window.delta_scale, is_button=True)
            event.accept()


class CustomEventFilterForLineEditScale(QObject):
    """スケール入力用LineEditのイベントフィルタ

    Enterキーでスケール値を確定します。
    """

    def __init__(self, parent):
        """初期化

        Args:
            parent: MyMainWindowインスタンス
        """
        super().__init__()
        self.main_window = parent
        # self.main_window: MyMainWindow  # 型ヒント（循環インポート回避のためコメントアウト）

    def eventFilter(self, obj, event):
        """イベントフィルタ

        Enterキー押下時にスケール値を適用します。
        """
        if event.type() == QEvent.Type.KeyPress and obj == self.main_window.lineEdit_scale:
            if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
                self.main_window.change_scale_on_line_edit()
                return True
        return False


class CustomEventFilterForLineEdit(QObject):
    """通常LineEditのイベントフィルタ

    データ入力用LineEditの複雑なイベント処理を担当します。
    フォーカスイン/アウト、Enterキー、Tab、ショートカットキーなど。
    """

    def __init__(self, parent, line_widget_obj):
        """初期化

        Args:
            parent: MyMainWindowインスタンス
            line_widget_obj: 対象のLineEditオブジェクト
        """
        super().__init__()
        self.main_window = parent
        # self.main_window: MyMainWindow  # 型ヒント（循環インポート回避のためコメントアウト）
        self.recieved_line_widget_obj = line_widget_obj
        self.focus_out_line_widget_obj = None
        self.focus_in_line_widget_obj = None
        self.is_event_filter_activated = True
        self.is_enter_pressed = False
        self.is_enter_pressed_2 = False
        self.previous_focus_in_line_widget_obj_name = None
        self.is_focus_out_event_executing = False
        self.char_for_conv = self.main_window.config_dict['insert_char']
        self.char_for_conv_2 = self.main_window.config_dict['insert_char2']
        self.char_for_conv_3 = self.main_window.config_dict['insert_char3']
        self.init_flags()

    def pr(self, *args, **kwargs):
        """デバッグ用プリント関数"""
        if not self.main_window.is_frozen:
            if args:
                print(args)
            if kwargs:
                print(kwargs)

    def init_flags(self):
        """フラグの初期化"""
        self.is_enter_pressed = False
        self.is_tab_pressed = False
        self.is_focus_out = False
        self.focus_out_line_widget_obj = None
        self.focus_in_line_widget_obj = None
        self.value_on_focus_in = None

    def init_main_window_flags(self):
        """メインウィンドウのフラグを初期化"""
        self.main_window.is_enter_pressed = False
        self.main_window.is_tab_pressed = False
        self.main_window.is_focus_out = False
        self.main_window.is_left_button_clicked_and_so_on = False
        self.main_window.focus_out_line_widget_obj = None
        self.value_on_focus_in = None

    def send_flags_to_main_window_on_focus_in(self):
        """フラグをメインウィンドウにセット（フォーカスアウト時）"""
        self.main_window.is_enter_pressed = self.is_enter_pressed
        self.main_window.is_tab_pressed = self.is_tab_pressed
        self.main_window.is_focus_out = self.is_focus_out
        self.main_window.focus_out_line_widget_obj = self.focus_out_line_widget_obj

    def enter_key_pressed_event(self, line_widget_obj):
        """エンターキーが押された場合の処理（メイン関数）"""
        # print('\n\n\n開始 エンターキーイベント')
        entered_obj = line_widget_obj
        self.main_window.focus_out_line_widget_obj_for_set_rect = entered_obj
        self.main_window.focus_in_line_widget_obj = entered_obj
        self.is_enter_pressed = True
        is_enter_pressed = True
        self.main_window.focus_in_line_widget_obj_buf_for_enter = self.main_window.focus_in_line_widget_obj
        if self.main_window.is_in_close_processing or self.main_window.is_show_init_dialog:
            return
        if self.main_window.radioButton_automove_on.isChecked():
            self.main_window.scrollArea_input_right.setUpdatesEnabled(False)
            self.main_window.scrollArea_input.setUpdatesEnabled(False)
        self.focus_out_line_widget_obj = line_widget_obj
        self.main_window.focus_out_line_widget_obj = line_widget_obj
        self.is_focus_out = True
        self.deactivate_all_event_filter()
        current_index = self.main_window.obj_name_to_index_dict[line_widget_obj.objectName()]
        is_last_line_edit = False
        if current_index == len(self.main_window.data_list) - 1:
            current_index = -1
            is_last_line_edit = True
            self.main_window.is_last_enter_pressed = True
        if not self.main_window.is_last_enter_canceled:
            self.main_window.next_line_edit(current_index)
        self.focus_out_event(line_widget_obj)
        # print('開始 ____エンターフォーカスインイベント')
        self.focus_in_event(is_enter_pressed=is_enter_pressed, entered_obj=entered_obj)
        if self.main_window.radioButton_automove_on.isChecked():
            self.main_window.graphicsView_main.setUpdatesEnabled(False)
        # print('終了 ____エンターフォーカスインイベント')
        def set_false_to_last_enter_var():
            self.main_window.is_last_enter_pressed = False
            self.main_window.is_last_enter_canceled = False
        QTimer.singleShot(0, set_false_to_last_enter_var)
        # print('終了 エンターキーイベント\n\n\n')
        if self.main_window.radioButton_automove_on.isChecked():
            if is_last_line_edit:
                QTimer.singleShot(100, lambda: self.main_window.graphicsView_main.setUpdatesEnabled(True))
            else:
                QTimer.singleShot(0, lambda: self.main_window.graphicsView_main.setUpdatesEnabled(True))
        if self.main_window.radioButton_automove_on.isChecked():
            QTimer.singleShot(20, lambda: self.main_window.scrollArea_input_right.setUpdatesEnabled(True))
            QTimer.singleShot(20, lambda: self.main_window.scrollArea_input.setUpdatesEnabled(True))
        self.activate_all_event_filter()

    def focus_out_event(self, focus_out_obj):
        """フォーカスアウト時の処理"""
        if self.main_window.is_initialaized:
            return
        self.main_window.focus_out_obj_for_list_check = focus_out_obj
        self.main_window.focus_out_obj_for_collation = focus_out_obj
        current_time = time.time()
        if current_time - self.main_window.last_executing_time_of_focus_out_event < 0.05:
            # print('!!!!!!!!!! リターンフォーカスアウト !!!!!!!!!!!')
            # print('フォーカスアウトtime', round(current_time - self.main_window.last_executing_time_of_focus_out_event, 6))
            return
        else:
            pass
        self.main_window.last_executing_time_of_focus_out_event = current_time
        if self.is_focus_out_event_executing == True:
            return
        self.is_focus_out_event_executing = True
        self.deactivate_all_event_filter()
        self.send_flags_to_main_window_on_focus_in()
        self.main_window.do_event_of_line_edit_focus_out()
        self.init_flags()
        self.init_main_window_flags()
        if self.main_window.list_widget_dd:
            self.main_window.list_widget_dd.close()
        self.activate_all_event_filter()
        self.is_focus_out_event_executing = False

    def focus_in_event(self, is_enter_pressed=False, entered_obj = None, target_line_edit_obj = None):
        """フォーカスイン時の処理"""
        if self.main_window.pixmap_item is not None:
            self.main_window.pixmap_item.delete_sub_rect()
        if self.main_window.is_show_collation_dialog_on_last_and_rept_in_type_check == True:
            self.main_window.is_show_collation_dialog_on_last_and_rept_in_type_check = False
            # print('!!!!!!!!!! リターンフォーカスイン collation !!!!!!!!!!!')
            return
        # print('____開始 フォーカスインイベント____')
        current_time = time.time()
        if current_time - self.main_window.last_executing_time_of_focus_in_event < 0.1:
            # print('!!!!!!!!!! リターンフォーカスイン time !!!!!!!!!!!')
            # print('フォーカスインtime', round(current_time - self.main_window.last_executing_time_of_focus_in_event, 6))
            return
        else:
            # print('____フォーカスイン実行')
            pass
        target_line_edit_obj = self.main_window.get_focused_line_edit_obj()
        def _set_ensure(target_line_edit_obj):
            if target_line_edit_obj is None:
                return
            if self.main_window.scrollArea_input.isVisible() and target_line_edit_obj is not None:
                self.main_window.scrollArea_input.ensureWidgetVisible(target_line_edit_obj.parentWidget(), xMargin=-100000, yMargin=0)
            elif self.main_window.scrollArea_input_right.isVisible() and target_line_edit_obj is not None:
                self.main_window.scrollArea_input_right.ensureWidgetVisible(target_line_edit_obj.parentWidget(), xMargin=-100000 , yMargin=0)
        QTimer.singleShot(50, lambda obj=target_line_edit_obj: _set_ensure(obj))
        if self.main_window.list_widget_dd:
            self.main_window.list_widget_dd.close()
            self.main_window.list_widget_dd = None
        # QTimer.singleShot(0, lambda: self.main_window.show_dd_list_widget(self.main_window.get_focused_line_edit_obj()))
        self.main_window.last_executing_time_of_focus_in_event = current_time
        self.deactivate_all_event_filter()
        if not is_enter_pressed:
            self.focus_in_line_widget_obj = self.recieved_line_widget_obj
        else:
            try:
                index = self.main_window.obj_name_to_index_dict[self.recieved_line_widget_obj.objectName()]
            except Exception as e:
                return
            if not self.main_window.data_list:
                return
            if index != len(self.main_window.data_list) - 1:
                self.focus_in_line_widget_obj = self.main_window.data_list[index + 1]['line_edit_obj']
            else:
                if not self.main_window.is_rept_mode:
                    self.focus_in_line_widget_obj = self.main_window.data_list[0]['line_edit_obj']
                else:
                    self.focus_in_line_widget_obj = self.recieved_line_widget_obj
        self.main_window.focus_in_line_widget_obj = self.focus_in_line_widget_obj
        self.previous_focus_in_line_widget_obj_name = self.focus_in_line_widget_obj.objectName()

        ime_mode = self.main_window.obj_name_to_ime_dict[self.focus_in_line_widget_obj.objectName()]
        self.main_window.set_ime_from_ime_mode_text(ime_mode)
        self.value_on_focus_in = self.focus_in_line_widget_obj.text()
        self.main_window.value_on_focus_in = self.value_on_focus_in
        if self.main_window.radioButton_automove_on.isChecked() and not self.main_window.is_last_enter_canceled:
            # >> 最後のエンターが実行されたときの処理
            if self.main_window.is_rept_mode:
                if is_enter_pressed:
                    pass
                    if self.main_window.focus_out_line_widget_obj_for_set_rect.objectName() == self.main_window.last_input_line_widget.objectName():
                        arg_obj = self.main_window.first_rept_line_widget_obj
                        def _set_rect_1(arg_obj):
                            self.main_window.pixmap_item.set_rect(current_focus_in_obj=arg_obj)
                        QTimer.singleShot(50, lambda: _set_rect_1(arg_obj))
                    else:
                        arg_obj = self.focus_in_line_widget_obj
                        def _set_rect_2():
                            self.main_window.pixmap_item.set_rect()
                        QTimer.singleShot(50, lambda: _set_rect_2())
                else:
                    def _set_rect_3():
                        if self.main_window.pixmap_item is not None \
                                and not self.main_window.is_show_type_error_for_rect:
                            self.main_window.pixmap_item.set_rect()
                    QTimer.singleShot(50, lambda: _set_rect_3())
            else:
                def _set_rect_4():
                    if self.main_window.pixmap_item is not None:
                        self.main_window.pixmap_item.set_rect()
                QTimer.singleShot(50, lambda: _set_rect_4())
        elif self.main_window.is_last_enter_canceled and self.main_window.radioButton_automove_on.isChecked():
            # 最後のエンターキャンセル時の処理...
            def _set_rect_5():
                self.main_window.pixmap_item.set_rect(index=len(self.main_window.data_list) - 1)
                self.main_window.is_last_enter_canceled = False
            QTimer.singleShot(50, lambda: _set_rect_5())
        # 最後のエンターが実行されたときの処理 <<
        # >> 情報ラベルに各フィールドの情報を表示
        if not self.main_window.is_last_enter_canceled:
            focus_in_obj = self.main_window.get_focused_line_edit_obj()
            if focus_in_obj is not None:
                info = self.main_window.obj_name_to_info_dict[focus_in_obj.objectName()]
                self.main_window.label_infomation.setText(info.replace('\n', ', '))
                self.main_window.label_infomation_right.setText(info)
        self.main_window.is_not_set_sub_rect = False
        self.activate_all_event_filter()
        # print('____終了 フォーカスインイベント____')

    def activate_all_event_filter(self):
        """全イベントフィルタをアクティブ化"""
        for event_filter in self.main_window.event_filter_dict.values():
            event_filter.is_event_filter_activated = True

    def deactivate_all_event_filter(self):
        """全イベントフィルタを非アクティブ化"""
        for event_filter in self.main_window.event_filter_dict.values():
            event_filter.is_event_filter_activated = False

    def eventFilter(self, obj, event):
        """イベントフィルタ

        キー押下、フォーカスイン/アウト、マウスクリックなどの
        各種イベントを処理します。
        """
        if self.is_event_filter_activated and not self.main_window.is_initialaized:
            # LineEditが右クリックされた場合
            if event.type() == QEvent.ContextMenu and obj == self.recieved_line_widget_obj:
                self.show_context_menu(event.globalPos())
                return True
            if event.type() == QEvent.Type.KeyPress:
                if event.key() == Qt.Key.Key_Tab or event.key() == Qt.Key.Key_Backtab:
                    if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                        self.is_tab_pressed = True
                    else:
                        self.is_tab_pressed = True
                elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                    if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                        pass
                    else:
                        self.is_enter_pressed = True
                        self.enter_key_pressed_event(self.recieved_line_widget_obj)
                elif event.key() == Qt.Key.Key_A:
                    if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                        self.main_window.scroll_to_position(self.main_window.graphicsView_main, 'left')
                        return True
                elif event.key() == Qt.Key.Key_F9:
                    if self.main_window.main_mode in ['factory']:
                        self.insert_char_to_line_edit(obj, self.char_for_conv_2, self.main_window.target_lineedit_for_insert_char_list)
                    else:
                        self.insert_char_to_line_edit(obj, self.char_for_conv)
                    return True
                elif event.key() == Qt.Key.Key_F10:
                    if self.main_window.main_mode in ['factory']:
                        self.insert_char_to_line_edit(obj, self.char_for_conv_3, self.main_window.target_lineedit_for_insert_char_list)
                    return True
                elif event.key() == Qt.Key.Key_F11:
                    if self.main_window.main_mode in ['factory']:
                        self.insert_char_to_line_edit(obj, self.char_for_conv)
                    return True
                elif event.key() == Qt.Key.Key_F1:
                    if self.main_window.main_mode in ['factory']:
                        if self.main_window.target_lineedit_for_text_dialog_list:
                            obj_names = [obj.objectName() for obj in self.main_window.target_lineedit_for_text_dialog_list]
                            if obj.objectName() in obj_names:
                                self.text_edit_dialog = MyTextEditDialog(self.main_window, obj)
                                self.text_edit_dialog.exec_()
                    return True
                elif event.key() == Qt.Key.Key_Up:
                    self.select_previous_line_obj(obj)
                    self.main_window.scrollArea_input_right.ensureWidgetVisible(obj)
                    self.main_window.scrollArea_input.ensureWidgetVisible(obj)
                    return True
                elif event.key() == SHORT_CUT_KEY_DD:
                    self.main_window.show_dd_list_widget(self.recieved_line_widget_obj)
                    return True
            # 2. フォーカスインイベントの場合...
            elif event.type() == QEvent.Type.FocusIn:
                # print('____開始 通常のフォーカスインイベント')
                self.focus_in_event(target_line_edit_obj = obj)

                # print('____終了 通常のフォーカスインイベント\n------')
            # 3. フォーカスアウトイベントの場合...
            elif event.type() == QEvent.Type.FocusOut:
                self.is_focus_out = True
                self.focus_out_line_widget_obj = self.recieved_line_widget_obj
                if self.main_window.is_focus_out_allowed:
                    # print('開始 普通のフォーカスアウトイベント')
                    self.focus_out_event(obj)
                    # print('終了 普通のフォーカスアウトイベント\n------')
            # 4. マウスボタンプレスイベントの場合...
            elif event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    # self.main_window.show_dd_list_widget(self.main_window.get_focused_line_edit_obj())
                    pass
        return super().eventFilter(obj, event)

    def select_previous_line_obj(self, current_obj):
        """上のLineEditにフォーカスを移動"""
        current_obj_name = current_obj.objectName()
        current_index = self.main_window.obj_name_to_index_dict[current_obj_name]
        if current_index == 0:
            return
        i = 0
        while True:
            i += 1
            previous_index = current_index - i
            previous_obj = self.main_window.data_list[previous_index]['line_edit_obj']
            if previous_index <= 0:
                break
            previous_obj_name = previous_obj.objectName()
            types = self.main_window.main_data_dict[previous_obj_name]['data_type'].split('_')
            if 'noedit' in types:
                continue
            is_show =self.main_window.main_data_dict[previous_obj_name]['is_show']
            if not is_show:
                continue
            break
        previous_obj.setFocus()

    def insert_char_to_line_edit(self, obj: QLineEdit, insert_char: str, target_lineedit_list: List[QLineEdit] = None):
        """LineEditに特殊文字を挿入

        Args:
            obj: 対象のLineEdit
            insert_char: 挿入する文字
            target_lineedit_list: 対象LineEditのリスト（Noneの場合は全て）
        """
        if target_lineedit_list:
            target_lineedit_names = [obj.objectName() for obj in target_lineedit_list]
            if not obj.objectName() in target_lineedit_names:
                return
        current_text = obj.text()
        pos = obj.cursorPosition()
        new_text = current_text[:pos] + insert_char + current_text[pos:]
        obj.blockSignals(True)
        obj.setText(new_text)
        obj.setCursorPosition(pos + len(insert_char))
        obj.blockSignals(False)

    def show_context_menu(self, pos):
        """コンテキストメニューを表示（現在は無効化）"""
        return
        # コンテキストメニューを作成
        self.main_window.deactivate_all_event_filter()
        context_menu = QMenu(self.recieved_line_widget_obj)
        # リストアイテムのアクションを追加
        items = ["Test item 1", "Test item 2", "Test item 3"]
        for item in items:
            action = QAction(item, self.recieved_line_widget_obj)
            action.triggered.connect(lambda _, item=item: self.recieved_line_widget_obj.setText(item))
            context_menu.addAction(action)
        # メニューを表示
        context_menu.exec_(pos)
        self.main_window.activate_all_event_filter()


class CustomEventFilterForPlaneTextEdit(QObject):
    """PlainTextEditのイベントフィルタ

    CollationDialog内のPlainTextEdit用のイベント処理を担当します。
    """

    def __init__(self, parent: 'CollationDialog', main_window):
        """初期化

        Args:
            parent: CollationDialogインスタンス
            main_window: MyMainWindowインスタンス
        """
        super().__init__()
        self.collation_dialog = parent
        self.current_lineedit = self.collation_dialog.line_edit_obj
        self.main_window = main_window
        self.char_for_conv = self.main_window.config_dict['insert_char']
        self.list_widget_dd = None

    def set_black_round_to_line_edit(self, obj: QtWidgets.QPlainTextEdit):
        """PlainTextEditに黒丸を挿入

        Args:
            obj: 対象のPlainTextEdit
        """
        current_text = obj.toPlainText()
        cursor = obj.textCursor()
        pos = cursor.position()
        new_text = current_text[:pos] + self.char_for_conv + current_text[pos:]
        obj.blockSignals(True)
        obj.setPlainText(new_text)
        cursor.setPosition(pos + 1)
        obj.setTextCursor(cursor)
        obj.blockSignals(False)

    def eventFilter(self, obj, event):
        """イベントフィルタ

        Enterキー、Tab、F9、ドロップダウン表示などを処理します。
        """
        if event.type() == QEvent.FocusOut:
            pass
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                self.collation_dialog.set_verified_text_to_line_edit()
                return True
            elif event.key() == Qt.Key.Key_Tab:
                    self.collation_dialog.focusPreviousChild()
                    return True
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                if event.key() == Qt.Key.Key_Tab or event.key() == Qt.Key.Key_Backtab:
                    obj.parentWidget().focusNextChild()
                    return True
            if event.key() == Qt.Key.Key_F9:
                self.set_black_round_to_line_edit(obj)
                return True
            elif event.key() == SHORT_CUT_KEY_DD:
                self.show_dd_list_widget_collation()
                return True
        return super().eventFilter(obj, event)

    def show_dd_list_widget_collation(self):
        """ドロップダウンリストを表示"""
        if self.current_lineedit is None:
            return
        line_type = self.main_window.obj_name_to_type_dict[self.current_lineedit.objectName()]
        if not 'list' in line_type:
            return
        self.collation_dialog.is_show_dd = True
        current_text = self.current_lineedit.text()
        if self.list_widget_dd is not None:
            self.list_widget_dd.clear()
            self.list_widget_dd.close()
            self.list_widget_dd = None
        self.list_widget_dd = QtWidgets.QListWidget(self.collation_dialog)
        self.event_filter_for_dd = CustomEventFilterForDD(self, self.list_widget_dd, self.current_lineedit)
        self.list_widget_dd.installEventFilter(self.event_filter_for_dd)
        self.list_widget_dd.itemClicked.connect(self.activated_dd_list_widget_collation)
        self.list_widget_dd.itemActivated.connect(self.activated_dd_list_widget_collation)
        line_width = self.collation_dialog.plainTextEdit_ver.width()
        line_height = self.collation_dialog.plainTextEdit_ver.height()
        self.list_widget_dd.clear()
        # >> フォント設定
        font = self.list_widget_dd.font()
        font.setPointSize(11)
        font.setFamily("BIZ UDゴシック")
        self.list_widget_dd.setFont(font)
        # フォント設定 <<
        dd_items = self.main_window.obj_name_to_list_item_dict[self.current_lineedit.objectName()].copy()
        init_index = dd_items.index(current_text) if current_text in dd_items else 0
        dd_items.append('空欄')
        dd_items.append('キャンセル')
        self.list_widget_dd.addItems(dd_items)
        for i in range(self.list_widget_dd.count()):
            item = self.list_widget_dd.item(i)
            item_font = item.font()
            item_font.setPointSize(11)
            item_font.setFamily("BIZ UDゴシック")
            item.setFont(item_font)
        item_height = self.list_widget_dd.sizeHintForRow(0)
        row_count = len(dd_items) + 2
        self.list_widget_dd.setMinimumSize(line_width, item_height * row_count)
        self.list_widget_dd.setMaximumSize(line_width, item_height * row_count)
        self.plain_textedit = self.collation_dialog.plainTextEdit_ver
        self.list_widget_dd.setWindowFlags(Qt.WindowType.Popup)
        self.list_widget_dd.show()
        self.list_widget_dd.setFocus()
        self.list_widget_dd.setCurrentRow(init_index)
        item_height = self.list_widget_dd.sizeHintForRow(0)
        row_count = self.list_widget_dd.count()
        global_pos = self.collation_dialog.plainTextEdit_ver.mapToGlobal(QtCore.QPoint(0, 0))
        self.list_widget_dd.setGeometry(global_pos.x(), global_pos.y(), line_width, int(item_height * (row_count + 1)))


    def activated_dd_list_widget_collation(self, item):
        """ドロップダウンリストのアイテムが選択されたときの処理

        Args:
            item: 選択されたQListWidgetItem
        """
        row = self.list_widget_dd.row(item)
        if row == self.list_widget_dd.count() - 2:
            self.plain_textedit.setPlainText('')
        elif row == self.list_widget_dd.count() - 1:
            pass
        else:
            self.plain_textedit.setPlainText(item.text())
        self.list_widget_dd.close()
        self.plain_textedit.setFocus()
        self.list_widget_dd = None
        def _set_false_to_is_show_dd():
            self.collation_dialog.is_show_dd = False
        QTimer.singleShot(0, lambda: _set_false_to_is_show_dd())


class CustomEventFilterForDD(QObject):
    """ドロップダウンリストのイベントフィルタ"""

    def __init__(self, main_window, parent, focused_line_edit_obj):
        """初期化

        Args:
            main_window: MyMainWindowインスタンス（または親オブジェクト）
            parent: ドロップダウンリストの親ウィジェット
            focused_line_edit_obj: フォーカスのあるLineEdit
        """
        super().__init__()
        self.main_window = main_window
        # self.main_window: MyMainWindow  # 型ヒント（循環インポート回避のためコメントアウト）
        self.focused_line_edit_obj = focused_line_edit_obj
        self.parent_widget = parent

    def eventFilter(self, obj, event):
        """イベントフィルタ

        Escapeキーでドロップダウンを閉じます。
        """
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Escape:
                try:
                    self.main_window.deactivate_all_event_filter()
                except AttributeError as e:
                    print('CustomEventFilterForDD eventFilter()\n', e)
                self.focused_line_edit_obj.setFocus()
                try:
                    self.main_window.activate_all_event_filter()
                except AttributeError as e:
                    print('CustomEventFilterForDD eventFilter()\n', e)
                self.parent_widget.close()
                self.parent_widget= None
        return super().eventFilter(obj, event)


class CustomEventFilterForButtonScrollArea(QObject):
    """スクロールエリア内のボタン用イベントフィルタ

    PageUp/PageDownキーでPDFページ切り替えを行います。
    """

    def __init__(self, parent):
        """初期化

        Args:
            parent: MyMainWindowインスタンス
        """
        super().__init__()
        self.main_window = parent
        # self.main_window: MyMainWindow  # 型ヒント（循環インポート回避のためコメントアウト）

    def eventFilter(self, obj, event):
        """イベントフィルタ

        PageUp/PageDownキーでページを切り替えます。
        """
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_PageUp:
                self.main_window.select_item_for_list_widget_for_pdf(-1)
                return True
            elif event.key() == Qt.Key.Key_PageDown:
                self.main_window.select_item_for_list_widget_for_pdf(1)
                return True
        return False
