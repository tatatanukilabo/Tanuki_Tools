import streamlit as st
from PIL import Image
import io
import json
import os

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

    # 📂 list.json を読み込む
    try:
        with open("assets/data/list.json", "r", encoding="utf-8") as f:
            gift_list = json.load(f)
    except Exception as e:
        st.error(f"画像一覧の読み込みに失敗しました: {e}")
        return

    # 🧠 初期化：全ギフトの目標値を session_state に保持
    for gift in gift_list:
        name = gift["filename"]
        key = f"goal_{name}"
        if key not in st.session_state:
            st.session_state[key] = resume_data.get(name, {}).get("goal", 0)

    # 🔃 ソート UI（point または category）
    st.markdown("---")
    st.markdown("### 🔃 ソート設定")
    sort_key = st.radio("ソート項目", options=["point", "category"])
    sort_order = st.radio("並び順", options=["昇順", "降順"])
    reverse = sort_order == "降順"

    sorted_list = sorted(gift_list, key=lambda x: x[sort_key], reverse=reverse)

    # 🔧 列数選択（初期値2列）
    st.markdown("---")
    col_count = st.selectbox("表示する列数を選択してください", options=list(range(1, 9)), index=1)

    # 🎨 ギフト画像と目標数入力
    cols = st.columns(col_count)
    for i, gift in enumerate(sorted_list):
        name = gift["filename"]
        display_name = os.path.splitext(name)[0]
        key = f"goal_{name}"
        path = os.path.join("assets", "data", name)
        try:
            with open(path, "rb") as f:
                img = Image.open(io.BytesIO(f.read()))
                with cols[i % col_count]:
                    st.image(img, width=150)

                    # ✅ 画像の下に個別情報を表示
                    st.markdown(f"**📄 ファイル名**: `{display_name}`")
                    st.markdown(f"**💎 ポイント**: `{gift['point']}pt`")
                    st.markdown(f"**🏷️ カテゴリ**: `{gift['category']}`")

                    st.number_input(
                        f"{display_name} の目標数",
                        min_value=0,
                        key=key
                    )
        except Exception as e:
            with cols[i % col_count]:
                st.warning(f"{name} の表示に失敗しました: {e}")

    # 📊 集計結果の表示（全ギフト対象）
    st.markdown("---")
    st.markdown("### ✅ 目標数集計結果（JSON）")

    result = {}
    for gift in gift_list:
        name = gift["filename"]
        key = f"goal_{name}"
        count = st.session_state.get(key, 0)
        if count > 0:
            received = resume_data.get(name, {}).get("received", 0)
            status = resume_data.get(name, {}).get("status", "未達")
            result[name] = {
                "goal": count,
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

# stlite 実行時のエントリポイント
if __name__ == "__main__":
    render()
