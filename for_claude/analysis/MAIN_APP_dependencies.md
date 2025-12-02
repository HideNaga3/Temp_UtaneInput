# MAIN_APP.py の依存関係と構造分析

作成日: 2025-10-24

---

## プロジェクト概要

このプロジェクトは、PDFや画像ファイルを表示し、画像上に矩形を配置して特定領域を選択・入力するGUIアプリケーションです。
PyQt5を使用して作成されており、給与検定などのデータ入力作業を効率化することを目的としています。

---

## メインスクリプト

**MAIN_APP.py**
- プロジェクトのメインアプリケーション
- ファイルサイズ: 約312.9KB（大規模なスクリプト）
- メインウィンドウクラス: `MyMainWindow`
- Python仮想環境: `input_img`
- Pythonバージョン: 3.10.14

---

## 依存関係マップ

```
MAIN_APP.py
    |
    +-- main_app_ui.py (UIファイル - Qt Designerで生成)
    |
    +-- _create_logger.py (ロガー作成)
    |
    +-- _draggable_pixmap_item.py (ドラッグ可能な画像アイテム)
    |       |
    |       +-- MAIN_APP.py (循環参照: 親ウィンドウへのアクセス用)
    |
    +-- _init_dialog_ui.py (初期化ダイアログUI)
    |
    +-- _collation_dialog_ui.py (照合ダイアログUI)
    |
    +-- _ime_control.py (IME制御)
    |       |
    |       +-- _create_logger.py
    |       +-- _ime_control.ahk (AutoHotkey v2スクリプト)
    |       +-- AutoHotkey64_2.0.18.exe
    |
    +-- _postnum_reader.py (郵便番号リーダー)
    |
    +-- _collation_two_text.py (2つのテキスト照合)
    |
    +-- _sub_lib.py (文字列変換サブライブラリ)
    |
    +-- _pdf_util.py (PDFユーティリティ)
    |       |
    |       +-- _draggable_pixmap_item.py
    |
    +-- _create_data_list.py (データリスト作成) [未読 - サイズ超過]
    |
    +-- _text_edit_dialog.py (テキスト編集ダイアログ)
    |       |
    |       +-- _text_edit_dialog_ui.py
```

---

## 各モジュールの詳細

### 1. _create_logger.py
**役割:** ログ出力の設定
- ログファイルとコンソールへの二重出力
- DEBUGレベル以上をコンソール出力
- INFOレベル以上をファイル出力
- エンコーディング: UTF-8

**主要関数:**
- `create_logger(log_path: str)` -> Logger

**依存ライブラリ:**
- logging (標準ライブラリ)

---

### 2. _draggable_pixmap_item.py
**役割:** 画像上での矩形選択とドラッグ操作

**主要クラス:**
- `DraggablePixmapItem(QGraphicsPixmapItem)`

**主要機能:**
- 画像の移動（moveモード）
- 矩形範囲の選択（selectモード）
- 矩形の位置・サイズの保存と復元
- スケール・回転角度に応じた座標変換
- 矩形の自動配置（ビューの中央に表示）

**重要なメソッド:**
- `set_sub_rect()` - 黄色の半透明矩形を描画
- `align_rect_to_view()` - 矩形をビューに合わせて配置
- `convert_rect()` - 矩形座標を100%スケール基準に変換
- `get_rect()` - 矩形情報を取得して設定に保存
- `set_rect()` - 保存された矩形情報から表示
- `delete_sub_rect()` - 矩形を削除

**循環参照の注意:**
- MAIN_APP.pyから`DraggablePixmapItem`をインポート
- `DraggablePixmapItem`内でMAIN_APP.pyをインポート（型ヒント用）

---

### 3. _sub_lib.py
**役割:** 日本語文字列変換ユーティリティ

**主要クラス:**
- `SubLib`

**主要機能:**
- 半角 ⇔ 全角 変換
- ひらがな ⇔ カタカナ 変換
- 数字・アルファベット・記号の変換オプション

**主要メソッド:**
- `h2z(text)` - 半角を全角に変換（すべて）
- `h2z_ans(text)` - 半角を全角に変換（数字・英字・記号のみ）
- `h2z_an(text)` - 半角を全角に変換（数字・英字のみ）
- `z2h(text)` - 全角を半角に変換（すべて）
- `z2h_ans(text)` - 全角を半角に変換（数字・英字・記号のみ）
- `z2h_an(text)` - 全角を半角に変換（数字・英字のみ）
- `hira2kata(text)` - ひらがなをカタカナに変換
- `kata2hira(text)` - カタカナをひらがなに変換
- `h2z_hira2kata(text)` - 全角カタカナに変換

**依存ライブラリ:**
- jaconv

**補助関数:**
- `pri(*args)` - デバッグ用の便利なprint関数

---

### 4. _pdf_util.py
**役割:** PDFファイルからページ画像を抽出

**主要クラス:**
- `PdfImgReader`
- `TestMainWindow` (テスト用)

**主要機能:**
- PDFファイルの一覧取得
- PDFの総ページ数カウント
- 指定ページの画像抽出（QPixmap形式）
- 画像の解像度調整（matrixパラメータ）

**主要メソッド:**
- `__init__(dobj: Path, matrix_int=2)` - 初期化
- `get_total_page_count()` -> int - 総ページ数取得
- `get_file_list()` -> list - ファイル一覧取得
- `get_page_list()` -> list - ページ一覧取得
- `get_img_from_pdf(file_name, page_index)` -> QPixmap - PDF画像取得

**データ構造:**
```python
file_record = {
    'file_index': int,
    'pdf_obj': Path,
    'file_name': str,
    'page_count': int
}

page_record = {
    'main_index': int,      # 全体通しページ番号
    'file_index': int,      # ファイル番号
    'page_index': int,      # ファイル内ページ番号
    'file_name': str,
    'pdf_obj': Path
}
```

**依存ライブラリ:**
- PyMuPDF (fitz)
- PyQt5

---

### 5. _ime_control.py
**役割:** IME（日本語入力）のオン/オフ制御

**主要機能:**
- AutoHotkey経由でIMEを制御
- 実行ファイル/スクリプト両対応
- エラーログ出力

**主要関数:**
- `set_ime_mode_jp_or_en(mode: str = 'en')` - IME切り替え

**モードオプション:**
- 'jp' - 日本語IMEをオン
- 'en' - 日本語IMEをオフ

**依存ファイル:**
- _ime_control.ahk (AutoHotkey v2スクリプト)
- AutoHotkey64_2.0.18.exe (実行ファイル)

**依存ライブラリ:**
- subprocess (標準)
- _create_logger

---

### 6. _postnum_reader.py
**役割:** 郵便番号から住所を検索

**主要クラス:**
- `PostNumReader`

**主要機能:**
- 郵便番号CSVの読み込みと変換
- 変換済みデータのキャッシュ（pickle形式）
- 郵便番号から都道府県・市区町村・町域名を検索

**主要メソッド:**
- `__init__(parent, is_debug=False)` - 初期化とデータ読み込み
- `get_city_and_town_from_postnum(postnum: str)` -> dict - 住所検索

**データ構造:**
```python
result = {
    'postnum': str,  # 例: '321-9999'
    'pref': str,     # 都道府県名
    'city': str,     # 市区町村名
    'town': str      # 町域名
}
```

**データソース:**
- `./data/postnum/*.csv` - 元データ（日本郵便公式）
- `./data/postnum/converted_postnum.pkl` - 変換済みキャッシュ

**データ処理:**
1. 元CSVから必要列のみ抽出（全15列中4列のみ使用）
2. 郵便番号にハイフン挿入（3桁-4桁形式）
3. 町域名から不要文字列を削除
4. pickle形式で保存

**依存ライブラリ:**
- pandas
- pathlib (標準)
- pickle (標準)
- re (標準)

---

### 7. _collation_two_text.py
**役割:** 2つのテキストの差異を検出

**主要クラス:**
- `CollationTwoText`

**主要機能:**
- 前方からの差異検出
- 後方からの差異検出
- 文字集合の差分抽出

**主要メソッド:**
- `collation_two_text(new_text, ver_text)` -> dict or None

**返り値の構造:**
```python
result_dict = {
    'normal_and_rev': [
        {
            'new': {'index': int, 'char': str},
            'ver': {'index': int, 'char': str}
        },
        # 後方差異がある場合は2要素目も存在
    ],
    'new_diff': set,  # newにのみ存在する文字
    'ver_diff': set   # verにのみ存在する文字
}
```

**依存ライブラリ:**
- なし（標準ライブラリのみ）

---

### 8. UIファイル群

#### main_app_ui.py
- Qt Designerで生成されたメインウィンドウのUI定義
- `Ui_MainWindow`クラス

#### _init_dialog_ui.py
- 初期化ダイアログのUI定義
- `Ui_InitDialog`クラス

#### _collation_dialog_ui.py
- 照合ダイアログのUI定義
- `Ui_CollationDialog`クラス

#### _text_edit_dialog_ui.py
- テキスト編集ダイアログのUI定義
- UI定義のみで、ビジネスロジックは`_text_edit_dialog.py`に実装

---

### 9. 未読の大規模ファイル

#### _create_data_list.py
- トークン数超過により詳細未読
- データリストとフレームリストの作成機能
- エクスポート関数: `create_data_list()`, `create_frame_list()`

#### _text_edit_dialog.py
- 詳細未読
- `MyTextEditDialog`クラス
- テキスト編集ダイアログの実装

---

## 外部ライブラリ依存関係

### 必須ライブラリ

1. **PyQt5** - GUIフレームワーク
   - QtWidgets
   - QtCore
   - QtGui

2. **pandas** - データ処理（郵便番号検索）

3. **exifread** - 画像のEXIF情報読み取り

4. **PyMuPDF (fitz)** - PDF処理

5. **jaconv** - 日本語文字変換

### オプション/外部実行ファイル

6. **AutoHotkey v2** - IME制御用
   - AutoHotkey64_2.0.18.exe
   - _ime_control.ahk

---

## データフォルダ構成

```
data/
    |
    +-- error.log                    # エラーログ
    |
    +-- postnum/                     # 郵便番号データ
    |       |
    |       +-- *.csv                # 元データ（日本郵便公式）
    |       +-- converted_postnum.pkl # 変換済みキャッシュ
    |
    +-- [その他の設定ファイル]
```

---

## PyInstaller対応

プロジェクトにはPyInstallerフック用のフォルダが存在:

```
pyinstaller_hooks/
    +-- hook-PyQt5.py
    +-- hook-PyQt5_unified.py
    +-- hook-PyQt5.QtCore.py
    +-- hook-PyQt5.QtGui.py
    +-- hook-PyQt5.QtWidgets.py
```

これらは実行ファイル化時にPyQt5の依存関係を正しく解決するために使用されます。

---

## 重要な設計パターン

### 1. 循環参照の管理
- `MAIN_APP.py` ⇔ `_draggable_pixmap_item.py`
- 親ウィンドウへの参照を保持する設計
- 型ヒントでのインポートで循環参照を回避

### 2. 座標系の管理
- 矩形座標を常に100%スケール基準で保存
- 表示時に現在のスケール・回転角度で変換
- `rect_item_xywz_100per_dict`にx, y, w, h, angle, scaleを格納

### 3. データキャッシュ
- 郵便番号データをpickle形式でキャッシュ
- 初回読み込み時に変換処理、以降は高速読み込み

---

## 注意点・制約事項

1. **大規模スクリプト**
   - MAIN_APP.pyは300KB超の大規模ファイル
   - 部分読み込みが必要な場合がある

2. **エンコーディング**
   - ログファイル: UTF-8
   - CSV: UTF-8（郵便番号データ）

3. **外部依存**
   - AutoHotkeyの実行ファイルが必要
   - 郵便番号CSVデータが必要（初回のみ）

4. **仮想環境**
   - 仮想環境名: `input_img`
   - Python 3.10.14

---

## 次の調査項目

1. `_create_data_list.py`の詳細調査（サイズが大きいため分割読み込み）
2. `_text_edit_dialog.py`の詳細調査
3. MAIN_APP.py本体の機能詳細（部分的に読み込み）
4. 設定ファイルの構造（rect_config等）
5. データフローの詳細分析

---

## セッション情報

- 調査日: 2025-10-24
- 調査対象: MAIN_APP.py および依存モジュール
- 未読ファイル: _create_data_list.py, _text_edit_dialog.py, MAIN_APP.py本体
