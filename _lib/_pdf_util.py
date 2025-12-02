import fitz # PyMuPDF
from pathlib import Path
import sys
from pprint import pprint as pp
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QSharedMemory, QSize, pyqtSignal, QObject, QEvent, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QGraphicsScene, QGraphicsPixmapItem,\
    QDialog, QAbstractItemView, QShortcut, QSizePolicy, QMenu, QAction, QGraphicsView, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPalette, QColor, QTextCursor, QKeySequence, QImage,\
    QTextCharFormat, QBrush, QKeyEvent
from PyQt5 import sip

class PdfImgReader:
    def __init__(self, dobj:Path, matrix_int=2):
        try:
            self.matrix_int = int(matrix_int)
        except:
            self.matrix_int = 2
        self.total_page_count = None
        self.file_list, self.file_dict, self.page_list, self.page_dict = [], {}, [], {}
        self.doc = None
        # ____
        self.parent_dobj = dobj
        self.pdf_objs = [fobj for fobj in dobj.iterdir() if fobj.suffix.lower() == '.pdf']
        self.pdf_objs = sorted(self.pdf_objs, key=lambda x: x.name)
        self.file_list = []
        for i, pdf_obj in enumerate(self.pdf_objs):
            file_record = {}
            file_record['file_index'] = i
            file_record['pdf_obj'] = pdf_obj
            file_record['file_name'] = pdf_obj.name
            self.file_list.append(file_record.copy())
        self.file_dict = {data['file_name']: data for data in self.file_list} # {file_name: data}
        _ = self._get_total_page_items()

    def get_total_page_count(self) -> int:
        return self.total_page_count

    def get_file_list(self) -> list:
        return self.file_list

    def get_file_dict(self) -> dict:
        return self.file_dict

    def get_page_list(self) -> list:
        return self.page_list

    def _get_total_page_items(self) -> int:
        self.total_page_count = 0
        for file_index, data_record in enumerate(self.file_list):
            pdf_obj = data_record['pdf_obj']
            pdf_path = str(pdf_obj.absolute())
            pdf_name = pdf_obj.name
            doc = fitz.open(pdf_path)
            page_count = doc.page_count
            data_record['page_count'] = page_count
            for page_index in range(page_count):
                page_record = {}
                page_record.update({
                        'main_index': self.total_page_count,
                        'file_index': file_index,
                        'page_index': page_index,
                        'file_name': pdf_name,
                        'pdf_obj': pdf_obj,
                })
                self.total_page_count += 1
                self.page_list.append(page_record.copy())
            doc.close()

    def get_img_from_pdf(self, file_name, page_index) -> QPixmap:
        pdf_obj = self.file_dict[file_name]['pdf_obj']
        pdf_path = str(pdf_obj.absolute())
        self.doc = fitz.open(pdf_path) # PDFを開く
        page_count = self.doc.page_count # ページ数を取得
        if page_count - 1 < page_index:
            return None
        page = self.doc.load_page(page_index) # ページを読み込む
        matrix = self.matrix_int if self.matrix_int <= 5 else 5 # 5以下の整数
        pixmap = page.get_pixmap(matrix=fitz.Matrix(matrix, matrix)) # ピクセルマップを取得
        qimage = QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888)
        qpixmap = QPixmap.fromImage(qimage)
        self.doc.close() # PDFを閉じる
        return qpixmap

    def get_data_list(self):
        return self.file_list

    def get_data_dict(self):
        return self.file_dict

class TestMainWindow(QMainWindow):
    def __init__(self, dobj):
        super().__init__()
        self.dobj = dobj

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.vframe_1 = QtWidgets.QFrame()
        self.central_layout.addWidget(self.vframe_1)
        self.vlayout_1 = QtWidgets.QVBoxLayout()
        self.vframe_1.setLayout(self.vlayout_1)

        self.graphicsview = QtWidgets.QGraphicsView()
        self.vlayout_1.addWidget(self.graphicsview)

        self.hframe_1 = QtWidgets.QFrame()
        self.central_layout.addWidget(self.hframe_1)
        self.hlayout_1 = QtWidgets.QHBoxLayout()
        self.hframe_1.setLayout(self.hlayout_1)

        self.button_1 = QtWidgets.QPushButton('Button 1')
        self.hlayout_1.addWidget(self.button_1)
        pass
        self.scene = QGraphicsScene()
        self.graphicsview.setScene(self.scene)

        self.update_pixmap()

    def update_pixmap(self):
        pdf_obj = self.dobj.iterdir().__next__().absolute()
        pdf_img_reader = PdfImgReader(self.dobj)
        from _draggable_pixmap_item import DraggablePixmapItem
        qpixmap = pdf_img_reader.get_img_from_pdf(pdf_obj.name, 0)
        if qpixmap is None:
            return
        self.pixmap_item = DraggablePixmapItem(self, qpixmap)
        self.pixmap_item.setTransformationMode(Qt.SmoothTransformation)
        self.scene.addItem(self.pixmap_item)
        self.scene.setSceneRect(self.pixmap_item.boundingRect())

if __name__ == '__main__':
    test_dp = './Sample防災_prevention'
    test_dobj = Path(test_dp).absolute()
    app = QApplication(sys.argv)
    window = TestMainWindow(test_dobj)
    window.show()
    sys.exit(app.exec_())
