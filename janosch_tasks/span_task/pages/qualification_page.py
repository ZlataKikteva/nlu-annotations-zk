import streamlit as st
import os

from core.scripts import user_repository, utils as core_utils
from span_task.common import logic, utils

if "qualification_progress" not in st.session_state:
    st.session_state.qualification_progress = user_repository.get_checkpoint("qualification") or 1
st.session_state.page = "span_task_qualification_samples" + str(st.session_state.qualification_progress)

if "finished_first_example" not in st.session_state:
    st.session_state.finished_first_example = False

# user qualification of -1 or 1 mean that the test was already attempted
user_qualification = user_repository.get_qualification()
if user_qualification > 0:
    st.markdown("\n## You have finished Qualification successfully. \n\n Time for the main study. Click 'Annotation' on the left.")

elif user_qualification == -1:
    st.markdown("\n## You did not pass the qualification test. \n\n You have already attempted the qualification test and failed. Sorry about that! Please copy the below completion code into Prolific.\n\n")
    st.markdown("## Your completion code: " + os.getenv("PROLIFIC_SCREENOUT_CODE"))

else:
    # get index of sample
    index = int(st.session_state.qualification_progress)

    #if index == 2:
    #    st.write("Remember to read the Task Intro before attempting the qualification test! \n\n *If you make a mistake here, you will get screened out early.*")

    back_button = None# st.button(label="Back", key = 10 * index + 7)

    st.write("""

## Before you start 

Each page shows a short story, one word in it, and one possible meaning of that word. For each page you will:

1. *Rate* how plausible the given meaning of the word is in this story.

2. *Explain* what shaped your rating: the story itself, what you know about the world, or both.

3. *Mark* the words that mattered most.
    

The first example is practice: If you make a mistake, we will tell you what you should have done.

The second and third examples are qualification: If you make a mistake, you will get screened out and partially compensated.

Then, the following seven examples are the real study.

    """)

    # print text and widgets
    question, slider, reason, spans, comment, next_input = utils.print_annotation_schema_sliders("qualification", index)

    annotation = {"question": question, "slider": slider, "reasons": reason, "spans": spans, "comment": comment}
    samples = core_utils.read_json_from_file(core_utils.TASK_INFO["span_task"]["qualification_filepath"])

    if next_input:
        if int(index) > 1:
            core_utils.handle_next_button(annotation, index, samples, "qualification", logic.check_if_qualified)

        else:
            st.write(":red[Here's an evaluation of your annotation.]")
            check1 = False
            check2 = False
            check3 = True
            check4 = False
            if index == 1:
                if slider not in [1, 2]:
                    st.write(f":red[1) Your rating of {slider}] appears unlikely. That would mean that the 'bat' in the story is relatively likely to be an animal. Isn't there another meaning that fits better?")
                else:
                    st.write(":green[1) Your rating of plausibility is correct. The displayed meaning is likely not intended. (Plausibility rating of 1 or 2)]")
                    check1 = True

                if reason["properties"]:
                    st.write(f":green[2) 'Objects', which you picked, is the most fitting reason here. The objects mentioned in the story are the biggest indicator.] Other categories might also be good choices in addition.")
                    check2 = True
                else:
                    st.write(":red[The objects mentioned in the story are the biggest hint towards the meaning. You should pick the corresponding category.]")

                if reason["spatial"]:
                    st.write("Also, you picked 'spatial reasoning'. The position of the objects may influence your decision. This is subjective, but a fair choice.")

                if reason["causal"]:
                    st.write(":red[Also, you picked 'causes and consequences'. This category is very flexible, but since there are no events here that could be considered causes or consequences, you should deselect it.]")
                    check3 = False

                if reason["temporal"]:
                    st.write(":red[Also, you picked 'temporal reasoning'. There is no information about time or duration in the story, so you should deselect it.]")
                    check3 = False

                if reason["social"]:
                    st.write(":red[Also, you picked 'social reasoning'. There is no mention of feelings or other people in the story, so you should deselect it.]")
                    check3 = False

                if reason["characters"]:
                    st.write(":red[Also, you picked 'characters'. We don't know anything about the main character, so it can't have influenced your decision. You should deselect it.]")
                    check3 = False

                if reason["language"]:
                    st.write("Also, you picked 'language'. This category is always subjective and should be picked if the way the story is formulated works better with one of the meanings. If you really think this is the case here, it is okay to select it.")


                if reason["setting"]:
                    st.write("You also picked 'setting'. Perhaps the location (shelf) has influenced your reading of the text. This is subjective, but a fair choice.")

                span_progress = 0
                for span_category in spans:
                    for span in span_category:
                        label = span["label"]
                        if "ball" in label:
                            span_progress += 1
                        if "glove" in label:
                            span_progress += 1

                if span_progress < 2:
                    st.write(":red[3) In the text above, you need to highlight spans of text that provide clues towards the intended meaning of 'bat' with your mouse cursor.]")

                else:
                    st.write(":green[3) And you marked the important spans. Here, the ball and glove are the most important words to mark.]")
                    check4 = True

                if check1 and check2 and check3 and check4:
                    st.write(":green[You passed the practice.] The next two examples will be a qualification test. Good luck!")
                    st.session_state.finished_first_example = True
                else:
                    st.write(":red[Practice by fixing the issues described above, then press the 'next' button again.]")

                    

    if index == 1 and st.session_state.finished_first_example:
        if st.button("Proceed to qualification test"):
            core_utils.handle_next_button(annotation, index, samples, "qualification", logic.check_if_qualified)

    if back_button:
        core_utils.handle_back_button(annotation, index, samples, "qualification")
