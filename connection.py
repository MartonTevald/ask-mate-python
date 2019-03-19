import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
question_header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_csv_data(filename):
    with open(filename) as csvfile:
        data = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
        return data


def write_to_file(filename, dictionary):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=question_header)
        writer.writerow(dictionary)
