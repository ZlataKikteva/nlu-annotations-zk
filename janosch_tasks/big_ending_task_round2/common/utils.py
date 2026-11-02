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
        samples = read_json_from_file(TASK_INFO["big_ending_task_round2"]["qualification_filepath"])

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
        samples = read_json_from_file(TASK_INFO["big_ending_task_round2"]["annotation_filepath"])

        # load values previously filled in checkboxes or None if this is first time annotating this sample
        sample_preload = load_annotation(subtask, index)
        if sample_preload is None:
            value_textbox1, value_textbox2 = "", ""
        else:
            value_textbox1, value_textbox2 = (sample_preload["ending"], sample_preload["comment"])

        display_progress(key=subtask)

        question = samples[str(index)]

        if question["displayed_meaning"] == question["meaning1"]:
            question["displayed_meaning_example"] = question["meaning1_example"]
        else:
            question["displayed_meaning_example"] = question["meaning2_example"]

        st.write(f"The ambiguous word is **{question["word"]}**")

        if st.toggle("Show word definitions", value=False, key=10 * index + 2):
            st.write(f"""The word {question["word"]} has multiple meanings, such as: 

1) {question["meaning1"]}  (as in: "{question["meaning1_example"]}")  
2) {question["meaning2"]} (as in: "{question["meaning2_example"]}") 

(Please note that the example sentences were automatically generated and may at times be mistaken.)

""")


        st.write("Read the first four sentences of this short story.")

        sentence = question["revision"]
        st.write("---")
        st.write(question["precontext"] + " ***" + sentence + "***")
        st.write("---")

        st.write(f"""
     
#### In this story, the intended meaning of {question["word"]} is: 
        
#### **"{question["displayed_meaning"]}"**.  
##### (as in: {question["displayed_meaning_example"]})

Write an ending sentence for the story WITHOUT using the word {question["word"]} again. Make sure that the intended meaning comes across as the most plausible meaning!
        """)

        ending_input = st.text_input(key = 10 * index + 1, label="Write your ending sentence here.", value=value_textbox1)

        comment_input = st.text_input(key = 10 * index + 8, label="(Optional) Space for you to add comments.", value=value_textbox2)

        next_input = None
        if ending_input:
            next_input = st.button(key = 10 * index + 9, label="Next", help="Save this annotation and advance to the next one.")

        return question, ending_input, comment_input, next_input
