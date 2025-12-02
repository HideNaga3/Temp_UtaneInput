# fill_rect_json.py
# rect.jsonのnullを上のデータで埋めるツール（Excelのフィル機能のように）
#
# 使い方:
#   python tools/fill_rect_json.py
#   （実行後、ファイルパスを入力）
#
# 注意:
#   - 元のファイルは自動的にバックアップされます（ファイル名_backup.json）
#   - ファイルパスの " は自動的に削除されます

import json
import sys
import shutil
from pathlib import Path
from datetime import datetime

def fill_null_with_previous(rect_data: dict) -> dict:
    """nullを上のデータで埋める（Excelのフィル機能）

    Args:
        rect_data: rect.jsonのデータ（辞書形式）

    Returns:
        dict: nullが埋められたデータ
    """
    filled_data = {}
    previous_rect = None

    # インデックスの数値順にソート
    sorted_keys = sorted(rect_data.keys(), key=lambda x: int(x))

    for key in sorted_keys:
        rect = rect_data[key]

        # すべての値がnullかチェック
        all_null = all(rect[field] is None for field in ['x', 'y', 'w', 'h', 'scale', 'angle'])

        if all_null and previous_rect is not None:
            # すべてnullの場合、前のデータをコピー
            filled_data[key] = previous_rect.copy()
            print(f"  [{key}] nullを前のデータで埋めました: x={filled_data[key]['x']}, y={filled_data[key]['y']}")
        else:
            # nullでない場合、そのまま使用
            filled_data[key] = rect.copy()
            # 次の反復のために保存（nullでない場合のみ）
            if not all_null:
                previous_rect = rect.copy()

    return filled_data


def main():
    """メイン処理"""
    print("=" * 80)
    print("rect.json フィルツール（Excelのフィル機能）")
    print("=" * 80)
    print()

    # ファイルパスを入力で取得
    file_path_input = input("rect.jsonのファイルパスを入力してください: ").strip()

    # ダブルクォートを削除
    file_path_input = file_path_input.replace('"', '').replace("'", '')

    input_path = Path(file_path_input)
    output_path = input_path  # 同じファイルに上書き

    print()
    print(f"入力ファイル: {input_path}")
    print(f"出力ファイル: {output_path}")
    print()

    # ファイルの存在確認
    if not input_path.exists():
        print(f"[ERROR] ファイルが見つかりません: {input_path}")
        sys.exit(1)

    # バックアップを作成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = input_path.parent / f"{input_path.stem}_backup_{timestamp}.json"

    print(f"[0] バックアップを作成中...")
    shutil.copy2(input_path, backup_path)
    print(f"    バックアップ保存: {backup_path}")
    print()

    # rect.jsonを読み込み
    print("[1] rect.jsonを読み込み中...")
    with open(input_path, 'r', encoding='utf-8') as f:
        rect_data = json.load(f)
    print(f"    エントリ数: {len(rect_data)}")

    # nullの数をカウント
    null_count = sum(1 for rect in rect_data.values()
                    if all(rect[field] is None for field in ['x', 'y', 'w', 'h', 'scale', 'angle']))
    print(f"    null エントリ数: {null_count}")
    print()

    # nullを埋める
    print("[2] nullを上のデータで埋めています...")
    filled_data = fill_null_with_previous(rect_data)
    print()

    # 結果を保存
    print("[3] 結果を保存中...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(filled_data, f, indent=4, ensure_ascii=False)
    print(f"    保存完了: {output_path}")
    print()

    # サマリー
    print("=" * 80)
    print(f"[SUCCESS] 完了しました！")
    print(f"  元ファイル: {input_path}")
    print(f"  バックアップ: {backup_path}")
    print(f"  null エントリ: {null_count} 個")
    print(f"  埋められたエントリ: {null_count} 個")
    print("=" * 80)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)