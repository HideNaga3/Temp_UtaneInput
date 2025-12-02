"""
distフォルダ内のexeファイルサイズを確認
"""
from pathlib import Path
from datetime import datetime

dist_folder = Path('dist')

if not dist_folder.exists():
    print("distフォルダが見つかりません")
    exit(1)

exe_files = list(dist_folder.glob('*.exe'))

if not exe_files:
    print("exeファイルが見つかりません")
    exit(1)

print("=" * 80)
print("dist フォルダ内のexeファイル")
print("=" * 80)

# ファイルサイズでソート
exe_files.sort(key=lambda x: x.stat().st_size, reverse=True)

for exe in exe_files:
    size_mb = exe.stat().st_size / (1024 * 1024)
    mtime = datetime.fromtimestamp(exe.stat().st_mtime)
    print(f"\n{exe.name}")
    print(f"  サイズ: {size_mb:.2f} MB")
    print(f"  最終更新: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")

print("\n" + "=" * 80)
print(f"合計: {len(exe_files)} 個のexeファイル")
print("=" * 80)
