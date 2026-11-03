import datetime
import os
import json
import sqlite3

import streamlit as st

from core.scripts.database_repository import db_connection

# Check if user exists in the database
def get_user(user_id: str):
    """
    Get a user from any task by user id.
    Returns None if no user found.

    :param user_id: ID-string of user
    :return: User or None
    """
    conn = st.session_state.conn
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data WHERE user_id=%s", (user_id,))
    user = cursor.fetchone()
    # conn.close()
    return user

def create_user(user_id: str, task: str = "example_task", data: dict = {}):
    """
    Creates a user with the specified user id.

    :param user_id: ID-string of user
    :param task:
    :param data: optional user metadata dict
    :return: None
    """
    conn = st.session_state.conn
    cursor = conn.cursor()

    # find annotator group
    cursor.execute("SELECT * from valid_ids WHERE user_id=%s", (user_id,))
    id_data = cursor.fetchone()
    annotator_group = id_data[2]

    data = json.dumps(data)

    cursor.execute("""
        INSERT INTO user_data (user_id, task, annotator_group, data)
        VALUES (%s, %s, %s, %s)
    """, (user_id, task, annotator_group, data))
    
    conn.commit()  # Commit changes to the database
    # conn.close()

def add_log(user_id: str, text: str):
    """
    Add the entry to the log of the given user id. The current time is also appended to the log.

    :param user_id:
    :param text: Whatever you want to log
    """
    user = get_user(user_id)

    logs = user[6]["log"]
    logs.append(text + "|" + str(datetime.datetime.now()))

    new_data = user[6]
    user[6]["log"] = logs

    new_data_str = json.dumps(new_data)

    conn = st.session_state.conn
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE user_data
        SET data = %s
        WHERE user_id = %s
    """, (new_data_str, user_id))
    st.session_state.user[6] = new_data_str
    conn.commit()


def save_one_annotation(user_id: str, key: str, question_index: int, question_annotation: dict):
    """
    Save one annotation for a sample to the database.
    
    :param user_id:
    :param key: The subcategory of sample, e.g. qualification or main
    :param question_index: At what index to save the annotation, e.g. 3 for the 3rd sample
    :param question_annotation: The annotation to save, which is a dict.
    """
    conn = st.session_state.conn
    cursor = conn.cursor()

    user = st.session_state.user

    annotations = user[5]

    if key not in annotations:
        annotations[key] = []

    # for new annotations, extend the saved annotation list to fit the new annotation at the proper spot.
    while len(annotations[key]) < question_index:
        annotations[key].append({})

    annotations[key][question_index - 1] = question_annotation
    annotations_json = json.dumps(annotations)
    cursor.execute("""
        UPDATE user_data
        SET annotations = %s
        WHERE user_id = %s
    """, (annotations_json, user_id))
    st.session_state.user[5] = annotations
    conn.commit()
    #conn.close()

def get_qualification() -> int:
    """
    Check if the user with the given id passed a qualification test.

    :param user_id: id-string of user
    :return: -1 if failed, 0 if no qualification, 1 if passed
    """
    qualified = st.session_state.user[2]
    return qualified


def get_checkpoint(key, print=True) -> int:
    """
    Find the last annotation that was being worked on for the given key (e.g. "qualification").
    Assumes that the samples are sorted. Return the highest index.
    """
    annotations = st.session_state.user[5]

    if key not in annotations:  # Did not even start the task, lead to first sample
        return 0
    
    if print:
        st.write("Returning to checkpoint from previous session")
    return len(annotations[key])

def reset_annotation(user_id: str, key: str):
    """
    Reset the user's annotation given a task key (like qualification or annotation)
    
    :param user_id:
    :param key: The key of the annotation data to delete, e.g. qualification
    """
    conn = st.session_state.conn
    cursor = conn.cursor()

    user = get_user(user_id)
    annotations = user[5]

    if key not in annotations:
        return
    del annotations[key]

    annotations_json = json.dumps(annotations)
    cursor.execute("""
        UPDATE user_data
        SET annotations = %s
        WHERE user_id = %s
    """, (annotations_json, user_id))
    conn.commit()
    # conn.close()

def set_qualification(user_id: str, setting: int=1):
    """
    Change the user's qualification setting.
    -1 = unqualified
    0 = not yet qualified
    1 = qualified

    :param user_id: 
    """
    conn = st.session_state.conn
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user_data
        SET qualified = %s
        WHERE user_id = %s
    """, (setting, user_id,))
    conn.commit()
    # conn.close()
    
    if st.session_state.user_id == "admin":
        st.write("Qualification updated.")
    else:
        st.session_state.user[2] = setting

def assign_to_weakest_group(user_id: str, task: str):
    """
    Assign the user to the group that currently has the least amount of members.
    Test accounts and unqualified accounts do not count towards the numbers.
    Lower indices are prioritized.
    Typically to be used after qualification.

    :param user_id: user string
    :param task: task string
    """
    from core.scripts.utils import TASK_INFO  # probably not great to have utils importing from each other...

    conn = st.session_state.conn
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM user_data
    """)
    users = cursor.fetchall()

    group_counts = {}
    for i in range(TASK_INFO[task]["number_of_annotator_groups"]):
        group_counts[i] = 0

    for user in users:
        u_id, user_task, qualified, group, progress, _, data = user
        if (user_task != task) or (qualified < 1) or (u_id == user_id):
            continue
        if "test" in data["prolific_id"].lower():
            continue
        group_counts[group] += 1

    weakest_group = min(group_counts, key = group_counts.get)

    if task == "eval_ending_task":
        # I have gotten to a point where I really only need group 1 anymore.
        weakest_group = 1

    print(task, group_counts, weakest_group)

    cursor.execute("""
        UPDATE user_data
        SET annotator_group = %s
        WHERE user_id = %s
    """, (weakest_group, user_id))
    st.session_state.user[3] = weakest_group
    conn.commit()

def mark_as_done(user_id):
    conn = st.session_state.conn
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user_data
        SET progress = -1
        WHERE user_id = %s
    """, (user_id,))
    conn.commit()
    st.session_state.user[4] = -1
    # conn.close()
    print("User ", user_id, " finished annotation!")

def check_if_done(user_id):
    if st.session_state.user[4] == -1:
        return True

def fetch_user_data():
    """
    DEBUG function.
    Fetch and display all rows from the user_data table.
    not used or tested currently
    """
    conn = st.session_state.conn
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    rows = cursor.fetchall()
    for row in rows:
        user_id, task, qualified, annotator_group, progress, annotations, data = row
        st.write(f"User ID: {user_id}, Qualified: {qualified}, Task: {task} Progress: {progress}, Annotations: {annotations}")
    # conn.close()

def fetch_task_annotations(task="adv_sentence_task"):
    """
    Fetch all non-qualification non-debug test annotations for the current task
    """
    conn = st.session_state.conn
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data WHERE task = %s AND NOT (data->>'prolific_id' ILIKE '%%test%%');", (task,))
    rows = cursor.fetchall()
    all_annotations = []
    for row in rows:
        user_id, task, qualified, annotator_group, progress, annotations, data = row
        if "annotation" in annotations:
            all_annotations += annotations["annotation"]
    return all_annotations