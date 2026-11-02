import os

import streamlit as st
import random

from core.scripts import user_repository
from core.scripts.utils import display_progress, read_json_from_file, handle_next_button, handle_back_button, TASK_INFO, skip_to_next_sample, load_annotation


samples = read_json_from_file(TASK_INFO["adv_eval_ending_task"]["annotation_filepath2"])

grouping_domain_mapping = {
    # just hardcoding it for now...
    0: ["military", "agriculture", "computer_science", "religion", "psychology", "history"],
    1: ["military", "agriculture", "computer_science", "religion", "psychology", "history"],
    2: ["military", "agriculture", "computer_science", "religion", "psychology", "history"],
    3: ["military", "agriculture", "computer_science", "religion", "psychology", "history"],
    4: ["military", "agriculture", "computer_science", "religion", "psychology", "history"],
    5: ["literature", "mathematics", "music", "pharmacy", "chemistry", "linguistics", "astronomy", "theatre"],
    6: ["literature", "mathematics", "music", "pharmacy", "chemistry", "linguistics", "astronomy", "theatre"],
    7: ["literature", "mathematics", "music", "pharmacy", "chemistry", "linguistics", "astronomy", "theatre"],
    8: ["literature", "mathematics", "music", "pharmacy", "chemistry", "linguistics", "astronomy", "theatre"]
}


def print_annotation_schema_connections(samples, index):
    """
    Print annotation schema for connect-the-concept type annotatoin.
    """
    domain = st.session_state.domain_list[index]
    question = samples[domain]
    # display the "Sample 1/5" thing
    # display_progress(key="annotation2")  # hmm this doesnt work, but maybe its not needed for now...

    st.markdown("""**As before, connect the terms on the left with the category that best describes it on the right.**
                
From now on, the terms will become much more obscure. You probably will not know most of them. **Please continue skipping terms that you don't know!**
                
Some tips:
                
- To connect, always press on the left word first and the right word second. If you made a mistake, press the reset button.
                
- **Please do not blindly guess or cheat by using search engines.** Being honest about what you know is most important for this study.
   
- If you don't know any of the words, that's okay! There's a button below you can press in that case.

- There will be about 8 of these 5x5 puzzles assigned to you in total. (The exact number may vary a bit.)
                    
**Please note: Do not leave/refresh the page or stay inactive for a prolonged period of time.**
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
                

    if not st.session_state.connections:
        self_assessment = st.segmented_control("If you are completely stuck, push this button to unlock the option to skip.", options=["I don't know enough about any of these words"], default=None, key=20*int(index)+17)
        if self_assessment:
            st.session_state.self_assessment = self_assessment

    else:
        st.write("Current connections:")
        for term, category in st.session_state.connections:
            st.write(f"{term} -> {category}")

        if st.button("Reset these connections (Start this page from the beginning)", key=20 * int(index) + 18):
            st.session_state.connections = []
            st.session_state.clipboard = None
            st.rerun()

    st.write("When you're finished or stuck, press the button below.")

    if len(st.session_state.connections) == 0:
        if st.session_state.self_assessment:
            st.write("Press the below button to confirm skipping this puzzle.")
        label = "Confirm - I don't know enough about any of these words"
        if st.session_state.progress2 > 0:
            st.write("**Your solution for the last word group was saved. Please check the new words above.**")
    elif len(st.session_state.connections) < 5:
        label = "Next - I don't know enough about the other words"
    else:
        label = "Next"

    if not st.session_state.self_assessment and not st.session_state.connections:
        st.write("Your connections were saved. Scroll up to see the next words.")
        next_input = None
    else:
        next_input = st.button(key = 20 * int(index) + 19, label=label, help="Press this button to continue to the next group of terms.")

    # not an issue anymore
    #st.write("**The terms above will update when you click the button. Be careful not to double-click it!**")


    return st.session_state.connections, next_input, st.session_state.self_assessment


def handle_next_button(annotation, index, samples):
    user_repository.save_one_annotation(st.session_state.user_id, "annotation2", index+1, annotation)

    if annotation["domain"] == "attention_check":  # attention check is last sample
        user_repository.set_qualification(st.session_state.user_id, user_repository.get_qualification() + 1)
        st.rerun()
    else:
        st.session_state.progress2 += 1

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

if "progress2" not in st.session_state and user_repository.get_qualification() > 1:
    st.session_state.progress2 = user_repository.get_checkpoint("annotation2")
    if not st.session_state.progress2:  # no checkpoint yet -> simply go to the first relevant sample

        # user will get a random sample order upon first visit.
        domains = list(samples)
        domains = [domain for domain in domains if (domain == "attention_check") or (domain in grouping_domain_mapping[int(st.session_state.user[3])])]
        attention_check = domains.pop()
        random.shuffle(domains)
        domains.append(attention_check)  # attention check has to be last (annotation automatically ends afterwards)

        for domain in samples.values():
            random.shuffle(domain)

        randomized_samples = {k: samples[k] for k in domains}

        st.session_state.samples = randomized_samples
        st.session_state.domain_list = list(randomized_samples.keys())

        st.session_state.progress2 = 0

        user_repository.save_one_annotation(st.session_state.user_id, "sample_order", 1, st.session_state.domain_list)

st.session_state.page = "expertise_samples"

if user_repository.get_qualification() > 3:
    st.write("## You have finished annotation. \n\nThank you for your time!")
    st.write("\n\n\n")
    st.write("**Your Prolific Completion Code:**")
    st.write("# " + os.getenv("PROLIFIC_COMPLETION_CODE"))
elif user_repository.get_qualification() < 3:
    st.write("## You must successfully clear Qualification (Part 1), Qualification (Part 2) and Main Study Part 1 to do this part.")

else:
    index = int(st.session_state.progress2)

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