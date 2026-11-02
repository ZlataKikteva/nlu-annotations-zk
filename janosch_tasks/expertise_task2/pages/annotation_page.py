import os

import streamlit as st
import random

from core.scripts import user_repository
from core.scripts.utils import display_progress, read_json_from_file, handle_next_button, handle_back_button, TASK_INFO, skip_to_next_sample, load_annotation


samples = read_json_from_file(TASK_INFO["expertise_task2"]["annotation_filepath"])



def print_annotation_schema_connections(samples, index):
    """
    Print annotation schema for connect-the-concept type annotatoin.
    """
    domain = st.session_state.domain_list[index]
    question = samples[domain]
    # display the "Sample 1/5" thing
    display_progress(key="annotation")

    st.markdown("""**As before, connect the terms on the left with the category that best describes it on the right.**
                
From now on, the terms will become much more obscure. You probably will not know most of them. **Please continue skipping terms that you don't know!**
                
Some tips:
                
- Each category will fit to at least one term. You may use process of elimination to connect the last term.
                
- **Please do not blindly guess or cheat by using search engines.** Being honest about what you know is most important for this study.
   
- There are 21 groups of 5 terms in total.
                    
**Please note: Do not leave/refresh the page or stay inactive for a prolonged period of time, as you may lose some progress.**
                """)
    
    print(question)

    if not st.session_state.list_of_terms:
        list_of_terms = [x[1] for x in question]
        random.shuffle(list_of_terms)
        st.session_state.list_of_terms = list_of_terms
        
        list_of_categories = list(set(x[3] for x in question))
        random.shuffle(list_of_categories)
        st.session_state.list_of_categories = list_of_categories

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Terms")
        for item in st.session_state.list_of_terms:
            if item in [x[0] for x in st.session_state.connections]:
                disable_item = True
            else:
                disable_item = False
            if st.session_state.clipboard == item:
                color = "secondary" #"primary"  # nevermind.. this would require a rerun
            else:
                color = "secondary"

            if st.button(item.lower(), key=f"{20*index}_a_{item}", disabled=disable_item, type=color):
                st.write(f"Connect {item.lower()} with what?")
                st.session_state.clipboard = item

    with col_right:
        st.subheader("Categories")
        for item in st.session_state.list_of_categories:
            categories_disabled = False
            if not st.session_state.clipboard:
                categories_disabled = True
            if st.button(item, key=f"{20*index}_b_{item}", disabled=categories_disabled):
                if st.session_state.clipboard:  # JUST TO BE SURE
                    st.write(f"{st.session_state.clipboard} connected to {item}!")
                    st.session_state.connections.append([st.session_state.clipboard, item])
                    st.session_state.clipboard = None
                    st.rerun()
                


    st.write("Current connections:")
    for term, category in st.session_state.connections:
        st.write(f"{term} -> {category}")

    if st.button("Reset these connections (Start this page from the beginning)", key=20 * int(index) + 18):
        st.session_state.connections = []
        st.session_state.clipboard = None
        st.rerun()

    st.write("When you're finished or stuck, press the button below.")

    if len(st.session_state.connections) == 0:
        label = "Next - I don't know any of these words"
        if st.session_state.progress > 0:
            st.write("**Your solution for the last word group was saved. Please check the new words above.**")
    elif len(st.session_state.connections) < 5:
        label = "Next - I don't know enough about the other words"
    else:
        label = "Next"

    if not st.session_state.know_nothing and not st.session_state.connections:
        next_input = None
    else:
        next_input = st.button(key = 20 * int(index) + 19, label=label, help="Press this button to continue to the next group of terms.")

    self_assessment = st.segmented_control("You haven't connected anything yet. If you want to continue, confirm that you are stuck by pressing this button.", options=["I don't know any of these words."], default=None, key=20*int(index)+17)
    if self_assessment:
        st.session_state.self_assessment = self_assessment

    # not an issue anymore
    #st.write("**The terms above will update when you click the button. Be careful not to double-click it!**")


    return st.session_state.connections, next_input, st.session_state.self_assessment

def print_annotation_schema(samples, index):
    """
    Prints the annotation schema for the annotation
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

if "clipboard" not in st.session_state:
    st.session_state.clipboard = None

if "connections" not in st.session_state:
    st.session_state.connections = []

if "list_of_categories" not in st.session_state:
    st.session_state.list_of_categories = []
    st.session_state.list_of_terms = []

if "self_assessment" not in st.session_state:
    st.session_state.self_assessment = False 

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

        user_repository.save_one_annotation(st.session_state.user_id, "sample_order", 1, st.session_state.domain_list)

st.session_state.page = "expertise_sample" + str(st.session_state.progress)

if user_repository.check_if_done(st.session_state.user_id):
    st.write("## You have finished annotation. \n\nThank you for your time!")
    st.write("\n\n\n")
    st.write("**Your Prolific Completion Code:**")
    st.write("# " + os.getenv("PROLIFIC_COMPLETION_CODE"))
elif user_repository.get_qualification() < 1:
    st.write("## You must successfully clear the qualification test before starting the main study.")

else:
    index = int(st.session_state.progress)

    back_button = None#st.button(label="Back", key = 10 * index + 7, help="Go back to the previous sample.")

    if "samples" not in st.session_state:
        st.write("(Note: Tried to re-load checkpoint after leaving page.)")
        st.session_state.domain_list = load_annotation("sample_order", 1)
        st.session_state.samples = samples

    choices, next_input, self_assessment = print_annotation_schema_connections(st.session_state.samples, index)
    domain = st.session_state.domain_list[index]
    annotation = {"domain": domain, "choices": choices, "self_assessment": self_assessment}

    if next_input:
        st.session_state.connections = []
        st.session_state.clipboard = None
        st.session_state.list_of_categories = []
        st.session_state.list_of_terms = []
        st.session_state.self_assessment = None
        handle_next_button(annotation, index, st.session_state.samples)