"""
プロジェクト内の全import文を収集して分析
"""
import re
from pathlib import Path
from collections import defaultdict

def extract_imports(file_path):
    """ファイルからimport文を抽出"""
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # import文を検出
                if line.startswith('import ') or line.startswith('from '):
                    # コメント行を除外
                    if not line.startswith('#'):
                        imports.append(line)
    except:
        pass
    return imports

def get_module_name(import_line):
    """import文からモジュール名を取得"""
    # from xxx import yyy の形式
    if import_line.startswith('from '):
        match = re.match(r'from\s+([^\s]+)', import_line)
        if match:
            module = match.group(1)
            # 相対インポートを除外
            if not module.startswith('.'):
                return module.split('.')[0]
    # import xxx の形式
    elif import_line.startswith('import '):
        match = re.match(r'import\s+([^\s,]+)', import_line)
        if match:
            return match.group(1).split('.')[0]
    return None

# プロジェクトルート
root = Path('.')

# 対象ファイル
files_to_check = [
    Path('MAIN_APP.py'),
] + list(Path('_lib').glob('*.py'))

# import文を収集
all_imports = defaultdict(list)

for file_path in files_to_check:
    if file_path.exists():
        imports = extract_imports(file_path)
        for imp in imports:
            module = get_module_name(imp)
            if module:
                all_imports[module].append((file_path.name, imp))

# 標準ライブラリ（一部）
stdlib = {
    'os', 'sys', 'io', 'json', 're', 'time', 'datetime', 'pathlib',
    'collections', 'itertools', 'functools', 'operator',
    'typing', 'dataclasses', 'abc',
    'traceback', 'logging', 'warnings',
    'subprocess', 'threading', 'multiprocessing', 'concurrent',
    'ctypes', 'struct', 'pickle',
    'math', 'random', 'statistics',
    'string', 'textwrap',
    'argparse', 'configparser',
    'shutil', 'tempfile', 'glob',
    'urllib', 'http', 'email', 'smtplib', 'ssl',
    'xml', 'html', 'sqlite3',
    'unittest', 'doctest', 'pdb',
}

# 結果を分類
external_modules = {}
stdlib_modules = {}
local_modules = {}

for module, usages in all_imports.items():
    if module.startswith('_') or module in ['main_app_ui']:
        local_modules[module] = usages
    elif module in stdlib:
        stdlib_modules[module] = usages
    else:
        external_modules[module] = usages

print("=" * 80)
print("外部ライブラリ（requirements.txtに含めるべき）")
print("=" * 80)
for module in sorted(external_modules.keys()):
    print(f"{module:20s} : {len(external_modules[module])} 箇所で使用")

print("\n" + "=" * 80)
print("標準ライブラリ（使用されているもの）")
print("=" * 80)
for module in sorted(stdlib_modules.keys()):
    print(f"{module:20s} : {len(stdlib_modules[module])} 箇所で使用")

print("\n" + "=" * 80)
print("使用されていない可能性のある標準ライブラリ")
print("=" * 80)
unused_stdlib = [
    'email', 'smtplib', 'http', 'urllib', 'ssl',
    'unittest', 'doctest', 'pdb',
    'multiprocessing', 'concurrent',
    'xml', 'html', 'sqlite3',
]

for module in unused_stdlib:
    if module not in stdlib_modules:
        print(f"[NOT USED] {module}")

print("\n" + "=" * 80)
print("openpyxlの使用確認")
print("=" * 80)
if 'openpyxl' in external_modules:
    print("[USED] openpyxl が使用されています")
    for file, line in external_modules['openpyxl']:
        print(f"  {file}: {line}")
else:
    print("[NOT USED] openpyxl は使用されていません")

# pandasのExcel関連機能の使用確認
print("\n" + "=" * 80)
print("pandas Excel機能の使用確認")
print("=" * 80)

excel_patterns = ['to_excel', 'read_excel', 'ExcelWriter', 'ExcelFile']
excel_used = False

for file_path in files_to_check:
    if file_path.exists():
        try:
            content = file_path.read_text(encoding='utf-8')
            for pattern in excel_patterns:
                if pattern in content:
                    excel_used = True
                    print(f"[FOUND] {pattern} in {file_path.name}")
        except:
            pass

if not excel_used:
    print("[NOT USED] pandas Excel機能（to_excel, read_excel等）は使用されていません")
    print("[推奨] openpyxlを除外して問題ありません")

print("\n" + "=" * 80)
print("まとめ")
print("=" * 80)
print(f"外部ライブラリ: {len(external_modules)} 個")
print(f"標準ライブラリ: {len(stdlib_modules)} 個")
print(f"ローカルモジュール: {len(local_modules)} 個")
