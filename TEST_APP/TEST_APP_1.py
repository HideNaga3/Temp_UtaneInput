from pprint import pprint

from PyQt5.QtWidgets import QGraphicsPixmapItem, QWidget, QGraphicsRectItem, QMessageBox, QGraphicsView, QPlainTextEdit ,\
        QMainWindow, QListWidget
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush, QTextCursor, QTextCharFormat, QFont
import re

from _draggable_pixmap_item import DraggablePixmapItem
from _collation_two_text import CollationTwoText


class MainWindow(QMainWindow):
    def __init__(self):
        # from PyQt5.QtCore import
        super().__init__()
        self.init_frame_1()
        self.init_frame_2()

    def init_frame_2(self):
        self.frame_2 = QWidget()
        self.layout_2 = QVBoxLayout()
        self.list_widget = QListWidget()
        self.layout_2.addWidget(self.list_widget)
        self.frame_2.setLayout(self.layout_2)
        self.setCentralWidget(self.frame_2)

    def init_frame_1(self):
        # シーンの作成
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 800, 600)

        self.current_angle = 0  # 回転角度
        self.current_scale = 1.0  # 拡大率

        # グラフィックビューの作成
        self.graphicsView_main = QGraphicsView(self.scene, self)
        self.graphicsView_main.setMouseTracking(True)

        self.lineEdit_angle = QLineEdit()
        self.lineEdit_angle.setReadOnly(True)
        self.lineEdit_scale = QLineEdit()
        self.lineEdit_scale.setReadOnly(True)

        self.button_move = QPushButton('移動モード')
        self.button_select = QPushButton('選択モード')
        self.button_rotate_left = QPushButton('左回転')
        self.button_rotate_right = QPushButton('右回転')
        self.button_zoom_in = QPushButton('拡大')
        self.button_zoom_out = QPushButton('縮小')
        self.button_get_rect = QPushButton('矩形取得')
        self.button_set_rect = QPushButton('矩形設定')
        self.button_test = QPushButton('テスト')
        self.button_reset_color = QPushButton('色リセット')

        self.above_layout = QHBoxLayout()
        self.above_layout.addWidget(self.button_move)
        self.above_layout.addWidget(self.button_select)
        self.above_layout.addWidget(self.button_rotate_left)
        self.above_layout.addWidget(self.button_rotate_right)
        self.above_layout.addWidget(self.button_zoom_in)
        self.above_layout.addWidget(self.button_zoom_out)
        self.above_layout.addWidget(self.lineEdit_angle)
        self.above_layout.addWidget(self.lineEdit_scale)
        self.above_layout.addWidget(self.button_get_rect)
        self.above_layout.addWidget(self.button_set_rect)
        self.above_layout.addWidget(self.button_test)
        self.above_layout.addWidget(self.button_reset_color)

        self.plainTextEdit_new = QPlainTextEdit()
        self.plainTextEdit_ver = QPlainTextEdit()
        # レイアウトの設定
        self.layout_1 = QVBoxLayout()
        self.layout_1.addLayout(self.above_layout)
        self.layout_1.addWidget(self.graphicsView_main)
        self.layout_1.addWidget(self.plainTextEdit_new)
        self.layout_1.addWidget(self.plainTextEdit_ver)

        self.plainTextEdit_new.setFont(QFont('Meiryo UI', 12))
        self.plainTextEdit_ver.setFont(QFont('Meiryo UI', 12))

        self.frame_1 = QWidget()
        self.frame_1.setLayout(self.layout_1)
        self.setCentralWidget(self.frame_1)
        self.frame_1.hide()

        # 画像アイテムをシーンに追加
        self.pixmap = QPixmap(r".\SampleImg\output_image_with_grid.jpg")  # 画像のパスを指定
        # self.pixmap_item = DraggablePixmapItem(self, self.pixmap)
        # self.scene.addItem(self.pixmap_item)
        self.set_image_from_pixmap()
        self.button_move.clicked.connect(lambda: self.change_mode(True))
        self.button_select.clicked.connect(lambda: self.change_mode(False))
        self.button_rotate_left.clicked.connect(lambda: self.rotate_image(-90))
        self.button_rotate_right.clicked.connect(lambda: self.rotate_image(90))
        self.button_zoom_in.clicked.connect(lambda: self.scaling_image(0.1))
        self.button_zoom_out.clicked.connect(lambda: self.scaling_image(-0.1))
        self.button_get_rect.clicked.connect(self.pixmap_item.get_rect)
        self.button_set_rect.clicked.connect(self.pixmap_item.set_rect)
        self.button_test.clicked.connect(self.set_color_to_diff_char)
        self.value_new = 'あかうえ打おかきくけこ'
        self.value_ver = 'あいうえおかきらけこ'
        self.plainTextEdit_new.setPlainText(self.value_new)
        self.plainTextEdit_ver.setPlainText(self.value_ver)
        self.button_reset_color.clicked.connect(lambda: self.reset_color_from_char([self.plainTextEdit_new, self.plainTextEdit_ver]))
        # self.collation_text(self.value_new, self.value_ver)
        self.collation_two_text = CollationTwoText()


# ************************** 文字に色付け開始 **************************
    def set_color_to_diff_char(self): # ドライバ
        print('start ##############')
        # 別モジュールからの呼び出し...
        result_dict = self.collation_two_text.collation_two_text(self.plainTextEdit_new.toPlainText(), self.plainTextEdit_ver.toPlainText())
        self.reset_color_from_char([self.plainTextEdit_new, self.plainTextEdit_ver])
        if result_dict is None:
            QMessageBox.information(self, '情報', 'テキストは一致しています')
            return
        print('result_dict')
        pprint(result_dict)
        original_cursor = self.plainTextEdit_new.textCursor()
        original_position = original_cursor.position()
        new_indexes = []
        ver_indexes = []
        for item in result_dict['normal_and_rev']:
            print(item['new']['index'])
            new_indexes.append(item['new']['index'])
            ver_indexes.append(item['ver']['index'])
        for new_index in new_indexes:
            self.set_color_to_char(self.plainTextEdit_new, new_index)
        for ver_index in ver_indexes:
            self.set_color_to_char(self.plainTextEdit_ver, ver_index)
        new_diff = result_dict['new_diff']
        ver_diff = result_dict['ver_diff']
        for new_char in new_diff:
            indexes = [m.start() for m in re.finditer(new_char, self.plainTextEdit_ver.toPlainText())]
            for index in indexes:
                self.set_color_to_char(self.plainTextEdit_ver, index)
        for ver_char in ver_diff:
            indexes = [m.start() for m in re.finditer(ver_char, self.plainTextEdit_new.toPlainText())]
            for index in indexes:
                self.set_color_to_char(self.plainTextEdit_new, index)
        original_cursor.setPosition(original_position)
        self.plainTextEdit_ver.setTextCursor(original_cursor)

    def set_color_to_char(self, plain_obj, indexes):
        cursor = plain_obj.textCursor()
        cursor.setPosition(indexes)
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)
        char_format = QTextCharFormat()
        char_format.setBackground(QColor(255, 0, 0, 70))
        cursor.setCharFormat(char_format)

    def reset_color_from_char(self, plain_objs: list):
        for plain_obj in plain_objs:
            cursol = plain_obj.textCursor()
            cursol.select(QTextCursor.Document)
            char_format = QTextCharFormat()
            char_format.clearBackground()
            cursol.setCharFormat(char_format)
# ************************** 文字に色付け終了 **************************


    def change_mode(self, pixmap_item_mode):
        self.pixmap_item.delete_sub_rect()
        if pixmap_item_mode:
            self.pixmap_item.mode = 'move'
        elif not pixmap_item_mode:
            self.pixmap_item.mode = 'select'

    def collation_text(self, new_text, ver_text): # ドライバ
        invalids = []
        new_len = len(new_text)
        ver_len = len(ver_text)
        text_len = new_len if new_len > ver_len else ver_len
        for i in range(len(new_text)):
            if new_text[i] != ver_text[i]:
                print(f'new_text[{i}]: {new_text[i]}')
                print(f'ver_text[{i}]: {ver_text[i]}')
                print('')
                invalids.append({'new': {'index': i, 'char': new_text[i]}, 'ver': {'index': i, 'char': ver_text[i]}})
        for i in range(text_len - 1, -1, -1):
            print(i)
            if new_text[i] != ver_text[i]:
                print(f'new_text[{i}]: {new_text[i]}')
                print(f'ver_text[{i}]: {ver_text[i]}')
                print('')
                invalids.append({'new_rev': {'index': i, 'char': new_text[i]}, 'ver_rev': {'index': i, 'char': ver_text[i]}})
        print(invalids)

    ############################### 画像処理 開始 #############################
    def set_image_from_pixmap(self):
        self.original_pixmap = self.pixmap.copy()  # 回転やズーム前の画像を保存
        self.pixmap_item = DraggablePixmapItem(self, self.pixmap)
        self.pixmap_item.setTransformOriginPoint(0, 0)  # 回転の原点を中心に設定
        self.rotate_image(0)
        self.scaling_image(0)
        self.scene.addItem(self.pixmap_item)
        self.graphicsView_main.setScene(self.scene)
        self.graphicsView_main.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def resizeEvent(self, event):
        # ウィンドウサイズが変更された際に画像を再フィット
        # self.graphicsView_main.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        super().resizeEvent(event)

    def adjust_image(self, mode: str = 'w'): # GraphicsViewの高さ、幅を取得して画像をフィットさせる
        view_width = self.graphicsView_main.width()
        view_height = self.graphicsView_main.height()
        original_width = self.original_pixmap.width()
        original_height = self.original_pixmap.height()
        vertical_scrollbar_width = self.graphicsView_main.verticalScrollBar().width()
        horizontal_scrollbar_height = self.graphicsView_main.horizontalScrollBar().height()
        transform = QTransform().rotate(self.current_angle) # pixmapをcurrent_angleの角度で回転
        self.pixmap = self.original_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        if mode == 'w':
            new_width = view_width
            new_width_without_scroll_var = new_width - vertical_scrollbar_width # スクロールバーの幅を除外
            if self.current_angle in [90, 270]: # 90度または270度の場合は幅と高さを入れ替える
                original_width, original_height = original_height, original_width
            scale_factor = new_width_without_scroll_var / original_width
            new_height = int(original_height * scale_factor)
            self.pixmap = self.pixmap.scaled(new_width_without_scroll_var, new_height, # リサイズした画像を新しいPixmapに設定
                    Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        elif mode == 'h':
            new_height = view_height
            new_height_without_scroll_var = new_height - horizontal_scrollbar_height
            if self.current_angle in [90, 270]: # 90度または270度の場合は幅と高さを入れ替える
                original_width, original_height = original_height, original_width
            scale_factor = new_height_without_scroll_var / original_height
            new_width = int(original_width * scale_factor)
            self.pixmap = self.pixmap.scaled(new_width, new_height_without_scroll_var, # リサイズした画像を新しいPixmapに設定
                    Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.pixmap_item.setPixmap(self.pixmap)  # 既存のpixmap_itemに新しいpixmapをセット
        self.pixmap_item.setPos(0, 0)  # アイテムの位置を初期化
        self.scene.setSceneRect(self.pixmap_item.boundingRect()) # シーンのサイズを画像のサイズに合わせる
        if self.current_angle in [0, 180]:
            self.current_scale = new_width / original_width
            # self.current_scale = round(new_width / original_width, 1)
        elif self.current_angle in [90, 270]:
            self.current_scale = new_height / original_height
            # self.current_scale = round(new_height / original_height, 1)
        self.show_angle_and_scale()
        # self.align_image_to_top_left()

    def rotate_image(self, angle: int, is_absolute = False): # 画像を回転させる
        if is_absolute:
            next_angle = angle
        else:
            next_angle = self.current_angle + angle
        transform = QTransform().rotate(next_angle) # 回転の角度transformを設定
        rotated_pixmap = self.original_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation) # 回転後のpixmapを取得
        if self.current_scale != 1.0: # 拡大処理が必要な場合
            new_width = int(rotated_pixmap.width() * self.current_scale)
            new_height = int(rotated_pixmap.height() * self.current_scale)
            rotated_pixmap = rotated_pixmap.scaled(
                    new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.pixmap_item.setPixmap(rotated_pixmap) # 回転後のpixmapをpixmap_itemにセット
        self.pixmap_item.setPos(0, 0) # アイテムの位置を左上に設定
        self.scene.setSceneRect(self.pixmap_item.boundingRect()) # シーンのサイズを画像のサイズに合わせる
        self.current_angle = int(next_angle % 360)
        self.show_angle_and_scale()

    def scaling_image(self, scale: float = 0, is_absolute: bool = False): # 画像を拡大縮小する
        next_scale = self.current_scale + scale
        if next_scale < 0.1:
            next_scale = 0.1
        elif is_absolute:
            next_scale = scale

        new_width = int(self.original_pixmap.width() * next_scale)
        new_height = int(self.original_pixmap.height() * next_scale)
        scaled_pixmap = self.original_pixmap.scaled(
                new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.pixmap_item.setPixmap(scaled_pixmap)
        self.pixmap_item.setPos(0, 0)
        self.scene.setSceneRect(self.pixmap_item.boundingRect())
        self.current_scale = next_scale
        if self.current_angle != 0:
            transform = QTransform().rotate(self.current_angle)
            rotated_pixmap = scaled_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
            self.pixmap_item.setPixmap(rotated_pixmap)
            self.pixmap_item.setPos(0, 0)
            self.scene.setSceneRect(self.pixmap_item.boundingRect())
        self.show_angle_and_scale()

    def align_image_to_top_left(self): # 画像を左上に合わせる 今は使っていない
        bounding_rect = self.pixmap_item.boundingRect()# バウンディングボックスを取得
        self.pixmap_item.setPos(-bounding_rect.width() / 2, -bounding_rect.height() / 2)# 左上に位置を調整
        self.scene.setSceneRect(self.pixmap_item.sceneBoundingRect())

    def show_angle_and_scale(self): # 回転角度と拡大率をラベルに表示
        self.lineEdit_angle.setText(str(self.current_angle))
        self.lineEdit_angle.blockSignals(True)
        self.lineEdit_scale.setText(str(round(self.current_scale * 100, 1)))
        self.lineEdit_angle.blockSignals(False)

    def change_scale_on_line_edit(self):
        scale = float(self.lineEdit_scale.text()) / 100
        if scale > 10:
            scale = 10
            self.lineEdit_scale.blockSignals(True)
            self.lineEdit_scale.setText('1000.0')
            self.lineEdit_scale.blockSignals(False)
        elif scale < 0.1:
            scale = 0.1
            self.lineEdit_scale.blockSignals(True)
            self.lineEdit_scale.setText('10.0')
            self.lineEdit_scale.blockSignals(False)
        if scale and self.is_float(scale): # 空白でない、かつ、フロート場合
            self.scaling_image(scale, is_absolute=True)
        else:
            return
    ############################### 画像処理 終了 #############################

if __name__ == "__main__":
    from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QGraphicsScene, QGraphicsView, \
            QLineEdit
    from PyQt5.QtGui import QPixmap, QTransform
    app = QApplication([])
    window = MainWindow()
    window.setWindowTitle('TestViewer')
    window.show()
    app.exec_()