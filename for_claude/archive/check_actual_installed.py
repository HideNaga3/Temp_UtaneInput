"""
実際にインストールされているパッケージで、
ビルドに含まれているが不要なものを特定
"""
import subprocess
import json

# pip listから実際にインストールされているパッケージを取得
result = subprocess.run(
    ['.venv/Scripts/python.exe', '-m', 'pip', 'list', '--format=json'],
    capture_output=True,
    text=True
)

installed = json.loads(result.stdout)
installed_names = {pkg['name'].lower() for pkg in installed}

print("=" * 80)
print("実際にインストールされているパッケージ")
print("=" * 80)
print(f"合計: {len(installed)} パッケージ")

# 不要そうなパッケージをチェック
suspicious = {
    'urllib3': 'HTTP通信未使用',
    'requests': 'HTTP通信未使用',
    'openpyxl': 'Excel機能未使用',
    'lxml': 'XML処理未使用',
    'beautifulsoup4': 'HTML解析未使用',
    'sqlalchemy': 'ORM未使用',
    'cryptography': '暗号化未使用',
    'pillow': 'PIL画像処理未使用',
    'matplotlib': 'グラフ描画未使用',
    'scipy': '科学計算未使用',
}

print("\n" + "=" * 80)
print("不要な可能性があるパッケージ（インストール済み）")
print("=" * 80)

found_suspicious = []
for pkg, reason in suspicious.items():
    if pkg in installed_names:
        # サイズ情報を取得
        size_result = subprocess.run(
            ['.venv/Scripts/python.exe', '-m', 'pip', 'show', pkg],
            capture_output=True,
            text=True
        )
        # サイズを抽出（大まかな目安）
        found_suspicious.append((pkg, reason))
        print(f"[FOUND] {pkg:20s} - {reason}")

if not found_suspicious:
    print("疑わしいパッケージは見つかりませんでした")
    print("（または全て既に除外設定済み）")

print("\n" + "=" * 80)
print("必須パッケージ（インストール確認）")
print("=" * 80)

required = ['pandas', 'numpy', 'pyqt5', 'pymupdf', 'exifread', 'jaconv']
for pkg in required:
    status = "OK" if pkg in installed_names else "NG"
    print(f"[{status}] {pkg}")

print("\n" + "=" * 80)
print("推奨アクション")
print("=" * 80)
if found_suspicious:
    print("以下のパッケージを除外設定に追加することで、サイズ削減の可能性があります：")
    for pkg, reason in found_suspicious:
        print(f"  --exclude-module {pkg}")
else:
    print("現在の除外設定は適切です。")
    print("これ以上の大幅なサイズ削減は難しい可能性があります。")
