import re
import sys

from pprint import pprint
import pandas as pd

from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsSceneMouseEvent, QWidget, QGraphicsRectItem, QMessageBox, QGraphicsView, QPlainTextEdit ,\
        QMainWindow, QListWidget, QApplication, QTableView, QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsScene
from PyQt5.QtCore import Qt, QRectF, QPointF, QItemSelectionModel, QRect
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush, QTextCursor, QTextCharFormat, QFont, QStandardItem, QStandardItemModel

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_vars()
        self.set_ui()
        self.set_button()

    def init_vars(self):
        self.rectitems = []

    def resize_scene(self):
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

    def delete_rectitem(self):
        if self.rectitems:
            di = [{'index': i, 'item': item} for i, item in enumerate(self.rectitems) if item.isSelected()]
            di = sorted(di, key=lambda x: x['index'], reverse=True)
            pprint(di)
            for d in di:
                self.rectitems.pop(d['index'])
                self.scene.removeItem(d['item'])
            pprint(self.rectitems)
            return

    def add_rectitem(self):
        if self.rectitems:
            prerect_item = self.rectitems[-1]
            prerect_item: QGraphicsRectItem
            prerect_item_pos = prerect_item.mapToScene(prerect_item.rect().topLeft())
            item_rectf = QRectF(prerect_item_pos.x() + 10, prerect_item_pos.y() + 10, 150, 100)
        else:
            item_rectf = QRectF(0, 0, 150, 100)
        rectitem = CustomRectItem(item_rectf)
        rectitem.setTransformOriginPoint(0, 0)
        rectitem.setBrush(QBrush(QColor(0, 255, 255, 100)))
        rectitem.setPos(0, 0)
        self.scene.addItem(rectitem)
        self.rectitems.append(rectitem)
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

    def move(self, deltas):
        self.rectitems[-1].moveBy(deltas[0], deltas[1])

    def show_selected_rectitem_count(self):
        selected_items = self.scene.selectedItems()
        print('selected_items', len(selected_items))

    def set_button(self):
        self.button_moveup = QPushButton('Up')
        self.button_movedown = QPushButton('Down')
        self.button_moveleft = QPushButton('Left')
        self.button_moveright = QPushButton('Right')
        self.button_add_rectitem = QPushButton('Add')
        self.button_delete_rectitem = QPushButton('Delete')
        self.button_resize_scene = QPushButton('Resize Scene')
        self.button_count_rectitem = QPushButton('Count RectItem')
        self.button_stop = QPushButton('Stop')

        self.hlayout_buttons_1.addWidget(self.button_moveup)
        self.hlayout_buttons_1.addWidget(self.button_movedown)
        self.hlayout_buttons_1.addWidget(self.button_moveleft)
        self.hlayout_buttons_1.addWidget(self.button_moveright)
        self.hlayout_buttons_2.addWidget(self.button_add_rectitem)
        self.hlayout_buttons_2.addWidget(self.button_delete_rectitem)
        self.hlayout_buttons_2.addWidget(self.button_resize_scene)
        self.hlayout_buttons_2.addWidget(self.button_count_rectitem)
        self.hlayout_buttons_2.addWidget(self.button_stop)

        self.button_moveup.clicked.connect(lambda: self.move([0, -10]))
        self.button_movedown.clicked.connect(lambda: self.move([0, 10]))
        self.button_moveleft.clicked.connect(lambda: self.move([-10, 0]))
        self.button_moveright.clicked.connect(lambda: self.move([10, 0]))
        self.button_add_rectitem.clicked.connect(self.add_rectitem)
        self.button_delete_rectitem.clicked.connect(self.delete_rectitem)
        self.button_resize_scene.clicked.connect(self.resize_scene)
        self.button_count_rectitem.clicked.connect(self.show_selected_rectitem_count)
        self.button_stop.clicked.connect(self.stop)

    def stop(self):
        try:
            rect_0 = self.rectitems[0]
            rect_0: QGraphicsRectItem
            pos_0 = rect_0.mapToScene(rect_0.rect().topLeft())
            print('pos_0', pos_0.x(), pos_0.y())
        except Exception as e:
            print(e)
        try:
            rect_1 = self.rectitems[1]
            rect_1: QGraphicsRectItem
            pos_1 = rect_1.mapToScene(rect_1.rect().topLeft())
            print('pos_1', pos_1.x(), pos_1.y())
        except Exception as e:
            print(e)
        pass

    def set_ui(self):
        self.graphicsview = QGraphicsView()
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(QColor(200, 200, 200)))
        self.graphicsview.setScene(self.scene)
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.mainlayout = QVBoxLayout()
        self.centralwidget.setLayout(self.mainlayout)
        self.vlayout_1 = QVBoxLayout()
        self.hlayout_buttons_1 = QHBoxLayout()
        self.frame_2 = QFrame()
        self.frame_1 = QFrame()
        self.frame_1.setLayout(self.vlayout_1)
        self.mainlayout.addWidget(self.frame_1)
        self.graphicsview.setGeometry(0, 0, 500, 400)
        self.setGeometry(0, 0, 700, 600)
        self.vlayout_1.addWidget(self.graphicsview)
        self.frame_2.setLayout(self.hlayout_buttons_1)
        self.hlayout_buttons_2 = QHBoxLayout()
        self.frame_3 = QFrame()
        self.frame_3.setLayout(self.hlayout_buttons_2)
        self.mainlayout.addWidget(self.frame_2)
        self.mainlayout.addWidget(self.frame_3)
        self.graphicsview.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.scene.setSceneRect(0, 0, self.scene.sceneRect().width(), self.scene.sceneRect().height())

class CustomRectItem(QGraphicsRectItem):
    def __init__(self, rect: QRectF):
        super().__init__(rect)
        self.startpos = None
        self.is_dragging = False
        self.dragging_rectitem = None
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)  # 選択可能にする

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.CursorShape.OpenHandCursor)
            self.startpos = event.pos()
            self.is_dragging = False
            self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        # if self.startpos is not None:
        #     print('mouseMoveEvent')
        #     self.is_dragging = True
        #     if self.dragging_rectitem is not None:
        #         self.scene().removeItem(self.dragging_rectitem)
        #     current_rectf = QRectF(self.startpos, event.pos()).normalized()
        #     self.dragging_rectitem = QGraphicsRectItem(current_rectf, self)
        #     self.dragging_rectitem.setPen(QPen(Qt.PenStyle.NoPen))
        #     self.dragging_rectitem.setBrush(QBrush(QColor(0, 0, 255, 100)))
        #     self.dragging_rectitem.setZValue(1)
        #     if self.dragging_rectitem.scene() is None:
        #         self.scene().addItem(self.dragging_rectitem)
        return super().mouseMoveEvent(event)

    # マウスがリリースされたときの処理
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ArrowCursor)  # マウスカーソルを元に戻す
        super().mouseReleaseEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())