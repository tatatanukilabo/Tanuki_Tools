import streamlit as st
from PIL import Image
import io
import json
import os
import math

def render():
    st.set_page_config(page_title="ギフト進捗確認画像作成", layout="wide")
    st.markdown("## 🖼️ ギフト進捗確認画像作成アプリ")

    uploaded_file = st.file_uploader("📥 ギフト進捗データ（JSON）をアップロード", type="json")

    if uploaded_file:
        try:
            gift_data = json.load(uploaded_file)
            st.success("✅ JSONの読み込みに成功しました")

            # 🔧 列数選択（1〜8） 初期値は2列（index=1）
            st.markdown("---")
            col_count = st.selectbox("表示する列数を選択してください", options=list(range(1, 9)), index=1)

            st.markdown("### 🎁 ギフト一覧プレビュー")
            cols = st.columns(col_count)

            images = []
            tile_size = (150, 150)

            # ✅ チェックマーク画像の読み込み（サイズ変更なし）
            try:
                check_path = os.path.join("assets", "icons", "check.png")
                with open(check_path, "rb") as f:
                    check_img = Image.open(f).convert("RGBA")
            except FileNotFoundError:
                st.warning("⚠️ チェックマーク画像が見つかりません。重ね処理はスキップされます。")
                check_img = None

            for i, filename in enumerate(gift_data):
                path = os.path.join("assets", "data", filename)
                try:
                    with open(path, "rb") as f:
                        img = Image.open(io.BytesIO(f.read())).convert("RGBA").resize(tile_size)

                        # ✅ 達成ステータスならチェックマークを中央に重ねる
                        if gift_data[filename].get("status") == "達成" and check_img:
                            cx = (tile_size[0] - check_img.width) // 2
                            cy = (tile_size[1] - check_img.height) // 2
                            img.paste(check_img, (cx, cy), check_img)

                        images.append(img)

                        with cols[i % col_count]:
                            display_name = os.path.splitext(filename)[0]
                            st.image(img, width=150)
                            st.markdown(f"📄 ギフト名: `{display_name}`")

                except Exception as e:
                    with cols[i % col_count]:
                        st.warning(f"{filename} の表示に失敗しました: {e}")

            # 🎨 背景色選択（初期値 #00BFFF）をプレビューの後に表示
            st.markdown("---")
            st.markdown("### 🎨 合成画像（進捗確認画像）の背景色を選択")
            bg_color_hex = st.color_picker("背景色を選択してください", value="#00BFFF")
            bg_color_rgb = tuple(int(bg_color_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (255,)

            # 🧩 合成画像（進捗確認画像）の生成と表示・ダウンロード
            st.markdown("---")
            st.markdown("### 🧩 進捗確認画像の生成とダウンロード")

            if images:
                gap = 10      # タイル間のスキマ
                margin = 10   # 外枠の余白
                rows_count = math.ceil(len(images) / col_count)

                canvas_width = tile_size[0] * col_count + gap * (col_count - 1) + margin * 2
                canvas_height = tile_size[1] * rows_count + gap * (rows_count - 1) + margin * 2
                canvas = Image.new("RGBA", (canvas_width, canvas_height), bg_color_rgb)

                for idx, img in enumerate(images):
                    x = margin + (idx % col_count) * (tile_size[0] + gap)
                    y = margin + (idx // col_count) * (tile_size[1] + gap)
                    canvas.paste(img, (x, y))

                st.image(canvas, caption="進捗確認画像", use_column_width=True)

                buf = io.BytesIO()
                canvas.save(buf, format="PNG")

                st.download_button(
                    label="📥 進捗画像をダウンロード",
                    data=buf.getvalue(),
                    file_name="progress.png",
                    mime="image/png"
                )

        except json.JSONDecodeError:
            st.error("❌ JSONの形式が正しくありません")

if __name__ == "__main__":
    render()
