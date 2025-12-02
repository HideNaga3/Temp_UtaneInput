# venv : input_img, python version : 3.10.14
import traceback
import unicodedata
from datetime import datetime
import time
import os
from pathlib import Path
import sys
from dataclasses import dataclass, field


import pandas as pd

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QSharedMemory, QSize, pyqtSignal, QObject, QEvent, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QGraphicsScene, \
    QDialog, QAbstractItemView, QShortcut, QSizePolicy, QMenu, QAction, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPalette, QColor, QTextCursor, QKeySequence, \
    QTextCharFormat, QPainter

@dataclass
class ResultData:
    combined_pixmap: QPixmap = None
    w: int = 0
    h: int = 0


def combine_pixmaps_w(pixmaps: list[QPixmap]) -> ResultData:
    w, h = 0, 0
    for cur_pixmap in pixmaps:
        w = w + cur_pixmap.width()
        h = max(h, cur_pixmap.height())
    combined_pixmap = QPixmap(w, h)
    combined_pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(combined_pixmap) # ペインターを作成
    cur_w = 0
    previous_pixmap = None
    for cur_pixmap in pixmaps:
        if not previous_pixmap:
            cur_w = 0
        else:
            cur_w = cur_w + previous_pixmap.width()
        painter.drawPixmap(cur_w, 0, cur_pixmap) # ペインターで描画
        previous_pixmap = cur_pixmap
    painter.end()
    return ResultData(combined_pixmap=combined_pixmap , w=w, h=h)

def combine_pixmaps_h(pixmaps: list[QPixmap]) -> ResultData:
    w, h = 0, 0
    for cur_pixmap in pixmaps:
        w = max(w, cur_pixmap.width())
        h += cur_pixmap.height()
    combined_pixmap = QPixmap(w, h)
    combined_pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(combined_pixmap) # ペインターを作成
    cur_h = 0
    previous_pixmap = None
    for cur_pixmap in pixmaps:
        if not previous_pixmap:
            cur_h = 0
        else:
            cur_h = cur_h + previous_pixmap.height()
        painter.drawPixmap(0, cur_h, cur_pixmap) # ペインターで描画
        previous_pixmap = cur_pixmap
    painter.end()
    return ResultData(combined_pixmap=combined_pixmap , w=w, h=h)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.vlayout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.vlayout)
        img_pobj_1 = Path('./SampleImg/rock.png').resolve()
        img_pobj_2 = Path('./SampleImg/player.png').resolve()
        if not img_pobj_1.exists() or not img_pobj_2.exists():
            raise('not found')
        self.pixmap_1 = QPixmap(str(img_pobj_1))
        self.pixmap_2 = QPixmap(str(img_pobj_2))
        self.pixmaps = [self.pixmap_1, self.pixmap_2]

        # 関数に切り出し
        result = combine_pixmaps_h(self.pixmaps)
        self.combined_pixmap, w, h = result.combined_pixmap, result.w, result.h
        # ここまで関数切り出し

        self.pixmap_item = QGraphicsPixmapItem(self.combined_pixmap)
        self.graphics_view = QGraphicsView(self)
        # シーンを作成
        self.scene = QGraphicsScene(self)
        self.scene.addItem(self.pixmap_item) # シーンにアイテムを追加
        self.scene.setBackgroundBrush(QColor(0, 255, 255))
        self.scene.setSceneRect(0, 0, w, h)

        self.graphics_view.setScene(self.scene)
        self.graphics_view.setSceneRect(0, 0, w, h) # シーンのサイズを設定
        self.vlayout.addWidget(self.graphics_view)



if __name__  == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())