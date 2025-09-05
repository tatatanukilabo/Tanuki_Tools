import streamlit as st
from PIL import Image
import io
import json

def render():
    st.markdown("## 🧮 リストアップギフト")
    st.write("各ギフトの目標数を設定してください。")

    # list.json を読み込む
    try:
        with open("assets/data/list.json", "r") as f:
            image_names = json.load(f)
    except Exception as e:
        st.error(f"画像一覧の読み込みに失敗しました: {e}")
        return

    st.markdown("### 🎁 ギフト画像一覧")

    # 入力値を保持する辞書
    counts = {}

    # 2列レイアウトで画像と数値入力（幅200pxに固定）
    cols = st.columns(2)
    for i, name in enumerate(image_names):
        path = f"assets/data/{name}"
        try:
            with open(path, "rb") as f:
                img = Image.open(io.BytesIO(f.read()))
                with cols[i % 2]:
                    st.image(img, caption=name, width=200)
                    count = st.number_input(f"{name} の個数", min_value=0, value=0, key=name)
                    counts[name] = count
        except Exception as e:
            with cols[i % 2]:
                st.warning(f"{name} の表示に失敗しました: {e}")

    st.markdown("---")
    if st.button("📦 カウント結果をまとめる"):
        result = {name: count for name, count in counts.items() if count > 0}
        if result:
            st.markdown("### ✅ カウント結果（JSON）")
            st.json(result)

            # JSON文字列に変換してダウンロードボタンを表示
            json_str = json.dumps(result, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 JSONをダウンロード",
                data=json_str,
                file_name="gift_counts.json",
                mime="application/json"
            )
        else:
            st.info("0以外のカウントがありません。")

# stlite 実行時のエントリポイント
if __name__ == "__main__":

    render()
