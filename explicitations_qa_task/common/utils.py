import streamlit as st
import random 
from core.scripts.utils import read_json_from_file, TASK_INFO, display_progress, load_annotation
import html

# Study setup -- with paraphrased gold option use GOLD_PARAPHRASED, otherswise for the control study use GOLD_ORIGINAL

ANSWER_VERSION = "GOLD_PARAPHRASED"
 
GOLD_KEYS = ["GOLD_ORIGINAL", "GOLD_PARAPHRASED"]
NONE_OPTION = "NONE_OF_THE_ABOVE"
NONE_TEXT = "None can be inferred from the target sentence."


def check_if_qualified(annotations: dict):
    """
    Checks if the user's annotations are enough to pass the qualification test.
    The annotator fails if they ticked:
      - the implausible option in 2 or more items, or
      - the plausible-in-a-different-context option in 5 or more items.

    :param annotations: User annotations, should have a 'qualification' key.
    """
    max_implausible = 2
    max_diff_context = 5
    max_none = 10

    implausible_count = 0
    diff_context_count = 0
    none_count = 0
    for item in annotations.get("qualification", []):
        selected = item.get("selected", [])
        if "IMPLAUSIBLE" in selected:
            implausible_count += 1
        if "PLAUSIBLE_DIFF_CONTEXT" in selected:
            diff_context_count += 1
        if NONE_OPTION in selected:
            none_count += 1

    return (implausible_count < max_implausible
            and diff_context_count < max_diff_context
            and none_count < max_none)

def get_options(question: dict, index: int) -> list:
    """
    Returns the answer options (chosen gold option plus non-gold options and the none can be inferred).
    Options are shuffled, none can be inferred always last.
    Seeded with index to ensure consistent order across reruns.
    """
    answer_options = question["generated"]["answer_options"]
    options = [(ANSWER_VERSION, answer_options[ANSWER_VERSION])]
    options += [(label, text) for label, text in answer_options.items() if label not in GOLD_KEYS]
    random.Random(index).shuffle(options)
    return options + [(NONE_OPTION, NONE_TEXT)]

def clean_text(text: str) -> str:
    """Put text on one line and stop Streamlit from reading symbols in it as formatting."""
    text = " ".join((text or "").split())   # remove line breaks and extra spaces
    text = html.escape(text, quote=False)   # show <, > and & as plain characters
    text = " ".join(word for word in text.split() if word != "*")  # drop wikiHow bullet markers
    for symbol in ["\\", "*", "_", "$", "#", "`"]:
        text = text.replace(symbol, "\\" + symbol)  # e.g. * would start italics, $ would start a formula
    return text


def print_annotation_schema(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema that is seen on the qualification and annotation page.
 
    :param subtask: qualification or annotation
    :param index: The number sample to show
    :return: The question, selected options, text input, and next button state.
    """
    if subtask == "qualification":
        samples = read_json_from_file(TASK_INFO["explicitations_qa_task"]["qualification_filepath"])
    else:
        samples = read_json_from_file(TASK_INFO["explicitations_qa_task"]["annotation_filepath"])
 
    # load values previously filled in or defaults if this is the first time annotating this sample
    sample_preload = load_annotation(subtask, index)
    if sample_preload is None:
        value_selected, value_textinput = [], ""
    else:
        value_selected = sample_preload.get("selected", [])
        value_textinput = sample_preload.get("textinput", "")
 
    question = samples[str(index)]
    # display the "Sample 1/5" thing
    # display_progress(key=subtask)

    # count only this annotator's group, e.g. "Sample 3/15" instead of "Sample 18/30"
    grouping = st.session_state.user[3]
    group_keys = [k for k, s in samples.items() if "grouping" not in s or s["grouping"] == grouping]
    position = group_keys.index(str(index)) + 1 if str(index) in group_keys else index
    st.write(f"**Sample {position}/{len(group_keys)}**")
 
    # Article title, then context and target sentence as one passage (target sentence in bold)
    st.markdown("#### Text")
    if question.get("article_name"):
        article_title = question["article_name"].removesuffix(".txt").replace("_", " ")
        st.markdown(f"**Article:** {clean_text(article_title)}")

    passage = []
    if question.get("context_before"):
        passage.append(clean_text(question["context_before"]))
    passage.append(f"<b>{clean_text(question['sentence_1'])}</b>")  # sentence_1 = without the explicitation
    if question.get("context_after"):
        passage.append(clean_text(question["context_after"]))
    st.markdown(" ".join(passage), unsafe_allow_html=True)
 
    st.markdown("#### Question")
    q = question["generated"]["question"]
    if not (q.startswith("I ") or q[:2].isupper()):
        q = q[0].lower() + q[1:]
    st.write(f"According to the target sentence and given the context, {q}")
 
    # Display the input widgets: radio so only one option can be selected at a time
    st.markdown("#### Select one answer")
    options = get_options(question, index)
    labels = [label for label, _ in options]
    texts = dict(options)
    preselected = labels.index(value_selected[0]) if value_selected and value_selected[0] in labels else None
    choice = st.radio(
        "Answer",
        labels,
        format_func=lambda label: texts[label],
        index=preselected,
        key=f"{subtask}_{index}_choice",
        label_visibility="collapsed",
    )
    selected = [choice] if choice else []

    #text_input = st.text_input(key=f"{subtask}_{index}_text", label="Comments (optional)",
                               # max_chars=200, value=value_textinput) # this is for the comment field, skipping it for now

    text_input = ""  # skipping the comment field for now

    # only show the next button once an option is selected
    if not selected:
        next_input = None
    else:
        next_input = st.button(key=f"{subtask}_{index}_next", label="Next")

    # return all the given input
    return question, selected, text_input, next_input
