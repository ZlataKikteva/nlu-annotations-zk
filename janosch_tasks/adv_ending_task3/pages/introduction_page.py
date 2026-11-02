import streamlit as st

st.session_state.page = "adv_ending_task3_introduction_page"

with open("adv_ending_task3/resources/intro_text.md", "r") as f:
    intro_text = f.read()

if not st.session_state.user_id:
    st.markdown("""
Note: You are **not logged in** in this tab, so the qualification and annotation task do not show up in the sidebar.  

---
""")

st.markdown(intro_text)