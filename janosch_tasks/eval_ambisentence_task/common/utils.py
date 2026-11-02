import streamlit as st

from core.scripts.utils import display_progress, read_json_from_file, load_annotation, TASK_INFO


def format_sentence(sentence):
    return "***" + sentence.replace("[", ":blue-background[") + "***\n"

def print_annotation_schema(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema that is seen on the qualification and annotation page.

    :param subtask: qualification or annotation
    :param index: The number sample to show
    :return: The sentence and widget inputs in the order they are displayed to the user.
    """
    if subtask == "qualification":
        samples = read_json_from_file(TASK_INFO["eval_ambisentence_task"]["qualification_filepath"])
    else:
        samples = read_json_from_file(TASK_INFO["eval_ambisentence_task"]["annotation_filepath"])

    # load values previously filled in checkboxes or None if this is first time annotating this sample
    sample_preload = load_annotation(subtask, index)
    if sample_preload is None:
        value_checkbox1, value_checkbox2, value_textinput1, value_checkbox3, value_textinput2 = None, None, "", None, ""
    else:
        value_checkbox1, value_checkbox2, value_textinput1, value_checkbox3, value_textinput2 = (sample_preload["meaning1"], sample_preload["meaning2"], 
                                                                                                 sample_preload["other_label"], sample_preload["nonsensical"],
                                                                                                 sample_preload["comment"])
    
    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key=subtask)

    st.markdown("Read the following sentence:")

    st.markdown(format_sentence(question["sentence"]))

    st.markdown("Focus on the highlighted word: :blue-background[" + question["word"] + "].\n")
    st.write("Which of these senses seem plausible?")
    checkbox1 = st.checkbox(key = 10 * index + 1, label=question["meaning1"], value=value_checkbox1)
    checkbox2 = st.checkbox(key = 10 * index + 2, label=question["meaning2"], value=value_checkbox2)
    text_input1 = st.text_input(key = 10 * index + 3, label = "(Only if you picked neither) Write the definition of a more fitting word sense.", max_chars=200, value=value_textinput1, help="Is there a third sense of the word that is more plausible than either of the above? Leave empty if one of the above meanings is the most plausible.")
    st.write("\n")  # leave some space
    checkbox3 = st.checkbox(key = 10 * index + 4, label = "Is the text nonsensical?", value=value_checkbox3)
    st.write("\n\n")

    text_input2 = st.text_input(key = 10 * index + 8, label = "Comments (optional)", value=value_textinput2, help="Optional free text for comments and thoughts", max_chars=1000)

    if checkbox1 or checkbox2 or text_input1:
        next_input = st.button(key = 10 * index + 9, label="Next", help="Save this annotation and advance to the next one.")
    else:
        next_input = None

    return question, checkbox1, checkbox2, text_input1, checkbox3, text_input2, next_input