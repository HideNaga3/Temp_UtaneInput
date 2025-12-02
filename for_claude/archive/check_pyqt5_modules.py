"""
PyQt5のどのモジュールがインポートされているか確認
使用していないQt5モジュールを特定
"""
from pathlib import Path
import re

# 全Pythonファイルを検索
py_files = [Path('MAIN_APP.py')] + list(Path('_lib').glob('*.py'))

# PyQt5のインポートを収集
pyqt5_imports = set()

for py_file in py_files:
    if py_file.exists():
        try:
            content = py_file.read_text(encoding='utf-8')
            # from PyQt5 import XXX または from PyQt5.XXX import の形式を検索
            matches = re.findall(r'from\s+PyQt5(?:\.(\w+))?\s+import\s+([^#\n]+)', content)
            for module, imports in matches:
                if module:
                    pyqt5_imports.add(module)
                else:
                    # from PyQt5 import XXX, YYY の形式
                    for item in imports.split(','):
                        item = item.strip()
                        if item and not item.startswith('('):
                            pyqt5_imports.add(item)
        except:
            pass

print("=" * 80)
print("使用中のPyQt5モジュール")
print("=" * 80)
for module in sorted(pyqt5_imports):
    print(f"  - {module}")

# 除外可能な大きなQt5モジュール
large_qt_modules = {
    'QtWebEngine': '20-30 MB',
    'QtWebEngineCore': '含まれる',
    'QtWebEngineWidgets': '含まれる',
    'QtWebEngineProcess': '含まれる',
    'QtMultimedia': '5-10 MB',
    'QtMultimediaWidgets': '含まれる',
    'QtNetwork': '2-5 MB',
    'QtPositioning': '1-3 MB',
    'QtQml': '5-10 MB',
    'QtQuick': '含まれる',
    'QtQuickWidgets': '含まれる',
    'QtSensors': '1-2 MB',
    'QtSerialPort': '1-2 MB',
    'QtSql': '1-2 MB',
    'QtSvg': '1-2 MB',
    'QtTest': '1-2 MB',
    'QtWebSockets': '1-2 MB',
    'QtXml': '1-2 MB',
    'QtXmlPatterns': '1-2 MB',
    'Qt3DCore': '5-10 MB',
    'Qt3DRender': '含まれる',
    'QtBluetooth': '1-2 MB',
    'QtDBus': '1-2 MB',
    'QtDesigner': '5-10 MB',
    'QtHelp': '1-2 MB',
    'QtLocation': '5-10 MB',
    'QtMacExtras': '1-2 MB',
    'QtNfc': '1-2 MB',
    'QtOpenGL': '1-2 MB',
    'QtPrintSupport': '1-2 MB',
    'QtWinExtras': '1-2 MB',
    'QtX11Extras': '1-2 MB',
}

print("\n" + "=" * 80)
print("除外可能なPyQt5モジュール（使用していない場合）")
print("=" * 80)

excludable = []
for module, size in large_qt_modules.items():
    if module not in pyqt5_imports:
        excludable.append((module, size))
        print(f"  - {module:30s} : {size}")

if not excludable:
    print("除外可能な大きなモジュールは見つかりませんでした")
    print("（または全て使用中）")

# 実際に使用しているもの
print("\n" + "=" * 80)
print("必須PyQt5モジュール（使用中）")
print("=" * 80)

essential = ['QtCore', 'QtGui', 'QtWidgets']
for module in essential:
    status = "使用中" if module in pyqt5_imports else "未検出"
    print(f"  - {module:30s} : {status}")

# hiddenimports推奨
print("\n" + "=" * 80)
print("推奨設定")
print("=" * 80)

if excludable:
    print("\n.ps1ファイルに以下を追加することで削減可能：\n")
    print("$ExcludeOptions = @(")
    print("    # 既存の除外設定...")
    print()
    print("    # PyQt5の不要モジュール（未使用）")
    for module, size in excludable[:10]:  # 上位10個
        print(f'    "--exclude-module", "PyQt5.{module}"')
    print(")")

    total_est = sum(
        20 if '20-30' in size else
        7 if '5-10' in size else
        1.5 if '1-2' in size else
        2.5 if '2-5' in size else
        0
        for _, size in excludable
    )
    print(f"\n推定削減サイズ: 約 {total_est:.0f} MB")
else:
    print("現在使用中のモジュールは全て必須です")

print("\n" + "=" * 80)
print("その他のサイズ削減方法")
print("=" * 80)

print("""
1. UPX圧縮を有効化
   変更前: "--noupx"
   変更後: "--upx", "--upx-dir", "C:\\path\\to\\upx"
   効果: 30-50% 削減（約25-40 MB削減）
   デメリット: 起動が若干遅くなる、ウイルススキャンで誤検知の可能性

2. バイトコード最適化
   .ps1に追加: $BasicOptions += "--optimize", "2"
   効果: 小幅削減（1-3 MB）
   デメリット: なし

3. 分割ビルド（--onedir）
   変更前: "--onefile"
   変更後: "--onedir"
   効果: メインexeは小さくなるが、総容量は変わらない
   メリット: 起動が速い、更新が容易

推奨順位:
1位: PyQt5不要モジュール除外（最も効果的、リスク低）
2位: バイトコード最適化（リスクなし）
3位: UPX圧縮（効果大、若干のリスク）
""")
