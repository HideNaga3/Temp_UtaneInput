# _config_manager.py
# 設定ファイル管理のヘルパークラス
# config.jsonやrect.jsonなどの読み書き処理を提供
#
# 作成日: 2025-10-25
# Phase A-4: 設定管理層の分離

import json
import os
from pathlib import Path
from typing import Union, Dict, Any, Optional


class ConfigManager:
    """JSON設定ファイルの管理クラス

    config.jsonやrect.jsonなどの設定ファイルの読み書き、
    整合性チェック、初期化処理を提供します。
    """

    def __init__(
        self,
        config_path: Union[str, Path],
        default_config: Dict[str, Any],
        encoding: str = 'utf-8'
    ):
        """初期化

        Args:
            config_path: 設定ファイルのパス
            default_config: デフォルト設定の辞書
            encoding: ファイルエンコーディング（デフォルト: utf-8）
        """
        self.config_path = str(config_path)
        self.default_config = default_config
        self.config_keys = list(default_config.keys())
        self.encoding = encoding
        self.config = {}

    def initialize(self) -> Dict[str, Any]:
        """設定ファイルの初期化

        ファイルが存在しない場合は作成し、存在する場合は読み込んで
        整合性をチェックします。

        Returns:
            Dict[str, Any]: 初期化された設定辞書
        """
        if not os.path.exists(self.config_path):
            self.write(self.default_config)
        self.config = self.read()
        self.check_and_fix()
        return self.config

    def read(self) -> Dict[str, Any]:
        """設定ファイルを読み込む

        Returns:
            Dict[str, Any]: 読み込んだ設定辞書
                           読み込みに失敗した場合はデフォルト設定を返す
        """
        try:
            with open(self.config_path, 'r', encoding=self.encoding) as f:
                config = json.load(f)
            self.config = config
            return config
        except Exception:
            # 読み込み失敗時はデフォルト設定のコピーを返す
            self.config = self.default_config.copy()
            return self.config

    def write(self, config: Dict[str, Any]) -> None:
        """設定ファイルに書き込む

        Args:
            config: 書き込む設定辞書
        """
        # キーをソートして見やすくする
        config = dict(sorted(config.items()))

        # ディレクトリが存在しない場合は作成
        config_dir = os.path.dirname(self.config_path)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)

        with open(self.config_path, 'w', encoding=self.encoding) as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    def check_and_fix(self) -> None:
        """設定の整合性をチェックして修正

        欠落したキーをデフォルト値で追加し、不要なキーを削除します。
        変更があった場合は自動的にファイルに保存します。
        """
        is_changed = False

        # 欠落したキーをデフォルト値で追加
        for key in self.default_config.keys():
            if self.config.get(key) is None:
                self.config[key] = self.default_config[key]
                is_changed = True

        # 不要なキー（デフォルト設定にないキー）を削除
        if set(self.config_keys) != set(self.config.keys()):
            self.config = {k: v for k, v in self.config.items() if k in self.config_keys}
            is_changed = True

        # 変更があった場合は保存
        if is_changed:
            self.write(self.config)

    def get(self, key: str, default: Any = None) -> Any:
        """設定値を取得

        Args:
            key: 設定キー
            default: キーが存在しない場合のデフォルト値

        Returns:
            Any: 設定値
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any, auto_save: bool = True) -> None:
        """設定値を設定

        Args:
            key: 設定キー
            value: 設定値
            auto_save: 自動保存するか（デフォルト: True）
        """
        self.config[key] = value
        if auto_save:
            self.write(self.config)

    def update(self, config_updates: Dict[str, Any], auto_save: bool = True) -> None:
        """複数の設定値を一括更新

        Args:
            config_updates: 更新する設定辞書
            auto_save: 自動保存するか（デフォルト: True）
        """
        self.config.update(config_updates)
        if auto_save:
            self.write(self.config)


class RectConfigManager(ConfigManager):
    """矩形設定ファイル（rect.json）専用の管理クラス

    rect.jsonは整数キーを使用するため、特別な処理が必要です。
    """

    def read(self) -> Dict[int, Any]:
        """設定ファイルを読み込む

        JSONは整数キーを文字列として保存するため、
        読み込み後に整数キーに変換します。

        Returns:
            Dict[int, Any]: 読み込んだ設定辞書（整数キー）
        """
        try:
            with open(self.config_path, 'r', encoding=self.encoding) as f:
                config = json.load(f)
            # 文字列キーを整数キーに変換
            self.config = {int(k): v for k, v in config.items()}
            return self.config
        except Exception:
            self.config = self.default_config.copy()
            return self.config

    def write(self, config: Dict[int, Any]) -> None:
        """設定ファイルに書き込む

        整数キーをソートして書き込みます。

        Args:
            config: 書き込む設定辞書（整数キー）
        """
        # 整数キーでソート
        config = dict(sorted(config.items(), key=lambda x: int(x[0])))

        # ディレクトリが存在しない場合は作成
        config_dir = os.path.dirname(self.config_path)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)

        with open(self.config_path, 'w', encoding=self.encoding) as f:
            json.dump(config, f, ensure_ascii=False, indent=4)


# ==================== 単体テスト ====================

def test_config_manager():
    """ConfigManager の簡易テスト"""
    print('=' * 60)
    print('ConfigManager テスト開始')
    print('=' * 60)
    print()

    # テスト用の一時ファイルパス
    test_config_path = './data/test_config.json'

    # テスト用のデフォルト設定
    default_config = {
        'username': 'test_user',
        'window_width': 800,
        'window_height': 600,
        'is_maximized': False
    }

    # テスト1: ConfigManagerのインスタンス化
    print('[テスト1] ConfigManagerのインスタンス化')
    manager = ConfigManager(test_config_path, default_config)
    assert manager is not None
    print('  [OK] ConfigManagerインスタンス作成成功')
    print()

    # テスト2: 初期化（ファイルが存在しない場合）
    print('[テスト2] initialize() - ファイルが存在しない場合')
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    config = manager.initialize()
    assert config == default_config
    assert os.path.exists(test_config_path)
    print('  [OK] デフォルト設定でファイルが作成された')
    print()

    # テスト3: 設定値の取得
    print('[テスト3] get() - 設定値の取得')
    username = manager.get('username')
    assert username == 'test_user'
    print(f'  [OK] username = {username}')
    print()

    # テスト4: 設定値の設定
    print('[テスト4] set() - 設定値の設定')
    manager.set('username', 'new_user', auto_save=False)
    assert manager.config['username'] == 'new_user'
    print('  [OK] 設定値が変更された（保存なし）')
    print()

    # テスト5: 設定の書き込み
    print('[テスト5] write() - 設定の書き込み')
    manager.write(manager.config)
    manager2 = ConfigManager(test_config_path, default_config)
    config2 = manager2.read()
    assert config2['username'] == 'new_user'
    print('  [OK] 設定が正しく保存・読み込みされた')
    print()

    # テスト6: check_and_fix() - 欠落したキーの追加
    print('[テスト6] check_and_fix() - 欠落したキーの追加')
    manager.config = {'username': 'test'}  # 一部のキーを削除
    manager.check_and_fix()
    assert 'window_width' in manager.config
    assert manager.config['window_width'] == 800
    print('  [OK] 欠落したキーがデフォルト値で追加された')
    print()

    # クリーンアップ
    if os.path.exists(test_config_path):
        os.remove(test_config_path)

    print('=' * 60)
    print('[SUCCESS] すべてのテストが完了しました')
    print('=' * 60)
    print()


if __name__ == '__main__':
    test_config_manager()
