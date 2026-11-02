import streamlit as st

from core.scripts import database_repository, admin_functions, utils

# TASK_OPTIONS = ("None selected", "ambiguity_task", "example_task", "ambistory_task", "ambisentence_task", "eval_ambisentence_task", "ambistory2_task", "ending_task", "eval_ending_task", "big_ambisentence_task", "big_ending_task", "big_ending_task_round2", "big_eval_ending_task", "big_eval_sentence_task", "var_ending_test", "var_ending_test2", "var_sentence_task", "var_sentence_task2", "adv_sentence_task", "adv_ending_task", "adv_ending_task2", "adv_ending_task3", "adv_ending_task4", "expertise_task", "expertise_task2",
#                 "adv_eval_ending_task", "adv_eval_ending_task2", "span_task")

TASK_OPTIONS = ("None selected", "example_task")

if "database" not in st.session_state:
    st.session_state.database = "Press the other button first"

st.write("# Welcome to the Admin Area.\n\nHere, you can manage annotations and users.")

st.write("## Download Annotation Data")

if st.button(label="Click Here to Get Database File Before Downloading!"):
    st.session_state.database = database_repository.convert_database_to_json()
    st.rerun()
    st.write("OK!")

st.download_button(label="Then click here to download", data = st.session_state.database, file_name="database.json")


st.markdown("""
            ---
            ## Generate New User Codes 
            
            Here you can generate new annotator codes to share with your annotators.
            The amount that is generated equals the amount of annotation groups for the task.
            (e.g. if there are 5 annotation groups, the first ID belongs to the first group, second to the second group, etc)

            """)

generation_button = None
generation_option = st.selectbox(
     "For which task to generate new users?", TASK_OPTIONS)

if generation_option and generation_option != "None selected":
    generation_slider = st.select_slider("How many IDs to generate", options=list(range(150)))
    groups_to_generate = st.selectbox(
        "For which groups to generate that many new users?", ["ALL"] + list(range(utils.TASK_INFO[generation_option]["number_of_annotator_groups"]))
    )
    generation_button = st.button("Click here to generate users")
    if generation_button:
        admin_functions.generate_users(generation_option, generation_slider, groups_to_generate)

st.markdown("""
            ---
            ## Manage Generated User Codes

            Select a task below to manage used and unused user codes.
            """
            )

code_manager_option = st.selectbox(
    "For which task to manage user codes?", TASK_OPTIONS
)
if code_manager_option and code_manager_option != "None selected":
    admin_functions.list_user_codes(code_manager_option)

st.markdown("""
            ---
            ## Manage And Track User Progress
            
            Select a task below to see users' progress and qualification success on this task.
            """)

tracking_option = st.selectbox(
    "Which task to check user progress on?", TASK_OPTIONS
)
if tracking_option:
    admin_functions.list_user_progress(tracking_option)

    tracking_option = st.selectbox(
    "Which task to check group progress on?", TASK_OPTIONS
)
if tracking_option:
    admin_functions.list_group_progress(tracking_option)


st.markdown("---")

danger_on = st.toggle("Enter Danger Zone")

if danger_on:
    text_input = st.text_input("Type DELETE in the field below to reset the database. Please don't do this on the deployed app without telling other admins.", max_chars=200)

    if st.button(label="Confirm") and (text_input == "DELETE"):
        st.write("OK :( Deleting")
        admin_functions.reset_database()
        st.write("Done. Please refresh the page.")



