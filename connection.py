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
        writer.writeheader()
        for elem in data:
            if elem['id'] == id:
                writer.writerow(dictionary)
            else:
                writer.writerow(elem)


def update_in_answer_file(filename, DATA_HEADER, dictionary, id):
    data = get_csv_data(filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        writer.writeheader()
        for elem in data:
            if elem['question_id'] == id:
                writer.writerow(dictionary)
            else:
                writer.writerow(elem)

# these need fixing:
def delete_in_question_file(filename, id):
    data = get_csv_data(filename) # was originally getting a nested list, but now we have dicts
    with open(filename, 'w', newline='') as csvfile:
        for elem in data:
            if elem['id'] == str(id):
                continue
            else:
                csv.writer(csvfile).writerow(elem)


def delete_in_answer_file(filename, id):
    data = get_csv_data(filename)
    with open(filename, 'w', newline='') as csvfile:
        for elem in data:
            if elem['question_id'] == str(id):
                continue
            else:
                csv.writer(csvfile).writerow(elem)
