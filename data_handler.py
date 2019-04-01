import connection
import time
from datetime import datetime
from operator import itemgetter


# question_header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
# answer_header = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']

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


#
# def get_answer_for_vote(answer_id):
#     data = connection.get_csv_data('answer.csv')
#     for row in data:
#         if row['id'] == answer_id:
#             return row


@connection.connection_handler
def get_question_id_for_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer 
                    WHERE id = %(answer_id)s""",
                   {'answer_id': int(answer_id)})
    question_id = cursor.fetchone()
    return question_id


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

#
# def edit_answer_row(filename, dictionary, id):
#     return connection.update_in_answer_file(filename, answer_header, dictionary, id)
#
#
# def edit_question_row(filename, dictionary, id):
#     return connection.update_in_question_file(filename, question_header, dictionary, id)
#
#
# def edit_answer_id(filename, dictionary, answer_id):
#     return connection.update_id_in_answer_file(filename, answer_header, dictionary, answer_id)
#
#
# def del_answer_row(filename, id):
#     return connection.delete_in_answer_file(filename, answer_header, id)

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
