# _helper_classes.py
# ヘルパークラス群 - IMEThread, SingleApplication
# MAIN_APP.pyから分離
#
# 作成日: 2025-10-25
# Phase: 小規模独立クラスの分離

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSharedMemory

from _lib._ime_control import set_ime_mode_jp_or_en


class IMEThread(QThread):
    """IME制御用スレッド

    日本語/英語入力モードを非同期で設定します。
    """
    finished = pyqtSignal(str)

    def __init__(self, mode: str):
        """初期化

        Args:
            mode: IMEモード ("jp" or "en")
        """
        super().__init__()
        self.mode = mode

    def run(self):
        """スレッド実行処理

        IMEモードを設定し、結果をfinishedシグナルで通知します。
        """
        try:
            set_ime_mode_jp_or_en(self.mode)
            self.finished.emit(f"IME mode set to {self.mode} successfully.")
        except Exception as e:
            try:
                self.finished.emit(f"IMEThread.run(): {e}")
            except Exception as e:
                print(f"IMEThread.run(): {e}")


class SingleApplication(QApplication):
    """シングルトンアプリケーションクラス

    QSharedMemoryを使用してアプリケーションの多重起動を防止します。

    Note:
        現在このクラスは使用されていません（MAIN_APP.pyでコメントアウト）。
        代わりにctypesのミューテックスを使用した多重起動防止が実装されています。
    """

    def __init__(self, argv):
        """初期化

        Args:
            argv: コマンドライン引数のリスト
        """
        super().__init__(argv)
        self._memory = None

    def exec_(self):
        """アプリケーション実行

        QSharedMemoryでインスタンスの存在を確認し、
        既に起動している場合はFalseを返して終了します。

        Returns:
            bool or int: 既に起動している場合はFalse、
                        正常に起動した場合はアプリケーションの終了コード
        """
        self._memory = QSharedMemory(self.applicationName())
        if self._memory.attach():
            # 他のインスタンスが存在する場合は終了
            return False
        self._memory.create(1)
        return super().exec_()

    def quit(self):
        """アプリケーション終了

        QSharedMemoryをデタッチしてから終了します。
        """
        if self._memory:
            self._memory.detach()
        super().quit()
