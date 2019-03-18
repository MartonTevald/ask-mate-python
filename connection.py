import csv


def get_csv_data(filename):
    data = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(dict(row))
        return data


def add_user_story_to_file(filename, DATA_HEADER):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        for row in writer:
            writer.writerow(row)
