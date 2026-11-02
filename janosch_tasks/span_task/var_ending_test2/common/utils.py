import json
import streamlit as st

from core.scripts.utils import display_progress, read_json_from_file, load_annotation, TASK_INFO

with open("var_ending_test2/resources/tutorial_text.json", "r") as f:
    tutorial_texts = json.load(f)

def reset_sample_state():
    st.session_state["sample_state"] = {"Beginning": "Select the first part.", "Ending": "Select the second part.",
                                         "editing": {"Beginning": False, "Ending": False},
                                         "choice": {"Beginning": "Select the first part.", "Ending": "Select the second part."}}
    if "tutorial_stage" in st.session_state:
        st.session_state["tutorial_stage"] = 0

if "sample_state" not in st.session_state:
    reset_sample_state()

print("running utils...")

def format_sentence(sentence):
    return "***" + sentence.replace("[", ":blue-background[") + "***\n"


def sentence_selection_box(sentences, index, part="Beginning", in_tutorial=False):
    if "sample_state" not in st.session_state: # no idea why this is necessary. man
        reset_sample_state()
    if "tutorial_stage" not in st.session_state:
        st.session_state["tutorial_stage"] = 0  # you can skip the tutorial and go straight to the annotation if you take a break

    disable_this_box = False
    if in_tutorial and part=="Beginning" and st.session_state["tutorial_stage"] in [4, 5, 6, 7]:
        disable_this_box = True
    elif in_tutorial and part=="Ending" and st.session_state["tutorial_stage"] in [0, 1, 2, 3]:
        disable_this_box = True
        
    if part == "Beginning":
        print_part = "First part"
        select_text = "Select the first part."
    else:
        print_part = "Second part"
        select_text = "Select the second part."

    contains_edited_sentence = False
    if st.session_state["sample_state"][part] not in ["Select the first part.", "Select the second part."]:
        contains_edited_sentence = True

    if not st.session_state["sample_state"]["editing"][part]:

        if not contains_edited_sentence:
            radio_selection = st.radio(print_part + ":", options=[st.session_state["sample_state"][part]] + sentences, key=index*20, disabled=disable_this_box)
        else:
            radio_selection = st.radio(print_part + ":", options=[st.session_state["sample_state"][part]], key=index*20+1, disabled=disable_this_box)

        if radio_selection != st.session_state["sample_state"][part]:
            st.session_state["sample_state"]["choice"][part] = radio_selection

        if part == "Beginning" and st.session_state["tutorial_stage"] == 1:
            st.write(tutorial_texts['1'])
        elif part == "Beginning" and st.session_state["tutorial_stage"] == 2:
            st.write(tutorial_texts["2"])
        elif part == "Beginning" and st.session_state["tutorial_stage"] == 3:
            st.write(tutorial_texts["3"])

        if not contains_edited_sentence:
            if st.button("Edit selected sentences", key=index*20+3, disabled=disable_this_box, help="Open a text editor to edit the currently selected option."):  
                st.session_state["sample_state"]["editing"][part] = True
                st.session_state["sample_state"][part] = radio_selection
                st.rerun()
        else:
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Edit", key=index*20+4, disabled=disable_this_box, help="Edit your story part."):  
                    st.session_state["sample_state"]["editing"][part] = True
                    st.session_state["sample_state"][part] = radio_selection
                    st.rerun()

            with col2:
                if st.button("Reset", key=index*20+5, disabled=disable_this_box, help="Reset the selection to display the templates again."):
                    st.session_state["sample_state"][part] = select_text
                    st.rerun()


    else:
        custom_text = st.text_area("Write your edit here and confirm by pressing the button below.", value=st.session_state["sample_state"][part], max_chars=1000)
        if st.button("Confirm", key=index*20+6):
            st.session_state["sample_state"][part] = custom_text
            st.session_state["sample_state"]["editing"][part] = False
            st.session_state["sample_state"]["choice"][part] = custom_text
            st.rerun()

def check_user_sample_progress():
    samples_done = 0
    samples_skipped = 0
    if "annotation" not in st.session_state.user[5]:
        return 0, 0
    annotations = st.session_state.user[5]["annotation"]
    for annotation in annotations:
        if not annotation:
            continue 
        if annotation["skipping_reason"]:
            samples_skipped += 1
        else:
            samples_done += 1
    print(samples_done, samples_skipped)
    return samples_done, samples_skipped
    

def print_annotation_schema(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema that is seen on the qualification and annotation page.

    :param subtask: qualification or annotation
    :param index: The number sample to show
    :return: The sentence and widget inputs in the order they are displayed to the user.
    """
    in_tutorial = False
    skipping_reason = ""
    skip_toggle = False
    next_input = False
    if subtask=="tutorial":
        in_tutorial = True


    if subtask == "qualification":
        samples = read_json_from_file(TASK_INFO["var_ending_test"]["qualification_filepath"])

        # load values previously filled in checkboxes or None if this is first time annotating this sample
        sample_preload = load_annotation(subtask, index)
        if sample_preload is None:
            value_checkbox1, value_checkbox2, value_textinput1, value_checkbox3, value_textinput2 = None, None, "", None, ""
        else:
            value_checkbox1, value_checkbox2, value_textinput1, value_checkbox3, value_textinput2 = (sample_preload["meaning1"], sample_preload["meaning2"], None, None, None)
        
        question = samples[str(index)]
        # display the "Sample 1/5" thing
        # display_progress(key=subtask)

        st.markdown("Read the following story:")

        st.markdown("**" + question["precontext"] + "**")
        st.markdown(format_sentence(question["sentence"]))

        st.markdown("Focus on the highlighted word: :blue-background[" + question["word"] + "].\n")
        st.write("Which of these is more plausible?")
        checkbox1 = st.checkbox(key=index*20+10, label=question["meaning1"], value=value_checkbox1)
        checkbox2 = st.checkbox(key =index*20+11, label=question["meaning2"], value=value_checkbox2)

        if (checkbox1 or checkbox2) and not (checkbox1 and checkbox2):
            next_input = st.button(key=index*20+12, label="Next", help="Save this annotation and advance to the next one.")
        else:
            next_input = None

        return question, checkbox1, checkbox2, next_input

    else:  # annotation and tutorial
        if subtask == "annotation":
            samples = read_json_from_file(TASK_INFO["var_ending_test2"]["annotation_filepath"])
        else:
            samples = read_json_from_file(TASK_INFO["var_ending_test"]["tutorial_filepath"])

        # load values previously filled in checkboxes or None if this is first time annotating this sample
        sample_preload = load_annotation(subtask, index)
        

        # display_progress(key=subtask)
        samples_done, samples_skipped = check_user_sample_progress()
        st.write(f"{samples_done} out of 10 stories finished.")

        question = samples[str(index)]
        
        if subtask == "annotation":


            if not in_tutorial:
                skip_toggle = st.toggle("Show options for skipping", key=index*20+12, help="Show options for skipping a story (Pressing this button does not yet skip the story).")
                if skip_toggle:
                    st.markdown("""
You are allowed to skip stories. Possible reasons are, for example: 
    
- The given sentence makes no sense
                                
- You are not familiar with the word's meanings
                                
- The given sentence is not ambiguous
                                
You will not be punished for skipping stories, but keep in mind that skipped stories won't count towards your task completion.""")
                    skipping_reason = st.text_input("Why do you want to skip this story? (Required)", max_chars=1000, key=index*20+13)
                    if skipping_reason:
                        skip_button = st.button("Send and skip to next sample.")
                        if skip_button:
                            picked_precontext = "SKIPPED"
                            picked_ending = "SKIPPED"
                            next_input = True

            st.markdown(f"""
                        
Construct a story around this sentence:

-------
## {question["sentence"]}     
-------                


This sentence contains the word **'{question["word"]}'**, which has these two meanings:

#### Meanings of {question['word']}:

##### 1) {question["meaning1"]}
(as in: {question["example1"]})

##### 2) {question["meaning2"]} 
(as in: {question["example2"]})

Use and edit the story building blocks so that the slightly more plausible sense of the word in this context becomes:
##### {question["focus_meaning"]}

-------
            """)

        additional_choices_precontext = ["(No text necessary)"]
        additional_choices_ending = ["(No text necessary)"]

        if in_tutorial:
            st.write(tutorial_texts["0"])
        else:
            if st.toggle("Show Guidelines", value=False, key=index*20+7):
                st.markdown("""
**Rules**
                            
- Select story parts from the templates to create a context in which the above meaning is more plausible for the given ambiguous words.
                            
- It should only be implied, not explicitly stated. Readers must use their world knowledge, reasoning and common sense to understand your story.
                            
- You can edit templates as much as you need to, e.g. to fix logical inconsistencies, imply one of the meanings, stylistic reasons, etc.
                            
- You must not use the ambiguous word in your story.
        

**Tips**
                            
- If one of the templates fits the meaning perfectly, simply pick it.

- If one of the templates almost fits, edit it so it fits. For example, maybe it's sometimes enough to replace one word with another one.
                            
- If none of the templates fit at all, you can also write your own. 
                            
- If the story is good as-is, you can also choose to not add anything.

""")
        
        # precontext
        sentence_selection_box(sentences=additional_choices_precontext + question["precontexts"], index=index*10+1, part="Beginning", in_tutorial=in_tutorial)

        if in_tutorial and st.session_state["tutorial_stage"] == 4:
            st.write(tutorial_texts["4"])

        sentence_box = st.radio("Central Sentence: (Cannot be changed)", options=[question["sentence"]], key=index*20+8)

        sentence_selection_box(sentences=additional_choices_ending + question["endings"], index=index*10+3, part="Ending", in_tutorial=in_tutorial)
                                
        if in_tutorial and st.session_state["tutorial_stage"] == 5:
            st.write(tutorial_texts["5"])
        elif in_tutorial and st.session_state["tutorial_stage"] == 6:
            st.write(tutorial_texts["6"])

        picked_precontext = st.session_state["sample_state"]["choice"]["Beginning"]
        picked_ending = st.session_state["sample_state"]["choice"]["Ending"]

        st.markdown(f"""
---------
Your constructed story:
                    
### {"" if picked_precontext=="(No text necessary)" else picked_precontext} {sentence_box.replace(question["word"], ":blue-background[" + question["word"] + "]")} {"" if picked_ending== "(No text necessary)" else picked_ending}

---------
        """)

        if in_tutorial and st.session_state["tutorial_stage"] == 6:
            st.write(tutorial_texts["7"])

        comment = ""
        confidence = ""

        if not in_tutorial:

            confidence = True#st.checkbox("Do you think this story came out above average compared to your other stories? (No impact on payment)", key=index*20+9, help="Pick this if the story is coherent, sounds natural, and implies the meaning successfully. It doesn't affect your payment or submission review, so just be honest. We know it's hard sometimes.")

            comment = st.text_input("Optional space for comments", max_chars=2000, key=index*20+10)

        if not in_tutorial:
            if skip_toggle:
                st.write(":red[Deactivate the 'Skip this story' option at the top to send the story normally]")
            elif picked_precontext == "Select the first part.":
                st.write(":red[You need to select an option for the first part.]")
            elif picked_ending == "Select the second part.":
                st.write(":red[You need to select an option for the second part.]")
            elif " " + question["word"] in picked_precontext:
                st.write(f":red[Your constructed story contains the focus word {question["word"]} in the first part. Please avoid that.]")
            elif " " + question["word"] in picked_ending:
                st.write(f":red[Your constructed story contains the focus word {question["word"]} in the second part. Please avoid that.]")
            else:

                st.write(f":green[OK.] Click next to finish this story.")
                next_input = st.button(key=index*20+11, label="Next", help="Save this story and advance to the next one.")


        print(picked_precontext, sentence_box, picked_ending, comment, confidence, skipping_reason, question, next_input)
        return picked_precontext, sentence_box, picked_ending, comment, confidence, skipping_reason, question, next_input
