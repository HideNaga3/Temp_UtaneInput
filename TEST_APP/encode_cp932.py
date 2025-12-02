import unicodedata

# CP932でエンコードできない漢字を取得する
def get_unencodable_kanji():
    unencodable = []
    # Unicode範囲の中から漢字を探索
    for codepoint in range(0x4E00, 0x9FFF + 1):  # CJK統合漢字範囲
        char = chr(codepoint)
        try:
            char.encode('cp932')
        except UnicodeEncodeError:
            unencodable.append(char)
    return unencodable

# CP932でエンコードできないCJK記号および句読点を取得する関数
def get_unencodable_symbols():
    symbols = []

    # 範囲を定義 (追加可能)
    ranges = [
        (0x2000, 0x206F),  # 一般的な記号
        (0x25A0, 0x25FF),  # 図形記号
        (0x3000, 0x303F),  # CJK記号および句読点
        (0xFF00, 0xFFEF)   # 半角・全角形
    ]
    for start, end in ranges:
        for codepoint in range(start, end + 1):
            char = chr(codepoint)
            # 記号のみを抽出 (P: 句読点, S: 記号)
            if unicodedata.category(char).startswith(('P', 'S')):
                symbols.append(char)
    unencodable = []
    for char in symbols:
        try:
            char.encode('cp932')
        except UnicodeEncodeError:
            unencodable.append(char)
    return unencodable

def write_unencodable_kanji():
    unencodable_kanji = get_unencodable_kanji()
    # 結果をファイルに保存（任意）
    with open("unencodable_kanji_cp932.txt", "w", encoding="utf-8") as f:
        f.write("".join(unencodable_kanji))
    # 結果を表示
    print(f"CP932でエンコードできない漢字の数: {len(unencodable_kanji)}")
    print("例:", unencodable_kanji[:50])  # 最初の50文字を表示

def write_unencodable_symbols():
    unencodable_cjk_symbols = get_unencodable_symbols()
    # 結果をファイルに保存（任意）
    with open("unencodable_symbols_cp932.txt", "w", encoding="utf-8") as f:
        f.write("".join(unencodable_cjk_symbols))
    # 結果を表示
    print(f"CP932でエンコードできないCJK記号および句読点の数: {len(unencodable_cjk_symbols)}")
    print("例:", unencodable_cjk_symbols[:50])  # 最初の50文字を表示

def check_unencodable_kanji():
    with open("unencodable_kanji_cp932.txt", "r", encoding="utf-8") as f:
        text = f.read()
    error_cnt = 0
    valid_cnt = 0
    for char in text:
        try:
            char.encode('cp932', errors='strict')
        except UnicodeEncodeError as e:
            error_cnt += 1
        else:
            valid_cnt += 1
    print(f'チェックした漢字の数: {len(text)}')
    print(f"CP932でエンコードできない漢字の数: {error_cnt}")
    print(f"CP932でエンコードできる漢字の数: {valid_cnt}")

def check_unencodable_symbols():
    with open("unencodable_symbols_cp932.txt", "r", encoding="utf-8") as f:
        text = f.read()
    error_cnt = 0
    valid_cnt = 0
    for char in text:
        try:
            char.encode('cp932', errors='strict')
        except UnicodeEncodeError as e:
            error_cnt += 1
        else:
            valid_cnt += 1
    print(f'チェックしたCJK記号および句読点の数: {len(text)}')
    print(f"CP932でエンコードできないCJK記号および句読点の数: {error_cnt}")
    print(f"CP932でエンコードできるCJK記号および句読点の数: {valid_cnt}")

if __name__ == '__main__':
    print(f'漢字総数: {len(range(0x4E00, 0x9FFF + 1))}')
    print(f'記号および句読点総数: {len(range(0x3000, 0x303F + 1))}')
    write_unencodable_symbols()