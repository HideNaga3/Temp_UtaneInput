# _init_dialog_main.py
# InitDialogクラス - 初期設定ダイアログ
# MAIN_APP.pyから分離
#
# 作成日: 2025-10-25
# Phase B-1: InitDialogの分離

import os
import sys
import re
from pathlib import Path
from collections import Counter
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
import pandas as pd
from typing import TYPE_CHECKING
from pprint import pprint as pp

from _init_dialog_ui import Ui_InitDialog
from _lib._data_io import DataIO
# from _lib._mode_config import ModeConfigManager

if TYPE_CHECKING:
    from typing import Optional
    from MAIN_APP import MyMainWindow
    # MyMainWindow の型ヒント用（循環インポート回避）


class InitDialog(QDialog, Ui_InitDialog):
    close_parent = pyqtSignal() # カスタムシグナルを定義（親ウィンドウを終了させるためのシグナル）
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        try:
            if getattr(sys, 'frozen', False): # 実行ファイルの場合
                application_path = sys._MEIPASS # 実行ファイルのパス
                icon_path = os.path.join(application_path, 'icon.ico')
            else: # スクリプトファイルの場合
                application_path = os.path.dirname(__file__)
                icon_path = os.path.join(application_path, '_icon', 'icon.ico')
            self.setWindowIcon(QIcon(icon_path)) # ウィンドウのアイコンを設定
        except:
            icon_path = None
        self.lineEdit_username: QtWidgets.QLineEdit
        self.lineEdit_img_path: QtWidgets.QLineEdit
        self.lineEdit_output_path: QtWidgets.QLineEdit
        self.pushButton_img_path_dialog: QtWidgets.QPushButton
        self.pushButton_output_path_dialog: QtWidgets.QPushButton
        self.pushButton_start: QtWidgets.QPushButton
        self.pushButton_cancel: QtWidgets.QPushButton
        self.comboBox_input_mode: QtWidgets.QComboBox
        self.radioButton_csvpath_true: QtWidgets.QRadioButton
        self.radioButton_csvpath_false: QtWidgets.QRadioButton
        self.radioButton_main_utane: QtWidgets.QRadioButton
        self.radioButton_main_card: QtWidgets.QRadioButton
        self.radioButton_main_foreigner: QtWidgets.QRadioButton
        self.radioButton_main_prevention: QtWidgets.QRadioButton
        self.radioButton_main_syuei: QtWidgets.QRadioButton
        self.radioButton_main_prevention2: QtWidgets.QRadioButton
        self.frame_main_mode: QtWidgets.QFrame
        self.radioButton_main_factory: QtWidgets.QRadioButton
        self.radioButton_main_payroll: QtWidgets.QRadioButton




        # self.frame_main_mode.show() # リピートモードのフレームを表示 / 非表示設定する __debug__
        self.main_window = parent
        # 型ヒント（文字列形式で循環インポート回避）
        self.main_window: 'MyMainWindow'  # type: ignore

        self.previous_output_path = None
        self.input_fobjs = []

        self.config_dict = self.main_window.read_config()
        self.main_window.config_dict = self.config_dict
        self.mode_config = self.main_window.mode_config_manager.modes[self.main_window.main_mode_init]
        self.is_start = False
        if self.main_window.is_frozen: # frozenの場合
            main_mode_init = self.main_window.main_mode_init
            for obj in self.frame_main_mode.findChildren(QtWidgets.QRadioButton):
                if obj.objectName().endswith(main_mode_init):
                    obj.setChecked(True)
            self.frame_main_mode.setVisible(False)
            self.resize(0, 0)

        if self.config_dict['input_mode'] == 'new1':
            self.comboBox_input_mode.setCurrentIndex(0)
            self.current_mode = 'new1'
            self.set_color_to_widget(self.comboBox_input_mode, 'blue', 'QComboBox')
        elif self.config_dict['input_mode'] == 'ver1':
            self.comboBox_input_mode.setCurrentIndex(1)
            self.current_mode = 'ver1'
            self.set_color_to_widget(self.comboBox_input_mode, 'red', 'QComboBox')
        for radio in [self.radioButton_main_foreigner, self.radioButton_main_utane, self.radioButton_main_card]:
            self.set_color_to_widget(radio, 'black')
            font = radio.font()
            font.setBold(False)
            radio.setFont(font)
        self.lineEdit_img_path.setReadOnly(True)
        self.lineEdit_output_path.setReadOnly(True)
        # 設定ファイルの読み込みと初期化処理...
        self.cwd = os.getcwd()
        img_dir_path = self.config_dict.get('img_dir_path', '')
        img_dir_path =  img_dir_path if os.path.exists(img_dir_path) else self.cwd # 存在しない場合はcwd
        img_fobj = Path(img_dir_path)
        output_path = self.config_dict.get('output_path', '')
        output_path = output_path if os.path.exists(output_path) else self.cwd # 存在しない場合はcwd
        output_fobj = Path(output_path)
        self.lineEdit_img_path.setText(str(img_fobj.resolve()))
        self.lineEdit_output_path.setText(str(output_fobj.resolve()))
        self.is_in_close_processing = False
        if self.radioButton_csvpath_true.isChecked():
            self.copy_img_path_to_csv_path()
        self.is_copy_csv_path = self.config_dict.get('is_copy_csv_path', True)
        if self.is_copy_csv_path:
            self.radioButton_csvpath_true.setChecked(True)
        else:
            self.radioButton_csvpath_false.setChecked(True)
        if self.config_dict['username']:
            self.lineEdit_username.setText(self.config_dict['username'])
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint) # ウィンドウフラグを設定して、クローズボタンを非表示にする
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.pushButton_start.setFocus()
        self.lineEdit_username.setFocus()
        self.pushButton_cancel.clicked.connect(self.emit_close_signal)
        self.pushButton_start.clicked.connect(self.start_main_window)
        self.pushButton_img_path_dialog.clicked.connect(self.select_image_dir_path)
        self.pushButton_output_path_dialog.clicked.connect(self.select_output_dir_path)
        self.comboBox_input_mode.currentTextChanged.connect(self.change_input_mode)
        self.radioButton_csvpath_true.clicked.connect(self.copy_img_path_to_csv_path)
        self.radioButton_csvpath_false.clicked.connect(self.set_previous_path_to_output_path)
        # # ショートカットキー...
        # self.shortcut_ctrl_a = QShortcut(QKeySequence('Ctrl+A'), self)
        # self.shortcut_ctrl_a.activated.connect(lambda: self.move_self('left'))

    def move_self(self, orientation: str):
        screen = self.screen()
        screen_geometry = screen.geometry()
        screen_w = screen_geometry.width()
        screen_h = screen_geometry.height()
        print(screen_w, screen_h)
        delta_x = 0
        delta_y = 0
        if orientation == 'up':
            delta_y = -100
        elif orientation == 'down':
            delta_y = 100
        elif orientation == 'left':
            delta_x = -100
        elif orientation == 'right':
            delta_x = 100
        x = max
        self.move(self.x() + delta_x, self.y() + delta_y)

    def set_data_list(self, main_mode):
        # mode_config_managerから直接取得
        # type: ModeConfigManager
        data_list = self.main_window.mode_config_manager.get_data_list(main_mode)
        if data_list is None:
            raise ValueError(f"不明なモード: {main_mode}")
        return data_list

    def get_and_check_previout_df(self, data_list, new1_file_path, main_mode):
        # headers = [data['index'] for data in data_list] # ヘッダーを取得 # DELETE
        # full_headers = headers + [10000, 20000, 30000] # DELETE
        full_headers = self.main_window.full_headers
        has_header = self.main_window.headers_dict[main_mode]['has_header']
        has_header = self.mode_config.has_header
        previous_df = DataIO.read_csv_with_header(
            self.main_window,
            new1_file_path,
            encoding=self.main_window.encode_type,
            headers=full_headers,
            has_header=has_header
        ) # WIP 20251107_1744_01

        if self.main_window.mode_config_manager.get_need_df_transformed(main_mode):
            valid_len = len(full_headers)
        else:
            valid_len = len(data_list) + 3
        if int(previous_df.shape[1]) != int(valid_len):
            QMessageBox.warning(self, 'エラー', '一次入力データの列の数が正しくありません\n\n'
                'CSVファイルを確認してください\n\n'
                f'一次入力データの列数: {previous_df.shape[1]}\n必要な列数: {len(data_list) + 3}\n\n'
                f'一次入力CSVパス: {new1_file_path}',
                QMessageBox.Ok)
            return None, False
        if previous_df.index.nlevels > 1: # インデックスがスカラーでない場合
            QMessageBox.warning(self, 'エラー', '一次入力データの列の数が正しくありません\n\n'
                    'CSVファイルを確認してください\n\n'
                    f'一次入力CSVパス: {new1_file_path}',
                    QMessageBox.Ok)
            return None, False
        if has_header:
            previous_df.columns = full_headers
        return previous_df, True

    # ファイル名,ファイル数の確認
    def check_file_count_and_file_name_for_verify(
        self, previous_df: pd.DataFrame, img_file_fobj_list,
        img_folder_pobj, previous_df_len, is_pdfmode, main_mode,
    ):
        img_file_count = len(img_file_fobj_list)
        current_fnames = [fobj.name for fobj in img_file_fobj_list]
        img_headers = [col for col in previous_df.columns if str(col) in ['10000', '画像名', '画像データ']] # IMPORTANT
        if img_headers:
            img_header = img_headers[0]
            previous_fnames = previous_df[img_header].to_list()
        else:
            previous_fnames = previous_df.iloc[:, -3].to_list() # 後ろから3つ目の列をリスト化(file name)
        # multi_pdfの場合
        if self.main_window.headers_dict[main_mode].get('is_multi_pdf', False):
            previous_fnames = [re.sub(r'_\d{2,4}(?=\.pdf)', '', fn) for fn in previous_fnames]
            previous_fnames = list(set(previous_fnames))
            previous_df_len = len(set(previous_fnames))

        required_filename = set(previous_fnames) - set(current_fnames)
        extra_filename = set(current_fnames) - set(previous_fnames)
        required_fn_text = '\n'.join(required_filename)
        extra_fn_text = '\n'.join(extra_filename)
        if not Counter(current_fnames) == Counter(previous_fnames):
            QMessageBox.warning(self, 'エラー',
                    '現在の画像ファイルが一次入力時の画像ファイルと異なります\nフォルダ内の画像と一次入力CSVを確認してください\n\n'
                    f'必要な画像ファイル名:\n{required_fn_text}\n\n'
                    f'余分と思われる画像ファイル名:\n{extra_fn_text}\n\n'
                    f'現在の画像フォルダ: {str(img_folder_pobj)}',
                    QMessageBox.Ok)
            return False
        elif img_file_count != previous_df_len:
            QMessageBox.warning(self, 'エラー',
                    '現在の画像ファイルの数が一次入力時の画像ファイルの数と異なります\n\nフォルダ内の画像を確認してください\n\n'
                    f'現在の画像数: {img_file_count}\n一次入力時の画像数: {previous_df_len}\n\n'
                    f'現在の画像フォルダ: {str(img_folder_pobj)}',
                    QMessageBox.Ok)
            return False
        return True

    def start_main_window(self):
        if self.main_window.is_frozen:
            main_mode = self.main_window.main_mode_init
        else:
            main_mode = self.main_window.main_mode_init
            if False:  # DELETE
                for radio_obj in self.frame_main_mode.findChildren(QtWidgets.QRadioButton):
                    if radio_obj.isChecked():
                        main_mode = radio_obj.objectName()[radio_obj.objectName().rfind('_') + 1:] # main_modeの取得
        # pdfシングルモード設定
        if self.main_window.mode_config_manager.get_is_single_pdf_mode_dict()[main_mode]: # 辞書からis_single_pdf_modeを取得
            self.main_window.is_single_pdf_mode = True
            is_single_pdf_mode = True
        else:
            self.main_window.is_single_pdf_mode = False
            is_single_pdf_mode = False
        # ____
        username = self.lineEdit_username.text()
        img_path = self.lineEdit_img_path.text()
        # pdf_mode確認（ModeConfigManagerから取得）
        file_type = self.main_window.mode_config_manager.get_file_type(main_mode)
        is_pdfmode = (file_type == 'pdf')
        # new1編集可能モード（現在は全モードでFalse）
        is_new1_no_edit = False
        # PDFモードで画像ファイルを読み込むか（ModeConfigManagerから取得）
        self.main_window.is_pdfmode_to_read_image_file = self.main_window.mode_config_manager.get_is_pdfmode_to_read_image_file(main_mode)
        is_rept_mode = self.main_window.mode_config_manager.get_is_rept_mode_dict()[main_mode] # メインモードからリピートモードを取得
        is_valid_img_path = False
        if is_pdfmode and not self.main_window.is_pdfmode_to_read_image_file:
            suffixes = ['.pdf']
        else:
            suffixes = ['.png', '.jpg', '.jpeg']
        for pobj in Path(img_path).resolve().iterdir():
            if pobj.suffix.lower() in suffixes:
                is_valid_img_path = True
                self.input_fobjs.append(pobj.resolve())
        is_valid_filename = True
        # ファイル名の確認が必要かどうか（ModeConfigManagerから取得）
        need_filename_check = self.main_window.mode_config_manager.get_need_filename_check()
        if need_filename_check:
            is_valid_filename, err_msg = self.main_window.data_transformer.check_filename(
                [fobj.name for fobj in self.input_fobjs]
            ) # return bool, str(err_msg)

        if not is_valid_img_path:
            if is_pdfmode:
                QMessageBox.warning(self, '警告', '画像ファイルが見つかりません\n\n対象画像ファイル[.pdf]')
            else:
                QMessageBox.warning(self, '警告', '画像ファイルが見つかりません\n\n対象画像ファイル[.png, .jpg, .jpeg]')
            return
        elif not is_valid_filename: # NEW ファイル名の形式が不正
            QMessageBox.warning(self, '警告', err_msg)
            return
        output_path = self.lineEdit_output_path.text()
        output_pobj = Path(output_path)
        img_folder_pobj = Path(img_path).resolve()
        img_parent_path = str(img_folder_pobj.parent.resolve())
        img_parent_name = str(img_folder_pobj.name)
        new1_file_path = Path(output_path).resolve() / f'{img_parent_name}_NEW1.csv'
        has_new1_file = os.path.exists(str(Path(new1_file_path).resolve()))
        answers_num = None
        if self.current_mode == 'ver1':
            if not has_new1_file: # ベリファイモードの場合のNewFile存在確認
                QMessageBox.warning(self, '警告',
                        '画像場所にNEW1.csvファイルが見つかりません\n\nNEW1.csvファイルの場所を選択してください')
                return
            ver1_csv_pobj = output_pobj / f'{img_folder_pobj.name}_VER1.csv'
            if os.path.exists(str(ver1_csv_pobj)): # すでにVER1ファイルが存在している場合
                if QMessageBox.warning(self, '確認', 'すでにVER1.csvファイルが存在しています\n\n'
                        '削除して新しくベリファイを行いますか？\n\n'
                        f'削除対象ファイル:\n{str(ver1_csv_pobj)}',
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                        )== QMessageBox.No:
                    return
                else: # YESの場合はファイルを削除
                    try:
                        os.remove(str(ver1_csv_pobj))
                        pass # 次 -> 新しいVER1ファイルを作成
                    except PermissionError:
                        QMessageBox.critical(self, 'エラー', 'VER1.csvファイルの削除に失敗しました\n\n' + 'ファイルが開かれていて削除できない可能性があります\n\n' +
                                f'対象ファイルパス；{str(ver1_csv_pobj)}')
                        return
                    with open(str(ver1_csv_pobj), 'w', encoding=self.main_window.encode_type) as f: # ログファイルの初期化
                        try:
                            f.write('')
                            pass #  # 次 -> ベリファイモードの場合のNewFile存在確認
                        except PermissionError:
                            QMessageBox.warning(self, 'エラー', 'VER1ファイルの作成に失敗しました', QMessageBox.Ok)
                            return
            QMessageBox.information(self, '確認', 'ベリファイモードで起動します')
        elif self.current_mode == 'new1':
            if has_new1_file: # 新規入力モードの場合のNewFile存在確認
                if not is_new1_no_edit:
                    answers_num = self.main_window.create_multi_button_msg(self, '確認',
                            'すでにNEW1ファイルが存在しています\n\n[新規] -> 既存のNEW1ファイルを削除して新規入力\n\n'
                            '[修正] -> 既存のNEW1ファイルを読み込んで修正\n\n'
                            f'対象ファイルパス:\n{str(new1_file_path)}',
                            ['新規', '修正', 'キャンセル'], default_index=1, icon_type='warning') # (self, parent, title, message, button_list) -> int:
                    if answers_num == 0: # 新規モード new1_file_pathを削除する
                        if QMessageBox.warning(self, '確認', '※再確認\nNEW1.csvファイルを削除して新規入力しますか？\n\n'
                                f'削除対象ファイルパス:\n{str(new1_file_path)}', QMessageBox.Yes | QMessageBox.No
                                ) == QMessageBox.No:
                            return
                        try:
                            os.remove(str(new1_file_path))
                        except PermissionError:
                            QMessageBox.critical(self, 'エラー', 'NEW1.csvファイルの削除に失敗しました\n\n' + 'ファイルが開かれていて削除できない可能性があります\n\n' +
                                    f'対象ファイルパス；{str(new1_file_path)}')
                            return
                    elif answers_num == 1: # 修正モード
                        pass
                    elif answers_num == 2: # キャンセル
                        return
                elif is_new1_no_edit:
                    if QMessageBox.warning(self, '確認', 'NEW1.csvファイルが存在しています\n\n'
                            '既存のNEW1ファイルを削除して新規入力しますか？\n\n'
                            f'削除対象ファイルパス:\n{str(new1_file_path)}', QMessageBox.Yes | QMessageBox.No
                            ) == QMessageBox.No:
                        return
                    if QMessageBox.warning(self, '確認', '※再確認\nNEW1.csvファイルを削除して新規入力しますか？\n\n'
                                f'削除対象ファイルパス:\n{str(new1_file_path)}', QMessageBox.Yes | QMessageBox.No
                                ) == QMessageBox.No:
                            return
                    try:
                        os.remove(str(new1_file_path))
                    except PermissionError:
                        QMessageBox.critical(self, 'エラー', 'NEW1.csvファイルの削除に失敗しました\n\n' + 'ファイルが開かれていて削除できない可能性があります\n\n' +
                                f'対象ファイルパス；{str(new1_file_path)}')
                        return
        previous_df = None
        data_list = self.main_window.data_list
        # previous_dfをチェック...
        if has_new1_file:
            if self.current_mode == 'ver1': # 修正モード、ベリファイモードの場合 pdfmodeは除く
                previous_df, is_valid_previous_df = self.get_and_check_previout_df(data_list, new1_file_path, main_mode)
                if not is_valid_previous_df:
                    return
                if (not is_pdfmode or is_single_pdf_mode) and not is_rept_mode:
                    # *** ファイル名のチェック ***
                    img_file_fobj_list = [p for p in img_folder_pobj.iterdir() if p.suffix.lower() in suffixes]
                    img_file_fobj_list = sorted(img_file_fobj_list, key=lambda x: x.name)
                    is_valid_files = self.check_file_count_and_file_name_for_verify(
                            previous_df, img_file_fobj_list, img_folder_pobj,
                            previous_df.shape[0], is_pdfmode, main_mode,
                    )
                    if not is_valid_files:
                        return
                    # *** ファイル名のチェック 終了 ***
        output_parent_path = str((Path(output_path).parent).resolve())
        if img_path == '' or output_path == '':
            QMessageBox.warning(self, '警告', '画像場所、出力場所を選択してください')
            return
        img_path = str(Path(img_path).resolve())
        output_path = str(Path(output_path).resolve())
        self.main_window.is_rept_mode = is_rept_mode
        if is_rept_mode:
            img_fobjs =  [img_fobj for img_fobj in Path(img_path).iterdir() if img_fobj.suffix.lower() in ['.png', '.jpg', '.jpeg']]
            if len(img_fobjs) != 1:
                QMessageBox.warning(self, '警告', 'リピートモードの場合は画像ファイルが1つだけである必要があります')
                return
        self.main_window.main_mode = main_mode # メインモードを設定
        self.main_window.previous_df = previous_df
        # self.main_window.data_list = data_list
        self.main_window.user_name = username
        self.main_window.img_dir_path = img_path
        self.main_window.output_path = output_path
        self.main_window.input_mode = self.current_mode
        self.main_window.is_pdfmode = is_pdfmode
        self.main_window.is_new1_no_edit = is_new1_no_edit
        self.main_window.input_fobjs = self.input_fobjs

        self.config_dict['username'] = username
        self.config_dict['img_dir_path'] = img_path
        self.config_dict['output_path'] = output_path
        self.config_dict['img_dir_parent_path'] = img_parent_path
        self.config_dict['output_parent_path'] = output_parent_path
        self.config_dict['input_mode'] = self.current_mode
        self.config_dict['main_mode'] = main_mode
        self.is_start = True
        self.close()

    def copy_img_path_to_csv_path(self):
        self.previous_output_path = self.lineEdit_output_path.text()
        self.lineEdit_output_path.setText(self.lineEdit_img_path.text())

    def set_previous_path_to_output_path(self):
        if self.previous_output_path and self.previous_output_path != self.lineEdit_output_path.text():
            self.lineEdit_output_path.setText(self.previous_output_path)

    def emit_close_signal(self):
        if self.is_in_close_processing:
            return
        if QMessageBox.question(self, '確認', '終了しますか？', QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            return # 終了しない場合
        self.is_in_close_processing = True
        self.main_window.is_in_close_processing = True
        if self.radioButton_csvpath_true.isChecked():
            self.config_dict['is_copy_csv_path'] =True
        elif self.radioButton_csvpath_false.isChecked():
            self.config_dict['is_copy_csv_path'] = False
        self.main_window.config_dict = self.config_dict
        self.main_window.write_config(self.config_dict)
        self.main_window.is_close_button_pressed = True # メインウィンドウ終了処理
        self.close_parent.emit()
        self.accept()

    def closeEvent(self, event):
        if self.radioButton_csvpath_true.isChecked():
            self.config_dict['is_copy_csv_path'] =True
        elif self.radioButton_csvpath_false.isChecked():
            self.config_dict['is_copy_csv_path'] = False
        self.main_window.config_dict = self.config_dict
        self.main_window.write_config(self.config_dict)
        if not self.is_start:
            self.emit_close_signal()
            super().closeEvent(event)

    def select_image_dir_path(self):
        parent_path = self.config_dict.get('img_dir_parent_path', '')
        init_dir_path = parent_path if os.path.exists(parent_path) else self.cwd
        dir_path = QFileDialog.getExistingDirectory(self, '画像フォルダを選択', init_dir_path)
        if dir_path:
            self.lineEdit_img_path.setText(dir_path)
            if self.radioButton_csvpath_true.isChecked(): # CSVファイルの場所と画像フォルダを同じにする場合
                self.lineEdit_output_path.setText(dir_path)

    def select_output_dir_path(self):
        if self.radioButton_csvpath_true.isChecked(): # CSVファイルの場所と画像フォルダを同じにする場合
            QMessageBox.information(
                    self, '確認',
                    '画像フォルダと異なる場所にCSVファイルを書き出す場合は\n\n上にあるラジオボタンを「いいえ」にしてください',
                    QMessageBox.Yes
            )
            return
        parent_path = self.config_dict.get('output_parent_path', '')
        init_dir_path = parent_path if os.path.exists(parent_path) else self.cwd
        dir_path = QFileDialog.getExistingDirectory(self, '出力フォルダを選択', init_dir_path)
        if dir_path:
            self.lineEdit_output_path.setText(dir_path)

    def change_input_mode(self, current_text):
        mode = current_text.split(': ')[0].lower()
        if mode == 'new1':
            self.set_color_to_widget(self.comboBox_input_mode, 'blue', 'QComboBox')
        elif mode == 'ver1':
            self.set_color_to_widget(self.comboBox_input_mode, 'red', 'QComboBox')
        self.current_mode = mode

    def set_color_to_widget(self, widget, color_text, widget_text='QWidget'):
        font = self.comboBox_input_mode.font()  # 現在のフォントを取得
        font_family = font.family()
        font_size = font.pointSize()
        widget.setStyleSheet(f"{widget_text} {{ color: {color_text}; font-family: {font_family}; font-size: {font_size}pt; }}")
        widget.setStyleSheet(f"{widget_text} {{ color: {color_text}; font-family: {font_family}; font-size: {font_size}pt; }}")
