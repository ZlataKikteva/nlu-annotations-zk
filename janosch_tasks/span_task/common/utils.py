import streamlit as st
from streamlit_annotation_tools import text_highlighter

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
        samples = read_json_from_file(TASK_INFO["span_task"]["qualification_filepath"])
    else:
        samples = read_json_from_file(TASK_INFO["span_task"]["annotation_filepath"])

    # ----------------- LOADING -----------------

    #sample_preload = load_annotation(subtask, index)
    #if not sample_preload:
    value_slider, value_nonsensical, value_comment = None, None, ""
    #else:
    #    value_slider, value_nonsensical, value_comment = (sample_preload["slider"], sample_preload["nonsensical"], sample_preload["comment"])
    #    if value_slider in slider_labels:
    #        value_slider = slider_labels[value_slider]
    #    else:
    #        value_slider = None

    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key=subtask)



    # ------------------- FIRST STORY PRINT -------------------------

    if question["focus_meaning"] == "meaning1":
        question["displayed_meaning_example"] = question["example1"]
    else:
        question["displayed_meaning_example"] = question["example2"]

    st.markdown("Read the following story")

    print(question)

    st.write("---")

    part1 = question["context"]["part1"]
    if "No text necessary" in part1:
        part1 = ""
    part3 = question["context"]["part3"]
    if "No text necessary" in part3:
        part3 = ""

    st.markdown(part1 + " " + format_sentence(question["sentence"]) + " " + part3)

    st.write("---")



    # --------------- PLAUSIBILITY RATING ---------------------

    st.markdown("Focus on the word: :blue-background[" + question["word"] + "].\n")


    st.write(f"""Given the context of the story, how plausible is the following meaning of the word?
    
    
#### {question["focus_meaning_gloss"]}
##### (as in: "{question["displayed_meaning_example"]}")
    """)

    slider_choice = st.segmented_control(
        "Select the plausibility of this meaning.",
        options=slider_label_list,
        selection_mode="single",
        default=value_slider,
        key = 50 * index + 1
    )

    guidelines_toggle_value = False
    if int(index) == 1:
        guidelines_toggle_value = True

    if st.toggle("Show guidelines for rating plausibility", key = 50 * index + 2, value=guidelines_toggle_value):
        st.markdown("""
**Annotate how plausible a meaning of a word is in the context of the short text using one of five scores:**

* **1**: The displayed meaning is not plausible at all given the context.
* **2**: The displayed meaning is theoretically conceivable, but less plausible than other meanings.
* **3**: The displayed meaning represents one of multiple, similarly plausible interpretations.
* **4**: The displayed meaning represents the most plausible interpretation; other meanings may still be conceivable.
* **5**: The displayed meaning is the only plausible meaning given the context.
        """)


    st.write("\n")

    slider_reason_labels = ["Not at all", "A little", "Somewhat", "A lot", "Almost entirely"]

    reason_story = None
    reason_logic = None
    reason_properties = None
    reason_location = None
    reason_characters = None
    reason_events = None
    reason_setting = None
    reason_other = None
    reason_story_other = None
    reason_story_other_comment = None
    reason_common = None
    reason_domain = None
    reason_spatial = None
    reason_causal = None
    reason_temporal = None
    reason_social = None
    reason_language = None
    reason_objects = None
    reason_logic_other = None
    reason_logic_other_comment = None
    reason_other = None

    # ---------------------------- REASONS ------------------------------------

    st.write("Please select the reasons for your choice above.")

    st.write("First, regarding the story itself. Did any of these factors influence your rating? (Select all that apply.)")

    reason_location = st.checkbox(label="**General setting**: The physical place, situation, activity or events described in the story.", key = 50 * index + 4, 
                                    help="**Example**: *At the baseball stadium, for some reason, I keep staring at the [bats].*  \n Given the location, a baseball bat seems very plausible.")

    reason_characters = st.checkbox(label="**Characters**: Who is involved, and what they do or are like.", key = 50 * index + 5, 
                                    help="**Example**: *The pianist was able to read the [notes].*  \n Given that the character is a pianist, it seems plausible that 'notes' refers to music notes rather than texts.")

    reason_properties = st.checkbox(label="**Objects**: What things/objects are involved, and what the story says about them.", key = 50 * index + 22, 
                                help="**Example**: *I found a [bat]. It's long and heavy.*  \n It refers to a baseball bat because the animal is not particularly long or heavy. You can also use this category for other properties, such as size, color, applications, etc.")

    #reason_events = st.checkbox(label="**Event**: What happens in the story.", key = 50 * index + 6, 
    #                            help="**Example**: *When the lights went out, a [bat] flew past his face.*  \n The events that happen appear more plausible if bat is an animal.")

    #reason_setting = st.checkbox(label="**General Setting**: The overall situation or activity, beyond the specific place.", key = 50 * index + 7, 
    #                            help="**Example**: *During their piano practice, she looked through the [notes].*  \n The described activity implies the music-related meaning of 'notes'.")

    reason_language = st.checkbox(label="**Language**: Grammar and stylistic choices that work better with a certain meaning.", key = 50 * index + 7,
                                 help="**Example**: *He found a [fair] place to settle the disagreement.*  \n 'Fair' surely means 'just'. The word can also refer to a community event, but the phrase 'a fair place' would sound unnatural if that was the intention.") 

    reason_story_other = st.checkbox(label="**Other**: Anything else in the story. Describe below.", key = 50 * index + 8, help="")

    if reason_story_other:
        reason_story_other_comment = st.text_area(key = 50 * index + 9, height=68, label = "What in the story shaped your rating?", max_chars=500)

    reason_story = st.segmented_control(
        "How much did these factors relating to the story itself shape your rating?",
        options=slider_reason_labels,
        selection_mode="single",
        default=None,
        key = 50 * index + 3
    )


    st.write("")
    st.write("")
    st.write(" \n\n Next, regarding things that are not explicit and require logic, reasoning or knowledge to understand.")

    st.write("Did any of these factors influence your rating? (Check all that apply)")

    reason_common = st.checkbox(label="**Most familiar meaning**: One meaning is more common than others.", key = 50 * index + 11, 
                                help="**Example**: *That thing was [lousy].*  \n 'Lousy' probably means 'bad' instead of 'infested with lice', because that meaning is just not as common.")

    reason_knowledge = st.checkbox(label="**Common knowledge**: Facts that you (and most others) know about the world.", key = 50 * index + 12, 
                                help="**Example**: *I entered the room. There was a [bat] on the ceiling.*  \n This probably describes the animal. It is common knowledge that it hangs on ceilings.")

    reason_domain = st.checkbox(label="**Domain knowledge**: Knowledge in a specific field (e.g. medicine, sports, law); things not everyone knows.", key = 50 * index + 6, 
                                help="**Example**: *The golfer's performance was below [par]. She became frustrated.*  \n A golf fan may know that 'par' is a certain number of strokes, and being 'below par' is a good thing, so it wouldn't make you frustrated.  \n This option can be picked in such cases where your judgment depends on your knowledge of a domain.")

    reason_causal = st.checkbox(label="**Causes and consequences**: Events, states or actions that tend to influence other events, states or actions.", key = 50*index + 13, 
                                help="**Example**: *I needed enough cash to go to the fancy restaurant. I went to a [bank].*  \n 'Bank' likely refers to a financial institution. It makes sense to go to the bank first in order to have enough money for the restaurant.")

    reason_spatial = st.checkbox(label="**Spatial**: Sizes, distances and how things are positioned.", key = 50 * index + 14, 
                                help="**Example**: *From across the living room, I could barely see the [pupils].*  \n Given the described distance and the size of normal students, that meaning does not make sense. It has to refer to the pupils of the eyes.")

    reason_temporal = st.checkbox(label="**Temporal**: The order, timing and duration of things.", key = 50 * index + 15, 
                                help="**Example**: *I spent 15 minutes writing down the [note].*  \n Writing down one musical note would not take that long. More likely to refer to some kind of message.")

    reason_social = st.checkbox(label="**Social**: What people usually feel, intend or how they interact.", key = 50 * index + 16, 
                                help="**Example**: *He was nervous about the [date] all day.*  \n Being nervous about a romantic date (rather than date, the fruit) seems like typical human behavior.")

    reason_logic_other = st.checkbox(label="**Other**: Any other kind of knowledge or reasoning. Describe below.", key = 50 * index + 17)

    if reason_logic_other:
        reason_logic_other_comment = st.text_area(height=68, key = 50 * index + 18, label = "What shaped your rating?", max_chars=500)

    reason_logic = st.segmented_control(
        "How much did you rely on these things that the story doesn't explicitly state?",
        options=slider_reason_labels,
        selection_mode="single",
        default=None,
        key = 50 * index + 10
    )

    if reason_logic in [slider_reason_labels[0]] and reason_story in [slider_reason_labels[0]]:

        reason_other = st.text_area(key = 50 * index + 19, height=68, label = "Something else shaped your rating? Describe it below.", help="If it is neither implicit nor explicit information in the story, what influenced your rating?")

    has_annotated_reasons = ((reason_story) and (reason_logic) and 
                             (reason_story and (reason_location or reason_characters or reason_events or reason_properties or reason_objects or reason_language or reason_setting or (reason_story_other and reason_story_other_comment))) or
                             (reason_logic and (reason_common or reason_domain or reason_causal or reason_knowledge or reason_temporal or reason_social or reason_spatial or (reason_logic_other and reason_logic_other_comment))) or
                             reason_other)

    annotated_reasons = {
        "story": reason_story,
        "logic": reason_logic,
        "location": reason_location,
        "characters": reason_characters,
        "events": reason_events,
        "properties": reason_properties,
        "setting": reason_setting,
        "language": reason_language,
        "story_other": reason_other,
        "story_comment": reason_story_other_comment,
        "common": reason_common,
        "domain": reason_domain,
        "causal": reason_causal,
        "spatial": reason_spatial,
        "temporal": reason_temporal,
        "social": reason_social,
        "logic_other": reason_logic_other,
        "logic_comment": reason_logic_other_comment,
        "other": reason_other
    }


    # ----------------------------- NONSENSICAL INPUT ---------------------------

    nonsense_input = None#st.checkbox(key = 10 * index + 4, label = "Check this box if the text is nonsensical.", value=value_nonsensical)
    #st.write("\n\n")



    # ---------------------------- HIGHLIGHTING -----------------------------------

    text = "  \n\n" + part1 + " " + question["sentence"] + " " + part3 + "  \n\n "

    prehighlight = [
        [
            {"start": 0, "end": 0, "label": "Mark words by selecting them with the mouse cursor."},
            {"start": len(text), "end": len(text), "label": "Mark words by selecting them with the mouse cursor."},
        ],
    ]

    st.write("Now please go through the story again and mark the words that influenced your decision for the reasons you gave above.")

    st.write("---")

    st.write("Select spans of text in the story below by holding left-click and dragging the mouse cursor over them. Mark a word again to undo. (You don't need to press the orange buttons)")

    annotations = text_highlighter(text, highlights=prehighlight)

    st.write("---")

    print(annotations)


    #------------------------------- COMMENTS --------------------------------

    comment_input = st.text_area(key = 50 * index + 20, label = "Comments (optional)", value=value_comment, help="Optional free text for comments and thoughts", max_chars=1000, height=68)

    if slider_choice and has_annotated_reasons:
        next_input = st.button(key = 50 * index + 21, label="Next", help="Save this annotation and advance to the next one.")
    else:
        next_input = None
        st.write(":red[You need to indicate one reason, select a plausibility rating and select an option on both of the 'How much did these factors...' buttons to advance to the next sample.]")

    if slider_choice:
        slider_choice = label_sliders[slider_choice]

    return_sample = {
        "index": str(index),
        "sentence": question["sentence"],
        "context": question["context"],
        "word": question["word"],
        "focus_meaning": question["focus_meaning"],
    }
    
    return return_sample, slider_choice, annotated_reasons, annotations, comment_input, next_input
