import connection


def get_all_details(filename):
    return connection.get_csv_data(filename)


def get_all_questions():
    return connection.get_csv_data('question.csv')


def write_to_file(filename, dictionary):
    return connection.write_to_file(filename, dictionary)

# def get_all_user_question(filename):
#     datas = get_csv_questions()
#     return datas
#
#
# def get_user_question(question_id):
#     return get_csv_questions(question_id)
#
#
# def get_next_id():
#     return uuid.uuid1()
#
#
# def get_csv_questions(question_id=None):
#     questions = []
#     with open('question.csv', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             question = dict(row)
#             # if its already filled return the filled one
#             if question_id is not None and question_id == question['id']:
#                 return question
#             questions.append(question)
#     return questions
#
#
# def add_user_question(question):
#     question['id'] = get_next_id()
#     add_user_question_to_file(question, True)
#
#
# def update_user_question(question):
#     add_user_question_to_file(question, False)
#
#
# def add_user_question_to_file(question, adding_new_question=True):
#     existing_data = get_all_user_question('question.csv')
#     with open('question.csv', 'a', newline='', encoding='utf-8') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=question_header)
#         for row in existing_data:
#             # If its update , just overwrite .
#             if not adding_new_question:
#                 if row['id'] == question['id']:
#                     row = question
#             writer.writerow(row)
#         if adding_new_question:
#             writer.writerow(question)
