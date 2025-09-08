import streamlit as st
from PIL import Image
import io
import json
import os

def render():
    st.set_page_config(page_title="ギフト目標設定", layout="wide")
    st.markdown("## 🧮 ギフト目標設定")
    st.write("各ギフトの目標数と受け取り数を設定してください。")

    # 📥 中断ファイルの読み込み
    st.markdown("### 📥 中断ファイル（JSON）を読み込む")
    resume_file = st.file_uploader("中断ファイルをアップロード", type="json", key="resume")

    resume_data = {}
    if resume_file:
        try:
            resume_data = json.load(resume_file)
            st.success("✅ 中断ファイルを読み込みました")
        except json.JSONDecodeError:
            st.error("❌ 中断ファイルの形式が正しくありません")

    # 📂 list.json を読み込む
    try:
        with open("assets/data/list.json", "r", encoding="utf-8") as f:
            gift_list = json.load(f)
    except Exception as e:
        st.error(f"画像一覧の読み込みに失敗しました: {e}")
        return

    # 🔃 ソート UI
    st.markdown("---")
    st.markdown("### 🔃 ソート設定")
    sort_key = st.radio("ソート項目", options=["point", "category"])
    sort_order = st.radio("並び順", options=["昇順", "降順"])
    reverse = sort_order == "降順"

    sorted_list = sorted(gift_list.items(), key=lambda x: x[1][sort_key], reverse=reverse)

    # 🔧 列数選択
    st.markdown("---")
    col_count = st.selectbox("表示する列数を選択してください", options=list(range(1, 9)), index=1)

    # 🎁 ギフト一覧（ページネーション）
    st.markdown("---")
    st.markdown("### 🎁 ギフト一覧")

    step = 20
    if "visible_count" not in st.session_state:
        st.session_state.visible_count = step

    if st.button("もっと見る"):
        st.session_state.visible_count += step

    visible_list = sorted_list[:st.session_state.visible_count]
    cols = st.columns(col_count)

    for i, (name, gift) in enumerate(visible_list):
        display_name = os.path.splitext(name)[0]
        goal_key = f"goal_{name}"
        path = os.path.join("assets", "data", name)

        initial_goal = resume_data.get(name, {}).get("goal", 0)
        initial_received = resume_data.get(name, {}).get("received", 0)

        try:
            with open(path, "rb") as f:
                img = Image.open(io.BytesIO(f.read()))
                with cols[i % col_count]:
                    st.image(img, width=150)
                    st.markdown(f"💎 ポイント: `{gift['point']}pt`")
                    st.markdown(f"🏷️ カテゴリ: `{gift['category']}`")
                    st.markdown(f"🎁 もらった数: `{initial_received}`")  # 固定表示
                    st.number_input(f"{display_name} の目標数", min_value=0, value=initial_goal, key=goal_key)
        except Exception as e:
            with cols[i % col_count]:
                st.warning(f"{name} の表示に失敗しました: {e}")

    # 📊 集計結果の表示
    st.markdown("---")
    st.markdown("### ✅ 目標数集計結果（JSON）")

    result = {}
    for name, gift in gift_list.items():
        goal = st.session_state.get(f"goal_{name}", 0)
        received = resume_data.get(name, {}).get("received", 0)
        status = "達成" if received >= goal and goal > 0 else "未達"

        if goal > 0:
            result[name] = {
                "goal": goal,
                "received": received,
                "status": status,
                "point": gift.get("point", 0),
                "category": gift.get("category", "")
            }

    st.json(result)

    # 📥 JSONダウンロード
    json_str = json.dumps(result, indent=2, ensure_ascii=False)
    st.download_button(
        label="📥 JSONをダウンロード",
        data=json_str,
        file_name="gift_goals.json",
        mime="application/json"
    )

if __name__ == "__main__":
    render()
