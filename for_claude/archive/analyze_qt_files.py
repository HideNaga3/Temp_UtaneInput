"""
buildフォルダ内のQt関連ファイルを分析
PyQt5モジュールがどのように含まれているか確認
"""
from pathlib import Path
from collections import defaultdict

build_folder = Path(r'build\給与計算検定1級入力アプリ_試作V1')

if not build_folder.exists():
    print("buildフォルダが見つかりません")
    exit(1)

print("=" * 80)
print("Qt関連ファイルの分析")
print("=" * 80)

# Qt関連のDLLとPYDを検索
qt_files = defaultdict(list)
qt_modules_found = set()

all_files = list(build_folder.rglob('*'))
all_files = [f for f in all_files if f.is_file()]

for file in all_files:
    name_lower = file.name.lower()

    # Qt DLLファイル
    if name_lower.startswith('qt5') or name_lower.startswith('qt6'):
        size_mb = file.stat().st_size / (1024 * 1024)
        qt_files['Qt DLL'].append((file.name, size_mb))

        # モジュール名を抽出
        if 'webengine' in name_lower:
            qt_modules_found.add('QtWebEngine')
        elif 'multimedia' in name_lower:
            qt_modules_found.add('QtMultimedia')
        elif 'network' in name_lower:
            qt_modules_found.add('QtNetwork')
        elif 'qml' in name_lower:
            qt_modules_found.add('QtQml')
        elif 'quick' in name_lower:
            qt_modules_found.add('QtQuick')
        elif 'svg' in name_lower:
            qt_modules_found.add('QtSvg')
        elif 'sql' in name_lower:
            qt_modules_found.add('QtSql')
        elif 'xml' in name_lower:
            qt_modules_found.add('QtXml')
        elif 'opengl' in name_lower:
            qt_modules_found.add('QtOpenGL')
        elif 'widgets' in name_lower:
            qt_modules_found.add('QtWidgets')
        elif 'gui' in name_lower:
            qt_modules_found.add('QtGui')
        elif 'core' in name_lower:
            qt_modules_found.add('QtCore')

    # PyQt5 PYDファイル
    elif 'pyqt5' in name_lower and file.suffix.lower() in ['.pyd', '.so']:
        size_mb = file.stat().st_size / (1024 * 1024)
        qt_files['PyQt5 PYD'].append((file.name, size_mb))

        # モジュール名を抽出
        if 'webengine' in name_lower:
            qt_modules_found.add('QtWebEngine')
        elif 'multimedia' in name_lower:
            qt_modules_found.add('QtMultimedia')
        elif 'network' in name_lower:
            qt_modules_found.add('QtNetwork')

# 結果を表示
for category, files in sorted(qt_files.items()):
    total_size = sum(size for _, size in files)
    print(f"\n{category}")
    print(f"  ファイル数: {len(files)}")
    print(f"  合計サイズ: {total_size:.2f} MB")

    # 大きいファイル順に表示
    files_sorted = sorted(files, key=lambda x: x[1], reverse=True)
    print(f"  上位10ファイル:")
    for name, size in files_sorted[:10]:
        if size > 0.1:  # 0.1MB以上のみ表示
            print(f"    {name:50s} {size:6.2f} MB")

print("\n" + "=" * 80)
print("検出されたQtモジュール")
print("=" * 80)
for module in sorted(qt_modules_found):
    print(f"  - {module}")

# 除外設定と比較
excluded_modules = {
    'QtWebEngine', 'QtWebEngineCore', 'QtWebEngineWidgets', 'QtWebEngineProcess',
    'QtMultimedia', 'QtMultimediaWidgets', 'QtNetwork', 'QtPositioning',
    'QtQml', 'QtQuick', 'QtQuickWidgets', 'QtSensors', 'QtSerialPort',
    'QtSql', 'QtSvg', 'QtTest', 'QtWebSockets', 'QtXml', 'QtXmlPatterns',
    'Qt3DCore', 'Qt3DRender', 'QtBluetooth', 'QtDBus', 'QtDesigner',
    'QtHelp', 'QtLocation', 'QtNfc', 'QtOpenGL', 'QtPrintSupport', 'QtWinExtras'
}

print("\n" + "=" * 80)
print("除外設定したが実際に含まれているモジュール")
print("=" * 80)

still_included = qt_modules_found.intersection(excluded_modules)
if still_included:
    for module in sorted(still_included):
        print(f"  [!] {module} - 除外設定したが含まれている")
else:
    print("  除外設定したモジュールは含まれていません")

# PyQt5関連のpycファイルも確認
print("\n" + "=" * 80)
print("PyQt5 Pythonモジュール (.pyc)")
print("=" * 80)

pyqt5_pyc = [f for f in all_files if 'pyqt5' in str(f).lower() and f.suffix == '.pyc']
print(f"PyQt5関連の.pycファイル数: {len(pyqt5_pyc)}")

# モジュール名を集計
module_names = defaultdict(int)
for file in pyqt5_pyc:
    parts = file.parts
    for part in parts:
        if part.lower().startswith('qt'):
            module_names[part] += 1

if module_names:
    print("\nPyQt5モジュール別ファイル数:")
    for module, count in sorted(module_names.items(), key=lambda x: x[1], reverse=True):
        print(f"  {module:30s}: {count:3d} ファイル")

print("\n" + "=" * 80)
print("結論")
print("=" * 80)
print("""
PyInstallerの--exclude-moduleは、Pythonモジュール(.pyc)の除外には効果がありますが、
Qt DLLファイルは別の方法で管理されています。

PyQt5の場合、以下の理由でサイズが減らない可能性があります：
1. Qt5Core.dll, Qt5Gui.dll, Qt5Widgets.dllは必須DLLで除外できない
2. 他のQtモジュールのDLLが依存関係で自動的に含まれている
3. --exclude-moduleはPython側のバインディングを除外するが、DLL自体は残る

有効な対策：
1. カスタム.specファイルでbinariesを手動で除外
2. ビルド後に不要なDLLを手動削除してテスト
3. より積極的なbinaries除外hookを作成
""")
