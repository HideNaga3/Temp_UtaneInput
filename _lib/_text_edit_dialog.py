
import sys
import os
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer, QSharedMemory, QSize, pyqtSignal, QObject, QEvent, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QGraphicsScene, \
    QDialog, QAbstractItemView, QShortcut, QSizePolicy, QMenu, QAction, QGraphicsView, QLineEdit, QListWidgetItem, \
    QTextEdit
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPalette, QColor, QTextCursor, QKeySequence, \
    QTextCharFormat, QBrush, QKeyEvent

from _text_edit_dialog_ui import Ui_MyTextEditDialog

if TYPE_CHECKING:
    from MAIN_APP import MyMainWindow, MainData

class MyTextEditDialog(QDialog, Ui_MyTextEditDialog): # 起動は .exec_() で行う
    def __init__(self, main_window:'MyMainWindow', main_wind_l_edit:QLineEdit):
        super().__init__()
        self.textEdit_main: QTextEdit
        self.label_sub: QTextEdit

        self.main_window = main_window
        self.main_win_l_edit = main_wind_l_edit
        self.setupUi(self)

        # テキストエディットウィジェット

        # font = self.textEdit_main.font()
        # font.setPointSize(12)
        # self.textEdit_main.setFont(font)
        self.main_data_ins = self.main_window.main_data_ins # main_data_ins of MyMainWindow
        self.cur_text = main_wind_l_edit.text()
        self.textEdit_main.setText(self.cur_text) # ラインエディットのテキストをセット
        self.set_text_len() # ラベルの文字数をセット
        cursor = self.textEdit_main.textCursor()
        cursor.setPosition(len(self.cur_text))
        self.textEdit_main.setTextCursor(cursor) # カーソルを最後に移動

        # カスタムフィルタをインストール
        self.custom_filter = MyCustomTextEditFilter(
            text_dialog=self, main_wind_l_edit=self.main_win_l_edit, main_data_ins=self.main_data_ins
        )
        self.textEdit_main.installEventFilter(self.custom_filter)
        self.textEdit_main.textChanged.connect(self.set_text_len)


        try:
            if getattr(sys, 'frozen', False): # 実行ファイルの場合
                application_path = sys._MEIPASS # 実行ファイルのパス
                icon_path = os.path.join(application_path, 'icon.ico')
            else: # スクリプトファイルの場合
                # _libフォルダの親ディレクトリ（プロジェクトルート）を取得
                application_path = os.path.dirname(os.path.dirname(__file__))
                icon_path = os.path.join(application_path, '_icon', 'icon.ico')
            self.setWindowIcon(QIcon(icon_path)) # ウィンドウのアイコンを設定
        except:
            icon_path = None


    def set_text_len(self):
        # テキストが変更されたときの処理
        try:
            text = self.textEdit_main.toPlainText()
            self.label_sub.setText(f'文字数：{len(text)}')
        except Exception as e:
            print('Error in set_text_len of MyTextEditDialog:', e)

class MyCustomTextEditFilter(QObject):
    # テキストエディットウィジェットのフィルタ
    def __init__(
        self, text_dialog: 'Ui_MyTextEditDialog', main_wind_l_edit:QLineEdit, main_data_ins: 'MainData'
    ):
        super().__init__(text_dialog)
        self.text_dialog = text_dialog
        self.text_dialog: Ui_MyTextEditDialog
        self.main_wind_l_edit = main_wind_l_edit
        self.main_data_ins = main_data_ins # メインデータ


    def set_text_to_lineedit(self):
        if not self.main_wind_l_edit:
            return
        text = self.text_dialog.textEdit_main.toPlainText()
        text = re.sub(r'[\r\n\t]', '', text)
        self.main_wind_l_edit.setText(text)
        self.text_dialog.close()


    def insert_char_to_t_edit(self, char):
        # テキストエディットウィジェットに文字を挿入
        t_edit = self.text_dialog.textEdit_main
        pos = t_edit.textCursor().position()
        pre_text = t_edit.toPlainText()
        next_text = pre_text[:pos] + char + pre_text[pos:]
        t_edit.setText(next_text)

        # カーソルを移動
        cursor = t_edit.textCursor()
        cursor.setPosition(pos + len(char))
        t_edit.setTextCursor(cursor)


    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.Type.KeyPress:
            key_event = event
            key_event: QKeyEvent
            key = key_event.key()
            if key in [Qt.Key.Key_Enter, Qt.Key.Key_Return]:
                # Enterキーが押されたときの処理
                self.set_text_to_lineedit()
                # ここにEnterキーが押されたときの処理を追加
                return True
            elif key in [Qt.Key.Key_Tab]:
                # Tabキーが押されたときの処理
                print("Tab key pressed")
                # ここにTabキーが押されたときの処理を追加
                return True
            elif key == Qt.Key.Key_F9:
                self.insert_char_to_t_edit(self.main_data_ins.insert_char_2)
                return True
            elif key == Qt.Key.Key_F10:
                self.insert_char_to_t_edit(self.main_data_ins.insert_char_3)
                return True
            elif key == Qt.Key.Key_F11:
                self.insert_char_to_t_edit(self.main_data_ins.insert_char_1)
                return True

        return False



class MyTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        from MAIN_APP import MainData
        self.main_data_ins = MainData()
        self.main_data_ins.insert_char_1 = '●'
        self.main_data_ins.insert_char_2 = 'これはテストです'
        self.main_data_ins.insert_char_3 = 'こっちもテスト'

        self.frame_1 = QtWidgets.QFrame(self)
        self.layout_1 = QtWidgets.QVBoxLayout(self.frame_1)
        self.button_1 = QtWidgets.QPushButton("Open Text Editor Dialog")
        self.layout_1.addWidget(self.button_1)
        self.setCentralWidget(self.frame_1)

        self.lineedit_1 = QLineEdit()
        self.event_filter = MyTestLineEditFilter(self)
        self.lineedit_1.installEventFilter(self.event_filter)
        self.layout_1.addWidget(self.lineedit_1)

        self.button_1.clicked.connect(self.show_dialog)

    def show_dialog(self):
        self.text_edit_dialog = MyTextEditDialog(self, self.lineedit_1)
        self.text_edit_dialog.exec_()


class MyTestLineEditFilter(QObject):
    def __init__(self, parent):
        super().__init__()
        self.main_window = parent
        self.main_window: MyTestWindow

    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.Type.KeyPress:
            key_event = event
            key_event: QKeyEvent
            if key_event.key() == Qt.Key.Key_F1:
                self.main_window.show_dialog()
                print('F1 key pressed')
                return True
        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyTestWindow()
    window.show()
    sys.exit(app.exec_())