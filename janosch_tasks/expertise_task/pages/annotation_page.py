import os

import streamlit as st
import random

from core.scripts import user_repository
from core.scripts.utils import display_progress, read_json_from_file, handle_next_button, handle_back_button, TASK_INFO, skip_to_next_sample, load_annotation


samples = read_json_from_file(TASK_INFO["expertise_task"]["annotation_filepath"])



def print_annotation_schema(samples, index):
    """
    Prints the annotation schema for the annotation

    :param subtask: str
    :param index: The number sample to show
    :return: The stuff to return
    """
    
    domain = st.session_state.domain_list[index]
    question = samples[domain]
    # display the "Sample 1/5" thing
    display_progress(key="annotation")

    st.markdown("""**Tell us if you are familiar with the following terms.**
                
To be 'familiar' with a term, you must have heard of it before and have an understanding of the concept, but you are not expected to know the details or definition. 
For example, if the term is 'cello', you may say you are familiar with it if you at least know that it is some type of string instrument.
                
The purpose of this study is simply to check the familiarity of English speakers with these terms. There is no point in cheating or lying, so please be honest. 
You probably won't be familiar with most of the words, and we promise you will not get rejected for 'knowing too little' or anything like that.
                
There are 105 terms in total. Have fun!
                
**Please note: Please do not leave/refresh the page or stay inactive for a prolonged period of time, or you will lose progress.**
                """)


    st.write("\n")

    radio_outputs = {}
    for i, (wn_id, word, sc) in enumerate(question):
        radio_outputs[word] = "-"
    
    for i, (wn_id, word, sc) in enumerate(question):
        radio_outputs[word] = st.radio(label=word, options=["Familiar", "Not familiar"], index=None, key=int(index)*10 + i)

    if not None in list(radio_outputs.values()):
        next_input = st.button(key = 10 * int(index) + 9, label="Next", help="Save this annotation and advance to the next one.")
    else:
        next_input = None
    
    return radio_outputs, next_input

def handle_next_button(annotation, index, samples):
    user_repository.save_one_annotation(st.session_state.user_id, "annotation", index+1, annotation)

    if st.session_state.progress > 19:
        user_repository.mark_as_done(st.session_state.user_id)
        st.rerun()
    else:
        st.session_state.progress += 1

    st.rerun()


if "progress" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint("annotation")
    if not st.session_state.progress:  # no checkpoint yet -> simply go to the first relevant sample

        # user will get a random sample order upon first visit.
        domains = list(samples)
        random.shuffle(domains)

        for domain in samples.values():
            random.shuffle(domain)

        randomized_samples = {k: samples[k] for k in domains}

        st.session_state.samples = randomized_samples
        st.session_state.domain_list = list(randomized_samples.keys())

        st.session_state.progress = 0

        user_repository.save_one_annotation(st.session_state.user_id, "samples", 1, randomized_samples)

st.session_state.page = "expertise_sample" + str(st.session_state.progress)

if user_repository.check_if_done(st.session_state.user_id):
    st.write("## You have finished annotation. \n\nThank you for your time!")
    st.write("\n\n\n")
    st.write("**Your Prolific Completion Code:**")
    st.write("# " + os.getenv("PROLIFIC_COMPLETION_CODE"))
else:
    index = int(st.session_state.progress)

    back_button = None#st.button(label="Back", key = 10 * index + 7, help="Go back to the previous sample.")

    if "samples" not in st.session_state:
        st.write("(Note: Using Failsafe after leaving page. You may experience unexpected behavior.)")
        st.session_state.samples = load_annotation("samples", 1)
        st.session_state.domain_list = list(st.session_state.samples.keys())

    choices, next_input = print_annotation_schema(st.session_state.samples, index)
    domain = st.session_state.domain_list[index]
    annotation = {"domain": domain, "choices": choices}

    if next_input:
        handle_next_button(annotation, index, st.session_state.samples)
