"""
opengl32sw.dllとd3dcompiler_47.dllがなぜ含まれているか調査
PyQt5のレンダリングシステムとの関係を確認
"""
from pathlib import Path
import sys

print("=" * 80)
print("PyQt5のグラフィックス関連DLL調査")
print("=" * 80)

# Qt5のドキュメントとアーキテクチャ
print("""
【背景知識】

PyQt5（Qt5）は、クロスプラットフォームでの描画を実現するため、
複数のレンダリングバックエンドを持っています：

1. **ANGLE (Almost Native Graphics Layer Engine)**
   - OpenGL ES → Direct3D 9/11 変換レイヤー
   - Windows環境でのOpenGL互換性を確保
   - d3dcompiler_47.dll を使用

2. **ソフトウェアOpenGL (Mesa)**
   - ハードウェアアクセラレーションなしで描画
   - opengl32sw.dll (MESA software renderer)
   - 古いPC、仮想マシン、GPUドライバがない環境用のフォールバック

3. **ネイティブOpenGL**
   - システムのOpenGL実装を直接使用
   - 最も高速だが、環境依存性が高い
""")

print("\n" + "=" * 80)
print("PyQt5のQt5プラットフォームプラグインを確認")
print("=" * 80)

pyqt5_path = Path('.venv/Lib/site-packages/PyQt5')
if not pyqt5_path.exists():
    print(f"PyQt5が見つかりません: {pyqt5_path}")
    exit(1)

# プラットフォームプラグインを確認
platforms_path = pyqt5_path / 'Qt5' / 'plugins' / 'platforms'
if platforms_path.exists():
    print(f"\nプラットフォームプラグイン: {platforms_path}")
    for plugin in platforms_path.glob('*.dll'):
        size_mb = plugin.stat().st_size / (1024 * 1024)
        print(f"  - {plugin.name:30s} {size_mb:6.2f} MB")

        # qwindows.dllの情報
        if plugin.name == 'qwindows.dll':
            print(f"\n    → これがWindowsメインプラットフォームプラグイン")
            print(f"    → OpenGL/ANGLEレンダリングに依存")

# Qt confファイルを確認
qt_conf = pyqt5_path / 'Qt5' / 'bin' / 'qt.conf'
if qt_conf.exists():
    print(f"\nQt設定ファイル: {qt_conf}")
    print(qt_conf.read_text(encoding='utf-8', errors='ignore'))

print("\n" + "=" * 80)
print("各DLLの役割と依存関係")
print("=" * 80)

dll_info = {
    'opengl32sw.dll': {
        'サイズ': '19.95 MB',
        '役割': 'Mesa ソフトウェアOpenGL実装',
        '使用目的': [
            'ハードウェアOpenGLが利用できない環境でのフォールバック',
            '仮想マシン、リモートデスクトップ環境',
            '古いGPU、ドライバがない環境',
            'Qt::AA_UseSoftwareOpenGL が有効な場合'
        ],
        '依存元': [
            'qwindows.dll (プラットフォームプラグイン)',
            'Qt5Gui.dll (OpenGLサポート)',
        ],
        '除外の影響': [
            '⚠ ハードウェアOpenGLがない環境で描画失敗',
            '⚠ RDP、VMwareなどで画面が表示されない可能性',
            '✓ 最新PC、物理マシンのみで使う場合は不要'
        ]
    },
    'd3dcompiler_47.dll': {
        'サイズ': '3.98 MB',
        '役割': 'Direct3D HLSLシェーダーコンパイラ',
        '使用目的': [
            'ANGLE（OpenGL → Direct3D変換）でシェーダーコンパイル',
            'Qt::AA_UseOpenGLES（デフォルト）で使用',
            'libGLESv2.dll経由でDirect3Dレンダリング'
        ],
        '依存元': [
            'libGLESv2.dll (ANGLE OpenGL ES実装)',
            'Qt5Gui.dll (OpenGL/ANGLEサポート)',
        ],
        '除外の影響': [
            '⚠ ANGLE使用時にシェーダーコンパイルエラー',
            '⚠ Qt Widgetsの一部エフェクトが動作しない可能性',
            '△ ネイティブOpenGLにフォールバックする可能性'
        ]
    },
    'libGLESv2.dll': {
        'サイズ': '3.23 MB',
        '役割': 'ANGLE OpenGL ES 2.0実装',
        '使用目的': [
            'OpenGL ES API → Direct3D 11変換',
            'Windowsでの安定したOpenGL互換レイヤー',
            'デフォルトのQtレンダリングバックエンド'
        ],
        '依存元': [
            'Qt5Gui.dll',
            'Qt5Widgets.dll',
            'qwindows.dll'
        ],
        '除外の影響': [
            '✗ 除外すると描画システムが動作しない',
            '✗ 必須DLL（Qt5のデフォルトレンダラー）'
        ]
    },
    'libEGL.dll': {
        'サイズ': '0.02 MB',
        '役割': 'EGL (OpenGL ESインターフェース)',
        '使用目的': [
            'OpenGL ESコンテキスト管理',
            'ANGLEとアプリケーション間の橋渡し'
        ],
        '依存元': [
            'libGLESv2.dll',
            'Qt5Gui.dll'
        ],
        '除外の影響': [
            '✗ 除外すると描画システムが動作しない',
            '✗ 必須DLL'
        ]
    }
}

for dll_name, info in dll_info.items():
    print(f"\n【{dll_name}】")
    print(f"サイズ: {info['サイズ']}")
    print(f"役割: {info['役割']}")
    print(f"\n使用目的:")
    for purpose in info['使用目的']:
        print(f"  • {purpose}")
    print(f"\n依存元:")
    for dep in info['依存元']:
        print(f"  ← {dep}")
    print(f"\n除外した場合の影響:")
    for impact in info['除外の影響']:
        print(f"  {impact}")

print("\n" + "=" * 80)
print("Qtのレンダリングバックエンド選択")
print("=" * 80)

print("""
Qtアプリケーションは起動時に以下の順序でレンダリングバックエンドを選択：

1. 環境変数 QT_OPENGL の確認
   - "desktop"    → ネイティブOpenGL
   - "angle"      → ANGLE (OpenGL ES → D3D)
   - "software"   → ソフトウェアレンダリング

2. QApplication::setAttribute() の確認
   - Qt::AA_UseDesktopOpenGL
   - Qt::AA_UseOpenGLES (デフォルト) ← ANGLE使用
   - Qt::AA_UseSoftwareOpenGL

3. 環境に応じて自動選択
   デフォルト: ANGLE (libGLESv2.dll + d3dcompiler_47.dll)
   フォールバック: Software (opengl32sw.dll)

【現在のMAIN_APP.pyの設定】
""")

# MAIN_APP.pyでの設定を確認
main_app = Path('MAIN_APP.py')
if main_app.exists():
    content = main_app.read_text(encoding='utf-8')

    # OpenGL関連の設定を検索
    opengl_settings = [
        'QT_OPENGL',
        'AA_UseDesktopOpenGL',
        'AA_UseOpenGLES',
        'AA_UseSoftwareOpenGL',
        'setAttribute'
    ]

    found_settings = []
    for setting in opengl_settings:
        if setting in content:
            # 該当行を抽出
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if setting in line and not line.strip().startswith('#'):
                    found_settings.append(f"  行{i}: {line.strip()}")

    if found_settings:
        print("OpenGL関連の設定が見つかりました:")
        for setting in found_settings:
            print(setting)
    else:
        print("→ 明示的なOpenGL設定なし")
        print("→ デフォルト: ANGLE (libGLESv2.dll + d3dcompiler_47.dll)")
        print("→ フォールバック: Software (opengl32sw.dll)")

print("\n" + "=" * 80)
print("推奨事項")
print("=" * 80)

print("""
【除外の判断基準】

1. opengl32sw.dll (19.95 MB)
   ✓ 除外推奨（以下の条件を満たす場合）
     • 対象ユーザーが物理マシン（非VM）を使用
     • Windows 7以降でGPUドライバがインストール済み
     • リモートデスクトップ経由での使用を想定しない

   ✗ 除外非推奨
     • 仮想マシン環境での使用を想定
     • 古いPCや、GPUドライバなし環境をサポート
     • リモートデスクトップ（RDP）経由での使用

2. d3dcompiler_47.dll (3.98 MB)
   △ 条件付き除外可能
     • ANGLE使用時は必須
     • ネイティブOpenGLにフォールバックできる
     • ただし、Qtのデフォルトバックエンド（ANGLE）が使えなくなる

   推奨: 残す（わずか4MBで互換性が大幅向上）

3. libGLESv2.dll (3.23 MB)
   ✗ 除外不可
     • QtのデフォルトレンダリングエンジンANGLE本体
     • 除外するとGUIが描画されない

【最終推奨】

オプション1: 安全重視（現在の設定）
  - opengl32sw.dll: 含める
  - d3dcompiler_47.dll: 含める
  - サイズ: 75.67 MB
  - 互換性: 最高（全環境で動作）

オプション2: サイズ重視（リスク小）
  - opengl32sw.dll: 除外
  - d3dcompiler_47.dll: 含める
  - サイズ: 約55-56 MB
  - 互換性: 高（最新PC、物理マシンで動作）
  - リスク: VM、古いPC、RDPで描画失敗の可能性

オプション3: 最小サイズ（リスク中）
  - opengl32sw.dll: 除外
  - d3dcompiler_47.dll: 除外
  - サイズ: 約51-52 MB
  - 互換性: 中（環境によってはエラー）
  - リスク: ANGLE使用時にシェーダーエラー

【テスト方法】

各オプションでビルド後、以下を確認：
1. 通常起動（物理マシン）
2. VM環境での起動（VirtualBox、VMwareなど）
3. リモートデスクトップ経由での起動
4. 古いPC（オンボードGPU）での起動

問題が発生した場合、次のレベルのフォールバックを含める。
""")

print("\n" + "=" * 80)
print("実行時にOpenGLバックエンドを確認する方法")
print("=" * 80)

print("""
アプリケーションにデバッグ出力を追加して、実際にどのバックエンドが
使用されているか確認できます：

```python
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

# OpenGLコンテキスト情報を取得
from PyQt5.QtGui import QOpenGLContext
context = QOpenGLContext()
if context.create():
    print(f"OpenGL Vendor: {context.functions().glGetString(0x1F00)}")
    print(f"OpenGL Renderer: {context.functions().glGetString(0x1F01)}")
    print(f"OpenGL Version: {context.functions().glGetString(0x1F02)}")
```

ソフトウェアレンダラーの場合:
  → Renderer: "llvmpipe" または "Software Rasterizer"

ANGLEの場合:
  → Renderer: "ANGLE (Direct3D11)"

ネイティブOpenGLの場合:
  → Renderer: GPUの名前（例: "NVIDIA GeForce GTX..."）
""")
