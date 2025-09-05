import os
import json

# スクリプト自身が存在するディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# そのディレクトリ内の .png ファイルを列挙
png_files = [f for f in os.listdir(script_dir) if f.lower().endswith('.png')]

# JSONとして改行付きで保存
json_path = os.path.join(script_dir, 'list.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(png_files, f, ensure_ascii=False, indent=2)

print(f"{json_path} に PNG一覧を保存しました。")