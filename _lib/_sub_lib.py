import jaconv

def pri(*args):
    if len(args) == 1:
        print(args[0])
    else:
        print(' >> '.join(args))

class SubLib:
    def __init__(self):
        self.halfwidth = (
            list(range(ord('A'), ord('Z') + 1)) +  # A-Z
            list(range(ord('a'), ord('z') + 1)) +  # a-z
            list(range(ord('0'), ord('9') + 1))    # 0-9
        )
        self.fullwidth = (
            list(range(ord('Ａ'), ord('Ｚ') + 1)) +  # Ａ-Ｚ
            list(range(ord('ａ'), ord('ｚ') + 1)) +  # ａ-ｚ
            list(range(ord('０'), ord('９') + 1))    # ０-９
        )

    def h2z(self, text:str): # 半角を全角に変換
        return jaconv.h2z(text, digit=True, ascii=True, kana=True)

    def h2z_kana_digit(self, text:str): # 半角を全角に変換（数値・ひらがな・カタカナのみ、英字・記号はそのまま）
        return jaconv.h2z(text, digit=True, ascii=False, kana=True)

    def h2z_ans(self, text:str): # 半角を全角に変換（数字, アルファベット, 記号のみ）
        return jaconv.h2z(text, digit=True, ascii=True, kana=False)

    def h2z_an(self, text:str): # 半角を全角に変換（数字, アルファベットのみ）
        translation_table = str.maketrans(
                {chr(h): chr(f) for h, f in zip(self.halfwidth, self.fullwidth)}
        )
        return text.translate(translation_table)


    def z2h(self, text:str): # 全角を半角に変換
        return jaconv.z2h(text, digit=True, ascii=True, kana=True)

    def z2h_ans(self, text:str): # 全角を半角に変換(数字, アルファベット, 記号のみ)
        return jaconv.z2h(text, digit=True, ascii=True, kana=False)

    def z2h_an(self, text:str): # 半角を全角に変換（数字, アルファベットのみ）
        translation_table = str.maketrans(
                {chr(h): chr(f) for h, f in zip(self.fullwidth, self.halfwidth)}
        )
        return text.translate(translation_table)

    def hira2kata(self, text): # ひらがなをカタカナに変換
        return jaconv.hira2kata(text)

    def h2z_hira2kata(self, text:str): # 全角カタカナに変換
        return jaconv.hira2kata(jaconv.h2z(text))

    def kata2hira(self, text: str): # カタカナをひらがなに変換
        return jaconv.kata2hira(text)

    def zerofill(self, text: str, width: int): # 文字列を指定幅でゼロ埋め
        return str(text).zfill(width)

    def z2h_digit_only(self, text: str) -> str: # 全角数字（０-９）のみを半角数字（0-9）に変換
        # stripしたtextが空欄でない場合（1文字以上）のみ変換処理を実行
        if len(text.strip()) > 0:
            result = []
            for char in text:
                # 全角数字の範囲: '０' ～ '９'
                if '０' <= char <= '９':
                    # 全角数字を半角数字に変換
                    result.append(chr(ord(char) - 0xFEE0))
                else:
                    # その他の文字はそのまま
                    result.append(char)
            return ''.join(result)
        else:
            # stripしたtextが空欄の場合はそのままreturn
            return text


if __name__ == '__main__':
    sublib = SubLib()
    # 以下にテストコードを書く
