import datetime
import os

import streamlit as st
import random

from core.scripts import user_repository
from core.scripts.utils import read_json_from_file, handle_next_button, TASK_INFO, skip_to_next_sample
from adv_sentence_task.common import utils


samples = read_json_from_file(TASK_INFO["adv_sentence_task"]["annotation_filepath"])


if "progress" not in st.session_state:
    st.session_state.progress = utils.check_number_of_annotations()

st.session_state.page = "adv_sentence_task_annotation_page_sample" + str(st.session_state.progress)

if user_repository.get_qualification() != 1:
    st.write("## You must pass qualification before you can start writing. \n\n Select **Qualification** in the navigation bar to your left to try the qualification test.")
elif utils.check_number_of_annotations() >= 5:
    st.write("## You have finished this task. \n\nThank you for your time!")
    st.write("\n\n\n")
    st.write("**Your Prolific Completion Code:**")
    st.write("# " + os.getenv("PROLIFIC_COMPLETION_CODE"))
else:
    index = int(st.session_state.progress)

    word, meaning1, meaning2, domain, sentence, next_input = utils.print_annotation_schema(index)
    annotation = {"domain": domain, "word": word, "meaning1": meaning1, "meaning2": meaning2, "sentence": sentence}

    if next_input:
        user_repository.add_log(st.session_state.user_id, "SUBMITTED a sample.")
        st.session_state.random_sample = utils.reroll_logic(samples)

        # using the normal next button behavior is proably not a good idea here...
        utils.save_one_annotation(st.session_state.user_id, "annotation", index, annotation)
        
        st.session_state.progress += 1
        st.rerun()
