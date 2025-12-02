# venv : input_img, python version : 3.10.14
import traceback
import unicodedata
from datetime import datetime
import time
import os
from pathlib import Path
import sys
import json
import re

import pandas as pd

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QSharedMemory, QSize, pyqtSignal, QObject, QEvent, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QGraphicsScene, \
    QDialog, QAbstractItemView, QShortcut, QSizePolicy, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPalette, QColor, QTextCursor, QKeySequence, \
    QTextCharFormat


class MyMainWindow(QMainWindow, ):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_vlayout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.central_vlayout)
        self.listwidget = QtWidgets.QListWidget() # listwidget
        self.central_vlayout.addWidget(self.listwidget)
        self.set_listitems()

        self.hlayout_buttons = QtWidgets.QHBoxLayout()
        self.central_vlayout.addLayout(self.hlayout_buttons)
        self.button_test1 = QtWidgets.QPushButton('Test1') # button_test1
        self.hlayout_buttons.addWidget(self.button_test1)

        # self.listwidget.currentItemChanged.connect(self.on_item_clicked)
        # self.listwidget.installEventFilter(self)

        self.button_test1.clicked.connect(self.on_test1_clicked)

    def set_listitems(self):
        self.listwidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        for i in range(10):
            item = QtWidgets.QListWidgetItem(f'item_{i}')
            self.listwidget.addItem(item)

    def on_item_clicked(self, pre_item, next_item):
        try:
            print('pre:', pre_item.text(), 'next ', next_item.text())
        except Exception as e:
            print(f'Error: {e}')

    def on_test1_clicked(self):
        row = self.listwidget.currentRow()
        self.listwidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        next_item = self.listwidget.item(row)
        self.listwidget.setCurrentItem(next_item)
        self.listwidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        selection = self.listwidget.selectedItems()
        if selection:
            for item in selection:
                print('selection[0]', item.text())
        print('Cur Row', self.listwidget.currentItem().text())


    # def eventFilter(self, obj, event):
    #     if obj == self.listwidget and event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonRelease):
    #         # ユーザーのクリック操作を無効化
    #         print("ユーザーのクリック操作を無効化しました")
    #         return True  # イベントを処理済みとして無効化
    #     return super().eventFilter(obj, event)


if __name__  == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())