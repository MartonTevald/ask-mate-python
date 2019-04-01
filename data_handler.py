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


# def write_to_file(filename, dictionary):
#     return connection.write_to_file(filename, question_header, dictionary)
#
#
# def write_to_answer_file(filename, dictionary):
#     return connection.write_to_file(filename, answer_header, dictionary)

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


def get_answer_for_vote(answer_id):
    data = connection.get_csv_data('answer.csv')
    for row in data:
        if row['id'] == answer_id:
            return row


def get_question_id_for_answer_id(filename, answer_id):
    data = connection.get_csv_data(filename)
    for row in data:
        if answer_id == row['id']:
            return row['question_id']


def edit_question_row(filename, dictionary, id):
    return connection.update_in_question_file(filename, question_header, dictionary, id)


def edit_answer_row(filename, dictionary, id):
    return connection.update_in_answer_file(filename, answer_header, dictionary, id)


def edit_answer_id(filename, dictionary, answer_id):
    return connection.update_id_in_answer_file(filename, answer_header, dictionary, answer_id)


def del_question_row(filename, id):
    return connection.delete_in_question_file(filename, question_header, id)


def del_answer_row(filename, id):
    return connection.delete_in_answer_file(filename, answer_header, id)


def answer_delete_by_id(filename, id):
    return connection.delete_in_answer_by_id(filename, answer_header, id)

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
