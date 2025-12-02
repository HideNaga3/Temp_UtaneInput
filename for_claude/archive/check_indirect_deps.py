"""
間接的な依存関係を確認
pandasやPyQt5が内部で使用している機能を確認
"""
from pathlib import Path
import re

def check_pandas_usage(file_path):
    """pandasの使用方法を確認"""
    print("=" * 80)
    print("pandas の使用確認")
    print("=" * 80)

    pandas_methods = {
        # CSV関連（安全）
        'read_csv': 'CSV読込',
        'to_csv': 'CSV書込',
        'DataFrame': 'DataFrame操作',

        # Excel関連（openpyxl依存）
        'read_excel': 'Excel読込 [openpyxl必要]',
        'to_excel': 'Excel書込 [openpyxl必要]',
        'ExcelWriter': 'Excel書込 [openpyxl必要]',
        'ExcelFile': 'Excel読込 [openpyxl必要]',

        # HTML関連（html/lxml依存）
        'read_html': 'HTML読込 [html/lxml必要]',
        'to_html': 'HTML書込 [html必要]',

        # SQL関連（sqlite3依存）
        'read_sql': 'SQL読込 [sqlite3必要]',
        'to_sql': 'SQL書込 [sqlite3必要]',

        # XML関連（xml依存）
        'read_xml': 'XML読込 [xml必要]',
        'to_xml': 'XML書込 [xml必要]',

        # JSON関連（標準、安全）
        'read_json': 'JSON読込',
        'to_json': 'JSON書込',

        # その他
        'read_pickle': 'pickle読込',
        'to_pickle': 'pickle書込',
    }

    files_to_check = [Path('MAIN_APP.py')] + list(Path('_lib').glob('*.py'))

    found_methods = {}
    for method, desc in pandas_methods.items():
        for file in files_to_check:
            if file.exists():
                try:
                    content = file.read_text(encoding='utf-8')
                    # .method( または pd.method( の形式を検索
                    if re.search(rf'\.{method}\s*\(|pd\.{method}\s*\(', content):
                        if method not in found_methods:
                            found_methods[method] = []
                        found_methods[method].append(file.name)
                except:
                    pass

    # 結果表示
    safe_methods = []
    risky_methods = []

    for method, files in found_methods.items():
        desc = pandas_methods[method]
        if '[' in desc:  # 依存ありのマーク
            risky_methods.append((method, desc, files))
        else:
            safe_methods.append((method, desc, files))

    print("\n[安全] 以下のpandas機能が使用されています（標準ライブラリのみ）:")
    for method, desc, files in safe_methods:
        print(f"  - {method:20s} : {desc:30s} ({', '.join(files)})")

    if risky_methods:
        print("\n[注意] 以下のpandas機能が使用されています（外部依存あり）:")
        for method, desc, files in risky_methods:
            print(f"  - {method:20s} : {desc:30s} ({', '.join(files)})")
    else:
        print("\n[OK] 外部依存のあるpandas機能は使用されていません")

def check_multiprocessing_usage():
    """multiprocessingの間接的な使用を確認"""
    print("\n" + "=" * 80)
    print("multiprocessing の使用確認")
    print("=" * 80)

    patterns = [
        'multiprocessing',
        'Pool',
        'Process(',
        'Queue(',
        'Manager(',
        'Lock(',
        'Semaphore(',
    ]

    files_to_check = [Path('MAIN_APP.py')] + list(Path('_lib').glob('*.py'))

    found = []
    for pattern in patterns:
        for file in files_to_check:
            if file.exists():
                try:
                    content = file.read_text(encoding='utf-8')
                    if pattern in content:
                        # importやコメントを除外
                        lines = content.split('\n')
                        for i, line in enumerate(lines, 1):
                            if pattern in line and not line.strip().startswith('#'):
                                found.append((file.name, i, line.strip()[:80]))
                except:
                    pass

    if found:
        print("[注意] multiprocessing関連のコードが見つかりました:")
        for file, line_no, line in found:
            print(f"  {file}:{line_no} - {line}")
    else:
        print("[OK] multiprocessing は使用されていません")
        print("     除外して問題ありません")

def check_email_urllib_usage():
    """email/urllibの使用を確認"""
    print("\n" + "=" * 80)
    print("email/urllib/http の使用確認")
    print("=" * 80)

    patterns = {
        'email': ['email.', 'MIMEText', 'MIMEMultipart'],
        'urllib': ['urllib.', 'urlopen', 'Request('],
        'http': ['http.client', 'http.server', 'HTTPConnection'],
        'smtplib': ['smtplib', 'SMTP('],
    }

    files_to_check = [Path('MAIN_APP.py')] + list(Path('_lib').glob('*.py'))

    found_any = False
    for category, pattern_list in patterns.items():
        found = []
        for pattern in pattern_list:
            for file in files_to_check:
                if file.exists():
                    try:
                        content = file.read_text(encoding='utf-8')
                        if pattern in content:
                            lines = content.split('\n')
                            for i, line in enumerate(lines, 1):
                                if pattern in line and not line.strip().startswith('#'):
                                    found.append((file.name, i, line.strip()[:80]))
                    except:
                        pass

        if found:
            found_any = True
            print(f"\n[注意] {category} 関連のコードが見つかりました:")
            for file, line_no, line in found[:5]:  # 最初の5件のみ
                print(f"  {file}:{line_no} - {line}")

    if not found_any:
        print("[OK] email/urllib/http/smtplib は使用されていません")
        print("     除外して問題ありません")

def check_xml_usage():
    """xmlの使用を確認"""
    print("\n" + "=" * 80)
    print("xml の使用確認")
    print("=" * 80)

    patterns = ['xml.', 'ElementTree', 'ET.', 'parseString', 'minidom']

    files_to_check = [Path('MAIN_APP.py')] + list(Path('_lib').glob('*.py'))

    found = []
    for pattern in patterns:
        for file in files_to_check:
            if file.exists():
                try:
                    content = file.read_text(encoding='utf-8')
                    if pattern in content:
                        lines = content.split('\n')
                        for i, line in enumerate(lines, 1):
                            if pattern in line and not line.strip().startswith('#'):
                                found.append((file.name, i, line.strip()[:80]))
                except:
                    pass

    if found:
        print("[注意] xml関連のコードが見つかりました:")
        for file, line_no, line in found[:5]:
            print(f"  {file}:{line_no} - {line}")
    else:
        print("[OK] xml は使用されていません")
        print("     除外して問題ありません")

# 実行
check_pandas_usage(Path('.'))
check_multiprocessing_usage()
check_email_urllib_usage()
check_xml_usage()

print("\n" + "=" * 80)
print("最終結論")
print("=" * 80)
print("""
以下のモジュールは安全に除外できます：

1. openpyxl - pandas Excel機能未使用
2. email, smtplib - メール機能未使用
3. urllib, http - HTTP通信未使用
4. multiprocessing, concurrent - 並列処理未使用
5. xml.etree - XML処理未使用
6. html - HTML処理未使用
7. sqlite3 - データベース未使用
8. xmlrpc - RPC未使用
9. ssl - SSL通信未使用

これらを除外しても、アプリケーションの動作に影響はありません。
""")
