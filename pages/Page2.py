import streamlit as st
from PIL import Image
import io
import json
import os

def render():
    st.markdown("## 🎯 ギフト目標と達成状況")

    uploaded_file = st.file_uploader("📥 ギフト目標データ（JSON）をアップロード", type="json")

    if uploaded_file:
        try:
            goal_data = json.load(uploaded_file)
            st.success("✅ JSONの読み込みに成功しました")

            st.markdown("### 🎁 ギフト一覧")
            cols = st.columns(4)  # 🔄 列数を4に変更
            result_data = {}

            for i, filename in enumerate(goal_data):
                path = os.path.join("assets", "data", filename)
                try:
                    with open(path, "rb") as f:
                        img = Image.open(io.BytesIO(f.read()))
                        with cols[i % 4]:  # 🔄 ここも4に変更
                            st.image(img, caption=filename, width=75)

                            goal = goal_data[filename]["goal"]
                            input_key = f"received_{filename}"

                            received = st.number_input(
                                f"{filename} のもらった数",
                                min_value=0,
                                value=goal_data[filename]["received"],
                                step=1,
                                key=input_key
                            )

                            status = "達成" if received >= goal else "未達"
                            st.markdown(f"🎯 目標: `{goal}`")
                            st.markdown(f"📦 もらった数: `{received}`")
                            st.markdown(f"{'✅' if status == '達成' else '❌'} {status}")

                            result_data[filename] = {
                                "goal": goal,
                                "received": received,
                                "status": status
                            }

                except Exception as e:
                    with cols[i % 4]:
                        st.warning(f"{filename} の表示に失敗しました: {e}")

            # 結果の表示とダウンロード
            if result_data:
                st.markdown("### 📤 結果のJSON表示とダウンロード")
                result_json = json.dumps(result_data, ensure_ascii=False, indent=2)
                st.code(result_json, language="json")

                st.download_button(
                    label="📥 結果をJSONでダウンロード",
                    data=result_json.encode("utf-8"),
                    file_name="gift_result.json",
                    mime="application/json"
                )

        except json.JSONDecodeError:
            st.error("❌ JSONの形式が正しくありません")

if __name__ == "__main__":
    render()


