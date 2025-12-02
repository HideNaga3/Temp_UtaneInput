"""
どのモジュールがPyQt5.QtMultimedia等を引き込んでいるか調査
"""
import sys
import importlib.util
from pathlib import Path

print("=" * 80)
print("PyQt5モジュールの依存関係調査")
print("=" * 80)

# 主要なインストール済みパッケージ
main_packages = [
    'pandas',
    'numpy',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
]

print("\n各パッケージがインポートするPyQt5モジュールを確認:")

for package_name in main_packages:
    print(f"\n{package_name}:")

    try:
        # モジュールをインポート
        if '.' in package_name:
            parts = package_name.split('.')
            module = __import__(package_name, fromlist=[parts[-1]])
        else:
            module = __import__(package_name)

        # モジュールの属性をチェック
        qt_refs = []
        for attr in dir(module):
            try:
                obj = getattr(module, attr)
                obj_module = getattr(obj, '__module__', '')
                if 'PyQt5' in obj_module or 'Qt5' in obj_module:
                    qt_refs.append(f"  - {attr} -> {obj_module}")
            except:
                pass

        if qt_refs:
            print("  PyQt5への参照を発見:")
            for ref in qt_refs[:10]:  # 最初の10個
                print(ref)
        else:
            print("  PyQt5への直接参照なし")

    except Exception as e:
        print(f"  インポートエラー: {e}")

# pandasのクリップボード機能を特に確認
print("\n" + "=" * 80)
print("pandasのクリップボード機能の確認")
print("=" * 80)

try:
    import pandas.io.clipboard
    print("pandas.io.clipboard をインポート成功")

    # このモジュールがどのバックエンドを使うか確認
    import inspect
    source_file = inspect.getfile(pandas.io.clipboard)
    print(f"ソースファイル: {source_file}")

    # ソースを読んで依存関係を確認
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'PyQt5' in content or 'QtCore' in content:
            print("\n[!] pandasのクリップボードモジュールがPyQt5を参照しています")
            # PyQt5の参照行を抽出
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'PyQt5' in line or 'QtCore' in line or 'QtWidgets' in line:
                    print(f"  行 {i}: {line.strip()}")
        else:
            print("\npandasのクリップボードモジュールはPyQt5を直接参照していません")

except Exception as e:
    print(f"確認エラー: {e}")

# PyQt5のインストール状況を確認
print("\n" + "=" * 80)
print("PyQt5のインストール状況")
print("=" * 80)

pyqt5_modules = [
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'PyQt5.QtMultimedia',
    'PyQt5.QtMultimediaWidgets',
    'PyQt5.QtNetwork',
    'PyQt5.QtWebEngine',
    'PyQt5.QtQml',
    'PyQt5.QtSql',
]

for module in pyqt5_modules:
    spec = importlib.util.find_spec(module)
    if spec:
        print(f"[存在] {module}")
        if spec.origin:
            path = Path(spec.origin)
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"        {spec.origin}")
            print(f"        サイズ: {size_mb:.2f} MB")
    else:
        print(f"[なし] {module}")

# DLLファイルを確認
print("\n" + "=" * 80)
print("PyQt5のDLLファイル")
print("=" * 80)

pyqt5_path = Path(sys.executable).parent / '.venv' / 'Lib' / 'site-packages' / 'PyQt5'
if not pyqt5_path.exists():
    pyqt5_path = Path('.venv') / 'Lib' / 'site-packages' / 'PyQt5'

if pyqt5_path.exists():
    dll_files = list(pyqt5_path.glob('*.dll'))
    if dll_files:
        print(f"DLLファイル数: {len(dll_files)}")
        print("\n大きなDLLファイル:")
        dll_sorted = sorted(dll_files, key=lambda x: x.stat().st_size, reverse=True)
        for dll in dll_sorted[:15]:
            size_mb = dll.stat().st_size / (1024 * 1024)
            if size_mb > 0.5:  # 0.5MB以上
                print(f"  {dll.name:40s} {size_mb:6.2f} MB")
    else:
        print("DLLファイルが見つかりません")
else:
    print(f"PyQt5ディレクトリが見つかりません: {pyqt5_path}")

print("\n" + "=" * 80)
print("結論")
print("=" * 80)
print("""
PyInstallerの--exclude-moduleがPython側のモジュールを除外しても、
以下の理由でDLLが残る可能性があります：

1. PyQt5のインストールには多数のDLLが含まれる
2. Qt5Core.dll, Qt5Gui.dll, Qt5Widgets.dllは他のモジュールからも参照される
3. PyInstallerはDLLの依存関係を自動で解決し、必要なものを全て含める
4. --exclude-moduleはPython側のインポートを防ぐが、DLLレベルでは防げない

解決策：
1. .specファイルのbinariesセクションを手動で編集してDLLを除外
2. PyInstallerのhookファイルを作成してDLLの自動収集を制御
3. ビルド後にEXEからDLLを抽出・削除して再パッケージ（高度）
""")
