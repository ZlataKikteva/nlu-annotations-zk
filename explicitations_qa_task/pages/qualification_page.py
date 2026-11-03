import os
import streamlit as st

from core.scripts import user_repository, utils
from explicitations_qa_task.common import utils as explicitations_qa_utils


# qualification progress dictates the current sample to show. Qualifications always need to have it
if "qualification_progress" not in st.session_state:
    st.session_state.qualification_progress = user_repository.get_checkpoint("qualification")
st.session_state.page = "explicitations_qa_task_qualification_page_sample" + str(st.session_state.qualification_progress)

# user qualification of -1 or 1 mean that the test was already attempted
user_qualification = user_repository.get_qualification()
if user_qualification == 1:
    st.markdown("\n## You have successfully completed the qualification test. \n\n Select **Annotation** on the navigation bar to your left to do some annotating.")
elif user_qualification == -1:
    st.markdown("\n## You have already attempted the qualification test. \n\n Unfortunately, you did not pass the qualification test. Contact us if you want to try again.")

else:
    # get index of sample
    index = int(st.session_state.qualification_progress)

    back_button = None
    if index > 1:
        # Print a back button
        back_button = st.button(label="Back", key = 10 * index + 7)
    
    # print text and widgets
    question, checkbox, text_input, next_button = explicitations_qa_utils.print_annotation_schema("qualification", index)

    samples = utils.read_json_from_file(utils.TASK_INFO["explicitations_qa_task"]["qualification_filepath"])
    annotation = {"sentence": question["sentence"], "checkbox": checkbox, "textinput": text_input}

    if next_button:
        utils.handle_next_button(annotation, index, samples, "qualification", explicitations_qa_utils.check_if_qualified)

    if back_button:
        utils.handle_back_button(annotation, index, samples, "qualification")