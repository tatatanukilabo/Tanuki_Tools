import streamlit as st
from PIL import Image
import io
import json
import os

def render():
    st.markdown("## 🧮 ギフト目標設定")
    st.write("各ギフトの目標数を設定してください。")

    # 📂 list.json を読み込む
    try:
        with open("assets/data/list.json", "r") as f:
            image_names = json.load(f)
    except Exception as e:
        st.error(f"画像一覧の読み込みに失敗しました: {e}")
        return

    # 📥 中断ファイルの読み込み（初期値に反映）
    st.markdown("---")
    st.markdown("### 📥 中断ファイル（JSON）を読み込む")
    resume_file = st.file_uploader("中断ファイルをアップロード", type="json", key="resume")

    resume_data = {}
    if resume_file:
        try:
            resume_data = json.load(resume_file)
            st.success("✅ 中断ファイルを読み込みました")
        except json.JSONDecodeError:
            st.error("❌ 中断ファイルの形式が正しくありません")

    # 🔧 列数をユーザーが選択できるようにする（1〜8）
    st.markdown("---")
    col_count = st.selectbox("表示する列数を選択してください", options=list(range(1, 9)), index=3)

    # 入力値を保持する辞書
    counts = {}

    # 🎨 ギフト画像と目標数入力
    cols = st.columns(col_count)
    for i, name in enumerate(image_names):
        path = os.path.join("assets", "data", name)
        try:
            with open(path, "rb") as f:
                img = Image.open(io.BytesIO(f.read()))
                with cols[i % col_count]:
                    st.image(img, caption=name, width=150)

                    default_goal = resume_data.get(name, {}).get("goal", 0)

                    count = st.number_input(
                        f"{name} の目標数",
                        min_value=0,
                        value=default_goal,
                        key=name
                    )
                    counts[name] = count
        except Exception as e:
            with cols[i % col_count]:
                st.warning(f"{name} の表示に失敗しました: {e}")

    # 📊 集計結果の表示
    st.markdown("---")
    st.markdown("### ✅ 目標数集計結果（JSON）")

    result = {}
    for name, count in counts.items():
        if count > 0:
            received = resume_data.get(name, {}).get("received", 0)
            status = resume_data.get(name, {}).get("status", "未達")
            result[name] = {
                "goal": count,
                "received": received,
                "status": status
            }

    st.json(result)

    # 📥 JSONダウンロードボタン
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
