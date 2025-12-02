from typing import TYPE_CHECKING
from PyQt5.QtWidgets import QApplication
from pprint import pprint as pp
from _lib._common_util import is_frozen, pr
from _lib._postnum_reader import PREFECTURE_LST

if TYPE_CHECKING:
    from MAIN_APP import MyMainWindow

import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 0)
pd.set_option('display.max_colwidth', None)

class Utane2:

    """ウタネ回覧用のデータ変換クラス"""
    def __init__(self, parent: "MyMainWindow"):
        self.main_window = parent
        self.is_frozen = self.main_window.is_frozen
        self.main_mode = self.main_window.main_mode_init
        self.mode_config_manager = self.main_window.mode_config_manager
        self.headers = self.mode_config_manager.get_headers(self.main_mode) # モードに応じたヘッダーリスト取得


    def transform_output_df(self, df: pd.DataFrame) -> pd.DataFrame: # WIP
        # df.columns = self.main_window.obj_name_lst + [10000, 20000, 30000] # DELETE
        for col in self.headers:
            if not col in df.columns:
                df[col] = ""
        df = self.strip_df(df)
        df = df[self.headers]
        df = self.input_df(df)
        return df


    def strip_df(self, df: pd.DataFrame) -> pd.DataFrame:
        '''DataFrame内の全ての文字列データの前後の空白を削除'''
        df = df.astype("string")
        for col in df.columns:
            df[col] = df[col].str.strip()
        return df


    def input_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df["画像ナンバー"] = df[10000] # ファイル名代入
        df['レコード№'] = df.index + 1

        # 得意先コードを追加
        df["得意先コード"] = df[10000].str.split("_").str[2].fillna("")

        # 通し番号
        df["通し№"] = (
            df[10000]
            .str.split("_").str[5].fillna("")
            .str.split(".").str[0].fillna("")
        )

        # 都道府県
        def extract_prefecture(addr: str) -> str:
            addr = addr.strip()
            for pref in PREFECTURE_LST:
                pref = pref.strip()
                if addr.startswith(pref):
                    return pref
            return ""
        df["都道府県"] = df["住所"].map(lambda addr: extract_prefecture((addr)))

        insert_char = self.main_window.insert_char

        df['フラッグ'] = df.apply(
            lambda row:
            int(row.astype(str).str.contains(insert_char).any()),
            axis=1
        )
        return df


    def check_filename(self, file_lst: list[str]) -> bool:
        for filename in file_lst:
            if filename.count("_") != 5:
                return False, f"ファイル名の形式が不正です: {filename}\n\n「_」の数が5つではありません"
        return True, ""



class DataTransformerFactory:
    """main_modeに応じて適切なTransformerクラスを生成"""

    def __init__(self, parent: 'MyMainWindow'):

        """
        Args:
            parent (MyMainWindow): メインウィンドウのインスタンス
        """
        self.main_window = parent
        self.main_mode = self.main_window.main_mode_init


    def get_transformer(self):

        if self.main_mode == 'utane2':
            return Utane2(self.main_window)
        else:
            return None





if __name__ == "__main__":
    def debug_output_list(lst, filename: str = "debug_output.txt"):
        lst = [str(x) for x in lst]
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lst))
    sample_lst = ["a", " b ", "　c　", "None", "dｅｆ", "１２３"]
    debug_output_list(sample_lst, "temp/debug_output.txt")
