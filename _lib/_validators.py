# _validators.py
# 入力値検証を担当するモジュール
# MAIN_APP.pyから分離したバリデーションメソッド

import re
from datetime import datetime
from typing import Optional, List, Dict, Tuple, Union


class InputValidator:
    """
    入力値の検証を担当するクラス

    MAIN_APP.pyから分離された26個のバリデーションメソッドを集約します。
    各メソッドは独立して使用でき、テストも容易です。
    """

    def __init__(self, sublib=None, encode_type='cp932'):
        """
        初期化

        Args:
            sublib: _sub_lib.SubLibのインスタンス（文字変換用）
            encode_type: エンコーディングタイプ（デフォルト: cp932）
        """
        self.sublib = sublib
        self.encode_type = encode_type

    # ========== 基本検証メソッド ==========

    def is_not_empty(self, s: str) -> bool:
        """
        空文字チェック

        Args:
            s: 検証する文字列

        Returns:
            bool: 空文字でない場合True
        """
        return True if s != '' else False

    def is_valid_date(self, s: str) -> bool:
        """
        日付形式チェック

        対応形式: YYYY/MM/DD, YYYY-MM-DD
        空文字またはNoneの場合はTrue

        Args:
            s: 検証する文字列

        Returns:
            bool: 有効な日付の場合True
        """
        if s == '' or s is None:
            return True
        formats = ['%Y/%m/%d', '%Y-%m-%d']
        for format in formats:
            try:
                datetime.strptime(s, format)
                return True
            except ValueError:
                continue
        return False

    def is_int(self, s: str) -> bool:
        """
        整数チェック

        空文字またはNoneの場合はTrue

        Args:
            s: 検証する文字列

        Returns:
            bool: 整数に変換可能な場合True
        """
        if s == '' or s is None:
            return True
        try:
            int(s)
            return True
        except ValueError:
            return False

    def is_float(self, s: str) -> bool:
        """
        浮動小数点数チェック

        空文字またはNoneの場合はTrue

        Args:
            s: 検証する文字列

        Returns:
            bool: 浮動小数点数に変換可能な場合True
        """
        if s == '' or s is None:
            return True
        try:
            float(s)
            return True
        except ValueError:
            return False

    def is_alphanumeric(self, s: str) -> bool:
        """
        英数字チェック（半角）

        空文字またはNoneの場合はTrue

        Args:
            s: 検証する文字列

        Returns:
            bool: 半角英数字のみの場合True
        """
        if s == '' or s is None:
            return True
        p = r'^[a-zA-Z0-9]+$'
        return True if re.match(p, s) else False

    # ========== 郵便番号・電話番号検証 ==========

    def is_post_number(self, s: str) -> bool:
        """
        郵便番号チェック（ハイフン付き）

        形式: 123-4567
        空文字またはNoneの場合はTrue

        Args:
            s: 検証する文字列

        Returns:
            bool: 郵便番号形式の場合True
        """
        if s == '' or s is None:
            return True
        return re.fullmatch(r'\d{3}-\d{4}', s) is not None

    def is_post_number_kuromaru(self, s: str) -> bool:
        """
        郵便番号チェック（●許可）

        形式: 123-4567, ●●●-●●●●, ● など
        空文字またはNoneの場合はTrue

        Args:
            s: 検証する文字列

        Returns:
            bool: 郵便番号形式（●許可）の場合True
        """
        if s == '' or s is None:
            return True
        return re.fullmatch(r'[\d●]{3}[\-●]?[\d●]{4}|●', s) is not None

    def is_tel_number(self, s: str) -> bool:
        """
        電話番号チェック

        形式: 080-3456-7890, 0123-45-6789, 1-2-123 など
        空文字またはNoneの場合はTrue

        Args:
            s: 検証する文字列

        Returns:
            bool: 電話番号形式の場合True
        """
        if s == '' or s is None:
            return True
        return re.fullmatch(r'\d{1,4}\-\d{1,4}\-\d{3,4}', s) is not None

    # ========== 文字種検証 ==========

    def is_hankaku(self, s: str) -> bool:
        """
        半角文字チェック

        空文字またはNoneの場合はTrue
        sublibが必要

        Args:
            s: 検証する文字列

        Returns:
            bool: すべて半角文字の場合True
        """
        if s == '' or s is None:
            return True
        if self.sublib is None:
            raise ValueError('sublibが設定されていません')
        # 文字列の各文字が半角かどうかをチェック
        for char in s:
            if self.sublib.z2h(char) != char:
                return False
        return True

    def is_zenkaku(self, s: str) -> bool:
        """
        全角文字チェック

        空文字またはNoneの場合はTrue
        sublibが必要

        Args:
            s: 検証する文字列

        Returns:
            bool: すべて全角文字の場合True
        """
        if s == '' or s is None:
            return True
        if self.sublib is None:
            raise ValueError('sublibが設定されていません')
        # 文字列の各文字が全角かどうかをチェック
        for char in s:
            if self.sublib.h2z(char) != char:
                return False
        return True

    def is_hankaku_eisu_kuromaru(self, s: str) -> bool:
        """
        半角英数字と●のみチェック

        空文字またはNoneの場合はTrue

        Args:
            s: 検証する文字列

        Returns:
            bool: 半角英数字と●のみの場合True
        """
        if s == '' or s is None:
            return True
        p = r'^[A-Za-z0-9●]+$'
        return True if re.match(p, s) else False

    def is_hankaku_kuromaru(self, s: str) -> bool:
        """
        半角文字と●のみチェック

        空文字またはNoneの場合はTrue
        sublibが必要

        Args:
            s: 検証する文字列

        Returns:
            bool: 半角文字または●のみの場合True
        """
        if s == '' or s is None:
            return True
        if self.sublib is None:
            raise ValueError('sublibが設定されていません')
        # 文字列の各文字が半角または●かどうかをチェック
        for char in s:
            if self.sublib.z2h(char) != char and char != '●':
                return False
        return True

    def is_zenkaku_katakana_kuromaru(self, s: str) -> bool:
        """
        全角カタカナと●のみチェック

        空文字またはNoneの場合はTrue

        Args:
            s: 検証する文字列

        Returns:
            bool: 全角カタカナと●のみの場合True
        """
        if s == '' or s is None:
            return True
        p = r'^[ァ-ヴ●]+$'
        return True if re.match(p, s) else False

    def is_hiragana_kuromaru(self, s: str) -> bool:
        """
        ひらがなと●のみチェック

        空文字またはNoneの場合はTrue

        Args:
            s: 検証する文字列

        Returns:
            bool: ひらがなと●のみの場合True
        """
        if s == '' or s is None:
            return True
        re_p = re.compile(r'^[ぁ-ゖゝ-ゟー●]+$')
        return True if re_p.match(s) else False

    # ========== エンコーディング検証 ==========

    def is_encodable(self, s: str, enable_return: bool = False) -> Union[bool, Tuple[str, int]]:
        """
        エンコード可能チェック

        Args:
            s: 検証する文字列
            enable_return: Trueの場合、エラー情報を返す

        Returns:
            bool or tuple: エンコード可能な場合True、
                          enable_return=Trueの場合はエラー文字とその位置のタプル
        """
        if s == '' or s is None:
            return True
        try:
            s.encode(self.encode_type, errors='strict')
            return True
        except UnicodeEncodeError as e:
            if not enable_return:
                return False
            else:
                start_num = e.start + 1
                char = s[e.start: e.end]
                return char, start_num

    # ========== リスト・範囲・長さ検証 ==========
    # これらのメソッドは追加のコンテキスト情報が必要なため、
    # 引数で明示的に渡すように設計

    def is_value_in_list(self, s: str, list_items: Optional[List[str]] = None) -> bool:
        """
        リスト内の値チェック

        Args:
            s: 検証する文字列
            list_items: 許可する値のリスト

        Returns:
            bool: リスト内の値の場合True
        """
        if s == '' or s is None:
            return True
        if list_items is None or not isinstance(list_items, list):
            return True
        return s in list_items

    def is_value_in_list_kuromaru(self, s: str, list_items: Optional[List[str]] = None) -> bool:
        """
        リスト内の値チェック（●許可）

        Args:
            s: 検証する文字列
            list_items: 許可する値のリスト

        Returns:
            bool: リスト内の値または●の場合True
        """
        if s == '' or s is None:
            return True
        if list_items is None or not isinstance(list_items, list):
            return True
        copyed_list_items = list_items.copy()
        copyed_list_items.append('●')
        return s in copyed_list_items

    def is_correct_length(self, s: str, max_length: int) -> bool:
        """
        最大長チェック

        Args:
            s: 検証する文字列
            max_length: 最大文字数

        Returns:
            bool: 最大文字数以下の場合True
        """
        if s == '' or s is None:
            return True
        return len(s) <= max_length

    def is_in_range(self, s: str, min_val: int, max_val: int) -> bool:
        """
        数値範囲チェック

        Args:
            s: 検証する文字列
            min_val: 最小値
            max_val: 最大値

        Returns:
            bool: 範囲内の整数の場合True
        """
        if s == '' or s is None:
            return True
        try:
            value = int(s)
        except ValueError:
            return False
        return min_val <= value <= max_val

    def is_in_len_range(self, s: str, min_len: int, max_len: int) -> bool:
        """
        文字列長範囲チェック

        Args:
            s: 検証する文字列
            min_len: 最小文字数
            max_len: 最大文字数

        Returns:
            bool: 文字数が範囲内の場合True
        """
        if s == '' or s is None:
            return True
        return min_len <= len(s) <= max_len

    def is_len_equal(self, s: str, length: int) -> bool:
        """
        文字列長一致チェック

        Args:
            s: 検証する文字列
            length: 期待する文字数

        Returns:
            bool: 文字数が一致する場合True
        """
        if s == '' or s is None:
            return True
        if not isinstance(length, int) or length <= 0:
            raise ValueError('lengthの設定が不正です')
        return len(s) == length

    def is_re_match(self, s: str, pattern: str, escape: bool = False) -> bool:
        """
        正規表現マッチチェック

        Args:
            s: 検証する文字列
            pattern: 正規表現パターン
            escape: Trueの場合、patternをリテラル文字列として扱う（特殊文字をエスケープ）

        Returns:
            bool: パターンにマッチする場合True
        """
        if s == '' or s is None:
            return True
        # escapeがTrueの場合、正規表現の特殊文字をエスケープ
        if escape:
            pattern = re.escape(pattern)
        return True if re.match(pattern, s) else False

    # ========== 統合検証メソッド ==========

    def check_type(self, current_value: str, data_type: str,
        list_items: Optional[List[str]] = None,
        max_length: Optional[int] = None,
        min_val: Optional[int] = None,
        max_val: Optional[int] = None,
        min_len: Optional[int] = None,
        max_len: Optional[int] = None,
        length: Optional[int] = None,
        pattern: Optional[str] = None,
        escape_pattern: bool = False
    ) -> bool:
        """
        data_typeに応じた複合検証

        data_typeは'_'で区切られた複数の型指定を受け付けます
        例: 'int_notempty', 'postnum_notempty', 'hankaku_length'

        Args:
            current_value: 検証する値
            data_type: データ型指定（'_'区切り）=data['data_type']
            list_items: リスト検証用のリスト
            max_length: 最大長検証用の最大値
            min_val, max_val: 範囲検証用の最小値・最大値
            min_len, max_len: 文字列長範囲検証用の最小値・最大値
            length: 文字列長一致検証用の長さ
            pattern: 正規表現検証用のパターン
            escape_pattern: Trueの場合、patternをリテラル文字列として扱う（特殊文字をエスケープ）

        Returns:
            bool: すべての検証を通過した場合True
        """
        data_types = data_type.split('_')
        is_valids = []

        # エンコード可能チェックは常に実施
        if not self.is_encodable(current_value):
            return False

        # 各型に応じた検証
        if 'int' in data_types:
            is_valids.append(self.is_int(current_value))
        if 'float' in data_types:
            is_valids.append(self.is_float(current_value))
        if 'date' in data_types:
            is_valids.append(self.is_valid_date(current_value))
        if 'postnum' in data_types:
            is_valids.append(self.is_post_number(current_value))
        if 'postnum-kuromaru' in data_types:
            is_valids.append(self.is_post_number_kuromaru(current_value))
        if 'telnum' in data_types:
            is_valids.append(self.is_tel_number(current_value))
        if 'hankaku' in data_types:
            is_valids.append(self.is_hankaku(current_value))
        if 'zenkaku' in data_types:
            is_valids.append(self.is_zenkaku(current_value))
        if 'hankaku-kuromaru' in data_types:
            is_valids.append(self.is_hankaku_kuromaru(current_value))
        if 'hankaku-eisu-kuromaru' in data_types:
            is_valids.append(self.is_hankaku_eisu_kuromaru(current_value))
        if 'katakana-kuromaru' in data_types:
            is_valids.append(self.is_zenkaku_katakana_kuromaru(current_value))
        if 'hiragana-kuromaru' in data_types:
            is_valids.append(self.is_hiragana_kuromaru(current_value))
        if 'alphanumeric' in data_types:
            is_valids.append(self.is_alphanumeric(current_value))

        # リスト検証
        if 'list' in data_types:
            is_valids.append(self.is_value_in_list(current_value, list_items))
        if 'list-kuromaru' in data_types:
            is_valids.append(self.is_value_in_list_kuromaru(current_value, list_items))

        # 範囲・長さ検証
        if 'range' in data_types and min_val is not None and max_val is not None:
            is_valids.append(self.is_in_range(current_value, min_val, max_val))
        if 'lenrange' in data_types and min_len is not None and max_len is not None:
            is_valids.append(self.is_in_len_range(current_value, min_len, max_len))
        if 'length' in data_types and length is not None:
            is_valids.append(self.is_len_equal(current_value, length))
        if 'maxlength' in data_types and max_length is not None:
            is_valids.append(self.is_correct_length(current_value, max_length))

        # 正規表現検証
        if 're' in data_types and pattern is not None:
            is_valids.append(self.is_re_match(current_value, pattern, escape=escape_pattern))

        # 空文字チェック
        if 'notempty' in data_types:
            is_valids.append(self.is_not_empty(current_value))

        # すべての検証結果がTrueかチェック
        return all(is_valids)


# ========== テスト・デバッグ用 ==========

if __name__ == '__main__':
    print('=' * 60)
    print('InputValidator テスト')
    print('=' * 60)
    print()

    # sublibなしでテスト
    validator = InputValidator()

    # 基本検証
    print('[TEST] 基本検証')
    assert validator.is_not_empty('test') == True
    assert validator.is_not_empty('') == False
    assert validator.is_int('123') == True
    assert validator.is_int('abc') == False
    assert validator.is_float('123.45') == True
    assert validator.is_alphanumeric('abc123') == True
    assert validator.is_alphanumeric('abc-123') == False
    print('[OK] 基本検証')
    print()

    # 郵便番号・電話番号
    print('[TEST] 郵便番号・電話番号')
    assert validator.is_post_number('123-4567') == True
    assert validator.is_post_number('1234567') == False
    assert validator.is_tel_number('080-1234-5678') == True
    print('[OK] 郵便番号・電話番号')
    print()

    # 文字種
    print('[TEST] 文字種')
    assert validator.is_zenkaku_katakana_kuromaru('アイウエオ') == True
    assert validator.is_zenkaku_katakana_kuromaru('あいうえお') == False
    assert validator.is_hiragana_kuromaru('あいうえお') == True
    assert validator.is_hiragana_kuromaru('アイウエオ') == False
    print('[OK] 文字種')
    print()

    # 範囲・長さ
    print('[TEST] 範囲・長さ')
    assert validator.is_in_range('50', 0, 100) == True
    assert validator.is_in_range('150', 0, 100) == False
    assert validator.is_in_len_range('abc', 1, 5) == True
    assert validator.is_len_equal('abc', 3) == True
    assert validator.is_correct_length('abcde', 10) == True
    print('[OK] 範囲・長さ')
    print()

    # リスト
    print('[TEST] リスト検証')
    assert validator.is_value_in_list('apple', ['apple', 'banana', 'orange']) == True
    assert validator.is_value_in_list('grape', ['apple', 'banana', 'orange']) == False
    print('[OK] リスト検証')
    print()

    # 統合検証
    print('[TEST] 統合検証')
    assert validator.check_type('123', 'int_notempty') == True
    assert validator.check_type('', 'int_notempty') == False
    assert validator.check_type('abc', 'int') == False
    assert validator.check_type('123-4567', 'postnum') == True
    print('[OK] 統合検証')
    print()

    print('=' * 60)
    print('[SUCCESS] すべてのテストが成功しました')
    print('=' * 60)
