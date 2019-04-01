import connection
import time
from datetime import datetime


@connection.connection_handler
def get_all_details(cursor):
    cursor.execute("""SELECT * FROM question;""")
    questions = cursor.fetchall()
    return questions


def date_time():
    dt = datetime.now()
    return dt


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

# def sort_ascending(filename, sort_by):
#     data = connection.get_csv_data(filename)
#     for values in data:
#         values['id'] = int(values['id'])
#         values['view_number'] = int(values['view_number'])
#         values['vote_number'] = int(values['vote_number'])
#     if sort_by == 'title':
#         return sorted(data, key=lambda k: k['title'])
#     if sort_by == sort_by:
#         return sorted(data, key=lambda k: k[sort_by], reverse=True)
#
