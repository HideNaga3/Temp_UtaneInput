# _mode_config.py
# モード設定を一元管理するモジュール
# MAIN_APP.pyから分離したモード設定

from dataclasses import dataclass
from typing import List, Dict, Optional, Any

# MAIN_APP.pyからインポートが必要なモジュール
# 実際の使用時には以下のインポートが必要
# from _create_data_list import create_data_list, create_frame_list
@dataclass
class ModeConfig:
    """
    1つのモードの設定を保持するデータクラス

    Attributes:
        mode_id: モードID ('payroll', 'card', 'utane', etc.)
        jp_name: 日本語名 ('給与検定', '名刺', etc.)
        title: ウィンドウタイトル
        file_type: ファイルタイプ ('img' or 'pdf')
        is_rept_mode: リピートモードかどうか
        is_single_pdf_mode: 1PDF1画像モードかどうか
        has_header: CSVヘッダーがあるか
        headers: CSVヘッダーリスト
        data_list: データリスト定義（create_data_listの結果）
        frame_list: フレームリスト定義（create_frame_listの結果）
        is_multi_pdf: 複数PDFモードかどうか（デフォルトFalse）
        is_pdfmode_to_read_image_file: PDFモードで画像ファイルを読み込むか（デフォルトFalse）
        df_name_column_index: DataFrameの氏名列インデックス（Noneの場合は氏名なし、空文字列を返す）
    """
    mode_id: str
    jp_name: str
    title: str
    file_type: str
    is_rept_mode: bool
    is_single_pdf_mode: bool
    has_header: bool
    headers: Optional[List[str]]
    data_list: List[Dict]
    frame_list: List[Dict]
    is_multi_pdf: bool = False
    is_pdfmode_to_read_image_file: bool = False
    df_name_column_index: Optional[int] = None
    need_df_transformed: bool = False  # DataFrame変換が必要かどうか（デフォルトFalse）
    need_filename_check: bool = False # ファイル名チェックが必要かどうか（デフォルトFalse）
    label_font_point: int = 10
    label_font_is_bold: bool = False


class ModeConfigManager:
    """
    すべてのモード設定を管理するクラス

    MAIN_APP.pyから分離されたモード設定を一元管理します。
    モード追加時は _init_all_modes() メソッド内に1箇所追加するだけでOKです。
    """

    def __init__(self, create_data_list_func=None, create_frame_list_func=None):
        """
        初期化

        Args:
            create_data_list_func: create_data_list関数（テスト時はモック可能）
            create_frame_list_func: create_frame_list関数（テスト時はモック可能）
        """
        import MAIN_APP
        self.modes: Dict[str, ModeConfig] = {}
        self.create_data_list = create_data_list_func
        self.create_frame_list = create_frame_list_func
        self.main_mode = MAIN_APP.G_MAIN_MODE

        if self.create_data_list and self.create_frame_list:
            self._init_all_modes()
            self.mode = self.modes[self.main_mode]  # モード設定を初期化, これを使ってgetプロパティを提供する

    def _init_all_modes(self):
        """すべてのモード設定を初期化"""
        # ========== utane2モード（ウタネ回覧2） ==========
        if self.main_mode == "utane2":
            utane2_headers = [
                'レコード№', '個人コード', '氏名', '郵便番号', '住所', '住所②', '電話番号', '得意先コード', '通し№', '70170', '37501', '37502', '70174', '70260', '70134', '37619', '70142',
                '70130', '60212', '70240', '70191', '17597', '18601', '60183', '60184', '37706', '70212', '70213', '60086', '70211', '70858', '60028', '60222', '70856', '38109', '70851',
                '70854', '70327', '70300', '70330', '19637', '70892', '37750', '20646', '60200', '13454', '70370', '37975', '70431', '70433', '37330', '38022', '70406', '60186', '14516',
                '70601', '70457', '70450', '70451', '70453', '70060', '70063', '60176', '70005', '70000', '70004', '70040', '70041', '70091', '70503', '70502', '70639', '60124', '60116',
                '70521', '70533', '70600', '09235', '70572', '70592', '30898', '30884', '30918', '30852', '12441', '90513', '90013', '28826', '38283', '70697', '70700', '70694', '70690',
                '60053', '70695', '70693', '70801', '70808', '70757', '70754', '70752', '70751', '70759', '70760', '38163', '70741', '70740', '画像ナンバー', '都道府県', 'フラッグ',
                10000, 20000, 30000,
            ]
            self.modes['utane2'] = ModeConfig(
                mode_id='utane2',
                jp_name='ウタネ回覧入力',
                title='ウタネ回覧入力ソフト',
                file_type='pdf',
                is_rept_mode=False,
                is_single_pdf_mode=True,
                has_header=True,
                headers=utane2_headers,
                data_list=self.create_data_list('utane2'),
                frame_list=self.create_frame_list('utane2'),
                is_pdfmode_to_read_image_file=True,
                df_name_column_index=1,  # 氏名列なし（空文字列を返す）
                need_df_transformed=True,  # DataFrame変換が必要
                need_filename_check=True,
                label_font_point = 12,
                label_font_is_bold = True,
            )

        # ========== Payrollモード（給与検定） ==========
        if self.main_mode == "payroll":
            self.modes['payroll'] = ModeConfig(
                mode_id='payroll',
                jp_name='給与検定1級',
                title='給与計算検定1級入力ソフト',
                file_type='pdf',
                is_rept_mode=False,
                is_single_pdf_mode=True,
                has_header=False,
                headers=None,
                data_list=self.create_data_list('payroll'),
                frame_list=self.create_frame_list('payroll'),
                df_name_column_index=2  # 氏名は2列目
            )

        # ========== Payrollモード（給与検定[2級]） ==========
        if self.main_mode == "payroll2":
            self.modes['payroll2'] = ModeConfig(
                mode_id='payroll2',
                jp_name='給与検定2級',
                title='給与計算検定2級入力ソフト',
                file_type='pdf',
                is_rept_mode=False,
                is_single_pdf_mode=True,
                has_header=False,
                headers=None,
                data_list=self.create_data_list('payroll2'),
                frame_list=self.create_frame_list('payroll2'),
                df_name_column_index=2  # 氏名は2列目
            )

        # ========== Syueiモード（イベント応募） ==========
        # syuei_headers = [
        #     '掲載号', '郵便番号', '住所①(都道府県)', '住所②（市町村・区）', '住所③（番地）', '住所④（建物名・部屋番号）',
        #     'カナ氏名（ふりがな）', '氏名', '電話番号', '年齢', '性別', '学校欄', '学年', '職業', '会場（1東京／2大阪）',
        #     '参加人数', '当選確率アップ券(1・アップ券あり）', 'チェック'
        # ]

        # self.modes['syuei'] = ModeConfig(
        #     mode_id='syuei',
        #     jp_name='イベント応募',
        #     title='イベント応募はがき入力アプリ',
        #     file_type='pdf',
        #     is_rept_mode=False,
        #     is_single_pdf_mode=True,
        #     has_header=True,
        #     headers=syuei_headers,
        #     data_list=self.create_data_list('syuei'),
        #     frame_list=self.create_frame_list('syuei'),
        #     is_pdfmode_to_read_image_file=True  # ! PDFモードで画像ファイルを読み込む
        # )


    # ========== アクセサメソッド ==========

    def get_mode(self, mode_id: str) -> Optional[ModeConfig]:
        """
        モード設定を取得

        Args:
            mode_id: モードID

        Returns:
            ModeConfig: モード設定（存在しない場合はNone）
        """
        return self.modes.get(mode_id)

    def get_all_mode_ids(self) -> List[str]:
        """
        すべてのモードIDを取得

        Returns:
            List[str]: モードIDのリスト
        """
        return list(self.modes.keys())

    def get_jp_name(self, mode_id: str) -> Optional[str]:
        """
        日本語名を取得

        Args:
            mode_id: モードID

        Returns:
            str: 日本語名（存在しない場合はNone）
        """
        mode = self.modes.get(mode_id)
        return mode.jp_name if mode else None

    def get_title(self, mode_id: str) -> Optional[str]:
        """
        ウィンドウタイトルを取得

        Args:
            mode_id: モードID

        Returns:
            str: ウィンドウタイトル（存在しない場合はNone）
        """
        mode = self.modes.get(mode_id)
        return mode.title if mode else None

    def get_file_type(self, mode_id: str) -> Optional[str]:
        """
        ファイルタイプを取得

        Args:
            mode_id: モードID

        Returns:
            str: ファイルタイプ ('img' or 'pdf')（存在しない場合はNone）
        """
        mode = self.modes.get(mode_id)
        return mode.file_type if mode else None

    def get_is_rept_mode(self, mode_id: str) -> bool:
        """
        リピートモードかどうかを取得

        Args:
            mode_id: モードID

        Returns:
            bool: リピートモードかどうか（存在しない場合はFalse）
        """
        mode = self.modes.get(mode_id)
        return mode.is_rept_mode if mode else False

    def get_is_single_pdf_mode(self, mode_id: str) -> bool:
        """
        シングルPDFモードかどうかを取得

        Args:
            mode_id: モードID

        Returns:
            bool: シングルPDFモードかどうか（存在しない場合はFalse）
        """
        mode = self.modes.get(mode_id)
        return mode.is_single_pdf_mode if mode else False

    def get_is_pdfmode_to_read_image_file(self, mode_id: str) -> bool:
        """
        PDFモードで画像ファイルを読み込むかどうかを取得

        Args:
            mode_id: モードID

        Returns:
            bool: PDFモードで画像ファイルを読み込むか（存在しない場合はFalse）
        """
        mode = self.modes.get(mode_id)
        return mode.is_pdfmode_to_read_image_file if mode else False

    def get_data_list(self, mode_id: str) -> Optional[List[Dict]]:
        """
        データリストを取得

        Args:
            mode_id: モードID

        Returns:
            List[Dict]: データリスト（存在しない場合はNone）
        """
        mode = self.modes.get(mode_id)
        return mode.data_list if mode else None

    def get_frame_list(self, mode_id: str) -> Optional[List[Dict]]:
        """
        フレームリストを取得

        Args:
            mode_id: モードID

        Returns:
            List[Dict]: フレームリスト（存在しない場合はNone）
        """
        mode = self.modes.get(mode_id)
        return mode.frame_list if mode else None

    def get_headers(self, mode_id: str) -> Optional[List[str]]:
        """
        CSVヘッダーを取得

        Args:
            mode_id: モードID

        Returns:
            List[str]: ヘッダーリスト（存在しない場合はNone）
        """
        mode = self.modes.get(mode_id)
        return mode.headers if mode else None

    def has_header(self, mode_id: str) -> bool:
        """
        CSVヘッダーがあるかどうかを取得

        Args:
            mode_id: モードID

        Returns:
            bool: ヘッダーがあるかどうか（存在しない場合はFalse）
        """
        mode = self.modes.get(mode_id)
        return mode.has_header if mode else False

    def is_multi_pdf(self, mode_id: str) -> bool:
        """
        複数PDFモードかどうかを取得

        Args:
            mode_id: モードID

        Returns:
            bool: 複数PDFモードかどうか（存在しない場合はFalse）
        """
        mode = self.modes.get(mode_id)
        return mode.is_multi_pdf if mode else False

    def get_df_name_column_index(self, mode_id: str) -> Optional[int]:
        """
        DataFrameの氏名列インデックスを取得

        Args:
            mode_id: モードID

        Returns:
            Optional[int]: 氏名列のインデックス（存在しない場合またはNoneの場合はNone）
        """
        mode = self.modes.get(mode_id)
        return mode.df_name_column_index if mode else None


    def get_need_df_transformed(self, mode_id: str) -> Optional[int]:
        mode = self.modes.get(mode_id)
        return mode.need_df_transformed if mode else None


    def get_name_from_df(self, mode_id: str, df, row_index: int) -> str:
        """
        モード設定に基づいてDataFrameから氏名を取得

        Args:
            mode_id: モードID
            df: DataFrame
            row_index: 行インデックス

        Returns:
            str: 氏名（設定がない場合は空文字列）
        """
        df_name_col_idx = self.get_df_name_column_index(mode_id)
        if df_name_col_idx is not None:
            return str(df.iloc[row_index, df_name_col_idx])
        else:
            return ""  # DataFrameにアクセスせず空文字列

    # ========== 互換性のための辞書形式アクセス ==========
    # MAIN_APP.pyの既存コードとの互換性を保つため、辞書形式でのアクセスも提供

    def get_jp_name_dict(self) -> Dict[str, str]:
        """
        全モードの日本語名を辞書形式で取得（互換性用）

        Returns:
            Dict[str, str]: {mode_id: jp_name}
        """
        return {mode_id: mode.jp_name for mode_id, mode in self.modes.items()}

    def get_title_dict(self) -> Dict[str, str]:
        """
        全モードのタイトルを辞書形式で取得（互換性用）

        Returns:
            Dict[str, str]: {mode_id: title}
        """
        return {mode_id: mode.title for mode_id, mode in self.modes.items()}

    def get_file_type_dict(self) -> Dict[str, str]:
        """
        全モードのファイルタイプを辞書形式で取得（互換性用）

        Returns:
            Dict[str, str]: {mode_id: file_type}
        """
        return {mode_id: mode.file_type for mode_id, mode in self.modes.items()}

    def get_is_rept_mode_dict(self) -> Dict[str, bool]:
        """
        全モードのリピートモード設定を辞書形式で取得（互換性用）

        Returns:
            Dict[str, bool]: {mode_id: is_rept_mode}
        """
        return {mode_id: mode.is_rept_mode for mode_id, mode in self.modes.items()}

    def get_is_single_pdf_mode_dict(self) -> Dict[str, bool]:
        """
        全モードのシングルPDFモード設定を辞書形式で取得（互換性用）

        Returns:
            Dict[str, bool]: {mode_id: is_single_pdf_mode}
        """
        return {mode_id: mode.is_single_pdf_mode for mode_id, mode in self.modes.items()}

    def get_label_font_point(self) -> int:
        return self.mode.label_font_point

    def get_label_font_is_bold(self) -> bool:
        return self.mode.label_font_is_bold

    def get_need_filename_check(self) -> bool:
        return self.mode.need_filename_check


    def get_headers_dict(self) -> Dict[str, Dict[str, Any]]:
        """
        全モードのヘッダー設定を辞書形式で取得（互換性用）

        Returns:
            Dict[str, Dict]: {mode_id: {'has_header': bool, 'headers': List[str], ...}}
        """
        result = {}
        for mode_id, mode in self.modes.items():
            result[mode_id] = {
                'has_header': mode.has_header,
                'headers': mode.headers
            }
            if mode.is_multi_pdf:
                result[mode_id]['is_multi_pdf'] = True
        return result


# ========== テスト・デバッグ用 ==========

if __name__ == '__main__':
    # テスト用のモック関数
    def mock_create_data_list(mode_id):
        """テスト用のモック関数"""
        return [{'name': f'{mode_id}_data_{i}'} for i in range(3)]

    def mock_create_frame_list(mode_id):
        """テスト用のモック関数"""
        return [{'name': f'{mode_id}_frame_{i}'} for i in range(2)]

    # ModeConfigManagerを作成
    manager = ModeConfigManager(
        create_data_list_func=mock_create_data_list,
        create_frame_list_func=mock_create_frame_list
    )

    print('[OK] ModeConfigManager初期化完了')
    print(f'[OK] 登録モード数: {len(manager.get_all_mode_ids())}')
    print(f'[OK] モードID一覧: {manager.get_all_mode_ids()}')
    print()

    # 各モードの情報を表示
    for mode_id in manager.get_all_mode_ids():
        mode = manager.get_mode(mode_id)
        print(f'モードID: {mode_id}')
        print(f'  日本語名: {mode.jp_name}')
        print(f'  タイトル: {mode.title}')
        print(f'  ファイルタイプ: {mode.file_type}')
        print(f'  リピートモード: {mode.is_rept_mode}')
        print(f'  シングルPDFモード: {mode.is_single_pdf_mode}')
        print(f'  ヘッダーあり: {mode.has_header}')
        if mode.headers:
            print(f'  ヘッダー数: {len(mode.headers)}')
        print()

    # 互換性メソッドのテスト
    print('[OK] 互換性メソッドテスト')
    print(f'日本語名辞書: {manager.get_jp_name_dict()}')
    print(f'リピートモード辞書: {manager.get_is_rept_mode_dict()}')
