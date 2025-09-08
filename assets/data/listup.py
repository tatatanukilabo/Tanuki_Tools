import os
import json
import re

# スクリプトのあるディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# JSONデータを格納する辞書
data = {}

# スクリプトのあるディレクトリ内のファイルを走査
for filename in os.listdir(script_dir):
    if filename.endswith(".png"):
        name = filename[:-4]  # 拡張子除去

        # 正規表現で category と point を抽出
        match = re.match(r"(.+?)_(\d+)_\d+", name)
        if match:
            category, point = match.groups()
            data[filename] = {
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