# _image_utils.py
# 画像操作のユーティリティ関数
# MAIN_APP.pyから画像・PDF操作の独立性の高い部分を抽出
#
# 作成日: 2025-10-24
# Phase 3: 画像・PDF操作層の分離

from pathlib import Path
from typing import Dict, List, Union, Optional
import exifread


class ImageUtils:
    """画像操作のユーティリティクラス

    独立性の高い画像処理機能を提供します。
    UI依存の画像操作（回転、拡大縮小など）はMAIN_APP.pyに残します。
    """

    def __init__(self, extensions: Optional[List[str]] = None):
        """初期化

        Args:
            extensions: サポートする画像拡張子のリスト
                       デフォルトは ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        """
        if extensions is None:
            self.extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        else:
            self.extensions = extensions

    def get_rotate_exif(self, file_path: str) -> int:
        """EXIFから回転情報を取得

        画像ファイルのEXIF情報から、適切な回転角度を返します。

        Args:
            file_path: 画像ファイルのパス

        Returns:
            回転角度 (0, 90, 180, 270)
        """
        rotate_map = {
            1: 0,
            3: 180,
            6: 90,
            8: 270
        }

        try:
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f)
                orientation = tags.get('Image Orientation')

                if orientation:
                    try:
                        orientation_num = orientation.values[0]
                        if orientation_num in [3, 6, 8]:
                            return rotate_map[orientation_num]
                    except Exception as e:
                        print(f'EXIF orientation_num error: {e}')
                else:
                    # EXIF情報がない場合は0度
                    pass
        except Exception as e:
            print(f'EXIF読み取りエラー: {e}')

        return 0

    def get_image_filepath_obj_dict(self,
                                     dir_path: Union[str, Path],
                                     extensions: Optional[List[str]] = None) -> Dict[int, Path]:
        """ディレクトリ内の画像ファイルパスを取得

        指定されたディレクトリ内の画像ファイルをすべて取得し、
        {index: Pathオブジェクト} の辞書として返します。

        Args:
            dir_path: ディレクトリパス
            extensions: 画像拡張子リスト（Noneの場合はインスタンス変数を使用）

        Returns:
            {0: Path('image1.jpg'), 1: Path('image2.png'), ...}
        """
        if extensions is None:
            extensions = self.extensions

        # str を Path に変換
        if isinstance(dir_path, str):
            dir_path = Path(dir_path)

        img_pobj_dict = {}
        cnt = 0

        # ディレクトリが存在しない場合は空の辞書を返す
        if not dir_path.exists() or not dir_path.is_dir():
            return img_pobj_dict

        # ディレクトリ内のファイルを走査
        for p in sorted(dir_path.iterdir()):
            if p.is_file() and p.suffix.lower() in extensions:
                img_pobj_dict[cnt] = p
                cnt += 1

        return img_pobj_dict

    def get_img_file_obj_list(self,
                               dir_path: Union[str, Path],
                               extensions: Optional[List[str]] = None) -> List[Path]:
        """ディレクトリ内の画像ファイルパスをリストで取得

        Args:
            dir_path: ディレクトリパス
            extensions: 画像拡張子リスト

        Returns:
            [Path('image1.jpg'), Path('image2.png'), ...]
        """
        if extensions is None:
            extensions = self.extensions

        if isinstance(dir_path, str):
            dir_path = Path(dir_path)

        if not dir_path.exists() or not dir_path.is_dir():
            return []

        img_fobj_list = []
        for p in sorted(dir_path.iterdir()):
            if p.is_file() and p.suffix.lower() in extensions:
                img_fobj_list.append(p)

        return img_fobj_list


# ==================== 単体テスト ====================

def test_image_utils():
    """ImageUtils の簡易テスト"""
    print('=' * 60)
    print('ImageUtils テスト開始')
    print('=' * 60)
    print()

    # ImageUtils インスタンス作成
    image_utils = ImageUtils()

    # テスト1: get_rotate_exif (モック)
    print('[テスト1] get_rotate_exif()')
    print('  Note: 実際のEXIFファイルがないため、デフォルト値0を返すことを確認')
    angle = image_utils.get_rotate_exif('dummy_path.jpg')
    assert angle == 0, f'EXIF角度が不正: {angle}'
    print(f'  [OK] デフォルト角度: {angle}')
    print()

    # テスト2: get_image_filepath_obj_dict (存在しないディレクトリ)
    print('[テスト2] get_image_filepath_obj_dict() - 存在しないディレクトリ')
    result = image_utils.get_image_filepath_obj_dict('non_existent_dir')
    assert result == {}, f'空の辞書が返されるはず: {result}'
    print(f'  [OK] 空の辞書が返されました')
    print()

    # テスト3: get_img_file_obj_list (存在しないディレクトリ)
    print('[テスト3] get_img_file_obj_list() - 存在しないディレクトリ')
    result = image_utils.get_img_file_obj_list('non_existent_dir')
    assert result == [], f'空のリストが返されるはず: {result}'
    print(f'  [OK] 空のリストが返されました')
    print()

    # テスト4: extensions のカスタマイズ
    print('[テスト4] カスタム拡張子リスト')
    custom_utils = ImageUtils(extensions=['.png', '.jpg'])
    assert custom_utils.extensions == ['.png', '.jpg']
    print(f'  [OK] カスタム拡張子: {custom_utils.extensions}')
    print()

    print('=' * 60)
    print('[SUCCESS] すべてのテストが完了しました')
    print('=' * 60)
    print()


if __name__ == '__main__':
    test_image_utils()
