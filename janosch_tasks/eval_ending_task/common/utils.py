import streamlit as st

from core.scripts.utils import display_progress, read_json_from_file, load_annotation, TASK_INFO


def format_sentence(sentence):
    return "***" + sentence.replace("[", ":blue-background[") + "***\n"

slider_labels = {
        0: "0 - defininitely wrong",
        1: "1 - very unlikely",
        2: "2 - a bit unlikely",
        3: "3 - plausible",
        4: "4 - very plausible",
        5: "5 - definitely correct"
}

def print_annotation_schema_sliders(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema for the annotation with the sliders. 
    I don't think anyone reads this docsstrings lalalalala

    :param subtask: str
    :param index: The number sample to show
    :return: The stuff to return
    """
    if subtask == "qualification":
        samples = read_json_from_file(TASK_INFO["eval_ending_task"]["qualification_filepath"])
    else:
        samples = read_json_from_file(TASK_INFO["eval_ending_task"]["annotation_filepath"])

    sample_preload = load_annotation(subtask, index)
    if not sample_preload:
        value_slider, value_nonsensical, value_comment = 0, None, ""
    else:
        value_slider, value_nonsensical, value_comment = (sample_preload["slider"], sample_preload["nonsensical"], sample_preload["comment"])

    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key=subtask)

    st.markdown("Read the following story")

    st.markdown(question["precontext"] + " " + format_sentence(question["sentence"].replace(question["word"], "[" + question["word"] + "]")) + " " + question["ending"])

    st.markdown("Focus on the highlighted word: :blue-background[" + question["word"] + "].\n")
    st.write("Given the context of the story, is this word sense plausible:")
    
    st.write("**" + question["displayed_meaning"] + "**")
    st.write("")  # some room to breathe.
    slider_choice = st.select_slider(
    "Select how likely you think this interpretation of the word in the story is.",
    options=[
        slider_labels[0],
        slider_labels[1],
        slider_labels[2],
        slider_labels[3],
        slider_labels[4],
        slider_labels[5]
    ],
    key = 10 * index + 3,
    value=slider_labels[value_slider]
)

    nonsense_input = st.checkbox(key = 10 * index + 4, label = "Is the story nonsensical?", value=value_nonsensical)
    st.write("\n\n")

    comment_input = st.text_input(key = 10 * index + 8, label = "Comments (optional)", value=value_comment, help="Optional free text for comments and thoughts", max_chars=1000)

    next_input = st.button(key = 10 * index + 9, label="Next", help="Save this annotation and advance to the next one.")


    slider_choice = int(slider_choice[0])
    return question, slider_choice, nonsense_input, comment_input, next_input
