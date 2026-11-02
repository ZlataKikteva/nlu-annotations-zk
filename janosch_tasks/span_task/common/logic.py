from core.scripts.utils import read_json_from_file, TASK_INFO

def check_if_qualified(annotations: dict) -> bool:
    """
    Check if the given annotations (from a user's annotation field) would pass the qualification test.

    :param annotations: user's annotation in dict form, should have a 'qualification' key
    :return bool: True if passed, False if not
    """
    qualification_questions = read_json_from_file(TASK_INFO["span_task"]["qualification_filepath"])

    needed_score = 0  # todo: wanna see what everyone picks for qualification for now
    score = 0
    #for question_id in qualification_questions:
    #    if annotations["qualification"][int(question_id)-1]["slider"] in qualification_questions[question_id]["correct_answer"]:
    #        score += 1

    return score >= needed_score