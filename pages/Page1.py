import streamlit as st
from PIL import Image
import io
import json
import os
from collections import defaultdict

def safe_int(val):
    try:
        return int(val)
    except:
        return 0

def calculate_result(gift_list, resume_data):
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
    return result

def render():
    st.set_page_config(page_title="ギフト目標設定", layout="wide")
    st.markdown("## 🧮 ギフト目標設定")
    st.write("各ギフトの目標数を設定してください。")

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

    # 📂 list.json を読み込む（辞書形式）
    try:
        with open("assets/data/list.json", "r", encoding="utf-8") as f:
            gift_list = json.load(f)  # { filename: {point, category}, ... }
    except Exception as e:
        st.error(f"画像一覧の読み込みに失敗しました: {e}")
        return

    # 🔧 列数選択（初期値2列）
    st.markdown("---")
    col_count = st.selectbox("表示する列数を選択してください", options=list(range(1, 9)), index=1)

    # 🎨 ギフト一覧をカテゴリ別にグループ化（ポイント昇順でソート）
    st.markdown("---")
    st.markdown("### 🎁 ギフト一覧（カテゴリ別）")

    grouped = defaultdict(list)
    for name, gift in gift_list.items():
        grouped[gift["category"]].append((name, gift))

    for category in grouped:
        grouped[category] = sorted(grouped[category], key=lambda x: safe_int(x[1].get("point", 0)))

    for category, items in grouped.items():
        st.markdown(f"#### 🏷️ カテゴリ: `{category}`")
        with st.expander(f"{category} のギフト一覧", expanded=False):
            bulk_goal = st.number_input(f"{category} の目標数を一括設定", min_value=0, value=0, key=f"bulk_{category}")
            if st.button(f"このカテゴリに一括設定", key=f"bulk_btn_{category}"):
                for name, _ in items:
                    st.session_state[f"goal_{name}"] = bulk_goal
                st.experimental_rerun()

            cols = st.columns(col_count)

            for i, (name, gift) in enumerate(items):
                display_name = os.path.splitext(name)[0]
                goal_key = f"goal_{name}"
                path = os.path.join("assets", "data", name)

                if goal_key not in st.session_state:
                    st.session_state[goal_key] = resume_data.get(name, {}).get("goal", 0)

                initial_received = resume_data.get(name, {}).get("received", 0)

                try:
                    with open(path, "rb") as f:
                        img = Image.open(io.BytesIO(f.read()))
                        with cols[i % col_count]:
                            st.image(img, width=150)
                            st.markdown(f"💎 ポイント: `{gift['point']}pt`")
                            st.markdown(f"🎁 もらった数: `{initial_received}`")
                            st.number_input(f"{display_name} の目標数", min_value=0, key=goal_key)
                except Exception as e:
                    with cols[i % col_count]:
                        st.warning(f"{name} の表示に失敗しました: {e}")

    # 📊 集計結果の表示（全ギフト対象）
    st.markdown("---")
    st.markdown("### ✅ 目標数集計結果（JSON）")

    result = calculate_result(gift_list, resume_data)
    st.json(result)

    # 📥 JSONダウンロード
    json_str = json.dumps(result, indent=2, ensure_ascii=False)
    st.download_button(
        label="📥 JSONをダウンロード",
        data=json_str,
        file_name="gift_goals.json",
        mime="application/json"
    )

# stlite 実行時のエントリポイント
if __name__ == "__main__":
    render()
