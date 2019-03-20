import connection
import time
from datetime import datetime

question_header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_all_details(filename):
    return connection.get_csv_data(filename)


def write_to_file(filename, dictionary):
    return connection.write_to_file(filename, question_header, dictionary)


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
    return datetime.utcfromtimestamp(submission_time).strftime('%Y-%m-%d|%H:%M')
