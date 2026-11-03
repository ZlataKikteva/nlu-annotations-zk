import json
import random
import string
import streamlit as st

from core.scripts import user_repository, database_repository

TASK_INFO = {
    "example_task": {
        "annotation_filepath": "example_task/resources/samples.json",
        "qualification_filepath": "example_task/resources/qualification_samples.json",
        "number_of_annotator_groups": 1
    },
    "explicitations_qa_task": {
        "annotation_filepath": "explicitations_qa_task/resources/samples.json",
        "qualification_filepath": "explicitations_qa_task/resources/qualification_samples.json",
        "number_of_annotator_groups": 1
    }
    # "ambiguity_task": {
    #     "annotation_filepath": "ambiguity_task/resources/pilot_samples.json",
    #     "qualification_filepath": "ambiguity_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 8
    # },
    # "example_task": {
    #     "annotation_filepath": "example_task/resources/samples.json",
    #     "qualification_filepath": "example_task/resources/qualification_samples.json",
    #     "number_of_annotator_groups": 2,
    # },
    # "ambistory_task": {
    #     "annotation_filepath": "ambistory_task/resources/story_samples.json",
    #     "qualification_filepath": "ambistory_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 1
    # },
    # "ambisentence_task": {
    #     "annotation_filepath": "ambisentence_task/resources/word_senses.json",
    #     "qualification_filepath": "ambisentence_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 1
    # },
    # "eval_ambisentence_task": {
    #     "annotation_filepath":  "eval_ambisentence_task/resources/human_samples.json",
    #     "qualification_filepath": "eval_ambisentence_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 1
    # },
    # "ambistory2_task": {
    #     "annotation_filepath": "ambistory2_task/resources/story_samples.json",
    #     "qualification_filepath": "ambistory2_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 1
    # },
    # "ending_task": {
    #     "annotation_filepath": "ending_task/resources/story_samples.json",
    #     "qualification_filepath": "ending_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 4,
    #     "group_assignment": "post-qualification"
    # },
    # "eval_ending_task": {
    #     "annotation_filepath": "eval_ending_task/resources/story_samples.json",
    #     "qualification_filepath": "eval_ending_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 4,
    #     "group_assignment": "post-qualification"
    # },
    # "big_ambisentence_task": {
    #     "annotation_filepath": "big_ambisentence_task/resources/word_senses.json",
    #     "qualification_filepath": "big_ambisentence_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 1
    # },
    # "big_ending_task": {
    #     "annotation_filepath": "big_ending_task/resources/annotation_samples.json",
    #     "qualification_filepath": "big_ending_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 65,
    #     "group_assignment": "post-qualification"
    # },
    # "big_ending_task_round2": {
    #     "annotation_filepath": "big_ending_task_round2/resources/big_ending_annotations_round2.json",
    #     "qualification_filepath": "big_ending_task_round2/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 35,
    #     "group_assignment": "post-qualification"
    # },
    # "big_eval_ending_task": {
    #     "annotation_filepath": "big_eval_ending_task/resources/annotation_samples.json",
    #     "qualification_filepath": "big_eval_ending_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 130
    # },
    # "big_eval_sentence_task": {
    #     "annotation_filepath": "big_eval_sentence_task/resources/annotation_samples.json",
    #     "qualification_filepath": "big_eval_sentence_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 30,
    #     "group_assignment": "post-qualification"
    # },
    # "var_ending_test": {
    #     "annotation_filepath": "var_ending_test/resources/new_samples.json",
    #     "qualification_filepath": "var_ending_test/resources/qualification_questions.json",
    #     "tutorial_filepath": "var_ending_test/resources/tutorial_questions.json",
    #     "number_of_annotator_groups": 15,
    #     "group_assignment": "post-qualification"
    # },
    # "var_ending_test2": {
    #     "annotation_filepath": "var_ending_test2/resources/new_samples.json",
    #     "qualification_filepath": "var_ending_test2/resources/qualification_questions.json",
    #     "tutorial_filepath": "var_ending_test2/resources/tutorial_questions.json",
    #     "number_of_annotator_groups": 15,
    #     "group_assignment": "post-qualification"
    # },
    # "var_sentence_task": {
    #     "annotation_filepath": "var_sentence_task/resources/sense_pairs.json",
    #     "qualification_filepath": "var_sentence_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 1
    # },
    # "var_sentence_task2": {
    #     "annotation_filepath": "var_sentence_task2/resources/sense_pairs.json",
    #     "qualification_filepath": "var_sentence_task2/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 1
    # },
    # "adv_sentence_task": {
    #     "annotation_filepath": "adv_sentence_task/resources/sense_pairs.json",
    #     "qualification_filepath": "adv_sentence_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 1
    # },
    # "adv_ending_task": {
    #     "annotation_filepath": "adv_ending_task/resources/contexts.json",
    #     "qualification_filepath": "var_ending_test2/resources/qualification_questions.json",
    #     "tutorial_filepath": "var_ending_test2/resources/tutorial_questions.json",
    #     "number_of_annotator_groups": 40,
    #     "group_assignment": "post-qualification"
    # },
    # "adv_ending_task2": {
    #     "annotation_filepath": "adv_ending_task2/resources/contexts.json",
    #     "qualification_filepath": "var_ending_test2/resources/qualification_questions.json",
    #     "tutorial_filepath": "adv_ending_task2/resources/tutorial_questions.json",
    #     "number_of_annotator_groups": 40,
    #     "group_assignment": "post-qualification"
    # },
    # "adv_ending_task3": {
    #     "annotation_filepath": "adv_ending_task3/resources/contexts_redo.json",
    #     "qualification_filepath": "adv_ending_task3/resources/qualification_questions.json",
    #     "tutorial_filepath": "adv_ending_task3/resources/tutorial_questions.json",
    #     "number_of_annotator_groups": 40,
    #     "group_assignment": "post-qualification"
    # },
    # "adv_ending_task4": {
    #     "annotation_filepath": "adv_ending_task4/resources/contexts_redo.json",
    #     "qualification_filepath": "adv_ending_task4/resources/qualification_questions.json",
    #     "tutorial_filepath": "adv_ending_task4/resources/tutorial_questions.json",
    #     "number_of_annotator_groups": 40,
    #     "group_assignment": "post-qualification"
    # },
    # "expertise_task": {
    #     "annotation_filepath": "expertise_task/resources/expertise_words.json",
    #     "number_of_annotator_groups": 1
    # },
    # "expertise_task2": {
    #     "annotation_filepath": "expertise_task2/resources/expertise_words.json",
    #     "qualification_filepath": "expertise_task2/resources/qualification_test.json",
    #     "number_of_annotator_groups": 1
    # },
    # "adv_eval_ending_task": {
    #     "annotation_filepath": "adv_eval_ending_task/resources/plausibility_story_samples.json",
    #     "annotation_filepath2": "adv_eval_ending_task/resources/expertise_words.json",
    #     "qualification_filepath": "adv_eval_ending_task/resources/qualification_questions.json",
    #     "qualification_filepath2": "adv_eval_ending_task/resources/qualification_connections.json",
    #     "number_of_annotator_groups": 8,
    #     "group_assignment": "post-qualification"
    # },
    # "adv_eval_ending_task2": {
    #     "annotation_filepath": "adv_eval_ending_task2/resources/stage2_samples.json",
    #     "annotation_filepath2": "adv_eval_ending_task2/resources/expertise_words.json",
    #     "qualification_filepath": "adv_eval_ending_task2/resources/qualification_questions.json",
    #     "qualification_filepath2": "adv_eval_ending_task2/resources/qualification_connections.json",
    #     "number_of_annotator_groups": 40,
    #     "group_assignment": "post-qualification"
    # },
    # "span_task": {
    #     "annotation_filepath": "span_task/resources/stage2_samples.json",
    #     "qualification_filepath": "span_task/resources/qualification_questions.json",
    #     "number_of_annotator_groups": 1
    # }
}

def read_json_from_file(path: str) -> dict:
    """
    Read a Json-file into a dict from a path.

    :param path: String filepath
    :return: dictionary object
    """
    # TODO Error handling
    with open(path, "r") as f:
        return json.loads(f.read())
    
def generate_random_string(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def authenticate_id(task: str, user_id: id):
    """
    Check if the user id trying to log in for a specific task is valid.
    """
    conn = st.session_state.conn
    cursor = conn.cursor()
    # Check if the user_id exists in the table
    cursor.execute('''
        SELECT 1 FROM valid_ids WHERE user_id = %s
                          AND task = %s
    ''', (user_id, task))
    result = cursor.fetchone()

    # conn.close()
    
    if result:
        return True
    return False


def get_amount_of_samples_for_group(key: str, task: str, group: int) -> int:
    """
    Find the amount of samples a member of a specific group has to do.

    :param task: str, e.g. ambiguity_task
    :param group: integer group index
    :return: int
    """
    if key == "qualification":
        samples = read_json_from_file(TASK_INFO[task]["qualification_filepath"])
    else:
        samples = read_json_from_file(TASK_INFO[task]["annotation_filepath"])
    if type(samples) == list:
        number_of_samples = len(samples)  # currently no cases where samples are list based and grouping based, so thats enough for now
    else:
        number_of_samples = len([x for x in samples if ("grouping" not in samples[x]) or (samples[x]["grouping"] == group)])
    return number_of_samples



def display_progress(key="annotation", user_id=None, print_progress: bool = True) -> str:
    """
    Returns the progress x/y ("x out of y") for a user on a subtask.

    :param key: The subtask, e.g. annotation or qualification
    :param user_id: Id of user to check, if None, display logged in user's progress
    :param print_progress: Whether to print the progress immediately instead of just returning the string
    :return: str
    """
    if not user_id:
        user = st.session_state.user
    else:
        user = user_repository.get_user(user_id)

    user_group = user[3]
    task = user[1]
    max_samples = get_amount_of_samples_for_group(key, task, user_group)

    if not user:
        return "NOT STARTED"

    # TODO show progress even when all annotations are finished (when revising annotations)
    
    # handle case that there are no annotations
    annotations = user[5]
    if key not in annotations:
        if print_progress:
            st.write("Sample 1")
        return "Annotation not started"
    annotations = annotations[key]

    count_finished = 0
    for annotation in annotations:
        if annotation:  # "unfinished" annotations will be empty
            count_finished += 1
    if print_progress:
        st.write("*Finished Samples*: " + str(count_finished) + "/" + str(max_samples))
    return str(count_finished) + "/" + str(max_samples)

def load_annotation(subtask: str, index: int) -> tuple:
    """
    Load one specific annotation from a user's saved data. 
    Useful for prefilling annotations the user already made when they look at previous samples.
    If the sample does not exist or is empty, all loaded values are None.

    :param user_id: id string of user to load from
    :param subtask: qualification or annotation
    :param index: the sample index to load
    :return: loaded sample
    """
    user = st.session_state.user
    annotations = user[5]
    if subtask not in annotations:
        return None
    if len(annotations[subtask]) < index:
        return None
    return annotations[subtask][index-1]

def finish_annotation():
    #st.write("You finished the annotation!")
    if user_repository.get_qualification() > 1:
        # Some tasks use qualification as nonbinary progress marker.
        user_repository.set_qualification(st.session_state.user_id, user_repository.get_qualification() + 1)
    else:
        user_repository.mark_as_done(st.session_state.user_id)
        user_repository.set_qualification(st.session_state.user_id, user_repository.get_qualification() + 1)
    st.rerun()
    st.write("Thank you for submitting your annotations.")


def finish_qualification(qualification_function: str):
    """
    Finish the current user's qualification and judge if they are qualified.
    Sets their qualification accordingly.
    
    :param qualification_function: function that returns True/False based on the user's annotations.
    """
    # if this is the last question, check for qualification
    user = st.session_state.user
    annotations = user[5]
    # check if the qualification was successful and set user state accordingly
    if qualification_function(annotations):
        st.write("The qualification test has ended. Please wait a moment...")
        user_repository.set_qualification(st.session_state.user_id)
        # Since the user is qualified, automatic group assignment can now take place...
        print("automatic group assignment is...")
        if "group_assignment" in TASK_INFO[user[1]] and TASK_INFO[user[1]]["group_assignment"] == "post-qualification":
            print("desired")
            user_repository.assign_to_weakest_group(st.session_state.user_id, user[1])
        st.rerun()
    else:
        st.write("The qualification test has ended. Please wait a moment...")
        user_repository.set_qualification(st.session_state.user_id, setting=-1)
        # user_repository.reset_annotation(st.session_state.user_id, key="qualification")
        st.rerun()

    # reset progress to beginning (important in case an admin decides to reset qualification)
    st.session_state.qualification_progress = 1

def finish_subtask(subtask: str="annotation", qualification_function=None):
    """
    Finish the current subtask. If it is the qualification, call the qualification function to check if the user passed.

    :param subtask: annotation or qualification
    :param qualification_function: a function that returns True/False depending on the user passing
    """
    print("Finishing subtask.")
    if subtask == "annotation":
        finish_annotation()
    elif subtask == "qualification":
        finish_qualification(qualification_function)


def skip_to_next_sample(index: int, samples: dict, grouping: int, direction: int=1, 
                        subtask: str="annotation", qualification_function=None) -> int:
    """
    From the specified index, move in the specified direction to find the next sample relevant to the group.

    :param index: Index of the current page/sample
    :param samples: dict of all the samples (keys are "1", "2", ...)
    :param grouping: group of user
    :param direction: 1 for going forward, -1 for going backward
    :param subtask: e.g. annotation or qualification
    :param qualification function: Function to evaluate whether qualification was passed, not needed if subtask!=qualification
    :return: Index of the next (or previous) sample
    """
    index += direction
    if index < 1:
        return 1
    while True:
        if index > len(samples):
            finish_subtask(subtask, qualification_function)
            break
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


def handle_back_button(annotation: dict, index: int, samples: dict, subtask="annotation"):
    """
    All-in-one behaviour of the back button: Saves revised annotations and skips to the next-oldest relevant sample.

    :param annotation: The annotation of the currently displayed sample
    :param index: The index of the current sample
    :param samples: List with all of the samples (including irrelevant ones for the grouping) for the current subtask
    :param subtask: The current subtask, e.g. annotation or qualification
    """
    # don't save when pressing back on the newest sample, since it will otherwise get skipped when returning later
    if index < user_repository.get_checkpoint(key=subtask, print=False):
        user_repository.save_one_annotation(st.session_state.user_id, subtask, index, annotation)

    grouping = st.session_state.user[3]
    # skip backwards over the samples of the other groups to arrive at the new index
    new_index = skip_to_next_sample(index, samples, grouping, direction=-1)

    if subtask == "qualification":
        st.session_state.qualification_progress = new_index
    else:
        st.session_state.progress = new_index

    st.rerun()



def handle_next_button(annotation: dict, index: int, samples: dict, subtask="annotation", qualification_function=None):
    """
    All-in-one behaviour of the next button: Saves annotation, skips to next relevant sample and finishes the annotation if the end is reached.
    
    :param annotation: The annotation of the current sample that should be saved.
    :param index: The index of the current sample
    :param samples: List with all of the samples (including irrelevant ones for the grouping) for the current subtask
    :param subtask: The current subtask, e.g. annotation or qualification
    :param qualification_function: If subtask=qualification, a function that evaluates success of qualification given user annotations
    """
    user_repository.save_one_annotation(st.session_state.user_id, subtask, index, annotation)

    if index >= len(samples):
        finish_subtask(subtask, qualification_function=qualification_function)
    else:
        grouping = st.session_state.user[3]
        # proceed until we find the next sample relevant for the grouping
        new_index = skip_to_next_sample(index, samples, grouping, direction=1)

    if subtask == "qualification":
        st.session_state.qualification_progress = new_index
    else:
        st.session_state.progress = new_index

    if new_index != index:
        st.rerun()