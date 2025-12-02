# PyQt5統合カスタムフック - 日本語パス対策
# このフックはPyQt5, PyQt5.QtCore, PyQt5.QtGui, PyQt5.QtWidgets全てに対応
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, get_module_file_attribute
import os
import sys

# 仮想ドライブのパスを使用
venv_path = r'X:\.venv\Lib\site-packages\PyQt5'

datas = []
binaries = []

# 必要最小限のプラグインのみを収集
# platforms: 必須（アプリケーション起動に必要）
# styles: オプション（スタイル設定用、削除可能）
# imageformats: オプション（画像表示用、必要に応じて）
required_plugins = ['platforms', 'styles', 'imageformats']

qt5_plugins_path = os.path.join(venv_path, 'Qt5', 'plugins')
if os.path.exists(qt5_plugins_path):
    for plugin_name in required_plugins:
        plugin_full_path = os.path.join(qt5_plugins_path, plugin_name)
        if os.path.isdir(plugin_full_path):
            for file in os.listdir(plugin_full_path):
                if file.endswith('.dll'):
                    src = os.path.join(plugin_full_path, file)
                    dst = os.path.join('PyQt5', 'Qt5', 'plugins', plugin_name)
                    binaries.append((src, dst))

# 必要最小限のQt5 DLLのみを収集
required_dlls = [
    'Qt5Core.dll',      # 必須
    'Qt5Gui.dll',       # 必須
    'Qt5Widgets.dll',   # 必須
]

qt5_bin_path = os.path.join(venv_path, 'Qt5', 'bin')
if os.path.exists(qt5_bin_path):
    for dll_name in required_dlls:
        dll_path = os.path.join(qt5_bin_path, dll_name)
        if os.path.exists(dll_path):
            binaries.append((dll_path, os.path.join('PyQt5', 'Qt5', 'bin')))

# 隠しインポート
hiddenimports = ['PyQt5.sip']

# 除外するインポート
excludedimports = []
