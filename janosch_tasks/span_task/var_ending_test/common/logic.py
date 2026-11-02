from core.scripts.utils import read_json_from_file, TASK_INFO

def check_if_qualified(annotations: dict) -> bool:
    """
    Check if the given annotations (from a user's annotation field) would pass the qualification test.

    :param annotations: user's annotation in dict form, should have a 'qualification' key
    :return bool: True if passed, False if not
    """
    qualification_questions = read_json_from_file(TASK_INFO["var_ending_test"]["qualification_filepath"])

    needed_score = 8
    score = 0
    for question_id in qualification_questions:
        if qualification_questions[question_id]["correct_answer"][0] == annotations["qualification"][int(question_id)-1]["meaning1"]:
            score += 1
        if qualification_questions[question_id]["correct_answer"][1] == annotations["qualification"][int(question_id)-1]["meaning2"]:
            score += 1
    return score >= needed_score