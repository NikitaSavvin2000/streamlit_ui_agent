import streamlit as st

st.set_page_config(page_title="Horizon AI", layout="wide")

import streamlit as st
import requests
import uuid
import pandas as pd
import streamlit.components.v1 as components
import random
import os
from dotenv import load_dotenv
load_dotenv()
import json

cwd = os.getcwd()
path_to_avatar = os.path.join(cwd, "src", "ui", "logos", "single_logo.png")
path_to_logo = os.path.join(cwd, "src", "ui", "logos", "short_logo_black.png")




st.set_page_config(page_title="Horizon AI", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None


def send_to_backend(session_id: str, chat_id: str, message: str = "", filename: str | None = None, data_json: list | None = None):
    base_url = os.getenv("CHAT_API", "http://0.0.0.0:7070")
    url = f"{base_url}/chat"
    payload = {
        "session_id": session_id,
        "chat_id": chat_id,
        "message": message,
        "filename": filename,
        "data_json": data_json,
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        res_json = response.json()["response"]
        return res_json
    return {"message": "Ошибка при запросе к бэкенду"}


def chat_data(session_id: str, chat_id: str):
    base_url = os.getenv("CHAT_API", "http://0.0.0.0:7070")
    url = f"{base_url}/chat_data"
    payload = {
        "session_id": session_id,
        "chat_id": chat_id,
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        res_json = response.json()["response"]
        return res_json
    return {"message": "Ошибка при запросе к бэкенду"}



def main():
    st.sidebar.image(path_to_logo)
    st.session_state.was_input = None

    st.sidebar.markdown(
        """
    **Horizon AI сейчас работает в режиме отладки.**
    
    ---
    
    Скоро он сможет:
    
    - Работать с таблицами CSV и XLSX  
    
    - Прогнозировать временные ряды  
    
    - Анализировать данные  
    
    - Рисовать информативные графики  
    
    - Обеспечивать интерактивное взаимодействие в чате  
    """
    )

    cols = st.columns(spec=[2,2,2])
    with cols[2].popover("Твои данные", use_container_width=True):
        session_id = '1234'
        chat_id = '2345'
        response = chat_data(
            session_id=session_id,
            chat_id=chat_id,
        )

        data = response["data"]
        col_name, col_popover = st.columns(spec=[2.5, 1])

        for dict in data:
            name = dict["name"]
            df = pd.DataFrame(dict["json_data"])
            col_name.write(name)

            with col_popover.popover("Показать"):
                st.write(df)





    messages = st.container(height=650, border=False)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "pending_input" not in st.session_state:
        st.session_state.pending_input = None

    emojis = ["🗿", "🚀", "🛸", "🏂", "🤺",]


    prompt = st.chat_input("Say something and/or attach an image", accept_file=True, file_type=["csv", "xlsx"])


    # if prompt and not st.session_state.pending_input:
    #     st.session_state.pending_input = prompt

    if prompt and not st.session_state.pending_input:
        st.session_state.was_input = True
        if prompt.text == '':
            st.session_state.pending_input = None

        else:
            st.session_state.pending_input = prompt.text
        if prompt.files:
            uploaded_file = prompt.files[0]
        else:
            uploaded_file = None

        df = None
        filename = None

        if uploaded_file is not None:
            filename = os.path.splitext(uploaded_file.name)[0]

            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(uploaded_file)

            # json_data = df.to_dict(orient="records")
            json_data = json.loads(
                json.dumps(df.to_dict(orient="records"), ensure_ascii=False)
            )
        else:
            json_data = None

        print(f"filename = {filename}")


    with messages:
        for role, content, df_data, html in st.session_state.chat_history:
            avatar = path_to_avatar if role == "assistant" else None
            with st.chat_message(role, avatar=avatar):
                st.write(content)
                if df_data:
                    st.dataframe(pd.DataFrame(df_data))
                if html:
                    components.html(html, height=500, scrolling=False)

        if st.session_state.was_input:
            with st.chat_message("user"):
                st.write(st.session_state.pending_input)

            with st.chat_message("assistant", avatar=path_to_avatar):
                # with st.spinner(f"{emoji} Horizon думает..."):
                with st.spinner(' '):

                    session_id = '1234'
                    chat_id = '2345'
                    user_input = st.session_state.pending_input
                    reply = send_to_backend(
                        session_id=session_id,
                        chat_id=chat_id,
                        message=user_input,
                        filename=filename,
                        data_json=json_data
                    )
                    st.session_state.chat_history.append(("user", user_input, None, None))
                    st.session_state.chat_history.append((
                        "assistant",
                        reply["message"],
                        reply.get("data"),
                        reply.get("chart_html")
                    ))
                    st.session_state.pending_input = None
                    st.session_state.was_input = None
                    st.rerun()

if __name__ == "__main__":
    main()
