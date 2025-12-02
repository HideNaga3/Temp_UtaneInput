# _data_io.py
# データ入出力のヘルパー関数
# CSV読み書きの共通処理を提供
#
# 作成日: 2025-10-25
# Phase 4: データ入出力層の分離（簡易版）

from pathlib import Path
from typing import Union, Optional, List, TYPE_CHECKING
import pandas as pd
from pprint import pprint as pp

if TYPE_CHECKING:
    from MAIN_APP import MyMainWindow

class DataIO:
    """データ入出力のヘルパークラス

    CSV読み書きの共通処理を提供します。
    """

    @staticmethod
    def read_csv_with_header(
        parent: 'MyMainWindow',
        file_path: Union[str, Path],
        encoding: str = 'cp932',
        headers: Optional[List[str]] = None,
        has_header: bool = True,
    ) -> pd.DataFrame:
        """CSVファイルを読み込む（ヘッダー有無対応）

        """
        if has_header:
            # ヘッダー行がある場合はskiprows=1でヘッダーをスキップ
            df = pd.read_csv(
                str(file_path),
                encoding=encoding,
                names=headers,
                dtype=str,
                skiprows=1,
            )
        else:
            # ヘッダー行がない場合
            df = pd.read_csv(
                str(file_path),
                encoding=encoding,
                names=headers,
                dtype=str,
                header=None,
            )

        # NaNを空文字に変換
        df = df.fillna('')
        df = df.astype(str)

        return df

    @staticmethod
    def write_csv_with_header(
        parent: 'MyMainWindow',
        df: pd.DataFrame,
        file_path: Union[str, Path],
        encoding: str = 'cp932',
        has_header: bool = True
    ) -> None:
        """DataFrameをCSVファイルに書き込む（ヘッダー有無対応）"""
        df.to_csv(
            str(file_path),
            index=False,
            encoding=encoding,
            header=has_header,
            errors='replace'
        )
        # df.to_pickle("jupyter\output_utane2.pkl")
        # print("export to pickle")
        pass # WIP 20251106

# ==================== 単体テスト ====================

def test_data_io():
    """DataIO の簡易テスト"""


if __name__ == '__main__':
    test_data_io()
