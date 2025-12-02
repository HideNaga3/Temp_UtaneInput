# ソート時文字列を数値として解釈するためのプロキシモデル
from PyQt5.QtCore import QSortFilterProxyModel

class NumericSortProxyModel(QSortFilterProxyModel):
    def lessThan(self, left, right):
        # ソート対象のカラムが-1の場合は行インデックスで比較
        if left.column() == -1 or right.column() == -1:
            return left.row() < right.row()

        leftData = self.sourceModel().data(left)
        rightData = self.sourceModel().data(right)
        if leftData is None or rightData is None:
            return False # Noneが含まれる場合は比較不可
        try:# 数値として解釈可能かどうかをチェック
            leftData = float(leftData)
            rightData = float(rightData)
        except ValueError:
            pass # 数値として解釈できない場合はそのまま文字列として比較
        except TypeError:
            pass # タイプエラーが発生した場合はそのまま文字列として比較
        try:
            return leftData < rightData # 正常処理
        except TypeError:
            return False