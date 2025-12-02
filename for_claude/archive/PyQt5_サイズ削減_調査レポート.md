# PyQt5 サイズ削減 調査レポート

## 調査日時
2025-11-04

## 現状
- **現在のEXEサイズ**: 79.08 MB
- **ビルド方法**: PyInstaller --onefile

## 問題の発見

### 1. --exclude-moduleの限界
PowerShellスクリプトで30個のPyQt5モジュールを`--exclude-module`で除外設定したが、**わずか0.4 MBしか削減できなかった**（79.48 MB → 79.08 MB）。

### 2. 原因の特定

#### 調査1: .specファイルの確認
```python
excludes=['PyQt5.QtWebEngine', 'PyQt5.QtMultimedia', ...]
```
✓ 除外設定は正しく.specファイルに反映されていた

#### 調査2: 実際のモジュールインポート確認
```
PyQt5.QtWebEngine: インポート不可 ✓（正しく除外）
PyQt5.QtMultimedia: インポート可能 ✗（除外されていない）
PyQt5.QtNetwork: インポート可能 ✗（除外されていない）
```

**結論**: `--exclude-module`はPythonバインディング(.pyd)のみ除外し、**Qt DLL(.dll)は除外されない**

#### 調査3: pandasの依存関係
```python
# pandas/io/clipboard/__init__.py
from PyQt5.QtWidgets import QApplication  # 行145
import PyQt5  # 行586
```
pandasのクリップボード機能がPyQt5を条件付きでインポートするため、PyQt5モジュールが含まれてしまう。

#### 調査4: Qt DLLファイルの実態

**PyQt5のQt DLLファイル**: 58個、合計 **79.26 MB**

| DLL名 | サイズ | 用途 | 除外可否 |
|-------|--------|------|----------|
| opengl32sw.dll | 19.95 MB | ソフトウェアOpenGL | △ 除外可能だが古いPCで影響 |
| Qt5Gui.dll | 6.68 MB | GUI基本機能 | ✗ 必須 |
| Qt5Core.dll | 5.74 MB | Qt基本機能 | ✗ 必須 |
| Qt5Widgets.dll | 5.24 MB | ウィジェット | ✗ 必須 |
| Qt5Designer.dll | 4.28 MB | デザイナーツール | ✓ 除外可能 |
| d3dcompiler_47.dll | 3.98 MB | Direct3Dコンパイラ | △ 除外可能 |
| Qt5Quick.dll | 3.96 MB | QML Quick | ✓ 除外可能 |
| Qt5Qml.dll | 3.43 MB | QMLエンジン | ✓ 除外可能 |
| libGLESv2.dll | 3.23 MB | OpenGL ES | △ レンダリングに必要な可能性 |
| libcrypto-1_1-x64.dll | 3.06 MB | OpenSSL暗号 | △ Qt Networkが使用 |
| Qt5XmlPatterns.dll | 2.52 MB | XMLパターン | ✓ 除外可能 |
| Qt5Location.dll | 1.57 MB | 位置情報 | ✓ 除外可能 |
| Qt5Network.dll | 1.28 MB | ネットワーク | △ pandasが使う可能性 |
| その他40個 | 約13 MB | 各種機能 | ✓ ほぼ全て除外可能 |

**除外可能な合計**: 約 **50.80 MB**

## 解決方法

### 方法1: .specファイルを直接編集（推奨）

#### 手順

1. `給与計算検定1級入力アプリ_試作V1.spec` を開く

2. `exe = EXE()` の**直前**に以下のコードを挿入：

```python
# ========== DLL除外処理 ==========
exclude_dll_names = [
    'opengl32sw.dll',      # 19.95 MB - Software OpenGL
    'Qt5Designer.dll',     # 4.28 MB
    'd3dcompiler_47.dll',  # 3.98 MB
    'Qt5Quick.dll',        # 3.96 MB
    'Qt5Qml.dll',          # 3.43 MB
    'Qt5XmlPatterns.dll',  # 2.52 MB
    'Qt5Location.dll',     # 1.57 MB
    'Qt5Multimedia.dll',   # 0.71 MB
    'Qt5MultimediaWidgets.dll',
    'Qt5Bluetooth.dll',
    'Qt5RemoteObjects.dll',
    'Qt5QuickParticles.dll',
    'Qt5QmlModels.dll',
    'Qt5DBus.dll',
    'Qt5Help.dll',
    'Qt5Svg.dll',
    'Qt5OpenGL.dll',
    'Qt5PrintSupport.dll',
    'Qt5Positioning.dll',
    'Qt5Test.dll',
    'Qt5WinExtras.dll',
    'Qt5Xml.dll',
    'Qt5Sql.dll',
    'Qt5Sensors.dll',
    'Qt5QuickControls2.dll',
    'Qt5WebSockets.dll',
    'Qt5Nfc.dll',
    'Qt5WebChannel.dll',
    'Qt5QuickTest.dll',
    'Qt5QuickShapes.dll',
    'Qt5PositioningQuick.dll',
    'Qt5QuickWidgets.dll',
    'Qt5WebView.dll',
    'Qt5SerialPort.dll',
    'Qt5QmlWorkerScript.dll',
    'Qt5TextToSpeech.dll',
]

exclude_dll_patterns = ['Qt5Quick3D']

filtered_binaries = []
for binary in a.binaries:
    dll_name = binary[0].split('\\')[-1].split('/')[-1]

    if dll_name in exclude_dll_names:
        print(f"Excluding: {dll_name}")
        continue

    exclude = False
    for pattern in exclude_dll_patterns:
        if dll_name.startswith(pattern):
            print(f"Excluding (pattern): {dll_name}")
            exclude = True
            break

    if not exclude:
        filtered_binaries.append(binary)

a.binaries = filtered_binaries
# ========== DLL除外処理終了 ==========
```

3. .specファイルを保存

4. PowerShellで.specから直接ビルド：
```powershell
python -m PyInstaller 給与計算検定1級入力アプリ_試作V1.spec
```

### 期待される結果
- **削減前**: 79.08 MB
- **削減後**: 約 **28.28 MB**（**64%削減**）

## 注意事項

### 除外する際の注意点

1. **opengl32sw.dll (19.95 MB)**
   - ソフトウェアOpenGLレンダラー
   - ハードウェアOpenGLが利用できない古いPCでは表示に問題が出る可能性
   - 削減効果は最大だが、対象ユーザーのPC環境を確認推奨

2. **Qt5Network.dll (1.28 MB)**
   - pandasのクリップボード機能が条件付きで使用
   - アプリでクリップボード機能を使う場合は慎重に
   - 削減効果は小さいので、安全性を考慮して残すのも選択肢

3. **libGLESv2.dll (3.23 MB)**
   - OpenGL ES（組み込み向けOpenGL）
   - Qt Widgetsのレンダリングに必要な可能性
   - 除外リストに含めていないが、問題があれば追加検討

### 段階的アプローチ（推奨）

**フェーズ1: 確実に不要なもの（約36 MB削減）**
```python
exclude_dll_names = [
    'Qt5Designer.dll',     # 4.28 MB
    'Qt5Quick.dll',        # 3.96 MB
    'Qt5Qml.dll',          # 3.43 MB
    'Qt5XmlPatterns.dll',  # 2.52 MB
    'Qt5Location.dll',     # 1.57 MB
    # 以下、小さいものも含めて約20 MB分
]
exclude_dll_patterns = ['Qt5Quick3D', 'Qt5Qml', 'Qt5Positioning']
```

**フェーズ2: 動作確認後、追加削減（約15 MB削減）**
```python
# フェーズ1に追加
'opengl32sw.dll',      # 19.95 MB
'd3dcompiler_47.dll',  # 3.98 MB
```

## 代替案

### 方法2: UPX圧縮（組み合わせ可能）
```powershell
# .ps1ファイルで --noupx を削除し、以下を追加：
"--upx-dir", "C:\path\to\upx"
```
- 効果: 30-50%の追加圧縮
- デメリット: 起動が若干遅くなる、ウイルススキャンで誤検知の可能性

### 方法3: --onedirモード（配布形態の変更）
```powershell
"--onefile" を "--onedir" に変更
```
- EXE本体は小さくなるが、DLL群がフォルダに展開される
- 総容量は変わらないが、起動は速くなる

## まとめ

### 核心的な発見
**`--exclude-module`ではQt DLLは除外できない！**

PyInstallerの`--exclude-module`フラグはPython側のバインディング(.pyd)のみを除外し、実際のQt DLL(.dll)ファイルは自動的に依存関係解決で含まれてしまう。

### 推奨する対策
1. **.specファイルでbinariesを直接フィルタリング**（今回実装）
2. 段階的に除外して動作確認
3. 最終的に約28 MBまで削減可能

### ファイル一覧
- `check_pyqt5_modules.py`: PyQt5モジュール使用状況確認
- `analyze_build_size.py`: buildフォルダ分析
- `check_qt_dlls.py`: Qt DLLサイズ確認
- `find_qt_dependencies.py`: PyQt5依存関係調査
- `analyze_dependencies.py`: PyInstallerビルド依存関係
- `create_custom_spec.py`: .spec編集ガイド
- **このレポート**: `PyQt5_サイズ削減_調査レポート.md`

---

## 次のステップ

1. .specファイルを編集（フェーズ1の保守的なリストで）
2. .specから直接ビルド
3. EXEサイズ確認
4. **動作確認**（重要！）
   - アプリの全機能が動作するか
   - 画像表示に問題ないか
   - クリップボード機能が動作するか
5. 問題なければフェーズ2を検討

**目標サイズ**: 28-35 MB（現在の約1/3）
