import os
import json
import re

# スクリプトのあるディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# 結果を格納する辞書
result = {}

# ディレクトリを再帰的に探索
for root, dirs, files in os.walk(script_dir):
    for file in files:
        if file.lower().endswith('.webp'):
            # ファイルのフルパス
            full_path = os.path.join(root, file)

            # ディレクトリ名（スクリプトディレクトリからの相対パス）
            rel_dir = os.path.relpath(root, script_dir)
            category = os.path.basename(rel_dir)

            # ファイル名から数値を抽出（先頭の数値）
            match = re.match(r'^(\d+)', file)
            point = int(match.group(1)) if match else None

            # キーを作成
            key = f"{category}/{file}"

            # 辞書に追加
            result[key] = {
                "category": category,
                "point": point
            }

# JSONとして保存（任意）
output_path = os.path.join(script_dir, "list.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"JSONファイルを保存しました: {output_path}")