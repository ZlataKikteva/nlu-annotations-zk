import os

import streamlit as st
import random

from core.scripts import user_repository
from core.scripts.utils import display_progress, read_json_from_file, handle_back_button, TASK_INFO, skip_to_next_sample, load_annotation


samples = read_json_from_file(TASK_INFO["adv_eval_ending_task"]["qualification_filepath2"])



def print_annotation_schema_connections(samples, index):
    """
    Print annotation schema for connect-the-concept type annotatoin.
    """
    domain = "qualification"
    question = samples[domain]
    # display the "Sample 1/5" thing

    st.markdown("""**Please read the following instructions. You will have to pass this qualification example before you can access the main study.**
                
**Connect the terms on the left with the category that best describes it on the right. For example, if one of the terms on the left is 'cat', you should look for a fitting category such as 'feline' or 'mammal'.**
                
**If you don't know a term, leave it be!** Only connect terms you know. Some are even made-up. Then, press the button below to send your connections. Many terms in this study are rather obscure and you are not expected to know most of them.

**Please do not blindly guess or use search engines.**
             
To connect a word, first **click on the term on the left side, then click on the category on the right.** The connection will be displayed below.
  
**Please note: Please do not leave/refresh the page or stay inactive for a prolonged period of time, as you may lose some progress.**
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
                

    self_assessment = None# st.segmented_control("Regarding the field these terms are from, and regardless of your performance here - would you consider yourself to usually be more knowledgeable in this field than the average person?", options=["Yes", "No", "I don't know"], default=None, key=20*int(index)+17)

    st.write("Current connections:")
    for term, category in st.session_state.connections:
        st.write(f"{term} -> {category}")

    st.write("Make sure all of these connections are correct, and that you avoided connecting unfamiliar terms. If you make a mistake here, you will be screened out.")

    if st.button("Reset these connections (Start Over)"):
        st.session_state.connections = []
        st.session_state.clipboard = None
        st.rerun()

    if len(st.session_state.connections) == 0:
        label = "Submit - I don't know any of these words"
    elif len(st.session_state.connections) < 5:
        label = "Submit - I don't know the other words"
    else:
        label = "Submit"

    next_input = st.button(key = 20 * int(index) + 15, label=label, help="Press this button to submit your connections.")

    return st.session_state.connections, next_input, self_assessment


def handle_next_button(annotation, index, samples):
    st.write("Please wait...")
    user_repository.save_one_annotation(st.session_state.user_id, "qualification", index+1, annotation)

    connections = annotation["choices"]
    connected_terms = [x[0] for x in connections]
    if ["green", "color"] in connections and ["microsoft", "company"] in connections and ["milkshake", "drink"] in connections \
        and ("dschanbaringta" not in connected_terms) and ("katanberoug" not in connected_terms):
        user_repository.set_qualification(st.session_state.user_id, setting=2)
        print("qualified")
    else:
        user_repository.set_qualification(st.session_state.user_id, setting=-1)
        print("unqualified")

    st.rerun()

if "clipboard" not in st.session_state:
    st.session_state.clipboard = None

if "connections" not in st.session_state:
    st.session_state.connections = []

if "list_of_categories" not in st.session_state:
    st.session_state.list_of_categories = []
    st.session_state.list_of_terms = []

st.session_state.page = "expertise_qualification_sample"

if user_repository.get_qualification() >= 2:
    st.write("## You finished the qualification test successfully! Now select 'Main Study Part 1' on the left to begin the study.")
elif user_repository.get_qualification() == 0:
    st.write("## You need to do the qualification tests in order! Do Qualification (Part 1) first.")
elif user_repository.get_qualification() == -1:
    st.write("## Sorry, you failed the qualification test. Please copy the below screenout code into Prolific.")
    st.write("## " + os.getenv("PROLIFIC_SCREENOUT_CODE"))
else:
    index = 1

    back_button = None#st.button(label="Back", key = 10 * index + 7, help="Go back to the previous sample.")

    domain_list = ["qualification"]

    choices, next_input, self_assessment = print_annotation_schema_connections(samples, index)
    domain = domain_list[0]
    annotation = {"domain": domain, "choices": choices, "self_assessment": self_assessment}

    if next_input:
        st.session_state.connections = []
        st.session_state.clipboard = None
        st.session_state.list_of_categories = []
        st.session_state.list_of_terms = []
        handle_next_button(annotation, index, samples)