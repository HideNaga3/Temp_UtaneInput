"""
buildフォルダを分析してサイズ削減方法を探す
"""
from pathlib import Path
from collections import defaultdict
import os

build_folder = Path(r'build\給与計算検定1級入力アプリ_試作V1')

if not build_folder.exists():
    print("buildフォルダが見つかりません")
    exit(1)

# 全ファイルを取得
all_files = list(build_folder.rglob('*'))
all_files = [f for f in all_files if f.is_file()]

# 拡張子別の統計
ext_stats = defaultdict(lambda: {'count': 0, 'total_size': 0, 'files': []})

for file in all_files:
    ext = file.suffix.lower() if file.suffix else '(なし)'
    size = file.stat().st_size
    ext_stats[ext]['count'] += 1
    ext_stats[ext]['total_size'] += size
    ext_stats[ext]['files'].append((file.name, size))

print("=" * 80)
print("拡張子別ファイル統計（サイズ順）")
print("=" * 80)

# サイズでソート
sorted_exts = sorted(ext_stats.items(), key=lambda x: x[1]['total_size'], reverse=True)

for ext, stats in sorted_exts[:20]:
    size_mb = stats['total_size'] / (1024 * 1024)
    print(f"\n{ext:15s} : {stats['count']:4d} 個, 合計 {size_mb:8.2f} MB")

    # 大きなファイル上位3個を表示
    top_files = sorted(stats['files'], key=lambda x: x[1], reverse=True)[:3]
    for fname, fsize in top_files:
        fsize_mb = fsize / (1024 * 1024)
        if fsize_mb > 0.1:  # 0.1MB以上のみ表示
            print(f"    - {fname[:50]:50s} {fsize_mb:6.2f} MB")

# 最大ファイル
print("\n" + "=" * 80)
print("最大ファイル TOP 20")
print("=" * 80)

all_files_sorted = sorted(all_files, key=lambda x: x.stat().st_size, reverse=True)

for i, file in enumerate(all_files_sorted[:20], 1):
    size_mb = file.stat().st_size / (1024 * 1024)
    rel_path = file.relative_to(build_folder)
    print(f"{i:2d}. {size_mb:8.2f} MB - {rel_path}")

# DLLファイルの分析
print("\n" + "=" * 80)
print("DLLファイル分析")
print("=" * 80)

dll_files = [f for f in all_files if f.suffix.lower() == '.dll']
dll_total = sum(f.stat().st_size for f in dll_files) / (1024 * 1024)

print(f"DLL総数: {len(dll_files)} 個")
print(f"DLL合計サイズ: {dll_total:.2f} MB")
print(f"\n大きなDLL TOP 10:")

dll_sorted = sorted(dll_files, key=lambda x: x.stat().st_size, reverse=True)
for i, dll in enumerate(dll_sorted[:10], 1):
    size_mb = dll.stat().st_size / (1024 * 1024)
    print(f"{i:2d}. {size_mb:6.2f} MB - {dll.name}")

# PYZファイルの分析
print("\n" + "=" * 80)
print("Python アーカイブファイル (.pyz)")
print("=" * 80)

pyz_files = [f for f in all_files if f.suffix.lower() in ['.pyz', '.pyc']]
if pyz_files:
    pyz_total = sum(f.stat().st_size for f in pyz_files) / (1024 * 1024)
    print(f"PYZ/PYC総数: {len(pyz_files)} 個")
    print(f"PYZ/PYC合計サイズ: {pyz_total:.2f} MB")
    for pyz in pyz_files:
        size_mb = pyz.stat().st_size / (1024 * 1024)
        if size_mb > 1:
            print(f"  - {pyz.name}: {size_mb:.2f} MB")

# 合計サイズ
total_size = sum(f.stat().st_size for f in all_files) / (1024 * 1024)
print("\n" + "=" * 80)
print(f"buildフォルダ合計サイズ: {total_size:.2f} MB")
print(f"総ファイル数: {len(all_files)}")
print("=" * 80)

# サイズ削減の提案
print("\n" + "=" * 80)
print("サイズ削減の提案")
print("=" * 80)

print("""
1. UPXによる圧縮（現在無効）
   - --noupx を削除して --upx を使用
   - DLLとEXEを圧縮（30-50%削減可能）
   - 起動速度が若干遅くなる可能性あり

2. バイトコード最適化
   - --optimize 2 を使用
   - Pythonバイトコードを最適化（小幅な削減）

3. PyQt5の不要モジュール除外
   - QtWebEngine, QtWebEngineCore, QtWebEngineWidgets
   - QtMultimedia, QtNetwork（未使用の場合）
   - 各モジュール10-30MB削減可能

4. DLLの精査
   - 不要なQt DLLを除外
   - msvcp, vcruntime以外のVC++ランタイム

5. データファイルの最適化
   - アイコンファイルの圧縮
   - 不要なリソースファイルの削除
""")
