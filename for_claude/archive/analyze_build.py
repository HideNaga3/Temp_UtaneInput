"""
PyInstallerのビルド分析スクリプト
Analysis-00.tocを読み込んで、含まれているモジュールを分析
"""
import ast
from pathlib import Path
from collections import defaultdict

# Analysis-00.tocファイルを読み込む
toc_file = Path(r"build\給与計算検定1級入力アプリ_試作V1\Analysis-00.toc")

with open(toc_file, 'r', encoding='utf-8') as f:
    content = f.read()

# tocファイルはPythonのタプルリストなので、evalで評価
try:
    toc_data = ast.literal_eval(content)
except:
    print("tocファイルの解析に失敗しました")
    exit(1)

# 含まれているモジュールを抽出（通常は14番目の要素）
if len(toc_data) > 14:
    modules = toc_data[14]

    # モジュール名でグループ化
    module_groups = defaultdict(list)

    for item in modules:
        if len(item) >= 3:
            module_name = item[0]
            module_type = item[2]

            # トップレベルのパッケージ名を取得
            top_package = module_name.split('.')[0]
            module_groups[top_package].append((module_name, module_type))

    # 結果を表示
    print(f"総モジュール数: {len(modules)}\n")
    print("=" * 80)
    print("トップレベルパッケージ別のモジュール数:")
    print("=" * 80)

    # モジュール数でソート
    sorted_groups = sorted(module_groups.items(), key=lambda x: len(x[1]), reverse=True)

    for package, items in sorted_groups[:50]:  # 上位50個を表示
        print(f"{package:30s} : {len(items):4d} モジュール")

    print("\n" + "=" * 80)
    print("不要そうなモジュール（チェック推奨）:")
    print("=" * 80)

    # 不要そうなパッケージをチェック
    suspicious = [
        'unittest', 'test', 'doctest', 'pdb', 'pydoc',
        'tkinter', 'turtle',
        'email', 'smtplib', 'poplib', 'imaplib',
        'http', 'urllib', 'xmlrpc',
        'sqlite3', 'dbm',
        'curses', 'asyncio',
        'multiprocessing', 'concurrent',
        'setuptools', 'pip', 'distutils',
        'IPython', 'jupyter', 'notebook',
        'matplotlib', 'scipy', 'sympy',
        'lxml', 'bs4', 'beautifulsoup',
        'requests', 'flask', 'django',
        'cryptography', 'ssl'
    ]

    found_suspicious = []
    for package in suspicious:
        if package in module_groups:
            found_suspicious.append((package, len(module_groups[package])))

    if found_suspicious:
        for package, count in found_suspicious:
            print(f"[WARNING] {package:30s} : {count:4d} モジュール")
    else:
        print("疑わしいモジュールは見つかりませんでした")

    print("\n" + "=" * 80)
    print("必要なモジュール（確認）:")
    print("=" * 80)

    # 必要なパッケージ
    required = ['PyQt5', 'pandas', 'numpy', 'PyMuPDF', 'fitz',
                'jaconv', 'ExifRead', 'win32']

    for package in required:
        if package in module_groups:
            print(f"[OK] {package:30s} : {len(module_groups[package]):4d} モジュール")
        else:
            print(f"[NG] {package:30s} : 見つかりません")

else:
    print("tocファイルの構造が予期しないものです")
