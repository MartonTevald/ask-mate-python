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


def update_id_in_answer_file(filename, DATA_HEADER, dictionary, id):
    data = get_csv_data(filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        writer.writeheader()
        for elem in data:
            if elem['id'] == id:
                writer.writerow(dictionary)
            else:
                writer.writerow(elem)



def delete_in_question_file(filename, DATA_HEADER, id):
    data = get_csv_data(filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        writer.writeheader()
        for elem in data:
            if elem.get('id') == id:
                continue
            writer.writerow(elem)


def delete_in_answer_file(filename, DATA_HEADER, id):
    data = get_csv_data(filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        writer.writeheader()
        for elem in data:
            if elem.get('question_id') == id:
                continue
            writer.writerow(elem)


def delete_in_answer_by_id(filename, DATA_HEADER, id):
    data = get_csv_data(filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        writer.writeheader()
        for elem in data:
            if elem.get('id') == id:
                continue
            writer.writerow(elem)


def write_plus_one_to_visit_question():
    pass




