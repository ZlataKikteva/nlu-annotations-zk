import streamlit as st

st.session_state.page = "var_ending_test2_introduction_page"

with open("var_ending_test2/resources/intro_text.md", "r") as f:
    intro_text = f.read()

if not st.session_state.user_id:
    st.markdown("""
Note: You are **not logged in** in this tab, so the qualification and annotation task do not show up in the sidebar.  

---
""")

st.markdown(intro_text)