import streamlit as st
from PIL import Image, ImageDraw
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

            # ⚙️ 設定ファイルの読み込み（オプション）
            st.markdown("---")
            st.markdown("### ⚙️ 設定ファイルの読み込み（オプション）")
            config_file = st.file_uploader("設定JSONをアップロード", type="json", key="config")

            default_config = {
                "col_count": 2,
                "progress_fill_hex": "#FF0000",
                "progress_bg_hex": "#DDDDDD",
                "frame_color_hex": "#00BFFF"
            }

            if config_file:
                try:
                    config_data = json.load(config_file)
                    default_config.update(config_data)
                    st.success("✅ 設定ファイルの読み込みに成功しました")
                except json.JSONDecodeError:
                    st.warning("⚠️ 設定ファイルの形式が正しくありません")

            # 🔧 列数選択（最大32列に拡張）
            st.markdown("---")
            col_count = st.selectbox("表示する列数を選択してください", options=list(range(1, 33)), index=default_config["col_count"] - 1)

            # 🎨 進捗バーの色設定
            st.markdown("### 🎨 進捗バーの色設定")
            progress_fill_hex = st.color_picker("進捗バーの色（達成部分）", value=default_config["progress_fill_hex"])
            progress_bg_hex = st.color_picker("進捗バーの背景色（未達部分）", value=default_config["progress_bg_hex"])
            progress_fill_rgb = tuple(int(progress_fill_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (255,)
            progress_bg_rgb = tuple(int(progress_bg_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (255,)

            # 🎨 枠の色
            st.markdown("### 🎨 進捗確認画像の枠の色を選択")
            frame_color_hex = st.color_picker("枠の色を選択してください", value=default_config["frame_color_hex"])
            frame_color_rgb = tuple(int(frame_color_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (255,)

            # 💾 設定の保存
            st.markdown("---")
            st.markdown("### 💾 現在の設定を保存")
            config_to_save = {
                "col_count": col_count,
                "progress_fill_hex": progress_fill_hex,
                "progress_bg_hex": progress_bg_hex,
                "frame_color_hex": frame_color_hex
            }
            config_json = json.dumps(config_to_save, ensure_ascii=False, indent=2)
            st.download_button(
                label="📥 設定JSONをダウンロード",
                data=config_json.encode("utf-8"),
                file_name="gift_config.json",
                mime="application/json"
            )

            # ✅ チェックマーク画像の読み込み
            try:
                check_path = os.path.join("assets", "icons", "check.png")
                with open(check_path, "rb") as f:
                    check_img = Image.open(f).convert("RGBA")
            except FileNotFoundError:
                st.warning("⚠️ チェックマーク画像が見つかりません。重ね処理はスキップされます。")
                check_img = None

            # 🔽 並び替え：カテゴリ昇順 → ポイント昇順
            sorted_items = sorted(
                gift_data.items(),
                key=lambda x: (x[1].get("category", "未分類"), x[1].get("point", 0))
            )

            # 🎨 タイル生成
            tile_size = (150, 150)
            tile_bg_rgb = (255, 255, 255, 255)
            images = []

            for filename, data in sorted_items:
                path = os.path.join("assets", "data", filename)
                try:
                    with open(path, "rb") as f:
                        original = Image.open(io.BytesIO(f.read())).convert("RGBA").resize(tile_size)

                    tile = Image.new("RGBA", tile_size, tile_bg_rgb)
                    tile.paste(original, (0, 0), original)

                    if data.get("status") == "達成" and check_img:
                        cx = (tile_size[0] - check_img.width) // 2
                        cy = (tile_size[1] - check_img.height) // 2
                        tile.paste(check_img, (cx, cy), check_img)

                    goal = data.get("goal", 0)
                    received = data.get("received", 0)
                    progress = min(received / goal, 1.0) if goal > 0 else 0

                    bar_margin = 5
                    bar_radius = 5
                    bar_height = 10
                    bar_width = tile_size[0] - bar_margin * 2
                    bar_x = bar_margin
                    bar_y = tile_size[1] - bar_height - bar_margin

                    draw = ImageDraw.Draw(tile)
                    draw.rounded_rectangle(
                        [bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
                        radius=bar_radius,
                        fill=progress_bg_rgb
                    )

                    fill_width = int(bar_width * progress)
                    if fill_width > 0:
                        draw.rounded_rectangle(
                            [bar_x, bar_y, bar_x + fill_width, bar_y + bar_height],
                            radius=bar_radius,
                            fill=progress_fill_rgb
                        )

                    images.append(tile)

                except Exception as e:
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
