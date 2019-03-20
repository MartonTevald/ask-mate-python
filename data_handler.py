import connection
import time
from datetime import datetime

question_header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_header = ['id','submission_time','vote_number','question_id','message','image']


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
    # unix_time = int(time.time())
    # return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d|%H:%M')
    return int(time.time())


def convert_unix_to_time(submission_time):
    return datetime.fromtimestamp(submission_time)
    # return datetime.utcfromtimestamp(submission_time).strftime('%Y-%m-%d|%H:%M')


def get_question_for_id(filename, id):
    data = connection.get_csv_data(filename)
    for row in data:
        if id == row['id']:
            return row


def get_answers_for_id(filename, id):
    data = connection.get_csv_data(filename)
    answer = []
    for row in data:
        if id == row['question_id']:
            answer.append(row)
    return answer


def edit_question_row(filename, dictionary, id):
    return connection.update_in_question_file(filename, question_header, dictionary, id)


def edit_answer_row(filename, dictionary, id):
    return connection.update_in_answer_file(filename, answer_header, dictionary, id)


def del_question_row(filename, id):
    return connection.delete_in_question_file(filename, question_header, id)


def del_answer_row(filename, id):
    return connection.update_in_answer_file(filename, answer_header, id)
