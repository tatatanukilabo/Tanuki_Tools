import csv
import json
import os

# 現在のディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))


# Shift_JIS → UTF-8 変換
input_file = os.path.join(current_dir, 'list.csv')
output_file = os.path.join(current_dir, 'list_utf8.csv')

with open(input_file, 'r', encoding='shift_jis') as f_in:
    content = f_in.read()

with open(output_file, 'w', encoding='utf-8') as f_out:
    f_out.write(content)

csv_path = os.path.join(current_dir, 'list_utf8.csv')
json_path = os.path.join(current_dir, 'list.json')

data = []

with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append({
            "filename": row["filename"],
            "point": int(row["point"]),
            "category": row["category"]
        })

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"変換完了: {json_path}")