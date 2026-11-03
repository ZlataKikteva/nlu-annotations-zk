import streamlit as st

from core.scripts import user_repository, utils
from explicitations_qa_task.common import utils as explicitations_qa_utils

if "progress" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint("annotation") or 1
st.session_state.page = "explicitations_qa_task_annotation_page_sample" + str(st.session_state.progress)


samples = utils.read_json_from_file(utils.TASK_INFO["explicitations_qa_task"]["annotation_filepath"])


if user_repository.get_qualification() != 1:
    st.write("## You must pass qualification before starting annotation. \n\n Select **Qualification** in the navigation bar to your left to try the qualification test.")
elif user_repository.check_if_done(st.session_state.user_id):
    st.write("## You have finished annotation. \n\nThank you for your time!")
else:
 
    index = int(st.session_state.progress)
 
    back_button = st.button(label="Back", key=10 * index + 7)
 
    question, selected, text_input, next_button = explicitations_qa_utils.print_annotation_schema("annotation", index)
    annotation = {
        "id": question["id"],
        "sentence": question["sentence_1"],
        "question": question["generated"]["question"],
        "answer_version": explicitations_qa_utils.ANSWER_VERSION,                                  # study condition shown
        "options_order": [label for label, _ in explicitations_qa_utils.get_options(question, index)],  # order seen
        "selected": selected,     # labels, e.g. ["GOLD_ORIGINAL", "PLAUSIBLE_GIVEN_CONTEXT_1"]
        "textinput": text_input,
    }


    if next_button:
        utils.handle_next_button(annotation, index, samples, "annotation")

    if back_button:
        utils.handle_back_button(annotation, index, samples, "annotation")