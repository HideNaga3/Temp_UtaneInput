# MAIN_APP.py リファクタリング実行計画書

作成日: 2025-10-24

---

## 現状の深刻な問題点

### 1. 圧倒的な複雑度
- **総行数: 5,138行**
- **インスタンス変数: 372個以上**
- **メソッド数: 約130個** (MyMainWindowクラスのみ)
- **self.への参照: 2,512箇所**

### 2. 神クラス (God Class) アンチパターン
MyMainWindowクラスがすべての責任を持っている:
- UI制御
- データ検証
- 画像操作
- PDF操作
- ファイル入出力
- 設定管理
- イベント処理
- ビジネスロジック

### 3. モード管理の複雑さ
**8つの異なるモード**を1つのクラスで管理:
1. card (名刺)
2. utane (ウタネ回覧)
3. foreigner (外国人旅行調査)
4. prevention (防災)
5. syuei (イベント応募)
6. prevention2 (防災v2)
7. factory (工場見学)
8. payroll (給与検定) [現在のメイン]

各モードごとに:
- `data_list_xxx` - データリスト定義
- `input_frames_data_list_xxx` - フレームリスト定義
- `xxx_headers` - CSVヘッダー定義
- モード別設定（リピートモード、PDFモード、タイトルなど）

### 4. 保守性の問題
コメントに「! モード追加時はここを忘れないこと」が複数箇所
→ 変更箇所が分散していて、追加・変更時にミスが発生しやすい

---

## リファクタリングの目標

### 短期目標（1-2週間）
1. **行数を半分以下に**: 5,138行 → 2,500行以下
2. **インスタンス変数を1/3に**: 372個 → 120個以下
3. **MyMainWindowのメソッドを半分に**: 130個 → 65個以下

### 中期目標（1-2ヶ月）
1. 各クラスが単一責任を持つ
2. テスト可能な構造
3. 新モード追加が容易

### 長期目標（3ヶ月以降）
1. 完全なMVCまたはMVVM構造
2. 包括的な自動テスト
3. ドキュメント完備

---

## 優先度付きリファクタリング計画

### 【最優先】フェーズ1: モード設定の分離
**重要度: ★★★★★ | 難易度: ★☆☆☆☆ | 効果: 行数 -300行**

#### 問題
8つのモード定義が `__init__` と `initializer` に散在:
- 各モードのdata_list定義
- 各モードのframe_list定義
- 各モードのheaders定義
- モード別設定辞書が6個以上

#### 解決策
```python
# 新規作成: _mode_config.py (for_claudeフォルダ内)

from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ModeConfig:
    """1つのモードの設定を保持するデータクラス"""
    mode_id: str                    # 'payroll', 'card', etc.
    jp_name: str                    # '給与検定', '名刺', etc.
    title: str                      # ウィンドウタイトル
    file_type: str                  # 'img' or 'pdf'
    is_rept_mode: bool             # リピートモードかどうか
    is_single_pdf_mode: bool       # 1PDF1画像モードかどうか
    has_header: bool               # CSVヘッダーがあるか
    headers: Optional[List[str]]   # CSVヘッダーリスト
    data_list: List[Dict]          # データリスト定義
    frame_list: List[Dict]         # フレームリスト定義
    is_multi_pdf: bool = False     # 複数PDFモードかどうか

class ModeConfigManager:
    """すべてのモード設定を管理するクラス"""

    def __init__(self):
        self.modes: Dict[str, ModeConfig] = {}
        self._init_all_modes()

    def _init_all_modes(self):
        """すべてのモード設定を初期化"""
        # Payrollモード（給与検定）
        self.modes['payroll'] = ModeConfig(
            mode_id='payroll',
            jp_name='給与検定',
            title='給与計算検定入力ソフト',
            file_type='pdf',
            is_rept_mode=False,
            is_single_pdf_mode=True,
            has_header=False,
            headers=None,
            data_list=create_data_list('payroll'),
            frame_list=create_frame_list('payroll')
        )

        # Cardモード（名刺）
        self.modes['card'] = ModeConfig(
            mode_id='card',
            jp_name='名刺',
            title='名刺入力アプリ',
            file_type='img',
            is_rept_mode=False,
            is_single_pdf_mode=False,
            has_header=False,
            headers=None,
            data_list=create_data_list('card'),
            frame_list=create_frame_list('card')
        )

        # 他の6モードも同様に定義...

    def get_mode(self, mode_id: str) -> ModeConfig:
        """モード設定を取得"""
        return self.modes.get(mode_id)

    def get_all_mode_ids(self) -> List[str]:
        """すべてのモードIDを取得"""
        return list(self.modes.keys())

    def get_jp_name(self, mode_id: str) -> str:
        """日本語名を取得"""
        return self.modes[mode_id].jp_name

    def get_title(self, mode_id: str) -> str:
        """ウィンドウタイトルを取得"""
        return self.modes[mode_id].title
```

#### MAIN_APP.pyでの使用方法
```python
# MAIN_APP.py の initializer() 内

# 旧コード（削除）
# self.data_list_payroll = create_data_list('payroll')
# self.input_frames_data_list_payroll = create_frame_list('payroll')
# self.main_mode_to_title_dict = {...}
# ... 等々

# 新コード
from _mode_config import ModeConfigManager

self.mode_manager = ModeConfigManager()
self.current_mode = self.mode_manager.get_mode(self.main_mode_init)

# アクセス例
self.setWindowTitle(self.current_mode.title)
self.data_list = self.current_mode.data_list
self.is_rept_mode = self.current_mode.is_rept_mode
```

#### メリット
- モード追加時は `_mode_config.py` の1箇所のみ変更
- データ構造が明確
- 型チェックが効く
- テストが容易

---

### 【高優先】フェーズ2: バリデーション層の分離
**重要度: ★★★★★ | 難易度: ★★☆☆☆ | 効果: 行数 -500行**

#### 問題
26個のバリデーションメソッドがMyMainWindowに混在

#### 解決策
```python
# 新規作成: _validators.py (for_claudeフォルダ内)

class InputValidator:
    """入力値検証を担当するクラス"""

    def __init__(self):
        pass

    # 基本検証
    def is_not_empty(self, s: str) -> bool:
        """空文字チェック"""
        return bool(s and s.strip())

    def is_int(self, s: str) -> bool:
        """整数チェック"""
        try:
            int(s)
            return True
        except:
            return False

    # ... 残り24個のメソッドを移動

    def check_type(self, value: str, data_type: str, **kwargs) -> bool:
        """
        data_typeに応じた検証を実行

        Args:
            value: 検証する値
            data_type: データ型 ('int', 'float', 'postnum', 'tel', etc.)
            **kwargs: 追加パラメータ (min_val, max_val, pattern, etc.)

        Returns:
            bool: 検証結果
        """
        # data_typeを解析して適切な検証メソッドを呼び出す
        type_parts = data_type.split('_')

        if 'notempty' in type_parts:
            if not self.is_not_empty(value):
                return False

        if 'int' in type_parts:
            return self.is_int(value)

        # ... 以下、各型に応じた処理
```

#### MAIN_APP.pyでの使用方法
```python
from _validators import InputValidator

# __init__内
self.validator = InputValidator()

# 使用箇所（既存メソッドから呼び出し）
def check_type_line_edit(self, current_value, data_type, current_obj=None):
    return self.validator.check_type(current_value, data_type,
                                     current_obj=current_obj)
```

---

### 【高優先】フェーズ3: 画像・PDF操作層の分離
**重要度: ★★★★☆ | 難易度: ★★★☆☆ | 効果: 行数 -600行**

#### 問題
17個の画像操作メソッド + PDF操作が混在

#### 解決策
```python
# 新規作成: _image_handler.py (for_claudeフォルダ内)

class ImageHandler:
    """画像表示・操作を担当するクラス"""

    def __init__(self, graphics_view: QGraphicsView, scene: QGraphicsScene):
        self.graphics_view = graphics_view
        self.scene = scene
        self.pixmap_item = None
        self.current_scale = 1.0
        self.current_angle = 0

    def load_image(self, filepath: str) -> bool:
        """画像ファイルを読み込み"""
        pass

    def rotate(self, angle: int, is_absolute: bool = False) -> None:
        """画像を回転"""
        pass

    def scale(self, scale_factor: float, is_absolute: bool = False) -> None:
        """画像を拡大縮小"""
        pass

    def fit_to_view(self, mode: str = 'w') -> None:
        """ビューにフィット"""
        pass

    # ... 他の画像操作メソッド
```

```python
# 新規作成: _pdf_handler.py (for_claudeフォルダ内)

class PDFHandler:
    """PDF操作を担当するクラス"""

    def __init__(self, pdf_reader: PdfImgReader, image_handler: ImageHandler):
        self.pdf_reader = pdf_reader
        self.image_handler = image_handler
        self.current_file_index = 0
        self.current_page_index = 0

    def load_pdf_folder(self, folder_path: str) -> bool:
        """PDFフォルダを読み込み"""
        pass

    def show_page(self, page_index: int) -> bool:
        """指定ページを表示"""
        pass

    def next_page(self) -> bool:
        """次のページへ"""
        pass

    def previous_page(self) -> bool:
        """前のページへ"""
        pass
```

---

### 【中優先】フェーズ4: データ入出力層の分離
**重要度: ★★★☆☆ | 難易度: ★★☆☆☆ | 効果: 行数 -400行**

#### 解決策
```python
# 新規作成: _data_manager.py (for_claudeフォルダ内)

class DataManager:
    """データの入出力を担当するクラス"""

    def __init__(self, mode_config: ModeConfig):
        self.mode_config = mode_config
        self.current_record = {}
        self.records = []

    def create_record_from_line_edits(self, line_edit_values: List[str]) -> dict:
        """LineEditの値からレコードを作成"""
        pass

    def export_to_csv(self, filepath: str, encoding: str = 'utf-8') -> bool:
        """CSVファイルにエクスポート"""
        pass

    def export_log(self, log_df: pd.DataFrame, filepath: str) -> bool:
        """ログファイルをエクスポート"""
        pass

    def load_previous_data(self, filepath: str) -> pd.DataFrame:
        """前回データを読み込み"""
        pass
```

---

### 【中優先】フェーズ5: UI制御層の整理
**重要度: ★★★☆☆ | 難易度: ★★★☆☆ | 効果: 行数 -300行**

#### 解決策
```python
# 新規作成: _ui_controller.py (for_claudeフォルダ内)

class UIController:
    """UI表示・レイアウトを担当するクラス"""

    def __init__(self, main_window: QMainWindow):
        self.window = main_window
        self.current_layout = 'vertical'
        self.screen_mode = 'normal'

    def set_layout(self, mode: str) -> None:
        """レイアウトを変更 ('vertical' or 'horizontal')"""
        pass

    def toggle_screen_mode(self) -> None:
        """画面モードを切り替え (normal/maximized/fullscreen)"""
        pass

    def update_line_edit_colors(self, validation_results: List[dict]) -> None:
        """検証結果に応じてLineEditの色を更新"""
        pass

    def show_info_labels(self, info_dict: dict) -> None:
        """情報ラベルを表示"""
        pass
```

---

### 【低優先】フェーズ6-8: その他の整理
**重要度: ★★☆☆☆ | 難易度: ★★☆☆☆ | 効果: 行数 -400行**

- フォーカス制御の分離
- リストウィジェット操作の分離
- 設定管理の分離

---

## ファイル構成計画

### 現在
```
プロジェクトルート/
├── MAIN_APP.py (5,138行)
├── main_app_ui.py
├── _create_logger.py
├── _draggable_pixmap_item.py
├── ... (その他のヘルパーファイル)
└── for_claude/ (作業フォルダ)
```

### リファクタリング後（中間目標）
```
プロジェクトルート/
├── MAIN_APP.py (約2,500行)
├── main_app_ui.py
├── _mode_config.py (新規 - モード設定)
├── _validators.py (新規 - バリデーション)
├── _image_handler.py (新規 - 画像操作)
├── _pdf_handler.py (新規 - PDF操作)
├── _data_manager.py (新規 - データ入出力)
├── _ui_controller.py (新規 - UI制御)
├── _create_logger.py (既存)
├── _draggable_pixmap_item.py (既存)
├── ... (その他のヘルパーファイル)
└── for_claude/
    ├── refactoring_analysis.md
    ├── refactoring_plan.md (このファイル)
    ├── prototype/ (プロトタイプコード)
    └── tests/ (テストコード)
```

### 最終目標（長期）
```
プロジェクトルート/
├── main.py (エントリーポイント)
├── ui/
│   ├── main_window.py
│   └── dialogs/
├── models/
│   ├── mode_config.py
│   └── data_model.py
├── controllers/
│   ├── image_controller.py
│   ├── pdf_controller.py
│   ├── data_controller.py
│   └── ui_controller.py
├── validators/
│   └── input_validator.py
├── utils/
│   ├── logger.py
│   ├── config.py
│   └── helpers.py
└── tests/
```

---

## 段階的移行の方針

### 原則
1. **元のコードを壊さない**: 新クラスを作成し、徐々に移行
2. **動作確認を頻繁に**: 各フェーズ完了時に必ず動作確認
3. **Gitでバージョン管理**: 各フェーズ完了時にコミット
4. **バックアップを作成**: CLAUDE_GLOBAL.mdの方針に従う

### 移行手順（各フェーズ共通）

#### ステップ1: プロトタイプ作成
- for_claude/prototype/フォルダに新クラスを作成
- 単体で動作確認
- 簡単なテストコードを作成

#### ステップ2: MAIN_APP.pyへの組み込み
- 新クラスをインポート
- インスタンスを作成
- 既存メソッドから新クラスのメソッドを呼び出す
- **この段階では既存メソッドは残す**

#### ステップ3: 動作確認
- アプリケーション全体を起動
- 主要機能を手動テスト
- 問題なければ次へ

#### ステップ4: 既存コードの削除
- 新クラスで置き換えた既存メソッドを削除
- 使用されていないインスタンス変数を削除

#### ステップ5: クリーンアップ
- 不要なコメントを削除
- インポートを整理
- コードフォーマット

---

## 具体的な作業スケジュール

### Week 1: フェーズ1（モード設定の分離）
- **Day 1-2**: プロトタイプ作成
  - `for_claude/prototype/_mode_config.py` を作成
  - 8モード全ての設定を移行
  - テストコード作成

- **Day 3-4**: MAIN_APP.pyへの組み込み
  - ModeConfigManagerをインポート
  - initializerメソッドを修正
  - モード関連の辞書を削除

- **Day 5**: 動作確認とクリーンアップ
  - 全モードで動作確認
  - バグ修正
  - Gitコミット

### Week 2: フェーズ2（バリデーション層の分離）
- **Day 1-2**: プロトタイプ作成
  - `for_claude/prototype/_validators.py` を作成
  - 26個のバリデーションメソッドを移行

- **Day 3**: MAIN_APP.pyへの組み込み
  - InputValidatorをインポート
  - 既存メソッドから呼び出し

- **Day 4-5**: 動作確認とクリーンアップ
  - 入力検証を網羅的にテスト
  - Gitコミット

### Week 3: フェーズ3（画像・PDF操作層の分離）
- **Day 1-3**: プロトタイプ作成
  - `_image_handler.py` を作成
  - `_pdf_handler.py` を作成

- **Day 4**: 組み込みと動作確認

- **Day 5**: クリーンアップとGitコミット

---

## リスク管理

### 想定されるリスク

#### リスク1: 循環参照の発生
**対策**:
- 依存関係を一方向にする
- 必要な場合はイベント駆動で解決

#### リスク2: 既存機能の破壊
**対策**:
- 段階的移行（既存コードを残したまま新コード追加）
- 頻繁な動作確認
- Gitでいつでも戻せる状態を維持

#### リスク3: 作業時間の超過
**対策**:
- 優先度の高いフェーズに集中
- 完璧を求めすぎない
- 途中でも使える状態を維持

---

## 成功の判断基準

### 必須項目
- [ ] アプリケーションが元と同じように動作する
- [ ] 総行数が3,000行以下になる
- [ ] インスタンス変数が150個以下になる
- [ ] 新モード追加時の変更箇所が5箇所以下

### 望ましい項目
- [ ] 各クラスが300行以下
- [ ] 各メソッドが50行以下
- [ ] テストカバレッジ50%以上

---

## 次のアクション

### 今すぐ実施可能
1. **for_claude/prototype/フォルダを作成**
2. **フェーズ1のプロトタイプ作成を開始**
   - `_mode_config.py` のスケルトンを作成
   - payrollモードの設定を移行
   - 動作確認

### ユーザー確認が必要な事項
1. この計画で進めてよいか？
2. フェーズ1から始めてよいか？
3. for_claudeフォルダ内でプロトタイプ作成してよいか？
4. 週1フェーズのペースで問題ないか？

---

作成者: Claude Code
作成日: 2025-10-24
