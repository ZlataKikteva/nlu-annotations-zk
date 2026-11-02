import os

import streamlit as st

from core.scripts import user_repository
from core.scripts.utils import read_json_from_file, handle_next_button, handle_back_button, TASK_INFO, skip_to_next_sample
from adv_eval_ending_task2.common import utils


samples = read_json_from_file(TASK_INFO["adv_eval_ending_task2"]["annotation_filepath"])

# Turns out if you dont check that, annotators may start with the wrong sample in the post-qualification grouping option.
if user_repository.get_qualification() >= 2:
    if "progress" not in st.session_state:
        st.session_state.progress = user_repository.get_checkpoint("annotation")
        if not st.session_state.progress:  # no checkpoint yet -> simply go to the first relevant sample
            st.session_state.progress = skip_to_next_sample(0, samples, st.session_state.user[3], 1, 
                                                            "annotation", qualification_function=None)
    st.session_state.page = "adv_eval_ending_task_annotation_page_sample" + str(st.session_state.progress)

if user_repository.get_qualification() < 2:
    st.write("## You must pass both qualifications before starting annotation. \n\n Select the **Qualification** tasks in the navigation bar to your left to try the qualification test.")
elif user_repository.get_qualification() == 3:
    st.write("## This part is complete. Just a little more!")
    st.write("\n\n\n")
    st.write("## You can now select 'Main Study Part 2' in the sidebar.")
else:
    index = int(st.session_state.progress)

    back_button = st.button(label="Back", key = 10 * index + 7, help="Go back to the previous sample.")

    question, slider_choice, nonsensical_input, comment_input, next_input = utils.print_annotation_schema_sliders("annotation", index)
    annotation = {"question": question, "slider": slider_choice, "nonsensical": nonsensical_input, "comment": comment_input}

    if next_input:
        handle_next_button(annotation, index, samples, "annotation")

    if back_button:
        handle_back_button(annotation, index, samples, "annotation")