import os

import streamlit as st

from core.scripts import user_repository
from core.scripts.utils import read_json_from_file, handle_next_button, handle_back_button, TASK_INFO, skip_to_next_sample
from var_ending_test.common import utils


samples = read_json_from_file(TASK_INFO["var_ending_test"]["annotation_filepath"])

if "progress" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint("annotation")
    if not st.session_state.progress:  # no checkpoint yet -> simply go to the first relevant sample
        st.session_state.progress = skip_to_next_sample(0, samples, st.session_state.user[3], 1, 
                                                        "annotation", qualification_function=None)
st.session_state.page = "var_ending_test_annotation_page_sample" + str(st.session_state.progress)

if "tutorial_stage" in st.session_state and st.session_state["tutorial_stage"] > 5:
    utils.reset_sample_state()

if user_repository.get_qualification() != 2:
    st.write("## You must do the qualification and tutorial before starting annotation. \n\n Select **Qualification**, then **Tutorial** in the navigation bar to your left.")
elif user_repository.check_if_done(st.session_state.user_id):
    st.write("## You have finished annotation. \n\nThank you for your time!")
    st.write("\n\n\n")
    st.write("**Your Prolific Completion Code:**")
    st.write("# " + os.getenv("PROLIFIC_COMPLETION_CODE"))
else:
    index = int(st.session_state.progress)

    # back button not really necessary here i think
    back_button = None#st.button(label="Back", key = 10 * index + 7, help="Go back to the previous sample.")

    precontext, sentence, ending, comment, confidence, skipping_reason, question, next_input = utils.print_annotation_schema("annotation", index)
    annotation = {"question": [question["word"], question["focus_meaning"]], "precontext": precontext, "sentence": sentence, "ending": ending, "comment": comment,
                  "confidence": confidence, "skipping_reason": skipping_reason}

    if next_input:
        st.write("Continuing to next story!")
        utils.reset_sample_state()
        handle_next_button(annotation, index, samples, "annotation")

    if back_button:
        utils.reset_sample_state()
        handle_back_button(annotation, index, samples, "annotation")