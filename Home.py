import streamlit as st
import pages.Page1 as Page1
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
            <h2 style="margin: 0;">たぬきツールズ</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("開発中。左上のボタンからサイドバーを開いてpage1から順に")

if __name__ == "__main__":

    render()

