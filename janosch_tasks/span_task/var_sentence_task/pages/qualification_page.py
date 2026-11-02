import streamlit as st
import os

from core.scripts import user_repository, utils as core_utils
from var_sentence_task.common import logic, utils

if "qualification_progress" not in st.session_state:
    st.session_state.qualification_progress = user_repository.get_checkpoint("qualification") or 1
st.session_state.page = "var_sentence_task_qualification_page_sample" + str(st.session_state.qualification_progress)

# user qualification of -1 or 1 mean that the test was already attempted
user_qualification = user_repository.get_qualification()
if user_qualification == 1:
    st.markdown("\n## You have successfully completed the qualification test. \n\nRemember that unlike these short stories, you are supposed to write singular sentences where both meanings apply!\n\n\n Select **Annotation** on the navigation bar to your left to write some sentences.")
elif user_qualification == -1:
    st.markdown("\n## You did not pass the qualification test. \n\n You have already attempted the qualification test and failed. Sorry about that! Please copy the below completion code into Prolific.\n\n")
    st.markdown("## Your completion code: " + os.getenv("PROLIFIC_SCREENOUT_CODE"))

else:
    # get index of sample
    index = int(st.session_state.qualification_progress)

    st.markdown("""## **Qualification Task**:
    
Please confirm that you are human by completing the following qualification task.  
You are presented a story where one word is highlighted in blue. Despite the word having multiple meanings, the meaning is not ambiguous in this case. Please select only the meaning for the colored word that is more plausible in the context of the story.
    
(Select exactly one checkbox for each story.)
    """)

    back_button = st.button(label="Back", key = 10 * index + 7)

    # print text and widgets
    question, checkbox1, checkbox2,  next_input = utils.print_annotation_schema_qualification(index)

    annotation = {"sentence": question["sentence"], "meaning1": checkbox1, "meaning2": checkbox2}
    samples = core_utils.read_json_from_file(core_utils.TASK_INFO["var_sentence_task"]["qualification_filepath"])

    if next_input:
        core_utils.handle_next_button(annotation, index, samples, "qualification", logic.check_if_qualified)

    if back_button:
        core_utils.handle_back_button(annotation, index, samples, "qualification")
