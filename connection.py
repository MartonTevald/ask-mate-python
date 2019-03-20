import csv


def get_csv_data(filename):
    data = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(dict(row))
        return data


def write_to_file(filename, DATA_HEADER, dictionary):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        writer.writerow(dictionary)


def update_in_question_file(filename, DATA_HEADER, dictionary, id):
    data = get_csv_data(filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        for elem in data:
            if elem[0] == str(id):
                writer.writerow(dictionary)
            else:
                csv.writer(csvfile).writerow(elem)


def update_in_answer_file(filename, DATA_HEADER, dictionary, id):
    data = get_csv_data(filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        for elem in data:
            if elem[3] == str(id):
                writer.writerow(dictionary)
            else:
                csv.writer(csvfile).writerow(elem)
