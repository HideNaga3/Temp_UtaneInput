import sys
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow, \
    QFrame
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path

class CustomVLayoutList(QVBoxLayout):
    def __init__(self, main_window, dir_path: str):
        super().__init__()
        self.main_window = main_window
        self.dir_path = dir_path
        self.dobj = Path(dir_path).resolve()
        if not self.dobj.exists():
            raise FileNotFoundError(f"Directory {self.dobj} does not exist.")

        self.add_item()

    def add_item(self):
        if not self.dobj.exists():
            self.dobj = Path("../SampleImg").resolve()
        img_fobjs = [fobj for fobj in self.dobj.iterdir() if fobj.suffix.lower() in ['.png', '.jpg', '.jpeg']]
        if len(img_fobjs) == 0:
            raise FileNotFoundError
        self.widgets = []
        for fobj in img_fobjs:

            img_fp = str(fobj)
            img_fn = fobj.name
            if not fobj.exists():
                raise FileNotFoundError
            custom_widget = CustomWidgetForListItem(img_fp, img_fn, 200, 200) # インスタンス作成
            self.addWidget(custom_widget) # レイアウトにカスタムウィジェットを追加
            custom_widget.pushButton_up.clicked.connect(
                    lambda _, w=custom_widget: self.swap_item(self.widgets.index(w), self.widgets.index(w) - 1)
            )
            custom_widget.pushButton_down.clicked.connect(
                    lambda _, w=custom_widget: self.swap_item(self.widgets.index(w), self.widgets.index(w) + 1)
            )
            self.widgets.append(custom_widget)

    def swap_item(self, index1, index2):
        if index2 < 0 or index2 >= len(self.widgets):
            return
        # リスト内でウィジェットを入れ替える
        if index1 > index2:
            widget1 = self.widgets.pop(index1)
            self.widgets.insert(index2, widget1)
            widget2 = self.widgets[index1]
        else:
            widget2 = self.widgets.pop(index2)
            self.widgets.insert(index1, widget2)
            widget1 = self.widgets[index2]
        # レイアウトでの位置を更新
        if index1 > index2:
            self.removeWidget(widget1)
            self.removeWidget(widget2)
            self.insertWidget(index2, widget1)
            self.insertWidget(index1, widget2)
        else:
            self.removeWidget(widget2)
            self.removeWidget(widget1)
            self.insertWidget(index1, widget2)
            self.insertWidget(index2, widget1)

class CustomWidgetForListItem(QWidget):
    def __init__(self, file_path: str, file_name: str, w:int=100 , h:int=100):
        super().__init__()
        self.file_name = file_name
        self.file_path = file_path
        self.w = w
        self.h = h
        self.set_ui()
        self.setLayout(self.main_horizontalLayout)
        self.label_fn.setText(self.file_name)
        QTimer.singleShot(0, self.set_pixmap)

    def set_pixmap(self):
        pixmap = QPixmap(self.file_path)
        if '画像1.png' in self.file_path:
            pass
        label_w = self.label_img.size().width()
        label_h = self.label_img.size().height()
        pix_w = pixmap.width()
        pix_h = pixmap.height()
        if label_w < pix_w:
            w = pix_w * label_w // pix_w
            h = pix_h * label_w // pix_w
        else:
            w = pix_w
            h = pix_h
        scaled_pixmap = pixmap.scaled(int(w), int(h))
        if label_h < h:
            h = pix_h * label_h // pix_h
            w = pix_w * label_h // pix_h
        scaled_pixmap = pixmap.scaled(int(w), int(h))
        if w > label_w or h > label_h:
            pass
        self.label_img.setPixmap(scaled_pixmap)

    def set_ui(self):
        font = QtGui.QFont()
        font.setFamily("BIZ UDゴシック")
        self.main_horizontalLayout = QtWidgets.QHBoxLayout()
        self.main_horizontalLayout.setGeometry(QtCore.QRect(10, 40, 361, 201))
        self.main_horizontalLayout.setObjectName("main_horizontalLayout")
        self.main_frame = QFrame()
        self.main_horizontalLayout.addWidget(self.main_frame)
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.main_frame.setLayout(self.horizontalLayout_1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout")
        self.frame_1 = QtWidgets.QFrame()
        self.frame_1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_1.setObjectName("frame_1")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.frame_1)
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.label_img = QtWidgets.QLabel(self.frame_1)
        self.label_img.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.label_img.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.label_img.setObjectName("label_img")
        self.label_img.setMinimumSize(QtCore.QSize(self.w, self.h)) # サイズ
        self.label_img.setMaximumSize(QtCore.QSize(self.w, self.h))
        self.verticalLayout_1.addWidget(self.label_img)
        self.label_fn = QtWidgets.QLabel(self.frame_1)
        self.label_fn.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.label_fn.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.label_fn.setObjectName("label_text")
        self.label_fn.setMinimumWidth(self.w)
        self.label_fn.setMaximumWidth(self.w)
        self.verticalLayout_1.addWidget(self.label_fn)
        self.frame_2 = QtWidgets.QFrame()
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(50, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_up = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_up.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_up.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_up.setObjectName("pushButton_up")
        self.verticalLayout_2.addWidget(self.pushButton_up)
        self.pushButton_down = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_down.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_down.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_down.setObjectName("pushButto_down")
        self.verticalLayout_2.addWidget(self.pushButton_down)
        self.label_img.setText("ImgLabel")
        self.label_fn.setText("TextLabel")
        self.pushButton_up.setText("↑")
        self.pushButton_down.setText("↓")
        self.horizontalLayout_1.addWidget(self.frame_1)
        self.horizontalLayout_1.addWidget(self.frame_2)
        self.verticalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.main_horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.main_horizontalLayout.setSpacing(0)
        self.horizontalLayout_2.setSpacing(0)
        self.verticalLayout_1.setStretch(0, 1)
        self.verticalLayout_1.setSpacing(0)
        self.verticalLayout_1.setSpacing(0)
        self.horizontalLayout_1.setSpacing(0)
        self.horizontalLayout_1.setContentsMargins(0, 0, 0, 0)

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QHBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.scrollarea = QtWidgets.QScrollArea(self.central_widget)
        self.scrollarea.setFrameShape(QFrame.Shape.Box)
        self.scrollarea.setFrameShadow(QFrame.Shadow.Raised)
        self.scrollwidget = QWidget()
        self.scrollarea.setWidget(self.scrollwidget)
        self.scrollarea.setWidgetResizable(True)
        self.central_layout.addWidget(self.scrollarea)
        self.vlayout_list = CustomVLayoutList(self, "../SampleImg")
        self.vlayout_list.setSpacing(0)
        self.scrollwidget.setLayout(self.vlayout_list)
        self.tree_layout = QVBoxLayout()
        self.central_layout.addLayout(self.tree_layout)
        self.treeview = QtWidgets.QTreeView()
        self.tree_layout.addWidget(self.treeview)
        self.button_layout = QHBoxLayout()
        self.central_widget.setLayout(self.button_layout)
        self.button_test_1 = QPushButton("Test1")
        self.central_layout.addWidget(self.button_test_1)
        self.button_test_1.clicked.connect(self.test_1)
        self.set_tree()

    def set_tree(self):
        self.model = QtGui.QStandardItemModel()
        self.treeview.setModel(self.model)
        self.item_a = QtGui.QStandardItem("Item A")
        self.item_b = QtGui.QStandardItem("Item B")
        self.item_a.appendRow(self.item_b)
        self.model.appendRow(self.item_a)

    def test_1(self):
        print(len(self.vlayout_list.widgets))
        for w in self.vlayout_list.widgets:
            w: CustomWidgetForListItem
            print(w.file_name, w.file_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())