import os

import streamlit as st

from core.scripts import user_repository
from core.scripts.utils import read_json_from_file, handle_next_button, handle_back_button, TASK_INFO, skip_to_next_sample

if "tutorial_stage" not in st.session_state:
    st.session_state["tutorial_stage"] = 0

from adv_ending_task4.common import utils


#print("Running from the top, current stage ", st.session_state["tutorial_stage"], "current story ", st.session_state["sample_state"])

def tutorial_stage_logic_checks():
    # tutorial stage logic checks
    precontext = st.session_state["sample_state"]["choice"]["Beginning"]
    ending = st.session_state["sample_state"]["choice"]["Ending"]
    print("Logic check! ", precontext, ending, st.session_state["tutorial_stage"])
    if st.session_state["tutorial_stage"] in [0, 1]: # selecting beginning.
        if precontext is None or "Select" in precontext:
            pass
        elif "connected my mouse" in precontext:
            st.session_state["tutorial_stage"] = 2
            st.rerun()
        else: # wrong
            if st.session_state["tutorial_stage"] == 0:
                st.session_state["tutorial_stage"] = 1
                print("changing tutorial stage and rerunning...")
                st.rerun()
    elif st.session_state["tutorial_stage"] in [2, 3]: # editing first textbox
        if "mouse" in st.session_state["sample_state"]["Beginning"] and not ("Select" in st.session_state["sample_state"]["Beginning"]):
            if st.session_state["tutorial_stage"] == 2:
                st.session_state["tutorial_stage"] = 3
                st.rerun()
        elif "Select" not in st.session_state["sample_state"]["Beginning"]:
            st.session_state["tutorial_stage"] = 4
            st.rerun()
    elif st.session_state["tutorial_stage"] in [4, 5]: # selecting ending
        if "Select" in ending:
            pass
        elif "squeak" in ending:
            if st.session_state["tutorial_stage"] == 4:
                st.session_state["tutorial_stage"] = 5
                st.rerun()
        else:
            st.session_state["tutorial_stage"] = 6
            user_repository.set_qualification(st.session_state.user_id, 2)
            st.rerun()
    elif st.session_state["tutorial_stage"] == 6:
        if "squeak" in ending:
            st.session_state["tutorial_stage"] = 5  # introducing negative progress
            st.rerun()
    

samples = read_json_from_file(TASK_INFO["adv_ending_task4"]["annotation_filepath"])

st.session_state.page = "adv_ending_task4_tutorial"

if user_repository.get_qualification() < 1:
    st.write("## You must pass qualification before starting the tutorial. \n\n Select **Qualification** in the navigation bar to your left to try the qualification test.")
elif user_repository.check_if_done(st.session_state.user_id):
    st.write("## You have finished annotation. \n\nThank you for your time!")
    st.write("\n\n\n")
    st.write("**Your Prolific Completion Code:**")
    st.write("# " + os.getenv("PROLIFIC_COMPLETION_CODE"))
else:
    index = int("1")

    precontext, sentence, ending, comment, confidence, skipping_reason, question, next_input = utils.print_annotation_schema("tutorial", index)
    precontext = st.session_state["sample_state"]["choice"]["Beginning"]
    ending = st.session_state["sample_state"]["choice"]["Ending"]
    print(precontext, sentence, ending)
    annotation = {"precontext": precontext, "sentence": sentence, "ending": ending}

    if next_input:
        handle_next_button(annotation, index, samples, "annotation")

    tutorial_stage_logic_checks()