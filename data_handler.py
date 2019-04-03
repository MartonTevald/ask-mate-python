import connection
import time
from datetime import datetime


@connection.connection_handler
def get_first_five_question(cursor):
    cursor.execute("""SELECT * FROM question ORDER BY submission_time DESC 
                        LIMIT 5 OFFSET 0""")
    question = cursor.fetchall()
    return question


@connection.connection_handler
def get_all_details(cursor):
    cursor.execute("""SELECT * FROM question;""")
    questions = cursor.fetchall()
    return questions


def date_time():
    dt = datetime.now()
    date = dt.strftime('%Y-%m-%d %H:%M:%S')
    return date


@connection.connection_handler
def edit_answer_row(cursor, new_data, id):
    cursor.execute("""UPDATE answer
                    SET submission_time= %(submission_time)s,
                    message = %(message)s,
                    image = %(image)s
                    WHERE id = %(id)s """
                   , {'id': id, 'submission_time': new_data['submission_time'],
                      'message': new_data['message'], 'image': new_data['image']})


@connection.connection_handler
def edit_question_row(cursor, new_data, id):
    cursor.execute("""UPDATE question
                    SET submission_time= %(submission_time)s,
                    view_number= view_number,
                    vote_number= vote_number,
                    title= %(title)s,
                    message= %(message)s,
                    image= %(image)s
                    WHERE id= %(id)s"""
                   , {'id': id, 'submission_time': new_data['submission_time'],
                      'view_number': new_data['view_number'], 'vote_number': new_data['vote_number'],
                      'title': new_data['title'], 'message': new_data['message'], 'image': new_data['image']})


@connection.connection_handler
def add_new_question(cursor, new_data):
    cursor.execute("""INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s)"""
                   , {'submission_time': new_data['submission_time'],
                      'view_number': new_data['view_number'], 'vote_number': new_data['vote_number'],
                      'title': new_data['title'], 'message': new_data['message'], 'image': new_data['image']})


@connection.connection_handler
def add_new_answer(cursor, new_data):
    cursor.execute("""INSERT INTO answer (submission_time,question_id,vote_number, message,image)
                    VALUES (%(submission_time)s,%(question_id)s,%(vote_number)s,%(message)s,%(image)s)"""
                   , {'submission_time': new_data['submission_time'], 'question_id': new_data['question_id'],
                      'vote_number': new_data['vote_number'],
                      'message': new_data['message'], 'image': new_data['image']})


@connection.connection_handler
def get_question_for_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(id)s """,
                   {'id': id})
    question = cursor.fetchall()
    return question


@connection.connection_handler
def get_answers_id_for_edit(cursor, id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(id)s""",
                   {'id': id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_answers_for_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(id)s""",
                   {'id': id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_answers_for_answer_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(id)s""",
                   {'id': id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_question_id_for_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer 
                    WHERE id = %(answer_id)s""",
                   {'answer_id': int(answer_id)})
    question_id = cursor.fetchall()
    return question_id[0].get('question_id')


@connection.connection_handler
def del_question_row(cursor, id):
    cursor.execute("""
                DELETE FROM answer
                WHERE question_id = %(id)s;
                DELETE FROM question
                WHERE id = %(id)s""",
                   {'id': id})


@connection.connection_handler
def answer_delete_by_id(cursor, id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(id)s""",
                   {'id': id})


@connection.connection_handler
def question_view_number_counter(cursor, id):
    cursor.execute("""
                UPDATE question
                SET view_number = view_number +1
                WHERE id = %(id)s""", {'id': id})


@connection.connection_handler
def question_vote_up(cursor, id):
    cursor.execute("""
                UPDATE question
                SET vote_number = vote_number +1
                WHERE id = %(id)s""", {'id': id})


@connection.connection_handler
def question_vote_down(cursor, id):
    cursor.execute("""
                UPDATE  question
                SET  vote_number = vote_number -1
                WHERE id= %(id)s""", {'id': id})


@connection.connection_handler
def answer_vote_up(cursor, id):
    cursor.execute("""
                UPDATE answer
                SET vote_number = vote_number +1
                WHERE id = %(id)s""", {'id': id})


@connection.connection_handler
def answer_vote_down(cursor, id):
    cursor.execute("""
                UPDATE answer
                SET vote_number = vote_number -1
                WHERE id = %(id)s""", {'id': id})


@connection.connection_handler
def add_new_comment(cursor, new_data):
    cursor.execute("""INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                    VALUES (%(question_id)s,%(answer_id)s,%(message)s,%(submission_time)s,%(edited_count)s)"""
                   , {'question_id': new_data['question_id'],
                      'answer_id': new_data['answer_id'],
                      'message': new_data['message'],
                      'submission_time': new_data['submission_time'],
                      'edited_count': new_data['edited_count']})


@connection.connection_handler
def update_comment(cursor, comment):
    cursor.execute("""UPDATE comment
                    SET 
                    message = %(message)s,
                    edited_count = edited_count +1
                    WHERE id = %(id)s"""
                   , {'id': comment['id'], 'message': comment['message']})


@connection.connection_handler
def get_question_comments(cursor, id):
    cursor.execute("""SELECT * FROM comment WHERE question_id = %(id)s""", {'id': id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def get_answer_comments(cursor):
    cursor.execute("""SELECT * FROM comment WHERE answer_id=answer_id""", {'id': id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def get_answer_comment_by_comment_id(cursor, id):
    cursor.execute("""SELECT * FROM comment WHERE id = %(id)s""", {'id': id})
    comment = cursor.fetchall()
    return comment[0]


@connection.connection_handler
def get_answer_id_by_comment_id(cursor, id):
    cursor.execute("""SELECT answer_id FROM comment WHERE id = %(id)s""", {'id': id})
    answer_id = cursor.fetchall()
    return answer_id[0].get('answer_id')


@connection.connection_handler
def get_question_id_by_answer_id(cursor, id):
    cursor.execute("""SELECT question_id FROM answer WHERE id = %(id)s""", {'id': id})
    question_id = cursor.fetchall()
    return question_id[0].get('question_id')


@connection.connection_handler
def sort_time_ascending(cursor):
    cursor.execute("""
                SELECT *
                FROM question
                ORDER BY submission_time ASC """)
    sub_asc = cursor.fetchall()
    return sub_asc


@connection.connection_handler
def sort_time_descending(cursor):
    cursor.execute("""
                SELECT *
                FROM question
                ORDER BY submission_time DESC """)
    sub_desc = cursor.fetchall()
    return sub_desc


@connection.connection_handler
def view_ascending(cursor):
    cursor.execute("""
                SELECT *
                FROM question
                ORDER BY view_number ASC """)
    view_asc = cursor.fetchall()
    return view_asc


@connection.connection_handler
def view_descending(cursor):
    cursor.execute("""
                SELECT *
                FROM question
                ORDER BY view_number DESC """)
    view_desc = cursor.fetchall()
    return view_desc


@connection.connection_handler
def vote_ascending(cursor):
    cursor.execute("""
                SELECT *
                FROM question
                ORDER BY vote_number ASC """)
    vote_asc = cursor.fetchall()
    return vote_asc


@connection.connection_handler
def vote_descending(cursor):
    cursor.execute("""
                SELECT *
                FROM question
                ORDER BY vote_number DESC """)
    vote_desc = cursor.fetchall()
    return vote_desc


@connection.connection_handler
def get_search_results_from_questions(cursor, search_phrase):
    phrase = search_phrase.lower()
    cursor.execute("""SELECT * FROM question
                        WHERE lower(title) LIKE '%%' || %(phrase)s || '%%' OR
                        lower (message ) LIKE '%%' || %(phrase)s || '%%' 
    """, {'phrase': phrase})
    search_results_from_questions = cursor.fetchall()
    return search_results_from_questions


@connection.connection_handler
def get_search_results_from_answers(cursor, search_phrase):
    phrase = search_phrase.lower()
    cursor.execute("""
    SELECT question_id FROM answer
    WHERE lower (message ) LIKE '%%' || %(phrase)s || '%%'""", {'phrase': phrase})
    question_id = cursor.fetchall()
    print(question_id)  # this is a list with dictionaries
    cursor.execute(""" SELECT * FROM question
                        WHERE id = %(question_id)s """, {'question_id': question_id[0]['question_id']})


def get_search_results(cursor, search_phrase):
    cursor.execute("""SELECT * FROM question
                        WHERE title LIKE %(search_phrase)s OR 
                        message LIKE %(search_phrase)s 
    """, {'search_phrase': search_phrase})
    search_result = cursor.fetchall()
    return search_result


@connection.connection_handler
def get_tag_id_from_question_id(cursor, id):
    cursor.execute("""SELECT tag_id FROM question_tag
                    WHERE question_id = %(id)s"""
                   , {'question_id': id})
    tag_id = cursor.fetchall()
    return tag_id


@connection.connection_handler
def get_tag_from_tag_id(cursor, id):
    tag_id = get_tag_id_from_question_id(id)
    cursor.execute("""SELECT name FROM tag
                        WHERE id = %(tag_id)s""",
                   {'id': tag_id})
    name = cursor.fethcall()
    return name


@connection.connection_handler
def get_tags_for_select(cursor):
    cursor.execute("""SELECT * FROM tag
    """)
    tags = cursor.fetchall()
    return tags


@connection.connection_handler
def add_to_tag_table(cursor, new_data):
    cursor.execute("""INSERT INTO tag (name)
                    VALUES (%(name)s)"""
                   , {'submission_time': new_data['submission_time']})


@connection.connection_handler
def write_to_question_tag(cursor, question_id, tag_id):
    cursor.execute("""
                    INSERT INTO question_tag (question_id, tag_id) 
                    VALUES (%(question_id)s,%(tag_id)s)"""
                   , {'question_id': question_id, 'tag_id': tag_id})


@connection.connection_handler
def delete_question_tag(cursor, id):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id = %(id)s
                    """, {'question_id': id})
