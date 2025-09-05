import streamlit as st
from PIL import Image
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

            st.markdown("### 🎁 ギフト一覧プレビュー")
            cols = st.columns(4)

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
                        img = Image.open(f).convert("RGBA").resize(tile_size)

                        # ✅ 達成ステータスならチェックマークを中央に重ねる
                        if gift_data[filename].get("status") == "達成" and check_img:
                            cx = (tile_size[0] - check_img.width) // 2
                            cy = (tile_size[1] - check_img.height) // 2
                            img.paste(check_img, (cx, cy), check_img)

                        images.append(img)

                        with cols[i % 4]:
                            st.image(img, caption=filename, width=150)

                except Exception as e:
                    with cols[i % 4]:
                        st.warning(f"{filename} の表示に失敗しました: {e}")

            # 🧩 合成画像の生成と表示・ダウンロード
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
