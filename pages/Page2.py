# 結果を保存する辞書
result_data = {}

# ギフト一覧のループ内で、結果を収集
for i, filename in enumerate(goal_data):
    path = f"assets/data/{filename}"
    try:
        with open(path, "rb") as f:
            img = Image.open(io.BytesIO(f.read()))
            with cols[i % 2]:
                st.image(img, caption=filename, width=200)

                goal = goal_data[filename]
                input_key = f"received_{filename}"

                received = st.number_input(
                    f"{filename} のもらった数",
                    min_value=0,
                    value=0,
                    step=1,
                    key=input_key
                )

                status = "達成" if received >= goal else "未達"
                st.markdown(f"🎯 目標: `{goal}`　｜　📦 もらった数: `{received}`　｜　{'✅' if status == '達成' else '❌'} {status}")

                # 結果を辞書に追加
                result_data[filename] = {
                    "goal": goal,
                    "received": received,
                    "status": status
                }

    except Exception as e:
        with cols[i % 2]:
            st.warning(f"{filename} の表示に失敗しました: {e}")

# 結果のJSON表示とダウンロード
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
