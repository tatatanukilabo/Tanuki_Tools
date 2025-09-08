import os
import json
import re

# スクリプトのあるディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# JSONデータを格納する辞書
data = {}

# ディレクトリを再帰的に走査
for root, _, files in os.walk(script_dir):
    for filename in files:
        if filename.endswith(".png"):
            name = filename[:-4]  # 拡張子除去

            # 正規表現で category と point を抽出
            match = re.match(r"(.+?)_(\d+)_\d+", name)
            if match:
                category, point = match.groups()

                # 相対パスを取得し、/ 区切りに変換
                rel_dir = os.path.relpath(root, script_dir)
                rel_path = os.path.join(rel_dir, filename) if rel_dir != "." else filename
                rel_path = rel_path.replace("\\", "/")  # Windowsの\を/に変換

                data[rel_path] = {
                    "category": category,
                    "point": int(point)
                }
            else:
                print(f"⚠️ スキップ: ファイル名の形式が不正 → {filename}")

# JSONファイルの保存先もスクリプトのあるディレクトリに
output_path = os.path.join(script_dir, "list.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ JSONファイルを作成しました: {output_path}")