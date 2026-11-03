import psycopg2
import streamlit as st

from core.scripts import database_repository, utils, user_repository

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "page" not in st.session_state:
    st.session_state.page = "main"

if "conn" not in st.session_state:
    st.session_state.conn = database_repository.db_connection()

# database_repository.init_db()  # can comment out now, since it already exists...


# Emoticons can be copied from here: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# define pages
main_page = st.Page(
    "core/pages/main_page.py", title="Start Page", icon="🏚️"
)
authentication_page = st.Page(
    "core/pages/authentication_page.py", title="Log In", icon="🎟️", url_path="authentication", default=True
)
admin_page = st.Page(
    "core/pages/admin_page.py", title="Admin Area", icon="💻"
)
logout_page = st.Page(
    "core/pages/logout_page.py", title="Log Out", icon="↩️"
)

# Example Task Pages 
example_start_page = st.Page(
    "example_task/pages/introduction_page.py", title="Introduction", icon="📜", url_path="example_task_introduction"
)
example_qualification_page = st.Page(
    "example_task/pages/qualification_page.py", title="Qualification", icon="🔑"
)
example_annotation_page = st.Page(
    "example_task/pages/annotation_page.py", title="Annotation", icon="🏭"
)

# Explicitation QA Task Pages 
explicitations_qa_start_page = st.Page(
    "explicitations_qa_task/pages/introduction_page.py", title="Introduction", icon="📜", url_path="explicitations_qa_task_introduction"
)
explicitations_qa_qualification_page = st.Page(
    "explicitations_qa_task/pages/qualification_page.py", title="Qualification", icon="🔑"
)
explicitations_qa_annotation_page = st.Page(
    "explicitations_qa_task/pages/annotation_page.py", title="Annotation", icon="🏭"
)


# # Big Ambisentence Task Pages
# big_ambisentence_start_page = st.Page(
#     "big_ambisentence_task/pages/introduction_page.py", title="Ambiguous Writing Intro", icon="❓"
# )
# big_ambisentence_qualification_page = st.Page(
#     "big_ambisentence_task/pages/qualification_page.py", title="Qualification", icon="🔑"
# )
# big_ambisentence_annotation_page = st.Page(
#     "big_ambisentence_task/pages/annotation_page.py", title="Annotation", icon="✏️"
# )

# big_ending_start_page = st.Page(
#     "big_ending_task/pages/introduction_page.py", title="Story Ending Task Intro",  icon="📙", url_path="ending_task_intro" 
# )
# big_ending_qualification_page = st.Page(
#     "big_ending_task/pages/qualification_page.py", title="Qualification", icon="🔑"
# )
# big_ending_annotation_page = st.Page(
#     "big_ending_task/pages/annotation_page.py", title="Annotation", icon="✏️"
# )

# big_ending_round2_start_page = st.Page(
#     "big_ending_task_round2/pages/introduction_page.py", title="Story Ending Task Intro",  icon="📙", url_path="ending_task_intro" 
# )
# big_ending_round2_qualification_page = st.Page(
#     "big_ending_task_round2/pages/qualification_page.py", title="Qualification", icon="🔑"
# )
# big_ending_round2_annotation_page = st.Page(
#     "big_ending_task_round2/pages/annotation_page.py", title="Annotation", icon="✏️"
# )

# big_eval_ending_start_page = st.Page(
#     "big_eval_ending_task/pages/introduction_page.py", title="Story Interpretation Task Intro", icon="📖"
# )
# big_eval_ending_qualification_page = st.Page(
#     "big_eval_ending_task/pages/qualification_page.py", title="Qualification", icon="🔑"
# )
# big_eval_ending_annotation_page = st.Page(
#     "big_eval_ending_task/pages/annotation_page.py", title="Annotation", icon="🏭"
# )


# big_eval_sentence_start_page = st.Page(
#     "big_eval_sentence_task/pages/introduction_page.py", title="Story Interpretation Task Intro", icon="📖"
# )
# big_eval_sentence_qualification_page = st.Page(
#     "big_eval_sentence_task/pages/qualification_page.py", title="Qualification", icon="🔑"
# )
# big_eval_sentence_annotation_page = st.Page(
#     "big_eval_sentence_task/pages/annotation_page.py", title="Annotation", icon="🏭"
# )

# var_ending_test_start_page = st.Page(
#     "var_ending_test/pages/introduction_page.py", title="Story Ending Task Intro",  icon="📙", url_path="ending_task_intro" 
# )
# var_ending_test_qualification_page = st.Page(
#     "var_ending_test/pages/qualification_page.py", title="Qualification", icon="🔑"
# )
# var_ending_test_annotation_page = st.Page(
#     "var_ending_test/pages/annotation_page.py", title="Annotation", icon="✏️"
# )
# var_ending_test_tutorial_page = st.Page(
#     "var_ending_test/pages/tutorial_page.py", title="Tutorial",icon="📖"
# )

# var_ending_test2_start_page = st.Page(
#     "var_ending_test2/pages/introduction_page.py", title="Story Ending Task Intro",  icon="📙", url_path="ending_task_intro" 
# )
# var_ending_test2_qualification_page = st.Page(
#     "var_ending_test2/pages/qualification_page.py", title="Qualification", icon="🔑"
# )
# var_ending_test2_annotation_page = st.Page(
#     "var_ending_test2/pages/annotation_page.py", title="Annotation", icon="✏️"
# )
# var_ending_test2_tutorial_page = st.Page(
#     "var_ending_test2/pages/tutorial_page.py", title="Tutorial",icon="📖"
# )

# var_sentence_task2_start_page = st.Page(
#     "var_sentence_task2/pages/introduction_page.py", title="Ambiguous Writing Task Intro",  icon="📙" 
# )
# var_sentence_task2_qualification_page = st.Page(
#     "var_sentence_task2/pages/qualification_page.py", title="Qualification",  icon="🔑" 
# )
# var_sentence_task2_annotation_page = st.Page(
#     "var_sentence_task2/pages/annotation_page.py", title="Annotation",  icon="✏️" 
# )

# adv_sentence_task_start_page = st.Page(
#     "adv_sentence_task/pages/introduction_page.py", title="Ambiguous Writing Task Intro",  icon="📙" 
# )
# adv_sentence_task_qualification_page = st.Page(
#     "adv_sentence_task/pages/qualification_page.py", title="Qualification",  icon="🔑" 
# )
# adv_sentence_task_annotation_page = st.Page(
#     "adv_sentence_task/pages/annotation_page.py", title="Annotation",  icon="✏️" 
# )

# adv_ending_task_start_page = st.Page(
#     "adv_ending_task/pages/introduction_page.py", title="Story Ending Task Intro",  icon="📙", url_path="ending_task_intro" 
# )
# adv_ending_task_qualification_page = st.Page(
#     "adv_ending_task/pages/qualification_page.py", title="Qualification", icon="🔑"
# )
# adv_ending_task_annotation_page = st.Page(
#     "adv_ending_task/pages/annotation_page.py", title="Annotation", icon="✏️"
# )
# adv_ending_task_tutorial_page = st.Page(
#     "adv_ending_task/pages/tutorial_page.py", title="Tutorial",icon="📖"
# )

# adv_ending_task2_start_page = st.Page(
#     "adv_ending_task2/pages/introduction_page.py", title="Story Ending Task Intro",  icon="📙", url_path="ending_task_intro" 
# )
# adv_ending_task2_qualification_page = st.Page(
#     "adv_ending_task2/pages/qualification_page.py", title="Qualification", icon="🔑"
# )
# adv_ending_task2_annotation_page = st.Page(
#     "adv_ending_task2/pages/annotation_page.py", title="Annotation", icon="✏️"
# )
# adv_ending_task2_tutorial_page = st.Page(
#     "adv_ending_task2/pages/tutorial_page.py", title="Tutorial",icon="📖"
# )


# adv_ending_task3_start_page = st.Page(
#     "adv_ending_task3/pages/introduction_page.py", title="Story Ending Task Intro",  icon="📙", url_path="ending_task_intro" 
# )
# adv_ending_task3_qualification_page = st.Page(
#     "adv_ending_task3/pages/qualification_page.py", title="Qualification", icon="🔑"
# )
# adv_ending_task3_annotation_page = st.Page(
#     "adv_ending_task3/pages/annotation_page.py", title="Annotation", icon="✏️"
# )
# adv_ending_task3_tutorial_page = st.Page(
#     "adv_ending_task3/pages/tutorial_page.py", title="Tutorial",icon="📖"
# )

# adv_ending_task4_start_page = st.Page(
#     "adv_ending_task4/pages/introduction_page.py", title="Story Ending Task Intro",  icon="📙", url_path="ending_task_intro" 
# )
# adv_ending_task4_qualification_page = st.Page(
#     "adv_ending_task4/pages/qualification_page.py", title="Qualification", icon="🔑"
# )
# adv_ending_task4_annotation_page = st.Page(
#     "adv_ending_task4/pages/annotation_page.py", title="Annotation", icon="✏️"
# )
# adv_ending_task4_tutorial_page = st.Page(
#     "adv_ending_task4/pages/tutorial_page.py", title="Tutorial",icon="📖"
# )

# expertise_task_annotation_page = st.Page(
#     "expertise_task/pages/annotation_page.py", title="Term Familarity Task", icon="📙"
# )
# expertise_task2_annotation_page = st.Page(
#     "expertise_task2/pages/annotation_page.py", title="Main Study", icon="📙"
# )
# expertise_task2_qualification_page = st.Page(
#     "expertise_task2/pages/qualification_page.py", title="Qualification Test", icon="🔑"
# )

# adv_eval_ending_start_page = st.Page(
#     "adv_eval_ending_task/pages/introduction_page.py", title="Introduction",  icon="📙"
# )
# adv_eval_ending_qualification1_page = st.Page(
#     "adv_eval_ending_task/pages/qualification_page.py", title="Qualification (Part 1)", icon="🔑"
# )

# adv_eval_ending_qualification2_page = st.Page(
#     "adv_eval_ending_task/pages/expertise_qualification_page.py", title="Qualification (Part 2)", icon="🔑"
# )

# adv_eval_ending_annotation1_page = st.Page(
#     "adv_eval_ending_task/pages/annotation_page.py", title="Main Study Part 1: Plausibility", icon="✏️"
# )

# adv_eval_ending_annotation2_page = st.Page(
#     "adv_eval_ending_task/pages/expertise_page.py", title="Main Study Part 2: Connection", icon="✏️"
# )





# adv_eval_ending2_start_page = st.Page(
#     "adv_eval_ending_task2/pages/introduction_page.py", title="Introduction",  icon="📙"
# )
# adv_eval_ending2_qualification1_page = st.Page(
#     "adv_eval_ending_task2/pages/qualification_page.py", title="Qualification (Part 1)", icon="🔑"
# )

# adv_eval_ending2_qualification2_page = st.Page(
#     "adv_eval_ending_task2/pages/expertise_qualification_page.py", title="Qualification (Part 2)", icon="🔑"
# )

# adv_eval_ending2_annotation1_page = st.Page(
#     "adv_eval_ending_task2/pages/annotation_page.py", title="Main Study Part 1: Plausibility", icon="✏️"
# )

# adv_eval_ending2_annotation2_page = st.Page(
#     "adv_eval_ending_task2/pages/expertise_page.py", title="Main Study Part 2: Connection", icon="✏️"
# )


# span_task_start_page = st.Page(
#     "span_task/pages/introduction_page.py", title="Ambiguous Writing Task Intro",  icon="📙" 
# )
# span_task_qualification_page = st.Page(
#     "span_task/pages/qualification_page.py", title="Qualification",  icon="🔑" 
# )
# span_task_annotation_page = st.Page(
#     "span_task/pages/annotation_page.py", title="Annotation",  icon="✏️" 
# )


# Create navigation bar

if st.session_state.user_id == "admin":
    pg = st.navigation(
        {
            "Home": [main_page, admin_page, logout_page],
        }
    )
elif st.session_state.user_id:
    available_pages = {
        "Home": [main_page]
    }

    if utils.authenticate_id("example_task", st.session_state.user_id):
         available_pages["Example Task"] = [example_start_page, example_qualification_page, example_annotation_page]

    if utils.authenticate_id("explicitations_qa_task", st.session_state.user_id):
             available_pages["Explicitations QA Task"] = [explicitations_qa_start_page, explicitations_qa_qualification_page, explicitations_qa_annotation_page]

    # if utils.authenticate_id("big_ambisentence_task", st.session_state.user_id):
    #     available_pages["Ambiguous Sentence Task"] = [big_ambisentence_start_page, big_ambisentence_qualification_page, big_ambisentence_annotation_page]

    # elif utils.authenticate_id("var_sentence_task2", st.session_state.user_id):
    #     available_pages["Ambiguous Sentence Task"] = [var_sentence_task2_start_page, var_sentence_task2_qualification_page, var_sentence_task2_annotation_page]

    # elif utils.authenticate_id("big_ending_task", st.session_state.user_id):
    #     available_pages["Story Ending Task"] = [big_ending_start_page, big_ending_qualification_page, big_ending_annotation_page]

    # elif utils.authenticate_id("big_ending_task_round2", st.session_state.user_id):
    #     available_pages["Story Ending Task"] = [big_ending_round2_start_page, big_ending_round2_qualification_page, big_ending_round2_annotation_page]

    # elif utils.authenticate_id("var_ending_test", st.session_state.user_id):
    #     available_pages["Story Building Task"] = [var_ending_test_qualification_page, var_ending_test_tutorial_page, var_ending_test_annotation_page]

    # elif utils.authenticate_id("var_ending_test2", st.session_state.user_id):
    #     available_pages["Story Building Task"] = [var_ending_test2_qualification_page, var_ending_test2_tutorial_page, var_ending_test2_annotation_page]

    # elif utils.authenticate_id("adv_ending_task", st.session_state.user_id):
    #     available_pages["Story Building Task"] = [adv_ending_task_qualification_page, adv_ending_task_tutorial_page, adv_ending_task_annotation_page]

    # elif utils.authenticate_id("adv_ending_task2", st.session_state.user_id):
    #     available_pages["Story Building Task"] = [adv_ending_task2_qualification_page, adv_ending_task2_tutorial_page, adv_ending_task2_annotation_page]

    # elif utils.authenticate_id("adv_ending_task2", st.session_state.user_id):
    #     available_pages["Story Building Task"] = [adv_ending_task2_qualification_page, adv_ending_task2_tutorial_page, adv_ending_task2_annotation_page]

    # elif utils.authenticate_id("adv_ending_task3", st.session_state.user_id):
    #     available_pages["Story Building Task"] = [adv_ending_task3_qualification_page, adv_ending_task3_tutorial_page, adv_ending_task3_annotation_page]

    # elif utils.authenticate_id("adv_ending_task4", st.session_state.user_id):
    #     available_pages["Story Building Task"] = [adv_ending_task4_qualification_page, adv_ending_task4_tutorial_page, adv_ending_task4_annotation_page]



    # elif utils.authenticate_id("big_eval_ending_task", st.session_state.user_id):
    #     if user_repository.get_qualification() != 1:
    #         available_pages["Story Interpretation Task"] = [big_eval_ending_start_page, big_eval_ending_qualification_page]
    #     else:
    #         available_pages["Story Interpretation Task"] = [big_eval_ending_start_page, big_eval_ending_qualification_page, big_eval_ending_annotation_page]

    # elif utils.authenticate_id("big_eval_sentence_task", st.session_state.user_id):
    #     if user_repository.get_qualification() != 1:
    #         available_pages["Sentence Interpretation Task"] = [big_eval_sentence_start_page,
    #                                                         big_eval_sentence_qualification_page]
    #     else:
    #         available_pages["Sentence Interpretation Task"] = [big_eval_sentence_start_page,
    #                                                         big_eval_sentence_qualification_page,
    #                                                         big_eval_sentence_annotation_page]

    # elif utils.authenticate_id("adv_sentence_task", st.session_state.user_id):
    #     available_pages["Ambiguous Sentence Task"] = [adv_sentence_task_start_page, adv_sentence_task_qualification_page, adv_sentence_task_annotation_page]

    # elif utils.authenticate_id("expertise_task", st.session_state.user_id):
    #     available_pages["Term Familiarity Task"] = [expertise_task_annotation_page]


    # elif utils.authenticate_id("expertise_task2", st.session_state.user_id):
    #     available_pages["Term Familiarity Task"] = [expertise_task2_qualification_page, expertise_task2_annotation_page]

    # elif utils.authenticate_id("adv_eval_ending_task", st.session_state.user_id):
    #     available_pages["Plausibility+Connection Task"] = [adv_eval_ending_start_page, adv_eval_ending_qualification1_page, adv_eval_ending_qualification2_page, 
    #                                                        adv_eval_ending_annotation1_page, adv_eval_ending_annotation2_page]

    # elif utils.authenticate_id("adv_eval_ending_task2", st.session_state.user_id):
    #     available_pages["Plausibility+Connection Task"] = [adv_eval_ending2_start_page, adv_eval_ending2_qualification1_page, adv_eval_ending2_qualification2_page, 
    #                                                        adv_eval_ending2_annotation1_page, adv_eval_ending2_annotation2_page]

    # elif utils.authenticate_id("span_task", st.session_state.user_id):
    #     available_pages["Ambiguity Explanation Task"] = [span_task_qualification_page, span_task_annotation_page]


    available_pages["Other"] = [logout_page]

    pg = st.navigation(available_pages)

else:
    pg = st.navigation(
        {
        "Home": [main_page, authentication_page],
        #"Task Previews": [adv_sentence_task_start_page]
        }
    )

try:
    pg.run()
except (psycopg2.InterfaceError, psycopg2.OperationalError) as e:
    st.markdown("# Your session was cancelled, likely due to prolonged inactivity. Please log out, then log in again.")
    print(e)