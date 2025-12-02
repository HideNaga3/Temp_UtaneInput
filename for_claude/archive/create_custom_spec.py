"""
カスタム.specファイルを生成して、不要なQt DLLを除外
"""
from pathlib import Path

spec_file = Path('給与計算検定1級入力アプリ_試作V1.spec')

if not spec_file.exists():
    print(f".specファイルが見つかりません: {spec_file}")
    exit(1)

# 現在の.specファイルを読み込む
content = spec_file.read_text(encoding='utf-8')

# DLL除外のためのフックを作成
exclude_dlls = [
    # 確実に不要（大きい順）
    'opengl32sw.dll',         # 19.95 MB - Software OpenGL
    'Qt5Designer.dll',        # 4.28 MB - Designer tools
    'd3dcompiler_47.dll',     # 3.98 MB - Direct3D compiler
    'Qt5Quick.dll',           # 3.96 MB - QML Quick
    'Qt5Qml.dll',             # 3.43 MB - QML engine
    'Qt5XmlPatterns.dll',     # 2.52 MB - XML patterns
    'Qt5Location.dll',        # 1.57 MB - Location services
    'Qt5Network.dll',         # 1.28 MB - Network (pandasのclipboard用に念のため残すか検討)
    'Qt5Quick3D*.dll',        # 1.19 MB+ - 3D rendering
    'Qt5QuickTemplates2.dll', # 1.06 MB - Quick templates
    'Qt5Multimedia*.dll',     # 0.81 MB - Multimedia
    'Qt5Bluetooth.dll',       # 0.52 MB
    'Qt5RemoteObjects.dll',   # 0.46 MB
    'Qt5QuickParticles.dll',  # 0.46 MB
    'Qt5QmlModels.dll',       # 0.42 MB
    'Qt5DBus.dll',            # 0.42 MB - Linux only
    'Qt5Help.dll',            # 0.41 MB
    'Qt5Svg.dll',             # 0.32 MB
    'Qt5OpenGL.dll',          # 0.31 MB - Old OpenGL API
    'Qt5PrintSupport.dll',    # 0.30 MB
    'Qt5Positioning.dll',     # 0.30 MB
    'Qt5Test.dll',            # 0.23 MB
    'Qt5WinExtras.dll',       # 0.23 MB
    'Qt5Quick3DRender.dll',   # 0.22 MB
    'Qt5QuickShapes.dll',     # 0.21 MB
    'Qt5Xml.dll',             # 0.20 MB
    'Qt5Sql.dll',             # 0.20 MB
    'Qt5Sensors.dll',         # 0.20 MB
    'Qt5QuickControls2.dll',  # 0.17 MB
    'Qt5WebSockets.dll',      # 0.14 MB
    'Qt5Nfc.dll',             # 0.13 MB
    'Qt5WebChannel.dll',      # 0.13 MB
    'Qt5QuickTest.dll',       # 0.12 MB
    'Qt5Quick3DAssetImport.dll', # 0.11 MB
    'Qt5PositioningQuick.dll',   # 0.10 MB
    'Qt5MultimediaWidgets.dll',  # 0.10 MB
    'Qt5QuickWidgets.dll',   # 0.08 MB
    'Qt5WebView.dll',        # 0.07 MB
    'Qt5SerialPort.dll',     # 0.07 MB
    'Qt5QmlWorkerScript.dll',# 0.05 MB
    'Qt5TextToSpeech.dll',   # 0.05 MB
    'Qt5Quick3DUtils.dll',   # 0.04 MB
]

# 推定削減サイズを計算
estimated_savings = 19.95 + 4.28 + 3.98 + 3.96 + 3.43 + 2.52 + 1.57 + 1.28 + 1.19 + 1.06 + 0.81 + 0.52 + 0.46 + 0.46 + 0.42 + 0.42 + 0.41 + 0.32 + 0.31 + 0.30 + 0.30 + 0.23 + 0.23 + 0.22 + 0.21 + 0.20 + 0.20 + 0.20 + 0.17 + 0.14 + 0.13 + 0.13 + 0.12 + 0.11 + 0.10 + 0.10 + 0.08 + 0.07 + 0.07 + 0.05 + 0.05 + 0.04

print("=" * 80)
print("カスタム.specファイル生成")
print("=" * 80)
print(f"\n現在の.specファイル: {spec_file}")
print(f"推定削減サイズ: {estimated_savings:.2f} MB")
print(f"現在のEXEサイズ: 79.08 MB")
print(f"削減後の予想サイズ: {79.08 - estimated_savings:.2f} MB")

# カスタムフック用のPythonスクリプトを生成
hook_content = f'''"""
PyQt5の不要なDLLを除外するためのカスタムフック
"""
def exclude_dlls(binaries):
    """不要なDLLを除外"""
    exclude_list = {exclude_dlls}

    new_binaries = []
    excluded_count = 0
    excluded_size_info = []

    for binary in binaries:
        dll_name = binary[0].split('\\\\')[-1].split('/')[-1].lower()

        # 除外リストとマッチするかチェック（ワイルドカード対応）
        should_exclude = False
        for pattern in exclude_list:
            pattern_lower = pattern.lower()
            if '*' in pattern_lower:
                # ワイルドカード処理
                pattern_prefix = pattern_lower.split('*')[0]
                if dll_name.startswith(pattern_prefix):
                    should_exclude = True
                    break
            else:
                if dll_name == pattern_lower:
                    should_exclude = True
                    break

        if should_exclude:
            excluded_count += 1
            excluded_size_info.append(binary[0])
        else:
            new_binaries.append(binary)

    print(f"除外したDLL: {{excluded_count}}個")
    for dll in excluded_size_info[:10]:  # 最初の10個を表示
        print(f"  - {{dll}}")

    return new_binaries


# PyInstallerのフック関数
from PyInstaller.utils.hooks import logger

def hook(hook_api):
    """PyInstallerフック"""
    logger.info("カスタムDLL除外フックを適用中...")
'''

hook_file = Path('hook-PyQt5_custom.py')
# hook_file.write_text(hook_content, encoding='utf-8')
# print(f"\nカスタムフックファイルを作成しました: {hook_file}")

# より簡単な方法: .specファイルを直接編集
print("\n" + "=" * 80)
print("推奨される方法: .specファイルを直接編集")
print("=" * 80)

print("""
以下の手順で.specファイルを編集してDLLを除外できます：

1. 給与計算検定1級入力アプリ_試作V1.spec を開く

2. Analysis() の後（exe = EXE() の前）に以下を追加：

# ========== DLL除外処理 ==========
exclude_dll_names = [
    'opengl32sw.dll',
    'Qt5Designer.dll',
    'd3dcompiler_47.dll',
    'Qt5Quick.dll',
    'Qt5Qml.dll',
    'Qt5XmlPatterns.dll',
    'Qt5Location.dll',
    # Qt5Network.dllは pandasのclipboardが使う可能性があるため注意
    # 'Qt5Network.dll',
    'Qt5Multimedia.dll',
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

# Quick3D関連（ワイルドカード）
exclude_dll_patterns = ['Qt5Quick3D']

# binariesから除外
filtered_binaries = []
for binary in a.binaries:
    dll_name = binary[0].split('\\\\')[-1].split('/')[-1]

    # 完全一致チェック
    if dll_name in exclude_dll_names:
        print(f"Excluding: {dll_name}")
        continue

    # パターンマッチチェック
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

3. .specファイルを保存

4. .specファイルから直接ビルド：
   python -m PyInstaller 給与計算検定1級入力アプリ_試作V1.spec

注意:
- Qt5Network.dllを除外すると、pandasのclipboard機能に影響がある可能性
- opengl32sw.dllを除外すると、古いPCで表示に問題が出る可能性
- まずは保守的に除外して、動作確認後に追加で除外を検討
""")

print("\n" + "=" * 80)
print("または、自動で編集したい場合")
print("=" * 80)
print("このスクリプトに編集機能を追加できますが、")
print("手動編集の方が安全で、カスタマイズも容易です。")
print("\n自動編集を希望する場合は、実行前にバックアップを作成してください。")
