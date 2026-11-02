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
        samples = read_json_from_file(TASK_INFO["ending_task"]["qualification_filepath"])

        # load values previously filled in checkboxes or None if this is first time annotating this sample
        sample_preload = load_annotation(subtask, index)
        if sample_preload is None:
            value_checkbox1, value_checkbox2, value_textinput1, value_checkbox3, value_textinput2 = None, None, "", None, ""
        else:
            value_checkbox1, value_checkbox2, value_textinput1, value_checkbox3, value_textinput2 = (sample_preload["meaning1"], sample_preload["meaning2"], None, None, None)
        
        question = samples[str(index)]
        # display the "Sample 1/5" thing
        display_progress(key=subtask)

        st.markdown("Read the following story:")

        st.markdown("**" + question["precontext"] + "**")
        st.markdown(format_sentence(question["sentence"]))

        st.markdown("Focus on the highlighted word: :blue-background[" + question["word"] + "].\n")
        st.write("Which of these is more plausible?")
        checkbox1 = st.checkbox(key = 10 * index + 1, label=question["meaning1"], value=value_checkbox1)
        checkbox2 = st.checkbox(key = 10 * index + 2, label=question["meaning2"], value=value_checkbox2)

        if (checkbox1 or checkbox2) and not (checkbox1 and checkbox2):
            next_input = st.button(key = 10 * index + 9, label="Next", help="Save this annotation and advance to the next one.")
        else:
            next_input = None

        return question, checkbox1, checkbox2, next_input

    else:
        samples = read_json_from_file(TASK_INFO["ending_task"]["annotation_filepath"])

        # load values previously filled in checkboxes or None if this is first time annotating this sample
        sample_preload = load_annotation(subtask, index)
        if sample_preload is None:
            value_textbox1, value_textbox2 = "", ""
        else:
            value_textbox1, value_textbox2 = (sample_preload["ending"], sample_preload["comment"])

        display_progress(key=subtask)

        st.write("Read the first four sentences of this short story.")

        question = samples[str(index)]

        sentence = question["sentence"].replace(question["word"], "[" + question["word"] + "]")
        st.write(question["precontext"] + " " + format_sentence(sentence))

        st.write(f"""The word {question["word"]} has multiple meanings, such as: 

1) {question["meaning1"]}  
2) {question["meaning2"]}

In this story, the intended meaning of {question["word"]} is: 
        
**"{question["meaning"]}"**.  

Write an ending sentence for the story. Make sure that the intended meaning comes across as the more likely meaning!
        """)

        ending_input = st.text_input(key = 10 * index + 1, label="Write your ending sentence here.", value=value_textbox1)

        comment_input = st.text_input(key = 10 * index + 8, label="(Optional) Space for you to add comments.", value=value_textbox2)

        next_input = None
        if ending_input:
            next_input = st.button(key = 10 * index + 9, label="Next", help="Save this annotation and advance to the next one.")

        return question, ending_input, comment_input, next_input
