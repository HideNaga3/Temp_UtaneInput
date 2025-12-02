from PyQt5.QtWidgets import QLineEdit, QCompleter, QApplication
from PyQt5.QtCore import Qt
import sys

class CustomLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.completer_items = ['70004','70000','70005','70008','70007','70040','70041','70042','70100','70106','70104','70102','70099','70103','70098','70093','70091','70092','70096','70090','12345','70304','70311','70303','70329','70312','70315','70335','70309','12333','70305','70324','12320','70307','70314','60172','70322','70333','70326','70374','70370','70373','70371','70433','22702','70400','70401','70410','70407','70404','70470','70475','70472','70473','70471','60103','70450','16550','70453','70451','70520','70527','70523','70535','70537','70526','70532','70524','70525','70529','70531','70530','70060','70063','70065','70601','70500','70504','70502','06130','70635','70620','70611','70632','70648','70623','70629','70572','70571','70808','70802','70807','70809','70801','70803','70805','70840','70842'] # リスト作成
        self.completer_items = sorted(self.completer_items, key=lambda x: int(x))
        self.completer = QCompleter(self.completer_items) # インスタンス作成 リストを渡す
        self.setCompleter(self.completer) # QLineEdit.setCompleter()でコンプリーターを設定
        self.is_completer_active = True

    def keyPressEvent(self, event):
        # IMEがアクティブな場合、コンプリートを無効にする
        # if event.key() in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Enter, Qt.Key_Return):
        #     if not self.is_completer_active:
        #         self.is_completer_active = True
        # else:
        #     if self.hasFocus() and self.inputMethodHints() == Qt.ImhPreferNumbers:
        #         self.is_completer_active = False
        super().keyPressEvent(event)

app = QApplication(sys.argv)
window = CustomLineEdit()
window.show()
sys.exit(app.exec_())
