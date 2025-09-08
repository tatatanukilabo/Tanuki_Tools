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

            # 🔧 列数選択（1〜8） 初期値は2列（index=1）
            st.markdown("---")
            col_count = st.selectbox("表示する列数を選択してください", options=list(range(1, 9)), index=1)

            st.markdown("### 🎁 ギフト一覧")
            cols = st.columns(col_count)

            total_items = len(goal_data)
            result_data = {}

            for i, filename in enumerate(goal_data):
                path = os.path.join("assets", "data", filename)
                try:
                    with open(path, "rb") as f:
                        img = Image.open(io.BytesIO(f.read()))
                        with cols[i % col_count]:
                            display_name = os.path.splitext(filename)[0]
                            point = goal_data[filename].get("point", 0)
                            category = goal_data[filename].get("category", "未分類")
                            goal = goal_data[filename].get("goal", 0)
                            default_received = goal_data[filename].get("received", 0)

                            st.image(img, width=150)
                            st.markdown(f"💎 ポイント: `{point}pt`")
                            st.markdown(f"🏷️ カテゴリ: `{category}`")

                            input_key = f"received_{filename}"
                            received = st.number_input(
                                f"{display_name} のもらった数",
                                min_value=0,
                                value=default_received,
                                step=1,
                                key=input_key
                            )

                            # 一時保存（集計は後でボタンで実行）
                            result_data[filename] = {
                                "goal": goal,
                                "received": received,
                                "point": point,
                                "category": category
                            }

                except Exception as e:
                    with cols[i % col_count]:
                        st.warning(f"{filename} の表示に失敗しました: {e}")

            # 🔄 集計ボタン
            st.markdown("---")
            st.markdown("### 📊 集計結果")
            if st.button("🔄 集計を更新"):
                achieved_count = 0
                for filename in result_data:
                    goal = result_data[filename]["goal"]
                    received = result_data[filename]["received"]
                    status = "達成" if received >= goal and goal > 0 else "未達"
                    progress_ratio = received / goal if goal > 0 else 0
                    progress_percent = int(progress_ratio * 100)
                    safe_ratio = min(progress_ratio, 1.0)

                    result_data[filename]["status"] = status

                    st.markdown(f"#### 🎁 {os.path.splitext(filename)[0]}")
                    st.markdown(f"🎯 目標: `{goal}`")
                    st.markdown(f"📦 もらった数: `{received}`")
                    st.markdown(f"{'✅' if status == '達成' else '❌'} {status}")
                    st.progress(safe_ratio)
                    st.markdown(f"📈 達成率: `{progress_percent}%`")

                    if status == "達成":
                        achieved_count += 1

                # 📊 全体の達成率表示
                overall_ratio = achieved_count / total_items if total_items > 0 else 0
                overall_percent = int(overall_ratio * 100)
                st.markdown("---")
                st.markdown("### 📊 全体の達成状況")
                st.markdown(f"✅ 達成ギフト数: `{achieved_count}` / `{total_items}`")
                st.progress(overall_ratio)
                st.markdown(f"📈 全体達成率: `{overall_percent}%`")

                # 📤 結果の表示とダウンロード
                st.markdown("---")
                st.markdown("### 📤 結果のJSON表示とダウンロード")
                result_json = json.dumps(result_data, ensure_ascii=False, indent=2)
                st.code(result_json, language="json")

                st.download_button(
                    label="📥 結果をJSONでダウンロード",
                    data=result_json.encode("utf-8"),
                    file_name="gift_result.json",
                    mime="application/json"
                )
            else:
                st.info("👆 上のボタンを押すと達成状況が集計されます")

        except json.JSONDecodeError:
            st.error("❌ JSONの形式が正しくありません")

if __name__ == "__main__":
    render()
