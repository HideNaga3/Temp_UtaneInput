# change_layout_horizontal の問題分析

## 問題の症状

横レイアウト (`change_layout_horizontal`) に切り替えると、1フレームに3ペアではなく6ペアが表示される。

## 原因の特定

### データ構造の問題

`_lib/_create_data_list.py` の `data_list_payroll` において、以下のフレームで `layout_a_name` の割り当てが正しくありません:

#### ❌ 問題のあるフレーム

**1. frame_1_ (問1-3)**
```
index 3 (問1): layout_a_name = 'horizontalLayout_0_'  ← 本来は 'horizontalLayout_1_'
index 4 (問2): layout_a_name = 'horizontalLayout_0_'  ← 本来は 'horizontalLayout_1_'
index 5 (問3): layout_a_name = 'horizontalLayout_0_'  ← 本来は 'horizontalLayout_1_'
```

**2. frame_2_ (問4-6)**
```
index 6 (問4): layout_a_name = 'horizontalLayout_0_'  ← 本来は 'horizontalLayout_2_'
index 7 (問5): layout_a_name = 'horizontalLayout_1_'  ← 本来は 'horizontalLayout_2_'
index 8 (問6): layout_a_name = 'horizontalLayout_2_'  ✓ これは正しい
```

### なぜ6ペアになるのか

`change_layout_horizontal` 関数は、`data_list` の各項目に対して:

```python
for data in self.data_list:
    current_hlayout_obj = data['layout_a_obj']  # 縦レイアウトのレイアウト
    next_hlayout_obj = data['layout_b_obj']      # 横レイアウトのレイアウト

    # ウィジェットを layout_a から layout_b に移動
    current_hlayout_obj.removeWidget(current_line_edit_obj)
    current_hlayout_obj.removeWidget(current_label_obj)
    next_hlayout_obj.insertWidget(0, current_label_obj)
    next_hlayout_obj.insertWidget(1, current_line_edit_obj)
```

#### 問題のメカニズム

**frame_2_ の場合:**

- **問4 (index 6)**:
  - `layout_a_name = 'horizontalLayout_0_'` (frame_0_ と共有)
  - frame_0_ の3つ (受験番号、会場、氏名) と問4が同じレイアウトを共有

- **問5 (index 7)**:
  - `layout_a_name = 'horizontalLayout_1_'` (frame_1_ と共有)
  - frame_1_ の3つ (問1-3) と問5が同じレイアウトを共有

- **問6 (index 8)**:
  - `layout_a_name = 'horizontalLayout_2_'` (正しい)
  - 問6だけが独立したレイアウト

**結果:**
横レイアウトに切り替えた時、`horizontalLayout_2_` に対応する `layout_b` レイアウトには:
- 問6のみが配置されるはずだが、
- 実際には frame_2_ の視覚的な領域に他のフレームのウィジェットも混在してしまう

または、逆に他のフレームに frame_2_ のウィジェットが混在する。

## 正しい構造

各フレームの全項目は、**同じ `layout_a_name`** を共有する必要があります:

```
frame_0_  (index 0-2)  → すべて 'horizontalLayout_0_'  ✓ 正しい
frame_1_  (index 3-5)  → すべて 'horizontalLayout_1_'  ✗ 現在は 0_
frame_2_  (index 6-8)  → すべて 'horizontalLayout_2_'  ✗ 現在は 0_, 1_, 2_
frame_3_  (index 9-11) → すべて 'horizontalLayout_3_'  ✓ 正しい
... (以降は正しい)
```

## 修正が必要な箇所

### _lib/_create_data_list.py

**修正1: frame_1_ (3箇所)**
```python
# 行9, 10, 11 あたり
'layout_a_name': 'horizontalLayout_0_'  →  'horizontalLayout_1_'
```

**修正2: frame_2_ (2箇所)**
```python
# 問4 (index 6)
'layout_a_name': 'horizontalLayout_0_'  →  'horizontalLayout_2_'

# 問5 (index 7)
'layout_a_name': 'horizontalLayout_1_'  →  'horizontalLayout_2_'

# 問6 (index 8) - すでに正しい
'layout_a_name': 'horizontalLayout_2_'  ✓
```

### 注意点

ファイル内に **2つのセクション** があります:
- **行9付近**: `data_list_payroll` の定義
- **行64付近**: 別の定義（おそらく別のモード用）

**両方のセクションを修正する必要があります。**

## 検証方法

修正後、以下のスクリプトで検証可能:

```bash
python temp/find_layout_pattern.py
```

すべてのフレームで "OK" が表示されれば修正完了。

## まとめ

**根本原因**: `frame_1_` と `frame_2_` の項目が、異なるフレームのレイアウトを参照している

**影響範囲**: 横レイアウトに切り替えた時のウィジェット配置

**修正箇所**: `_lib/_create_data_list.py` の2箇所（行9付近と行64付近）

**修正内容**: 合計8行の `layout_a_name` を修正
- frame_1_: 3行 (index 3, 4, 5)
- frame_2_: 2行 (index 6, 7)