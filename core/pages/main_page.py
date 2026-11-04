import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
from core.scripts import user_repository

st.session_state.page = "main_page"

if not st.session_state.user_id:
    st.markdown("""
    # Welcome!
                
    This is the annotation website for the Natural Language Understanding Research Group at the University of Technology Nuremberg.

    ## Are you here for annotation?
                
    If you were redirected here for the purpose of annotation, find the 'Log In' option in the sidebar to your left.
    Then, enter the unique annotator ID that we shared with you.
    Once you have successfully logged in, new options will become available to you so you can start taking the qualification test.
    """)

else:
    st.markdown("""
    # Welcome!
                
    This is the annotation website for the Natural Language Understanding Research Group at the University of Technology Nuremberg.

    ## Are you here for annotation?
                
    **You have successfully logged in as an annotator.**  
    Click on the items in the leftside menu to start the task.
    """)

    #if s := st.selectbox("Set curr user qualification (debug)", options=[-1, 0, 1, 2, 3, 4], #index=None):
    #    user_repository.set_qualification(st.session_state.user_id, s)
