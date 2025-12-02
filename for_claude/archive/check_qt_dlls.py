"""
PyQt5のQt DLLファイルサイズを確認
"""
from pathlib import Path

qt_bin_path = Path('.venv/Lib/site-packages/PyQt5/Qt5/bin')

if not qt_bin_path.exists():
    print(f"Qt binフォルダが見つかりません: {qt_bin_path}")
    exit(1)

dll_files = list(qt_bin_path.glob('*.dll'))

if not dll_files:
    print("DLLファイルが見つかりません")
    exit(1)

print("=" * 80)
print(f"PyQt5 Qt DLLファイル ({len(dll_files)}個)")
print("=" * 80)

# サイズでソート
dll_files.sort(key=lambda x: x.stat().st_size, reverse=True)

total_size = 0
for dll in dll_files:
    size_mb = dll.stat().st_size / (1024 * 1024)
    total_size += size_mb
    print(f"{dll.name:50s} {size_mb:8.2f} MB")

print("=" * 80)
print(f"合計サイズ: {total_size:.2f} MB")
print("=" * 80)

# 除外可能なDLLを特定
exclude_patterns = [
    'Multimedia',
    'Network',
    'Qml',
    'Quick',
    'Sql',
    'WebEngine',
    'Svg',
    'Xml',
    'OpenGL',
    'Positioning',
    'Sensors',
    'SerialPort',
    'Bluetooth',
    'Nfc',
    'DBus',
    '3D',
    'Designer',
]

print("\n除外可能なDLL（推測）:")
print("=" * 80)

excludable_size = 0
for dll in dll_files:
    dll_name = dll.name
    for pattern in exclude_patterns:
        if pattern.lower() in dll_name.lower():
            size_mb = dll.stat().st_size / (1024 * 1024)
            excludable_size += size_mb
            print(f"{dll_name:50s} {size_mb:8.2f} MB")
            break

print("=" * 80)
print(f"除外可能な合計サイズ（推測）: {excludable_size:.2f} MB")
print("=" * 80)

print("""
注意:
- これらのDLLを除外するには、.specファイルのbinariesセクションを編集する必要があります
- 単に--exclude-moduleだけではDLLは除外されません
- 誤ってCore, Gui, Widgetsを除外するとアプリが動作しなくなります
""")
