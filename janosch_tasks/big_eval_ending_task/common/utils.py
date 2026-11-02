import streamlit as st

from core.scripts.utils import display_progress, read_json_from_file, load_annotation, TASK_INFO


def format_sentence(sentence):
    return "***" + sentence.replace("[", ":blue-background[") + "***\n"

slider_labels = {
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5"
}  # now that the string labels were replaced with numbers. this code is pretty dumb.

label_sliders = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5
}

slider_label_list = list(slider_labels.values())

def print_annotation_schema_sliders(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema for the annotation with the sliders. 

    :param subtask: str
    :param index: The number sample to show
    :return: The stuff to return
    """
    if subtask == "qualification":
        samples = read_json_from_file(TASK_INFO["big_eval_ending_task"]["qualification_filepath"])
    else:
        samples = read_json_from_file(TASK_INFO["big_eval_ending_task"]["annotation_filepath"])

    sample_preload = load_annotation(subtask, index)
    if not sample_preload:
        value_slider, value_nonsensical, value_comment = None, None, ""
    else:
        value_slider, value_nonsensical, value_comment = (sample_preload["slider"], sample_preload["nonsensical"], sample_preload["comment"])
        if value_slider in slider_labels:
            value_slider = slider_labels[value_slider]
        else:
            value_slider = None

    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key=subtask)


    if question["judged_meaning"] == question["sentence_info"]["meaning1"]:
        question["displayed_meaning_example"] = question["sentence_info"]["meaning1_example"]
    else:
        question["displayed_meaning_example"] = question["sentence_info"]["meaning2_example"]


    st.markdown("Read the following story")

    print(question)

    st.write("---")

    st.markdown(question["precontext"] + " " + format_sentence(question["sentence"]) + " " + question["ending"])

    st.write("---")

    st.markdown("Focus on the word: :blue-background[" + question["word"] + "].\n")


    st.write(f"""Given the context of the story, how plausible is the following meaning of the word?
    
    
#### {question["judged_meaning"]}
##### (as in: "{question["displayed_meaning_example"]}")
    """)

    slider_choice = st.segmented_control(
        "Select the plausibility of this meaning.",
        options=slider_label_list,
        selection_mode="single",
        default=value_slider,
        key = 10 * index + 3
    )

    if st.toggle("Show guidelines for rating plausibility", key = 10 * index + 5):
        st.markdown("""
**Annotate how plausible a meaning of a word is in the context of the short text using one of five scores:**

* **1**: The displayed meaning is not plausible at all given the context.
* **2**: The displayed meaning is theoretically conceivable, but less plausible than other meanings.
* **3**: The displayed meaning represents one of multiple, similarly plausible interpretations.
* **4**: The displayed meaning represents the most plausible interpretation; other meanings may still be conceivable.
* **5**: The displayed meaning is the only plausible meaning given the context.
        """)


    st.write("\n")

    nonsense_input = st.checkbox(key = 10 * index + 4, label = "Check this box if the text is nonsensical.", value=value_nonsensical)
    st.write("\n\n")

    comment_input = st.text_input(key = 10 * index + 8, label = "Comments (optional)", value=value_comment, help="Optional free text for comments and thoughts", max_chars=1000)

    if slider_choice:
        next_input = st.button(key = 10 * index + 9, label="Next", help="Save this annotation and advance to the next one.")
    else:
        next_input = None

    if slider_choice:
        slider_choice = label_sliders[slider_choice]

    return_sample = {
        "index": str(index),
        "sentence": question["sentence"],
        "ending": question["ending"],
        "word": question["word"],
        "judged_meaning": question["judged_meaning"]
    }
    
    return return_sample, slider_choice, nonsense_input, comment_input, next_input
