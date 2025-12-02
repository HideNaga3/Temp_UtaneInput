import pandas as pd
from pathlib import Path
import pickle
import re

PREFECTURE_LST = [
    '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県',
    '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県',
    '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県',
    '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県',
    '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'
]

class PostNumReader:
    # ------------------------------------
    # self.is_valid_csv == Trueの場合
    # 親ウィンドウでself.conv_dfを使用できる
    # ------------------------------------
    def __init__(self, parent, is_debug: bool=False):
        if is_debug:
            print('__ini__ PostNumReader')
        self.main_window = parent
        self.conv_df = None
        # 変換後のCSVファイル検査
        new_headers = ['postnum', 'pref', 'city', 'town']
        self._converted_pkl_fp = './data/postnum/converted_postnum.pkl'
        conv_fobj = Path(self._converted_pkl_fp).absolute()
        self.is_valid_pkl = False
        if conv_fobj.exists(): # ________変換後のCSVファイルが存在する場合
            if is_debug:
                print('converted_postnum.pklが存在します')
            # DF検査
            try:
                with open(str(conv_fobj), 'rb') as pkl_f:
                    self.conv_df = pd.read_pickle(pkl_f)
                if not self.conv_df.columns.to_list() == new_headers:
                    if is_debug:
                        print('カラムが違います')
                else:
                    if is_debug:
                        print('正常なConverted CSVファイル')
                    self.is_valid_pkl = True
                    return # ここで終了 self.conv_dfをMainwindowで使う
            except Exception as e:
                print('変換後のCSVファイルが存在しない', e)
                # 処理を継続...
        try:
        # = 変換後のCSVに問題がある場合
            self._postnum_dp = './data/postnum'
            self._postnum_dobj = Path(self._postnum_dp).absolute()
            self._dl_csv_fobjs = [
                pobj for pobj in self._postnum_dobj.iterdir()
                if (
                    pobj.is_file() and pobj.suffix.lower() == '.csv' and
                    'converted_postnum' not in pobj.name
                )
            ]
            if not self._postnum_dobj.exists():
                if is_debug:
                    print('郵便番号フォルダが存在しない')
                return
            elif len(self._dl_csv_fobjs) !=1:
                if is_debug:
                    print('ダウンロードcsvファイルが 0 か 2 以上')
            dl_csv_fobj = self._dl_csv_fobjs[0]
            headers = [i for i in range(15)]
            dl_csv_df = pd.read_csv(str(dl_csv_fobj), encoding='utf-8', dtype=str, names=headers)
            dl_csv_df = dl_csv_df.drop([0,1,3,4,5,9,10,11,12,13,14], axis=1)
            dl_csv_df.columns = new_headers
            dl_csv_df = dl_csv_df.fillna('')
                    # dl_csv_df = dl_csv_df.drop_duplicates()
                    # dl_csv_df = dl_csv_df[dl_csv_df.duplicated(keep=False)]
            dl_csv_df['postnum'] = dl_csv_df['postnum'].str[:3] + '-' + dl_csv_df['postnum'].str[3:]
            dl_csv_df['town'] = dl_csv_df['town'].str.replace('以下に掲載がない場合', '')
            dl_csv_df['town'] = dl_csv_df['town'].str.split('（').str[0]
            for col in dl_csv_df.columns:
                dl_csv_df[col] = dl_csv_df[col].str.strip() # 前後の空白削除
            self.conv_df = dl_csv_df.copy()
            self.conv_df.to_csv(self._converted_pkl_fp, index=False, encoding='utf-8') # 変換後のCSVファイルを保存
            self.conv_df.to_pickle(self._converted_pkl_fp)
            if is_debug:
                print('変換後のpklファイルを作成しました')
            self.is_valid_pkl = True
        except Exception as e:
            if is_debug:
                print('postnum_df 使用不可', e)
            self.is_valid_pkl = False
            return

    def get_city_and_town_from_postnum(self, postnum: str) -> pd.DataFrame:
        if not self.is_valid_pkl or not postnum:
            return None
        postnum = postnum.strip()
        if re.search(r'^[0-9]{7}$', postnum):
            postnum = postnum[:3] + '-' + postnum[3:]
        pref_city_town_dicts = self.conv_df[self.conv_df['postnum'] == postnum].to_dict('records')
        if len(pref_city_town_dicts) > 0:
            pref_city_town_dict = pref_city_town_dicts[0]
            return pref_city_town_dict
        else:
            return None


if __name__ == '__main__':
    post_num_reader = PostNumReader('', is_debug=True)
    print('csvは使用可能か', post_num_reader.is_valid_pkl)

    print(post_num_reader.conv_df.head())

    import time
    start = time.time()
    print( di := post_num_reader.get_city_and_town_from_postnum('321-99995') )
    print('経過時間', time.time() - start)
    if di is None:
        print('該当なし')
        exit()

    pref, city, town = di['pref'], di['city'], di['town']
    print(pref, city, town)

"""
0. 全国地方公共団体コード（JIS X0401、X0402）………　半角数字
1. （旧）郵便番号（5桁）………………………………………　半角数字
    2. 郵便番号（7桁）………………………………………　半角数字
3. 都道府県名　…………　全角カタカナ（コード順に掲載）　（※1）
4. 市区町村名　…………　全角カタカナ（コード順に掲載）　（※1）
5. 町域名　………………　全角カタカナ（五十音順に掲載）　（※1）
    6. 都道府県名　…………　漢字（コード順に掲載）　（※1,2）
    7. 市区町村名　…………　漢字（コード順に掲載）　（※1,2）
    8. 町域名　………………　漢字（五十音順に掲載）　（※1,2）
"""
