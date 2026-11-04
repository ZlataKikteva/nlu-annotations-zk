import streamlit as st
import random 
from core.scripts.utils import read_json_from_file, TASK_INFO, display_progress, load_annotation

# Study setup -- with paraphrased gold option use GOLD_PARAPHRASED, otherswise for the control study use GOLD_ORIGINAL

ANSWER_VERSION = "GOLD_PARAPHRASED"
 
GOLD_KEYS = ["GOLD_ORIGINAL", "GOLD_PARAPHRASED"]
NONE_OPTION = "NONE_OF_THE_ABOVE"
NONE_TEXT = "None of the above"


def check_if_qualified(annotations: dict):
    """
    Checks if the user's annotations are enough to pass the qualification test.
    The annotator fails if they ticked:
      - the implausible option in 2 or more items, or
      - the plausible-in-a-different-context option in 5 or more items.

    :param annotations: User annotations, should have a 'qualification' key.
    """
    max_implausible = 2
    max_diff_context = 5
    max_none = 10

    implausible_count = 0
    diff_context_count = 0
    none_count = 0
    for item in annotations.get("qualification", []):
        selected = item.get("selected", [])
        if "IMPLAUSIBLE" in selected:
            implausible_count += 1
        if "PLAUSIBLE_DIFF_CONTEXT" in selected:
            diff_context_count += 1
        if NONE_OPTION in selected:
            none_count += 1

    return (implausible_count < max_implausible
            and diff_context_count < max_diff_context
            and none_count < max_none)

def get_options(question: dict, index: int) -> list:
    """
    Returns the answer options (chosen gold option plus non-gold options and the none of the above).
    Options are shuffled, none of the above always last.
    Seeded with index to ensure consistent order across reruns.
    """
    answer_options = question["generated"]["answer_options"]
    options = [(ANSWER_VERSION, answer_options[ANSWER_VERSION])]
    options += [(label, text) for label, text in answer_options.items() if label not in GOLD_KEYS]
    random.Random(index).shuffle(options)
    return options + [(NONE_OPTION, NONE_TEXT)]


def print_annotation_schema(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema that is seen on the qualification and annotation page.
 
    :param subtask: qualification or annotation
    :param index: The number sample to show
    :return: The question, selected options, text input, and next button state.
    """
    if subtask == "qualification":
        samples = read_json_from_file(TASK_INFO["explicitations_qa_task"]["qualification_filepath"])
    else:
        samples = read_json_from_file(TASK_INFO["explicitations_qa_task"]["annotation_filepath"])
 
    # load values previously filled in or defaults if this is the first time annotating this sample
    sample_preload = load_annotation(subtask, index)
    if sample_preload is None:
        value_selected, value_textinput = [], ""
    else:
        value_selected = sample_preload.get("selected", [])
        value_textinput = sample_preload.get("textinput", "")
 
    question = samples[str(index)]
    # display the "Sample 1/5" thing
    # display_progress(key=subtask)
    st.write(f"**Sample {index}/{len(samples)}**")
 
    # Context and target sentence (sentence_1 = without the explicitation)
    st.markdown("#### Target sentence in context")
    if question.get("context_before"):
        st.caption("**Context before**")
        st.markdown(f"<span style='color:gray'>{question['context_before']}</span>", unsafe_allow_html=True)
    st.caption("**Target sentence**")
    st.markdown(f"**{question['sentence_1']}**")
    if question.get("context_after"):
        st.caption("**Context after**")
        st.markdown(f"<span style='color:gray'>{question['context_after']}</span>", unsafe_allow_html=True)
 
    st.markdown("#### Question")
    st.write(question["generated"]["question"])
 
    # Display the input widgets: one checkbox per option, so several can be selected.
    # String keys with subtask, index and label keep every widget unique.
    st.markdown("#### Select all answers that apply")
    selected = []
    for label, text in get_options(question, index):
        if st.checkbox(text, key=f"{subtask}_{index}_{label}", value=label in value_selected):
            selected.append(label)
 
    text_input = st.text_input(key=f"{subtask}_{index}_text", label="Comments (optional)",
                               max_chars=200, value=value_textinput)
 
    # only show the next button once the selection is valid
    if not selected:
        next_input = None
    elif NONE_OPTION in selected and len(selected) > 1:
        st.warning(f"'{NONE_TEXT}' can't be combined with other answers.")
        next_input = None
    else:
        next_input = st.button(key=f"{subtask}_{index}_next", label="Next")
 
    # return all the given input
    return question, selected, text_input, next_input
