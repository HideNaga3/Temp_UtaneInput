@echo off

:: Qt Designer UIファイルをPythonファイルに変換
pyuic5.exe main_app_ui.ui -o main_app_ui.py
pyuic5.exe _init_dialog_ui.ui -o _init_dialog_ui.py
pyuic5.exe _collation_dialog_ui.ui -o _collation_dialog_ui.py
pyuic5.exe _text_edit_dialog_ui.ui -o _text_edit_dialog_ui.py

echo 変換が完了しました
