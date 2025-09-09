import streamlit as st

def render():
    st.markdown("### 📝 ライセンス情報")
    st.markdown("""
    - **著作権** © 2025 tanukitools
    - **著者**：Tatatanuki (@ta_ta_ta_nu_ki)
    - **バージョン**：0.1.1
    - **ライセンス**：MITライセンスの下でライセンスされています。
    """)

    st.markdown("### 📄 利用規約")
    st.markdown("""
    本アプリケーションの機能およびコンテンツは、予告なく変更または終了される場合がありますのでご了承ください。
    """)

    st.markdown("### ⚠️ 免責事項")
    st.markdown("""
    本アプリケーションの使用により生じたいかなる損害についても、著者は一切の責任を負いません。
    """)

    st.markdown("### 🤩 Special Thanks")
    st.markdown("""
    本アプリケーションの開発にあたり、以下の方々のご協力をいただきました。
    - 黒魅月那 さん ()
    - 緋月悠鮫 さん ()
    - 瑠璃原すやり さん ()
    - 蛍火秋那 さん ()
    """)

# stlite 実行時のエントリポイント
if __name__ == "__main__":
    render()