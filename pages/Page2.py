import streamlit as st
from PIL import Image
import io
import json
import os
from collections import defaultdict

def render():
    st.markdown("## 🎯 ギフト目標と達成状況")

    uploaded_file = st.file_uploader("📥 ギフト目標データ（JSON）をアップロード", type="json")

    if uploaded_file:
        try:
            goal_data = json.load(uploaded_file)
            st.success("✅ JSONの読み込みに成功しました")

            st.markdown("---")
            col_count = st.selectbox("表示する列数を選択してください", options=list(range(1, 9)), index=1)

            grouped = defaultdict(list)
            for filename, data in goal_data.items():
                category = data.get("category", "未分類")
                grouped[category].append((filename, data))

            for category in grouped:
                grouped[category].sort(key=lambda x: x[1].get("point", 0))

            result_data = {}
            total_items = len(goal_data)
            achieved_count = 0

            st.markdown("### 🎁 ギフト一覧（カテゴリ別）")
            for category, items in grouped.items():
                with st.expander(f"🏷️ カテゴリ: {category}", expanded=False):
                    cols = st.columns(col_count)
                    for i, (filename, data) in enumerate(items):
                        path = os.path.join("assets", "data", filename)
                        try:
                            with open(path, "rb") as f:
                                img = Image.open(io.BytesIO(f.read()))
                                with cols[i % col_count]:
                                    display_name = os.path.splitext(filename)[0]
                                    point = data.get("point", 0)
                                    goal = data.get("goal", 0)
                                    default_received = data.get("received", 0)

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

                                    status = "達成" if received >= goal and goal > 0 else "未達"
                                    progress_ratio = received / goal if goal > 0 else 0
                                    progress_percent = int(progress_ratio * 100)
                                    safe_ratio = min(progress_ratio, 1.0)

                                    gift_goal_point = goal * point
                                    gift_received_point = received * point

                                    st.markdown(f"🎯 目標: `{goal}`")
                                    st.markdown(f"📈 達成率: `{progress_percent}%`")
                                    st.progress(safe_ratio)
                                    st.markdown(f"{'✅' if status == '達成' else '❌'} {status}")
                                    st.markdown(f"🎯 目標ポイント: `{gift_goal_point}pt`")
                                    st.markdown(f"📦 受取ポイント: `{gift_received_point}pt`")

                                    result_data[filename] = {
                                        "goal": goal,
                                        "received": received,
                                        "status": status,
                                        "point": point,
                                        "category": category
                                    }

                                    if status == "達成":
                                        achieved_count += 1

                        except Exception as e:
                            with cols[i % col_count]:
                                st.warning(f"{filename} の表示に失敗しました: {e}")

            st.markdown("---")
            st.markdown("### 📊 全体の達成状況")
            overall_ratio = achieved_count / total_items if total_items > 0 else 0
            overall_percent = int(overall_ratio * 100)
            st.markdown(f"✅ 達成ギフト数: `{achieved_count}` / `{total_items}`")
            st.progress(overall_ratio)
            st.markdown(f"📈 全体達成率: `{overall_percent}%`")

            total_goal_points = 0
            total_received_points = 0
            for data in result_data.values():
                total_goal_points += data["goal"] * data["point"]
                total_received_points += data["received"] * data["point"]

            point_ratio = total_received_points / total_goal_points if total_goal_points > 0 else 0
            point_percent = int(point_ratio * 100)

            st.markdown("---")
            st.markdown("### 📊 全体のポイント達成状況")
            overall_ratio = achieved_count / total_items if total_items > 0 else 0
            st.markdown(f"🎯 目標ポイント合計: `{total_goal_points}pt`")
            st.markdown(f"📦 受取ポイント合計: `{total_received_points}pt`")
            st.progress(point_ratio)
            st.markdown(f"💎 ポイント全体達成率: `{point_percent}%`")
            

            st.markdown("---")
            st.markdown("### 📤 結果のJSON表示とダウンロード")
            result_json = json.dumps(result_data, ensure_ascii=False, indent=2)

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

