# 既知の問題と対処法

## 1. PowerShellでの日本語文字化け

### 問題
PowerShellの`Get-Content`コマンドでUTF-8ファイルを読み込むと日本語が文字化けする

### 例
```powershell
Get-Content 'for_claude\log.txt'
# 結果: ���[�h�ŗL���W�b�N (文字化け)
```

### 対処法
- **推奨**: Readツールを使用
- **代替**: `-Encoding UTF8`を指定（完全には解決しない）
- **最善**: UTF-8 BOMで保存

### コード例
```python
# 正しい方法: Readツールを使用
Read("for_claude/log.txt")

# Python内でUTF-8 BOM保存
with open('file.txt', 'w', encoding='utf-8-sig') as f:
    f.write(content)
```

---

## 2. Serena言語サーバーの警告

### 問題
インデックス作成時に大量の警告が表示される
```
WARNING: Received None response from the Language Server
```

### 原因
- 構文エラーのあるファイル
- 不完全なテストファイル
- 言語サーバーが理解できないコード構造

### 対処法
- **通常は無視してOK** - インデックス作成には影響しない
- 特定のファイルで問題が続く場合は `ignored_paths` に追加

---

## 3. モード固有ロジックの分散

### 問題
モード別の処理がMAIN_APP.pyに散在し、拡張性が低い

### 対処法 (セッション10で実施済み)
- `_mode_config.py`に設定を一元化
- `get_name_from_df()`等のメソッドでカプセル化
- 新モード追加時は設定するだけ

### コード例
```python
# 悪い例 (削除済み)
if main_mode in ['prevention', 'syuei']:
    name_column = 7
elif main_mode == 'prevention2':
    name_column = 8
# ...

# 良い例 (現在)
name = self.mode_config_manager.get_name_from_df(
    self.main_mode, df, row_index
)
```

---

## 4. ハードコードされたリスト

### 問題
フレームリストが手動で膨大に定義されている

### 対処法 (セッション9で実施済み)
- ループ生成に変更
- 設定辞書で管理

### コード例
```python
# 悪い例 (削除済み)
frame_list = [
    {'index': 0, 'frame_name': 'frame_0_', ...},
    {'index': 1, 'frame_name': 'frame_1_', ...},
    # ... 49行続く
]

# 良い例 (現在)
frame_list = [
    {
        'index': i,
        'frame_name': f'frame_{i}_',
        'frame_obj': '',
        'is_visible': True,
        'stretch': [0, 1, 0, 1, 0, 1]
    }
    for i in range(start_index, start_index + frame_count)
]
```

---

## 5. 共通パターンの重複

### 問題
スクロールエリア更新制御、モード判定ロジック等が複数箇所に重複

### 対処法 (今後の課題)
- コンテキストマネージャ化
- 統一メソッド化
- デコレーター化

### 推定効果
- 100-150行削減
- 保守性向上
