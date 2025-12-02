import sys
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path


class CustomWidgetForListItem(QWidget):
    def __init__(self, file_path, file_name):
        super().__init__()
        self.file_name = file_name
        self.file_path = file_path
        self.set_ui()
        self.setLayout(self.horizontalLayoutWidget)
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
        self.horizontalLayoutWidget = QtWidgets.QHBoxLayout()
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 40, 361, 201))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_1 = QtWidgets.QFrame()
        self.frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setObjectName("frame_1")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.frame_1)
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.label_img = QtWidgets.QLabel(self.frame_1)
        self.label_img.setFrameShape(QtWidgets.QFrame.Box)
        self.label_img.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_img.setObjectName("label_img")
        self.verticalLayout_1.addWidget(self.label_img)
        self.label_fn = QtWidgets.QLabel(self.frame_1)
        self.label_fn.setFrameShape(QtWidgets.QFrame.Box)
        self.label_fn.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_fn.setObjectName("label_text")
        self.verticalLayout_1.addWidget(self.label_fn)
        self.verticalLayout_1.setStretch(0, 1)
        self.horizontalLayout.addWidget(self.frame_1)
        self.frame_2 = QtWidgets.QFrame()
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(50, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_3")
        self.pushButton_up = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_up.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_up.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_up.setObjectName("pushButton_up")
        self.verticalLayout_2.addWidget(self.pushButton_up)
        self.pushButto_down = QtWidgets.QPushButton(self.frame_2)
        self.pushButto_down.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButto_down.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButto_down.setObjectName("pushButto_down")
        self.verticalLayout_2.addWidget(self.pushButto_down)
        self.horizontalLayout.addWidget(self.frame_2)
        self.label_img.setText("ImgLabel")
        self.label_fn.setText("TextLabel")
        self.pushButton_up.setText("↑")
        self.pushButto_down.setText("↓")
        self.horizontalLayoutWidget.addWidget(self.frame_1)
        self.horizontalLayoutWidget.addWidget(self.frame_2)
        self.verticalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutWidget.setContentsMargins(0, 0, 0, 0)

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.frame_1 = QtWidgets.QFrame()
        self.central_layout.addWidget(self.frame_1)
        self.layout_1 = QVBoxLayout()
        self.frame_1.setLayout(self.layout_1)
        self.listwidget = QListWidget()
        self.layout_1.addWidget(self.listwidget)
        dobj = Path("./SampleImg").absolute()
        if not dobj.exists():
            dobj = Path("../SampleImg").absolute()
        img_fobjs = [fobj for fobj in dobj.iterdir() if fobj.suffix.lower() in ['.png', '.jpg', '.jpeg']]
        if len(img_fobjs) == 0:
            raise FileNotFoundError
        self.item_widget_map = []
        for i, fobj in enumerate(img_fobjs):
            item = QListWidgetItem()
            item.setSizeHint(QtCore.QSize(200, 200))
            self.listwidget.addItem(item)
            img_fp = str(fobj)
            img_fn = fobj.name
            if not fobj.exists():
                raise FileNotFoundError
            custom_widget = CustomWidgetForListItem(img_fp, img_fn)
            custom_widget.pushButton_up.clicked.connect(
                    lambda _, i=i: self.swap_item(i, i - 1 if i - 1 >= 0 else None)
            )
            custom_widget.pushButto_down.clicked.connect(lambda _, i=i: print(f"DOWN index = {i}"))
            self.listwidget.setItemWidget(item, custom_widget)
            self.item_widget_map.append((item, custom_widget))

    def swap_item(self, index1, index2):
        if index2 is None:
            print("Swap skipped because index2 is None")
            return

        print(f'Swapping items at index1={index1}, index2={index2}')

        item1, widget1 = self.item_widget_map[index1]
        item2, widget2 = self.item_widget_map[index2]

        # ウィジェットの設定を解除
        self.listwidget.setItemWidget(item1, None)
        self.listwidget.setItemWidget(item2, None)

        # アイテムをリストから削除して再挿入し、位置を入れ替える
        self.listwidget.takeItem(index1)
        self.listwidget.takeItem(index2)
        self.listwidget.insertItem(index2, item1)
        self.listwidget.insertItem(index1, item2)

        # item_widget_map の内容を更新
        self.item_widget_map[index1], self.item_widget_map[index2] = self.item_widget_map[index2], self.item_widget_map[index1]

        # 即座にウィジェットを再設定
        self.listwidget.setItemWidget(item1, widget2)
        self.listwidget.setItemWidget(item2, widget1)

        print("Swap completed.")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())