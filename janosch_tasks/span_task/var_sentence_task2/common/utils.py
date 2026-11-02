import json
import streamlit as st
import random

from core.scripts.utils import display_progress, read_json_from_file, load_annotation, TASK_INFO, user_repository


def format_sentence(sentence):
    return "***" + sentence.replace("[", ":blue-background[") + "***\n"


def check_number_of_annotations():
    if "annotation" not in st.session_state.user[5]:
        return 0
    annotations = st.session_state.user[5]["annotation"]
    return len([annotation for annotation in annotations if annotation])

def save_one_annotation(user_id: str, key: str, question_index: int, question_annotation: dict):
    """
    Save one annotation for a sample to the database. Special saving logic for a very special task.

    :param user_id:
    :param key: The subcategory of sample, e.g. qualification or main
    :param question_index: At what index to save the annotation, e.g. 3 for the 3rd sample
    :param question_annotation: The annotation to save, which is a dict.
    """
    conn = st.session_state.conn
    cursor = conn.cursor()
    print(question_index)

    user = st.session_state.user

    annotations = user[5]

    if key not in annotations:
        annotations[key] = []

    while len(annotations[key]) <= 5:
        annotations[key].append({})

    annotations[key][question_index] = question_annotation  # barely have to change anything actually
    annotations_json = json.dumps(annotations)
    cursor.execute("""
        UPDATE user_data
        SET annotations = %s
        WHERE user_id = %s
    """, (annotations_json, user_id))
    st.session_state.user[5] = annotations
    conn.commit()


def print_annotation_schema(index: int) -> tuple:
    """
    Prints the annotation schema that is seen on the annotation page.

    :param index: The number sample user is on
    :return: the word, meaning1, meaning2, inputted sentence as tuple
    """
    st.write("Completed", str(check_number_of_annotations()), "out of 5 sentences")

    samples = read_json_from_file(TASK_INFO["var_sentence_task2"]["annotation_filepath"])

    if "random_sample" not in st.session_state:
        random.shuffle(samples)
        sample = samples[0]
        st.session_state.random_sample = sample

    st.write("Can't think of anything? You can press the button below to get a different word. Don't worry, you can press it as often as you want to.")
    reroll_button = st.button(key = 10 * index + 1, label="A different word, please!")

    sample = st.session_state.random_sample

    st.markdown(f"""
    ### The word ***{sample["word"]}*** has two meanings: 

    ##### **Meaning 1**: *{sample["meaning1"]}*   
    (as in: "{sample["example1"]}")  

    ##### **Meaning 2**: *{sample["meaning2"]}*  
    (as in: "{sample["example2"]}")
    
    *Can you write a sentence where the word {sample["word"]} is used in such a way that both of these meanings are plausible interpretations?*
    """)

    next_input = False

    text_input = st.text_input(key=10*index, label="Write your sentence here.", max_chars=1000)

    if text_input:
        if text_input.lower().split().count(sample["word"].lower()) > 1:
            st.write("This sentence is **invalid** as the ambiguous word appears multiple times. Please refer to the guidelines.")
        elif len(text_input) < 10:
            st.write("Try something longer.")
        else:
            next_input = st.button(key = 10 * index + 9, label="Next", help="Save this annotation and advance to the next one.")

    if reroll_button:
        user_repository.add_log(st.session_state.user_id, f"REROLL on word <{sample["word"]}> <{sample["meaning1"]}> <{sample["meaning2"]}>")
        random.shuffle(samples)
        sample = samples[0]
        st.session_state.random_sample = sample
        st.rerun()

    return sample["word"], sample["meaning1"], sample["meaning2"], text_input, next_input



def print_annotation_schema_qualification(index: int) -> tuple:
    """
    Prints the annotation schema that is seen on the qualification page.

    :param index: The number sample to show
    :return: The sentence and widget inputs in the order they are displayed to the user.
    """
    samples = read_json_from_file(TASK_INFO["var_sentence_task2"]["qualification_filepath"])

    # load values previously filled in checkboxes or None if this is first time annotating this sample
    sample_preload = load_annotation("qualification", index)
    if sample_preload is None:
        value_checkbox1, value_checkbox2 = None, None
    else:
        value_checkbox1, value_checkbox2 = (sample_preload["meaning1"], sample_preload["meaning2"])
    
    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key="qualification")

    st.markdown("Read the following story:")

    st.markdown(format_sentence(question["precontext"] + "\n" + question["sentence"]))

    st.markdown("Focus on the highlighted word: :blue-background[" + question["word"] + "].\n")
    st.write("Which of these senses seem plausible?")
    checkbox1 = st.checkbox(key = 10 * index + 1, label=question["meaning1"], value=value_checkbox1)
    checkbox2 = st.checkbox(key = 10 * index + 2, label=question["meaning2"], value=value_checkbox2)

    if (checkbox1 or checkbox2) and (not (checkbox1 and checkbox2)):
        next_input = st.button(key = 10 * index + 9, label="Next", help="Save this annotation and advance to the next one.")
    else:
        st.write("Pick ONE option.")
        next_input = None

    return question, checkbox1, checkbox2, next_input