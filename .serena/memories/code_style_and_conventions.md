# コードスタイルと規約

## 言語設定
- **必ず日本語で記述**: コメント、変数名、ドキュメント、エラーメッセージなど
- **絵文字は厳禁**: Windows環境・CP932エンコーディングで文字化けするため

## ファイルエンコーディング
- **Pythonファイル (.py)**: UTF-8
- **PowerShellファイル (.ps1)**: UTF-8 BOM（日本語文字化け防止）
- **CSVファイル**: CP932（Shift-JIS）

## コーディング規約

### 命名規則
- **クラス名**: PascalCase (例: `MyMainWindow`, `DataIO`)
- **メソッド名**: snake_case (例: `read_config`, `get_image_filepath_obj_dict`)
- **変数名**: snake_case (例: `current_df`, `img_pobj_dict`)
- **定数**: UPPER_SNAKE_CASE (例: `SHORT_CUT_KEY_DD`, `G_MAIN_MODE`)

### 型ヒント
- 積極的に使用
- 例: `def read_csv_with_header(file_path: str, encoding: str, headers: list, has_header: bool) -> pd.DataFrame:`

### Docstring
- 主要なクラス・メソッドに記述
- 日本語で記述
- 形式は自由（プロジェクト内で一貫性を保つ）

### Import順序
1. 標準ライブラリ
2. サードパーティライブラリ（PyQt5, pandas等）
3. プロジェクト内モジュール（_lib/配下）

例:
```python
import json
from pathlib import Path

import pandas as pd
from PyQt5.QtWidgets import QMainWindow

from _lib._mode_config import ModeConfigManager
from _lib._validators import InputValidator
```

## デザインパターンと設計方針

### モジュール化
- 単一責任原則（SRP）を重視
- 機能ごとに_lib/配下のモジュールに分離
- MAIN_APP.pyは可能な限りシンプルに保つ

### クラス設計
- **Managerクラス**: 設定・状態管理（例: ConfigManager, ModeConfigManager）
- **Utilsクラス**: ユーティリティ関数集（例: ImageUtils, DataIO）
- **Mixinクラス**: 再利用可能な機能（例: InitializerMixin）

### 依存関係の方向
- 下位モジュール → 上位モジュールのみ
- 循環インポートを避ける

### エラーハンドリング
- 例外を適切にキャッチ
- ログに記録（log_ファイル経由）
- ユーザーにQMessageBoxで通知

## コードの分離方針（現在進行中）

### 統合済みモジュール
1. **_mode_config.py**: 8モードの設定管理
2. **_validators.py**: バリデーション処理（22個のメソッド）
3. **_image_utils.py**: 画像関連ユーティリティ
4. **_data_io.py**: CSV読み書き処理

### 今後の分離予定
- UI操作層: イベントハンドラ系メソッド
- 画像処理層: 回転・拡大縮小・フィット処理
- データ管理層: DataFrame操作
- 設定管理層: config.json/rect.json操作

## テスト方針
- 各モジュールに単体テスト関数を含める（if __name__ == "__main__":ブロック）
- リファクタリング時は必ずユーザーに動作確認を依頼
- 動作確認手順を文書化

## バックアップ方針
- ファイル編集前に必ずバックアップ作成
- 約10分間隔でバックアップ
- バックアップ先: backup/YYYY-MM-DD/
- 3日前より古いバックアップは自動削除
- バイナリファイルは除外
