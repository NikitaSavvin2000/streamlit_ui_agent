import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Horizon AI", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def bot_response_stream():
    reply = "👋 Привет! Я — ИИ агент **Horizon** 🤖. Сейчас я нахожусь в разработке 🛠️. В будущем я смогу:📈 строить прогнозы временных рядов, 📊 анализировать данные, 📉 рисовать графики, 📋 и работать с таблицами, Оставайтесь на связи — скоро будет мощно! 🚀"
    for char in reply:
        yield char
        time.sleep(0.01)

def main():
    with st.sidebar:
        st.button("Новый чат", use_container_width=True)
        st.title("💬 Чаты")
        st.button("Чат 1", use_container_width=True)
        st.button("Чат 2", use_container_width=True)
        st.button("Чат 3", use_container_width=True)

    _, central, _ = st.columns([1, 3, 1])
    central.title("🧠 Horizon AI")
    messages = central.container(height=500, border=False)

    prompt = central.chat_input("Say something and/or attach an image", accept_file=True, file_type=["csv", "xlsx"])

    if prompt:
        if prompt.text:
            st.session_state.chat_history.append(("user", prompt.text))
            st.session_state.chat_history.append(("assistant_stream", None))

        if prompt.files:
            file = prompt.files[0]
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file)
            else:
                df = None

            if df is not None:
                st.session_state.chat_history.append(("user", f"Файл: {file.name}"))
                st.session_state.chat_history.append(("assistant_stream", None))

    for msg_type, msg_content in st.session_state.chat_history:
        if msg_type == "assistant_stream":
            messages.chat_message("assistant").write_stream(bot_response_stream)
        else:
            messages.chat_message(msg_type).write(msg_content)

if __name__ == "__main__":
    main()
