import sys
import subprocess
import importlib.util


def install_package(package):
    if importlib.util.find_spec(package) is None:
        print(f"📦 {package} belum terinstall. Menginstall...")
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "-U",
            package,
        ])


# Install dependency otomatis
install_package("transformers")
install_package("torch")


import streamlit as st
from transformers import pipeline


st.set_page_config(
    page_title="DeepSeek V4 Flash",
    page_icon="🤖",
)

st.title("🤖 DeepSeek V4 Flash")


@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="deepseek-ai/DeepSeek-V4-Flash",
    )


pipe = load_model()


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Tulis pesan..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Generating..."):

            result = pipe(st.session_state.messages)

            try:
                response = result[0]["generated_text"][-1]["content"]
            except (KeyError, TypeError, IndexError):
                response = str(result)

            st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
    })
