import streamlit as st
from PIL import Image, ImageDraw, ImageOps
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

            # 🎨 ギフト画像の背景色（透過部分に敷く色）
            st.markdown("---")
            st.markdown("### 🎨 ギフト画像の背景色を選択")
            tile_bg_hex = st.color_picker("ギフト画像の背景色", value="#FFFFFF")
            tile_bg_rgb = tuple(int(tile_bg_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (255,)

            # 🎨 進捗バーの色設定
            st.markdown("### 🎨 進捗バーの色設定")
            progress_fill_hex = st.color_picker("進捗バーの色（達成部分）", value="#FF0000")
            progress_bg_hex = st.color_picker("進捗バーの背景色（未達部分）", value="#DDDDDD")
            progress_fill_rgb = tuple(int(progress_fill_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (255,)
            progress_bg_rgb = tuple(int(progress_bg_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (255,)

            # 🎨 枠の色（全体背景）を選択
            st.markdown("---")
            st.markdown("### 🎨 進捗確認画像の枠の色を選択")
            frame_color_hex = st.color_picker("枠の色を選択してください", value="#00BFFF")
            frame_color_rgb = tuple(int(frame_color_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (255,)

            
            
            st.markdown("### 🎁 ギフト一覧プレビュー")
            cols = st.columns(col_count)

            tile_size = (150, 150)
            images = []

            
            # ✅ チェックマーク画像の読み込み
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
                        original = Image.open(io.BytesIO(f.read())).convert("RGBA").resize(tile_size)

                        # ギフト背景色を敷いたタイルを作成
                        tile = Image.new("RGBA", tile_size, tile_bg_rgb)
                        tile.paste(original, (0, 0), original)

                        # ✅ チェックマークを重ねる
                        if gift_data[filename].get("status") == "達成" and check_img:
                            cx = (tile_size[0] - check_img.width) // 2
                            cy = (tile_size[1] - check_img.height) // 2
                            tile.paste(check_img, (cx, cy), check_img)

                        # ✅ 進捗バーを描画（角丸＋余白）
                        goal = gift_data[filename].get("goal", 0)
                        received = gift_data[filename].get("received", 0)
                        progress = min(received / goal, 1.0) if goal > 0 else 0

                        bar_margin = 5
                        bar_radius = 5
                        bar_height = 10
                        bar_width = tile_size[0] - bar_margin * 2
                        bar_x = bar_margin
                        bar_y = tile_size[1] - bar_height - bar_margin

                        draw = ImageDraw.Draw(tile)

                        # 背景バー（未達部分）
                        draw.rounded_rectangle(
                            [bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
                            radius=bar_radius,
                            fill=progress_bg_rgb
                        )

                        # 進捗バー（達成部分）
                        fill_width = int(bar_width * progress)
                        if fill_width > 0:
                            draw.rounded_rectangle(
                                [bar_x, bar_y, bar_x + fill_width, bar_y + bar_height],
                                radius=bar_radius,
                                fill=progress_fill_rgb
                            )

                        images.append(tile)

                        with cols[i % col_count]:
                            display_name = os.path.splitext(filename)[0]
                            st.image(tile, width=150)
                            st.markdown(f"📄 ギフト名: `{display_name}`")

                except Exception as e:
                    with cols[i % col_count]:
                        st.warning(f"{filename} の表示に失敗しました: {e}")

            # 🧩 合成画像の生成と表示・ダウンロード
            st.markdown("---")
            st.markdown("### 🧩 進捗確認画像の生成とダウンロード")

            if images:
                gap = 10
                margin = 10
                rows_count = math.ceil(len(images) / col_count)

                canvas_width = tile_size[0] * col_count + gap * (col_count - 1) + margin * 2
                canvas_height = tile_size[1] * rows_count + gap * (rows_count - 1) + margin * 2
                canvas = Image.new("RGBA", (canvas_width, canvas_height), frame_color_rgb)

                for idx, tile in enumerate(images):
                    x = margin + (idx % col_count) * (tile_size[0] + gap)
                    y = margin + (idx // col_count) * (tile_size[1] + gap)
                    canvas.paste(tile, (x, y))

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
