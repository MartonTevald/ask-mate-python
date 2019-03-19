import connection

question_header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_all_details(filename):
    return connection.get_csv_data(filename)


def write_to_file(filename, dictionary):
    return connection.write_to_file(filename, question_header, dictionary)


def get_id(filename):
    return connection.get_csv_data(filename)[-1]['id']
