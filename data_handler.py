import connection
import time
from datetime import datetime


@connection.connection_handler
def get_first_five_question(cursor):
    cursor.execute("""SELECT * FROM question ORDER BY submission_time DESC 
                        LIMIT 5 OFFSET 0""")
    question = cursor.fetchall()
    return question


@connection.connection_handler
def get_all_details(cursor):
    cursor.execute("""SELECT * FROM question;""")
    questions = cursor.fetchall()
    return questions


def date_time():
    dt = datetime.now()
    date = dt.strftime('%Y-%m-%dT%H:%M:%S')
    return date


@connection.connection_handler
def add_new_question(cursor, new_data):
    cursor.execute("""INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s)"""
                   , {'submission_time': new_data['submission_time'],
                      'view_number': new_data['view_number'], 'vote_number': new_data['vote_number'],
                      'title': new_data['title'], 'message': new_data['message'], 'image': new_data['image']})


@connection.connection_handler
def add_new_answer(cursor, new_data):
    cursor.execute("""INSERT INTO answer (submission_time,question_id,vote_number, message,image)
                    VALUES (%(submission_time)s,%(question_id)s,%(vote_number)s,%(message)s,%(image)s)"""
                   , {'submission_time': new_data['submission_time'], 'question_id': new_data['question_id'],
                      'vote_number': new_data['vote_number'],
                      'message': new_data['message'], 'image': new_data['image']})


@connection.connection_handler
def get_question_for_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(id)s """,
                   {'id': id})
    question = cursor.fetchall()
    return question


@connection.connection_handler
def get_answers_for_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(id)s""",
                   {'id': id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_question_id_for_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer 
                    WHERE id = %(answer_id)s""",
                   {'answer_id': int(answer_id)})
    question_id = cursor.fetchall()
    return question_id[0].get('question_id')


@connection.connection_handler
def del_question_row(cursor, id):
    cursor.execute("""
                DELETE FROM answer
                WHERE question_id = %(id)s;
                DELETE FROM question
                WHERE id = %(id)s""",
                   {'id': id})


@connection.connection_handler
def answer_delete_by_id(cursor, id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(id)s""",
                   {'id': id})


@connection.connection_handler
def question_view_number_counter(cursor, id):
    cursor.execute("""
                UPDATE question
                SET view_number = view_number +1
                WHERE id = %(id)s""", {'id': id})


@connection.connection_handler
def question_vote_up(cursor, id):
    cursor.execute("""
                UPDATE question
                SET vote_number = vote_number +1
                WHERE id = %(id)s""", {'id': id})


@connection.connection_handler
def question_vote_down(cursor, id):
    cursor.execute("""
                UPDATE  question
                SET  vote_number = vote_number -1
                WHERE id= %(id)s""", {'id': id})


@connection.connection_handler
def answer_vote_up(cursor, id):
    cursor.execute("""
                UPDATE answer
                SET vote_number = vote_number +1
                WHERE id = %(id)s""", {'id': id})


@connection.connection_handler
def answer_vote_down(cursor, id):
    cursor.execute("""
                UPDATE answer
                SET vote_number = vote_number -1
                WHERE id = %(id)s""", {'id': id})


@connection.connection_handler
def add_new_comment(cursor, new_data):
    cursor.execute("""INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                    VALUES (%(question_id)s,%(answer_id)s,%(message)s,%(submission_time)s,%(edited_count)s)"""
                   , {'question_id': new_data['question_id'],
                      'answer_id': new_data['answer_id'],
                      'message': new_data['message'],
                      'submission_time': new_data['submission_time'],
                      'edited_count': new_data['edited_count']})


# @connection.connection_handler
# def sort_time_ascending(cursor):
#     cursor.execute("""
#                 SELECT *
#                 FROM question
#                 ORDER BY submission_time ASC """)
#     sub_asc = cursor.fetchall()
#     return sub_asc
#
#
# @connection.connection_handler
# def sort_time_descending(cursor):
#     cursor.execute("""
#                 SELECT *
#                 FROM question
#                 ORDER BY submission_time DESC """)
#     sub_desc = cursor.fetchall()
#     return sub_desc


@connection.connection_handler
def sort_ascending(cursor, sort_by):
    if sort_by == 'submission_time':
        cursor.execute("""
                        SELECT * FROM question ORDER BY submission_time""")
        asc = cursor.fetchall()
        if asc == asc:
            cursor.execute("""
                                    SELECT * FROM question ORDER BY submission_time DESC""")
            desc = cursor.fetchall()
            return desc
        else:
            return asc
    elif sort_by == 'title':
        cursor.execute("""
                        SELECT * FROM question ORDER BY title""")
        order = cursor.fetchall()
        return order
    elif sort_by == 'view_number':
        cursor.execute("""
                        SELECT * FROM question ORDER BY view_number""")
        order = cursor.fetchall()
        return order
    elif sort_by == 'vote_number':
        cursor.execute("""
                        SELECT * FROM question ORDER BY vote_number""")
        order = cursor.fetchall()
        return order
