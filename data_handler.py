import connection
import time
from datetime import datetime
from operator import itemgetter

question_header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_header = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_details(filename):
    return connection.get_csv_data(filename)


def write_to_file(filename, dictionary):
    return connection.write_to_file(filename, question_header, dictionary)


def write_to_answer_file(filename, dictionary):
    return connection.write_to_file(filename, answer_header, dictionary)


def get_id(filename):
    existing_data = get_all_details(filename)
    if len(existing_data) == 0:
        return '1'
    return str(int(existing_data[-1]['id']) + 1)


def date_time():
    return int(time.time())


def convert_unix_to_time(submission_time):
    # return datetime.fromtimestamp(submission_time)
    return datetime.utcfromtimestamp(submission_time).strftime('%Y-%m-%d|%H:%M')


def get_question_for_id(filename, id):
    data = connection.get_csv_data(filename)
    for row in data:
        if id == row['id']:
            return row


def get_answer_for_vote(answer_id):
    data = connection.get_csv_data('answer.csv')
    for row in data:
        if row['id'] == answer_id:
            return row


def get_answers_for_id(filename, id):
    data = connection.get_csv_data(filename)
    answer = []
    for row in data:
        if id == row['question_id']:
            answer.append(row)
    return answer


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

def vote_up_(filename):
    # data = open(filename)
    # for elem in data:
    #     elem['vote_number'] = elem['vote_number'] + str(1)
    pass
