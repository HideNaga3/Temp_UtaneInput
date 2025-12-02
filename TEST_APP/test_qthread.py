import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox

# QThreadを継承したクラスを作成
class WorkerThread(QThread):
    update_signal = pyqtSignal(int)  # 値の更新を通知するシグナル
    msg_signal = pyqtSignal(str)  # メッセージを通知するシグナル

    def run(self):
        for i in range(1, 11):
            self.sleep(1)  # スレッド内で1秒間待機
            self.update_signal.emit(i)  # 値をシグナルで送信
            if i == 5:
                self.msg_signal.emit(f'カウントが{i}になりました。')  # メッセージをシグナルで送信

# メインウィンドウクラス
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel("カウント: 0", self)
        self.button = QPushButton("スタート", self)
        self.button.clicked.connect(self.start_thread) # ボタンクリック時にスレッドを開始

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.worker_thread = WorkerThread() # ワーカースレッドインスタンス作成 <---重要
        # self.worker_thread.finished.connect(self.worker_thread.deleteLater) # スレッド終了時に削除 何度も使う場合はコメントアウト
        self.worker_thread.update_signal.connect(self.update_label) # カウントのシグナル
        self.worker_thread.msg_signal.connect(self.show_msg) # メッセージのシグナル

    def show_msg(self, msg):
        QMessageBox.information(self, "5秒時のメッセージ", msg)

    def start_thread(self):
        self.worker_thread.start()  # スレッドを開始 start()

    def update_label(self, value):
        self.label.setText(f"カウント: {value}")

# アプリケーションの実行
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
