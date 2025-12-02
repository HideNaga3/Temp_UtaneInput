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
        self.vlayout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.vlayout)
        self.listwidget = QtWidgets.QListWidget()

if __name__  == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())