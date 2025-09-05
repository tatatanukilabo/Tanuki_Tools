import streamlit as st
from PIL import Image
import io
import json

def render():
    st.markdown("## 🎯 ギフト目標と達成状況")

    uploaded_file = st.file_uploader("📥 ギフト目標データ（JSON）をアップロード", type="json")

    if uploaded_file:
        try:
            goal_data = json.load(uploaded_file)
            st.success("✅ JSONの読み込みに成功しました")

            st.markdown("### 🎁 ギフト一覧")
            cols = st.columns(2)

            for i, filename in enumerate(goal_data):
                path = f"assets/data/{filename}"
                try:
                    with open(path, "rb") as f:
                        img = Image.open(io.BytesIO(f.read()))
                        with cols[i % 2]:
                            st.image(img, caption=filename, width=200)

                            goal = goal_data[filename]
                            input_key = f"received_{filename}"

                            # もらった数の入力（0以上）
                            received = st.number_input(
                                f"{filename} のもらった数",
                                min_value=0,
                                value=0,
                                step=1,
                                key=input_key
                            )

                            # 達成状況の表示
                            status = "✅ 達成" if received >= goal else "❌ 未達"
                            st.markdown(f"🎯 目標: `{goal}`　｜　📦 もらった数: `{received}`　｜　{status}")

                except Exception as e:
                    with cols[i % 2]:
                        st.warning(f"{filename} の表示に失敗しました: {e}")

        except json.JSONDecodeError:
            st.error("❌ JSONの形式が正しくありません")

if __name__ == "__main__":

    render()
