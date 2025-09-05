import streamlit as st
from PIL import Image, ImageDraw
import io
import json
import os
import math

def render():
    st.markdown("## 🖼️ ギフト進捗確認画像作成アプリ")

    uploaded_file = st.file_uploader("📥 ギフト進捗データ（JSON）をアップロード", type="json")

    if uploaded_file:
        try:
            gift_data = json.load(uploaded_file)
            st.success("✅ JSONの読み込みに成功しました")

            # タイル表示設定
            st.markdown("### 🎁 ギフト一覧プレビュー")
            cols = st.columns(4)

            images = []
            tile_size = (150, 150)
            check_path = os.path.join("assets", "icon", "check.png")
            check_img = Image.open(check_path).convert("RGBA").resize((40, 40))

            for i, filename in enumerate(gift_data):
                path = os.path.join("assets", "data", filename)
                try:
                    with open(path, "rb") as f:
                        img = Image.open(io.BytesIO(f.read())).convert("RGBA").resize(tile_size)
                        if gift_data[filename].get("status") == "達成":
                            img.paste(check_img, (tile_size[0] - 45, tile_size[1] - 45), check_img)
                        images.append(img)
                        with cols[i % 4]:
                            st.image(img, caption=filename, width=150)
                except Exception as e:
                    with cols[i % 4]:
                        st.warning(f"{filename} の表示に失敗しました: {e}")

            # 合成画像の生成
            st.markdown("---")
            st.markdown("### 🧩 進捗確認画像の生成とダウンロード")

            if images:
                cols_count = 4
                rows_count = math.ceil(len(images) / cols_count)
                canvas = Image.new("RGBA", (tile_size[0] * cols_count, tile_size[1] * rows_count), (255, 255, 255, 255))

                for idx, img in enumerate(images):
                    x = (idx % cols_count) * tile_size[0]
                    y = (idx // cols_count) * tile_size[1]
                    canvas.paste(img, (x, y))

                # 表示とダウンロード
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

