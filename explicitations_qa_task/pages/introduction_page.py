import streamlit as st

st.session_state.page = "explicitations_qa_task_introduction_page"

with open("explicitations_qa_task/resources/intro_text.md", "r", encoding="utf-8") as f:
    intro_text = f.read()

st.markdown(intro_text)