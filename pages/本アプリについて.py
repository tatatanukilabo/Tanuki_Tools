import streamlit as st
import base64

def get_base64_image(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def render():
    image_base64 = get_base64_image("assets/icons/icon.png")
    st.markdown(
        f"""
        <style>
        .custom-logo {{
            height: 3em;
            margin-right: 0.5em;
            filter: drop-shadow(0 0 6px white);
        }}
        </style>
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{image_base64}" class="custom-logo">
            <h2 style="margin: 0;">たぬきツールズについて</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("### 📝 ライセンス情報")
    st.markdown("""
    - **著作権** Copylight © 2025 tanukitools All rights reserved.
    - **著者**：たたたぬき (X:@ta_ta_ta_nu_ki)
    - **バージョン**：0.1.1
    """)
    st.markdown("---")
    st.markdown("### 📄 利用規約")
    st.markdown("""
    - 本アプリケーションの機能およびコンテンツは、予告なく変更または終了される場合がありますのでご了承ください。
    """)

    st.markdown("---")
    st.markdown("### ⚠️ 免責事項")
    st.markdown("""
    - 本アプリケーションの使用により生じたいかなる損害についても、著者は一切の責任を負いません。
    """)

    st.markdown("---")
    st.markdown("### 🤩 Special Thanks")
    st.markdown("""
    本アプリケーションの開発にあたり、以下の方々のご協力をいただきました。この場を借りてお礼申し上げます。
    - 〇〇〇〇 さん (X:, IRIAM:)
    """)

# stlite 実行時のエントリポイント
if __name__ == "__main__":
    render()