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


'''
def write_to_file(filename, DATA_HEADER):
    data = get_csv_data(filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        for row in data:
            writer.writerow(row)
# ez még nincs kész
'''