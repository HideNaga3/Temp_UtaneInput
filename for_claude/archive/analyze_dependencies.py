"""
PyInstallerのTOC（Table of Contents）を解析
実際にEXEに含まれているファイルを確認
"""
from pathlib import Path
import re

# warn-*.txtファイルを探す
build_folder = Path(r'build\給与計算検定1級入力アプリ_試作V1')

if not build_folder.exists():
    print("buildフォルダが見つかりません")
    exit(1)

print("=" * 80)
print("PyInstallerビルド依存関係分析")
print("=" * 80)

# warn-xxx.txtファイルを探す
warn_files = list(build_folder.glob('warn-*.txt'))

if warn_files:
    print(f"\n警告ファイルが見つかりました: {len(warn_files)}個")
    for warn_file in warn_files:
        print(f"\n--- {warn_file.name} ---")
        content = warn_file.read_text(encoding='utf-8', errors='ignore')
        # Qtに関する警告を抽出
        qt_warnings = [line for line in content.split('\n') if 'qt' in line.lower() or 'pyqt' in line.lower()]
        if qt_warnings:
            print("Qt関連の警告:")
            for warning in qt_warnings[:20]:  # 最初の20行
                print(f"  {warning}")

# xref-*.htmlを確認（クロスリファレンス）
xref_files = list(build_folder.glob('xref-*.html'))
if xref_files:
    print(f"\n\nクロスリファレンスファイル: {len(xref_files)}個")
    for xref in xref_files:
        print(f"  - {xref.name}")

# Analysis-*.txtを確認
analysis_files = list(build_folder.glob('Analysis-*.txt'))
if analysis_files:
    print(f"\n\n解析ファイル: {len(analysis_files)}個")
    # 最新のファイルを読む
    latest = max(analysis_files, key=lambda x: x.stat().st_mtime)
    print(f"\n最新の解析ファイル: {latest.name}")

    try:
        content = latest.read_text(encoding='utf-8', errors='ignore')

        # PyQt5関連の行を抽出
        lines = content.split('\n')
        pyqt5_lines = [line for line in lines if 'pyqt5' in line.lower() or 'qt5' in line.lower()]

        if pyqt5_lines:
            print(f"\nPyQt5/Qt5関連の依存関係: {len(pyqt5_lines)}行")
            print("\n最初の50行:")
            for i, line in enumerate(pyqt5_lines[:50], 1):
                print(f"  {i:3d}. {line[:100]}")

        # 除外されたモジュールを確認
        excluded = [line for line in lines if 'exclud' in line.lower()]
        if excluded:
            print(f"\n\n除外関連の記述: {len(excluded)}行")
            print("\n最初の20行:")
            for i, line in enumerate(excluded[:20], 1):
                print(f"  {i:3d}. {line[:100]}")

    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")

# PYZアーカイブを確認
pyz_files = list(build_folder.glob('*.pyz'))
if pyz_files:
    print(f"\n\nPYZアーカイブ: {len(pyz_files)}個")
    for pyz in pyz_files:
        size_mb = pyz.stat().st_size / (1024 * 1024)
        print(f"  - {pyz.name}: {size_mb:.2f} MB")

# PKGファイルを確認
pkg_files = list(build_folder.glob('*.pkg'))
if pkg_files:
    print(f"\n\nPKGファイル: {len(pkg_files)}個")
    for pkg in pkg_files:
        size_mb = pkg.stat().st_size / (1024 * 1024)
        print(f"  - {pkg.name}: {size_mb:.2f} MB")

# 実際のビルドログを確認するための推奨
print("\n\n" + "=" * 80)
print("推奨: PyInstallerをデバッグモードで再実行")
print("=" * 80)
print("""
以下のコマンドで詳細なログを取得できます：

PowerShell内で.ps1スクリプトを編集し、以下を追加：
  \"--log-level\", \"DEBUG\"

または、手動でPyInstallerを実行：
  python -m PyInstaller --log-level=DEBUG (他のオプション...)

これにより、どのモジュールが実際に除外されているか確認できます。
""")

# 実際にインポートされるモジュールを動的に確認
print("\n" + "=" * 80)
print("実行時の実際のPyQt5モジュール確認")
print("=" * 80)

try:
    import PyQt5.QtCore
    print(f"PyQt5.QtCore: インポート成功")
    print(f"  パス: {PyQt5.QtCore.__file__}")
except ImportError as e:
    print(f"PyQt5.QtCore: インポート失敗 - {e}")

try:
    import PyQt5.QtWidgets
    print(f"PyQt5.QtWidgets: インポート成功")
    print(f"  パス: {PyQt5.QtWidgets.__file__}")
except ImportError as e:
    print(f"PyQt5.QtWidgets: インポート失敗 - {e}")

# 除外を試みたモジュール
excluded_test = [
    'PyQt5.QtWebEngine',
    'PyQt5.QtMultimedia',
    'PyQt5.QtNetwork',
]

print(f"\n除外を試みたモジュールのインポート確認:")
for module in excluded_test:
    try:
        __import__(module)
        print(f"  [!] {module}: インポート可能（除外されていない）")
    except ImportError:
        print(f"  [OK] {module}: インポート不可（正しく除外された）")
