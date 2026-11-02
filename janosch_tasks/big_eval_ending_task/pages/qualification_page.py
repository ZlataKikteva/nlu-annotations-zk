import streamlit as st
import os

from core.scripts import user_repository, utils as core_utils
from big_eval_ending_task.common import logic, utils

if "qualification_progress" not in st.session_state:
    st.session_state.qualification_progress = user_repository.get_checkpoint("qualification") or 1
st.session_state.page = "big_eval_ending_task_qualification_page_sample" + str(st.session_state.qualification_progress)

# user qualification of -1 or 1 mean that the test was already attempted
user_qualification = user_repository.get_qualification()
if user_qualification == 1:
    st.markdown("\n## You have finished the qualification test. \n\n Select **Annotation** on the navigation bar to your left to do some annotating.")

    st.markdown("""For the purpose of the exercise, you will get access to the annotation page regardless of your performance in the qualification test.
                
For your information, the 'correct' answers were:
                
* 'It was a hard puzzle.* -> 1 or 2
                
* 'The service there was really lousy.* -> 4 or 5
                
* 'If he had a fan, the heat would be bearable.* -> 1 or 2
                
* 'In the end, she beat him in the race.' -> 4 or 5
                
                """)
elif user_qualification == -1:
    st.markdown("\n## You did not pass the qualification test. \n\n You have already attempted the qualification test and failed. Sorry about that! Please copy the below completion code into Prolific.\n\n")
    st.markdown("## Your completion code: " + os.getenv("PROLIFIC_SCREENOUT_CODE"))

else:
    # get index of sample
    index = int(st.session_state.qualification_progress)

    if index == 1:
        st.write("Remember to read the Task Intro before attempting the qualification test!")

    back_button = st.button(label="Back", key = 10 * index + 7)

    # print text and widgets
    question, slider, nonsense, comment, next_input = utils.print_annotation_schema_sliders("qualification", index)

    annotation = {"question": question, "slider": slider, "nonsensical": nonsense, "comment": comment}
    samples = core_utils.read_json_from_file(core_utils.TASK_INFO["big_eval_ending_task"]["qualification_filepath"])

    if next_input:
        core_utils.handle_next_button(annotation, index, samples, "qualification", logic.check_if_qualified)

    if back_button:
        core_utils.handle_back_button(annotation, index, samples, "qualification")
