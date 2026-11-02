import os

import streamlit as st

from core.scripts import user_repository
from core.scripts.utils import read_json_from_file, handle_back_button, TASK_INFO, finish_subtask
from adv_ending_task4.common import utils


samples = read_json_from_file(TASK_INFO["adv_ending_task4"]["annotation_filepath"])

SAMPLES_NEEDED = 10

    
def skip_to_next_sample(index: int, samples: dict, grouping: int, direction: int=1, 
                        subtask: str="annotation", qualification_function=None) -> int:
    """
    A modified version of the utils skip_to_next_sample function.
    From the specified index, move upwards to find the next sample relevant to the group.
    If there are no more samples, increase the grouping by 2 and start from the beginning.
    It increases by 2 instead of 1 so it is guaranteed to get new sentences
    This ensures that even when someone skips, there will always be work to be done...

    :param index: Index of the current page/sample
    :param samples: dict of all the samples (keys are "1", "2", ...)
    :param grouping: group of user
    :param direction: 1 for going forward, -1 for going backward
    :param subtask: e.g. annotation or qualification
    :param qualification function: Function to evaluate whether qualification was passed, not needed if subtask!=qualification
    :return: Index of the next (or previous) sample
    """
    samples_done, samples_skipped = utils.check_user_sample_progress()
    samples_in_group = len([x for x in samples if samples[x]["grouping"] == grouping])
    loops_done = int((samples_done + samples_skipped) / (samples_in_group))
    index += direction
    if index < 1:
        return 1
    
    start_grouping = grouping
    
    grouping = (grouping + 2 * loops_done) % TASK_INFO["adv_ending_task4"]["number_of_annotator_groups"] 
    
    while True:
        if index > len(samples):
            index = 1  # grouping will increase, get reborn.
            if grouping == start_grouping:
                # Thats not supposed to happen...
                grouping = (grouping + 2) % TASK_INFO["adv_ending_task4"]["number_of_annotator_groups"] 

        if str(index) not in samples:  # account for samples having id gaps
            index += direction
            continue
        checked_sample = samples[str(index)]
        if ("grouping" not in checked_sample) or (grouping == checked_sample["grouping"]):
            break  # break when finding relevant sample
        else:
            index += direction
            if index < 1:  # went back too far
                index = 1
                direction = 1  # reverse to find first sample again
    # return index where it found a sample
    return index


def handle_next_button(annotation, index, samples):
    user_repository.save_one_annotation(st.session_state.user_id, "annotation", index, annotation)

    if utils.check_user_sample_progress()[0] >= 10:
        finish_subtask("annotation")
    else:
        grouping = st.session_state.user[3]
        # proceed until we find the next sample relevant for the grouping
        new_index = skip_to_next_sample(index, samples, grouping, direction=1)

        st.session_state.progress = new_index

    if new_index != index:
        st.rerun()



if user_repository.get_qualification() > 1 and "progress" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint("annotation")
    if not st.session_state.progress:  # no checkpoint yet -> simply go to the first relevant sample
        st.session_state.progress = skip_to_next_sample(0, samples, st.session_state.user[3], 1)
st.session_state.page = "adv_ending_task4_annotation_page_sampleX"

if "tutorial_stage" in st.session_state and st.session_state["tutorial_stage"] > 5:
    utils.reset_sample_state()

if user_repository.get_qualification() < 2:
    st.write("## You must do the qualification and tutorial before starting annotation. \n\n Select **Qualification**, then **Tutorial** in the navigation bar to your left.")
elif user_repository.get_qualification() == 3:
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

        # need some special logic now
        handle_next_button(annotation, index, samples)

    if back_button:
        utils.reset_sample_state()
        handle_back_button(annotation, index, samples, "annotation")