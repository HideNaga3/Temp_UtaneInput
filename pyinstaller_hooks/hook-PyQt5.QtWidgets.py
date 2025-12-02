# PyQt5.QtWidgets用カスタムフック - 日本語パス対策
# hook-PyQt5_unified.pyから設定をインポート
import os
import sys

# hook-PyQt5_unified.pyの内容を実行
exec(open(os.path.join(os.path.dirname(__file__), 'hook-PyQt5_unified.py'), encoding='utf-8').read())

