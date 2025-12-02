
from PyQt5.QtWidgets import QGraphicsPixmapItem, QWidget, QGraphicsRectItem, QMessageBox, QGraphicsView
from PyQt5.QtCore import Qt, QRectF, QPointF, QTimer
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush

# 黄色の矩形もここで定義

class DraggablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, parent, pixmap):
        from MAIN_APP import MyMainWindow
        super().__init__(pixmap)
        self.main_window = parent
        self.main_window: MyMainWindow
        self.start_pos = None
        self.current_rect_item = None
        self.setFlag(QGraphicsPixmapItem.ItemIsMovable, True)  # アイテムを移動可能に設定
        self.setFlag(QGraphicsPixmapItem.ItemIsSelectable, True)  # アイテムを選択可能に設定
        self.setAcceptedMouseButtons(Qt.LeftButton)  # 左ボタンでドラッグを受け入れる設定
        self.is_dragging = False  # ドラッグが行われたかどうかを追跡するフラグ
        self.rect = None  # 選択矩形の座標を保持
        self.rect_buf = None
        self.rect_item_xywz_100per_dict = None
        self.mode = 'move'  # move or select


    def set_sub_rect(self):
        # 黄色矩形を描画する
        self.current_rect_item = QGraphicsRectItem(self.rect, self)
        self.current_rect_item.setPen(QPen(Qt.NoPen))  # 枠線なし
        self.current_rect_item.setBrush(QBrush(QColor(255, 255, 0, 50)))  # 半透明の黄色
        self.current_rect_item.setZValue(1)  # アイテムの重なり順を設定（画像の上に描画）
        if not self.current_rect_item.scene():
            self.scene().addItem(self.current_rect_item)


    def align_rect_to_view(self, is_test=False):
        if self.main_window.is_not_set_sub_rect and self.main_window.radioButton_automove_off.isChecked():
            return
        # 100% スケールで保存された座標を取得
        original_x = self.rect_item_xywz_100per_dict['x']
        original_y = self.rect_item_xywz_100per_dict['y']
        original_angle = self.rect_item_xywz_100per_dict['angle']
        # self.main_window.rotate_image(original_angle, is_absolute=True)
        # 現在の回転角度を取得
        try:
            current_angle = float(self.main_window.lineEdit_angle.text())
            self.main_window.rotate_image(current_angle, is_absolute=True) # ! 回転テスト中
        except Exception as e:
            print('Error in align_rect_to_view, 矩形設定後の回転:', e)
        # 現在のスケールを取得
        scale = self.main_window.current_scale
        # 現在のスケールに基づいて移動量を計算
        x = original_x * scale
        y = original_y * scale
        if is_test:
            x = -100  # 負の座標をテストケースとして設定
            y = -50
        # ビューの左上をシーン座標に変換
        view_top_left_scene_pos = self.main_window.graphicsView_main.mapToScene(0, 0)
        # ビューの左上に合わせるための座標調整
        pix_x = view_top_left_scene_pos.x() - x
        pix_y = view_top_left_scene_pos.y() - y
        view_w = self.main_window.graphicsView_main.width()
        view_h = self.main_window.graphicsView_main.height()
        rect_w = self.rect_item_xywz_100per_dict['w'] * scale
        rect_h = self.rect_item_xywz_100per_dict['h'] * scale
        result_x = pix_x + view_w / 2 - rect_w / 2
        result_y = pix_y + view_h / 2 - rect_h / 2
        if not self.current_rect_item:
            self.set_sub_rect()
        # `rect_item` を `pixmap_item` の子アイテムに設定
        self.current_rect_item.setParentItem(self.main_window.pixmap_item)
        # `rect_item` の位置を `pixmap_item` の左上に基づいて設定
        self.current_rect_item.setPos(0, 0)  # 子アイテムの位置を親アイテムの左上（基準位置）に揃える
        # `pixmap_item` の位置をビューの左上に合わせる
        self.main_window.pixmap_item.setPos(int(result_x), int(result_y))

    def convert_rect(self) -> dict:
        if not self.rect:
            return
        x = self.rect.topLeft().x()
        y = self.rect.topLeft().y()
        w = self.rect.width()
        h = self.rect.height()
        angle = self.main_window.current_angle
        scale = self.main_window.current_scale
        original_x = round(x / scale)
        original_y = round(y / scale)
        original_w = round(w / scale)
        original_h = round(h / scale)
        self.rect_item_xywz_100per_dict = {'x': original_x, 'y': original_y, 'w': original_w, 'h': original_h, 'scale': scale, 'angle': angle}

    def get_rect(self):
        if not self.rect:
            return
        self.rect_buf = self.rect
        self.convert_rect()
        current_focus_in_obj = self.main_window.focus_in_line_widget_obj
        current_index = self.main_window.obj_name_to_index_dict[current_focus_in_obj.objectName()]
        self.main_window.rect_config[current_index]['w'] = self.rect_item_xywz_100per_dict['w']
        self.main_window.rect_config[current_index]['h'] = self.rect_item_xywz_100per_dict['h']
        self.main_window.rect_config[current_index]['x'] = self.rect_item_xywz_100per_dict['x']
        self.main_window.rect_config[current_index]['y'] = self.rect_item_xywz_100per_dict['y']
        self.main_window.rect_config[current_index]['angle'] = self.rect_item_xywz_100per_dict['angle']
        self.main_window.rect_config[current_index]['scale'] = self.rect_item_xywz_100per_dict['scale']
        self.main_window.write_rect_config(self.main_window.rect_config)
        current_index = self.main_window.obj_name_to_index_dict[current_focus_in_obj.objectName()]
        self.main_window.deactivate_all_event_filter()
        if current_index == len(self.main_window.data_list) - 1:
            next_obj = self.main_window.index_to_obj_dict[0]
        else:
            next_obj = self.main_window.index_to_obj_dict[current_index + 1]
        next_obj.setFocus()
        self.main_window.activate_all_event_filter()

    def set_rect(self, is_test=False, is_first=False, index=None, current_focus_in_obj = None, is_auto=False):
        if self.main_window.is_not_set_sub_rect and self.main_window.radioButton_automove_off.isChecked():
            return
        if self.main_window.is_last_enter_pressed == True and self.main_window.is_rept_mode == False:
            return
        if not self.rect_buf:
            self.rect = QRectF(QPointF(0, 0), QPointF(0, 0))
        if current_focus_in_obj is None:
            current_focus_in_obj = self.main_window.focus_in_line_widget_obj
        if current_focus_in_obj is None:
            return
        # if 'lineEdit_8_' == current_focus_in_obj.objectName():
        #     pass
        if is_first: # フォーカスインオブジェクトが無い場合は最初のオブジェクトを選択
            current_focus_in_obj = self.main_window.index_to_obj_dict[0]
        if index is None:
            current_index = self.main_window.obj_name_to_index_dict[current_focus_in_obj.objectName()]
        else:
            current_index = index
        current_recode = self.main_window.rect_config[current_index]
        is_valid_value = True
        try:
            # print('set_rect current_obj', current_focus_in_obj.objectName())
            if current_focus_in_obj.objectName() == 'lineEdit_0_':
                check_lineedit_name = ''
                for data in self.main_window.data_list:
                    if 'ischeck' in data['data_type'].split('_'):
                        check_lineedit_name = data['line_edit_name']
                        if self.main_window.focus_out_obj_for_collation.objectName() == check_lineedit_name \
                                and self.main_window.focus_out_obj_for_collation.hasFocus():
                            return
        except:
            pass
        for v in current_recode.values(): # None が含まれている場合は処理を中断
            if v is None:
                is_valid_value = False
                self.delete_sub_rect()
                break
        if not is_valid_value:
            if self.main_window.pixmap_item_pos_on_collation_dialog is not None:
                self.setPos(self.main_window.pixmap_item_pos_on_collation_dialog)
                self.main_window.pixmap_item_pos_on_collation_dialog = None
            return
        self.rect_item_xywz_100per_dict = {
            'x': current_recode['x'], 'y': current_recode['y'], 'w': current_recode['w'], 'h': current_recode['h'],
            'angle': current_recode['angle'], 'scale': current_recode['scale']}
        self.rect = self.rect_buf
        conv_x = self.rect_item_xywz_100per_dict['x'] * self.main_window.current_scale
        conv_y = self.rect_item_xywz_100per_dict['y'] * self.main_window.current_scale
        conv_w = self.rect_item_xywz_100per_dict['w'] * self.main_window.current_scale
        conv_h = self.rect_item_xywz_100per_dict['h'] * self.main_window.current_scale
        self.rect = QRectF(QPointF(conv_x, conv_y), QPointF(conv_x + conv_w, conv_y + conv_h))
        self.delete_sub_rect()
        # self.set_sub_rect() # ! ここを変更
        self.align_rect_to_view(is_test=is_test)
        QTimer.singleShot(50, lambda: self.adjust_scene_to_fit_item())


    def adjust_scene_to_fit_item(self):
        # アイテムのシーン内でのバウンディングボックスを取得
        item_scene_rect = self.main_window.pixmap_item.sceneBoundingRect()
        # シーンの現在の矩形を取得
        current_scene_rect = self.main_window.graphicsView_main.sceneRect()
        # アイテムがシーンの現在の範囲外にあるか確認
        if not current_scene_rect.contains(item_scene_rect):
            # シーンを広げるために、新しい幅と高さを計算
            new_scene_left = min(current_scene_rect.left(), item_scene_rect.left())
            new_scene_top = min(current_scene_rect.top(), item_scene_rect.top())
            new_scene_right = max(current_scene_rect.right(), item_scene_rect.right())
            new_scene_bottom = max(current_scene_rect.bottom(), item_scene_rect.bottom())
            # 新しいシーン矩形を設定
            new_scene_rect = QRectF(new_scene_left, new_scene_top,
                                    new_scene_right - new_scene_left,
                                    new_scene_bottom - new_scene_top)
            self.main_window.graphicsView_main.setSceneRect(new_scene_rect)
            # self.main_window.graphicsView_main.setSceneRect(item_scene_rect)

    def delete_sub_rect(self):
        if self.current_rect_item and self.current_rect_item.scene():
            self.scene().removeItem(self.current_rect_item)
            self.current_rect_item = None

    # マウスが押されたときの処理
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.mode == 'move':
                self.setCursor(Qt.ClosedHandCursor)  # マウスカーソルをドラッグ中の形に変更
            elif self.mode == 'select':
                self.setCursor(Qt.CrossCursor)
            self.start_pos = event.pos()  # ドラッグ開始位置を保存
            self.is_dragging = False  # ドラッグフラグをリセット
            # 通常モード（画像を動かすモード）の場合、アイテムを移動可能に設定
            self.setFlag(QGraphicsPixmapItem.ItemIsMovable, True if self.mode == 'move' else False)
        super().mousePressEvent(event)

    # マウスがドラッグされたときの処理
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.mode == 'move':
                delta = event.pos() - self.start_pos  # ドラッグの移動量を計算
                self.setPos(self.pos() + delta)  # アイテムの位置を更新
            elif self.mode == 'select':
                # ドラッグ中に選択矩形を更新
                if self.start_pos:
                    self.is_dragging = True  # ドラッグが行われたとマーク
                    # 古い矩形を削除
                    if self.current_rect_item:
                        self.scene().removeItem(self.current_rect_item)
                    # 現在の矩形の座標を取得
                    self.rect = QRectF(self.start_pos, event.pos()).normalized()
                    self.set_sub_rect()
        super().mouseMoveEvent(event)

    # マウスがリリースされたときの処理
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ArrowCursor)  # マウスカーソルを元に戻す
            if not self.is_dragging and self.current_rect_item and self.current_rect_item.scene():
                self.delete_sub_rect()
        super().mouseReleaseEvent(event)

