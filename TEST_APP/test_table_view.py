import re
import sys

from pprint import pprint
import pandas as pd

from PyQt5.QtWidgets import QGraphicsPixmapItem, QWidget, QGraphicsRectItem, QMessageBox, QGraphicsView, QPlainTextEdit ,\
        QMainWindow, QListWidget, QApplication, QTableView, QFrame, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QRectF, QPointF, QItemSelectionModel
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush, QTextCursor, QTextCharFormat, QFont, QStandardItem, QStandardItemModel

from _numeric_sort_proxy_model import NumericSortProxyModel

class MyTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tableview = QTableView()
        self.init_tableview(self.tableview)
        self.set_ui()
        df = pd.DataFrame(
                [
                    [1, '100', 'ccc', 4, 'abbc'],
                    [5, '5', 'bbb', 2, 'dge'],
                    [1, '1', 'aaa', 4, 'geis']
                ],
        )
        self.button_set_df.clicked.connect(lambda: self.set_df_to_tableview(df))
        self.button_get_df.clicked.connect(lambda: self.get_df_from_tableview())
        self.button_add_row.clicked.connect(lambda: self.add_row_to_tableview())
        self.button_test_1.clicked.connect(lambda: self.test_1())

    def test_1(self):
        self.tableview.sortByColumn(-1, Qt.AscendingOrder)

    def init_tableview_item(self):
        for row in range(self.model.rowCount()):
            for col in range(self.model.columnCount()):
                if self.model.item(row, col) is not None:
                    item = self.model.item(row, col)
                else:
                    item = QStandardItem('')
                item.setFont(QFont('Consolas', 12))
                self.model.setItem(row, col, item)

    def add_row_to_tableview(self):
        current_row = self.tableview.currentIndex().row()
        current_col = self.tableview.currentIndex().column()
        if current_row == -1:
            return
        df = self.get_df_from_tableview()
        blank_array = [['' for _ in range(df.shape[1])]]
        blank_df = pd.DataFrame(blank_array, columns=df.columns)
        df = pd.concat([df.iloc[:current_row, :], blank_df, df.iloc[current_row:, :]], axis=0)
        df = df.reset_index(drop=True)
        print(df)
        self.model.clear()
        self.set_df_to_tableview(df)
        self.init_tableview_item()
        print('row', current_row, 'col', current_col)
        index = self.model.index(current_row, current_col)
        self.tableview.selectionModel().select(index, QItemSelectionModel.SelectionFlag.Select)
        self.tableview.setCurrentIndex(index)
        self.tableview.setFocus()

    def set_df_to_tableview(self, df: pd.DataFrame):
        df = df.fillna('')
        df = df.astype(str)
        array = df.values.tolist()
        self.model.clear()
        print(array)
        for i in range(df.shape[0]):
            record = array[i]
            items = [QStandardItem(str(value)) for value in record]
            self.model.appendRow(items)
        self.init_tableview_item()
        self.tableview.setSortingEnabled(True)

    def get_df_from_tableview(self):
        array = []
        for row in range(self.model.rowCount()):
            record_array = []
            for col in range(self.model.columnCount()):
                item = self.model.item(row, col)
                record_array.append(item.text())
            array.append(record_array)
        df = pd.DataFrame(array)
        return df

    def init_tableview(self, tableview: QTableView):
        self.model = QStandardItemModel()
        self.proxy_model = NumericSortProxyModel()
        self.tableview.setSortingEnabled(False)
        self.proxy_model.setSourceModel(self.model)
        tableview.setModel(self.proxy_model)

    def set_blank_to_tableview(self):
        for row in self.model.rowCount():
            for col in self.model.columnCount():
                item = self.model.item(row, col)
                item.setText('')

    def set_ui(self):
        self.central_widget = QWidget()
        self.layout_main = QVBoxLayout()
        self.central_widget.setLayout(self.layout_main)
        self.frame_1 = QFrame()
        self.layout_1 = QVBoxLayout()
        self.frame_1.setLayout(self.layout_1)
        self.frame_2 = QFrame()
        self.layout_2 = QHBoxLayout()
        self.frame_2.setLayout(self.layout_2)
        self.button_set_df = QPushButton('SetDf')
        self.button_get_df = QPushButton('GetDf')
        self.button_add_row = QPushButton('AddRow')
        self.button_test_1 = QPushButton('Test1')
        self.layout_2.addWidget(self.button_set_df)
        self.layout_2.addWidget(self.button_get_df)
        self.layout_2.addWidget(self.button_add_row)
        self.layout_2.addWidget(self.button_test_1)
        self.central_widget.setLayout(self.layout_main)
        self.layout_main.addWidget(self.frame_1)
        self.layout_main.addWidget(self.frame_2)
        self.setCentralWidget(self.central_widget)
        self.layout_1.addWidget(self.tableview)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window =  MyTestWindow()
    window.show()
    sys.exit(app.exec_())