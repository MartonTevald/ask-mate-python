import bcrypt as bcrypt
from psycopg2 import sql
import connection
from datetime import datetime


@connection.connection_handler
def get_latest_five_questions(cursor):
    cursor.execute("""
            SELECT * 
            FROM question 
            ORDER BY submission_time DESC 
            """)
    question = cursor.fetchmany(5)
    return question


@connection.connection_handler
def get_all_details(cursor):
    cursor.execute("""SELECT * FROM question
    ;""")
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
                   , {'id': id,
                      'submission_time': new_data['submission_time'],
                      'view_number': new_data['view_number'],
                      'vote_number': new_data['vote_number'],
                      'title': new_data['title'],
                      'message': new_data['message'],
                      'image': new_data['image']})


@connection.connection_handler
def add_new_question(cursor, new_data):
    cursor.execute("""INSERT INTO question (submission_time, view_number, vote_number, title, message, image, userid)
                    VALUES (%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s,%(userid)s)"""
                   , {'submission_time': new_data['submission_time'],
                      'view_number': new_data['view_number'],
                      'vote_number': new_data['vote_number'],
                      'title': new_data['title'],
                      'message': new_data['message'],
                      'image': new_data['image'],
                      'userid': new_data['userid']})


@connection.connection_handler
def add_new_answer(cursor, new_data):
    cursor.execute("""INSERT INTO answer (submission_time,question_id,vote_number, message,image,userid)
                    VALUES (%(submission_time)s,%(question_id)s,%(vote_number)s,%(message)s,%(image)s,%(userid)s)"""
                   , {'submission_time': new_data['submission_time'], 'question_id': new_data['question_id'],
                      'vote_number': new_data['vote_number'],
                      'message': new_data['message'], 'image': new_data['image'], 'userid': new_data['userid']})


@connection.connection_handler
def get_question_for_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(id)s """,
                   {'id': id})
    question = cursor.fetchall()
    return question[0]


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
                    WHERE question_id = %(id)s
                     ORDER BY submission_time""",
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
def get_all_comments_for_answer(cursor, question_id):
    answer_ids = get_all_answer_id_to_delete_comments(question_id)
    if len(answer_ids) > 0:
        cursor.execute("""
                        DELETE FROM comment
                        WHERE answer_id IN %(id)s """,
                       {'id': answer_ids})
    else:
        return


@connection.connection_handler
def get_all_answer_id_to_delete_comments(cursor, question_id):
    cursor.execute("""
                SELECT id FROM answer
                WHERE question_id = %(id)s
                """, {'id': question_id})

    answer_ids = cursor.fetchall()

    id_values = []
    for ids in answer_ids:
        id_values.append(ids['id'])
    id_values = tuple(id_values)
    return tuple(id_values)


@connection.connection_handler
def del_question_row(cursor, id):
    cursor.execute("""
                DELETE FROM question_tag
                WHERE question_id = %(id)s;
                DELETE FROM comment
                WHERE question_id = %(id)s;
                DELETE FROM answer
                WHERE question_id = %(id)s;
                DELETE FROM question
                WHERE id = %(id)s""",
                   {'id': id})


@connection.connection_handler
def answer_delete_by_id(cursor, id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE answer_id = %(id)s;
                    DELETE FROM answer
                    WHERE id = %(id)s;
                    """,
                   {'id': id})


@connection.connection_handler
def question_view_number_counter(cursor, id):
    cursor.execute("""
                UPDATE question
                SET view_number = view_number +1
                WHERE id = %(id)s""", {'id': id})


@connection.connection_handler
def vote_up(cursor, id, table):
    cursor.execute(
        sql.SQL("""
        UPDATE {table}
        SET vote_number = vote_number + 1
        WHERE id = @id""").format(table=sql.Identifier(table), id=sql.Identifier(id)))


@connection.connection_handler
def vote_down(cursor, id, table):
    cursor.execute(
        sql.SQL("""
            UPDATE {table}
            SET vote_number = vote_number -1
            WHERE id = @id""").format(table=sql.Identifier(table), id=sql.Identifier(id)))


@connection.connection_handler
def add_new_comment(cursor, new_data):
    cursor.execute("""INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, userid)
                    VALUES (%(question_id)s,%(answer_id)s,%(message)s,%(submission_time)s,%(edited_count)s,%(userid)s)"""
                   , {'question_id': new_data['question_id'],
                      'answer_id': new_data['answer_id'],
                      'message': new_data['message'],
                      'submission_time': new_data['submission_time'],
                      'edited_count': new_data['edited_count'],
                      'userid': new_data['userid']})


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
def delete_comment_by_comment_id(cursor, id):
    cursor.execute("""DELETE FROM comment WHERE id = %(id)s""", {'id': id})


@connection.connection_handler
def get_question_id_by_answer_id(cursor, id):
    cursor.execute("""SELECT question_id FROM answer WHERE id = %(id)s""", {'id': id})
    question_id = cursor.fetchall()
    return question_id[0].get('question_id')


@connection.connection_handler
def get_question_id_by_comment_id(cursor, id):
    cursor.execute("""select question_id from comment where id = %(id)s""", {'id': id})
    question_id = cursor.fetchall()
    return question_id[0].get('question_id')


@connection.connection_handler
def ascending_order(cursor, sorted):
    if sorted == 'sub_asc':
        sort = 'submission_time'
    if sorted == 'view_asc':
        sort = 'view_number'
    if sorted == 'vote_asc':
        sort = 'vote_number'
    cursor.execute(sql.SQL("""
                    SELECT *
                    FROM question
                    ORDER BY {sort} ASC """)
                   .format(sort=sql.Identifier(sort)))

    sort_asc = cursor.fetchall()
    return sort_asc


@connection.connection_handler
def descending_order(cursor, sorted):
    if sorted == 'sub_desc':
        sort = 'submission_time'
    if sorted == 'view_desc':
        sort = 'view_number'
    if sorted == 'vote_desc':
        sort = 'vote_number'
    cursor.execute(sql.SQL("""
                        SELECT *
                        FROM question
                        ORDER BY {sort} DESC """)
                   .format(sort=sql.Identifier(sort)))

    sort_desc = cursor.fetchall()
    return sort_desc


def do_search(search_phrase):
    question_ids_from_questions = get_search_question_ids(search_phrase)
    question_ids_from_answers = get_search_answers_ids(search_phrase)
    ids_ = []
    if len(question_ids_from_answers) > 0 and len(question_ids_from_questions) > 0:
        print('both valid')
        ids_ = question_ids_from_answers + question_ids_from_questions

    elif len(question_ids_from_answers) > 0:
        print('fromanswers is valid only')
        ids_ = question_ids_from_answers
    elif len(question_ids_from_questions) > 0:
        ids_ = question_ids_from_questions
        print('fromquestions is valid only')

    result = make_the_result(ids_)
    return result


@connection.connection_handler
def get_search_question_ids(cursor, search_phrase):
    phrase = search_phrase.lower()
    cursor.execute("""SELECT id FROM question
                        WHERE lower(title) LIKE '%%' || %(phrase)s || '%%' OR
                        lower (message ) LIKE '%%' || %(phrase)s || '%%' 
    """, {'phrase': phrase})

    ids_dictsinlist = cursor.fetchall()
    ids = []
    for id in ids_dictsinlist:
        ids.append(id['id'])
    return ids


@connection.connection_handler
def get_search_answers_ids(cursor, search_phrase):
    phrase = search_phrase.lower()
    cursor.execute("""
    SELECT question_id FROM answer
    WHERE lower (message ) LIKE '%%' || %(phrase)s || '%%'""", {'phrase': phrase})
    question_id = cursor.fetchall()
    if len(question_id) > 0:
        # print(question_id)   #this is a list with dictionaries
        cursor.execute(""" SELECT * FROM question
                           WHERE id = %(question_id)s """, {'question_id': question_id[0]['question_id']})
        ids_dictsinlist = cursor.fetchall()
        ids = []
        for id in ids_dictsinlist:
            ids.append(id['id'])
        return ids
    else:
        return []


@connection.connection_handler
def make_the_result(cursor, ids_):
    if len(ids_) > 0:
        cursor.execute(""" SELECT * FROM question
                            WHERE id IN %(ids)s""", {'ids': tuple(ids_)})
        result_table = cursor.fetchall()
        return result_table
    else:
        return []


def get_search_results(cursor, search_phrase):
    cursor.execute("""SELECT * FROM question
                        WHERE title LIKE %(search_phrase)s OR 
                        message LIKE %(search_phrase)s 
    """, {'search_phrase': search_phrase})
    search_result = cursor.fetchall()
    return search_result


@connection.connection_handler
def get_all_tag_name_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT tag.name,tag.id FROM question_tag
                    INNER JOIN tag  on question_tag.tag_id = tag.id
                    WHERE question_id = %(question_id)s
                    """, {'question_id': question_id})
    tag_names = cursor.fetchall()
    return tag_names


@connection.connection_handler
def get_tag_id_from_tag_name(cursor, name):
    cursor.execute(""" SELECT id  FROM tag
                    WHERE name = %(name)s
    """, {'name': name})
    tag_id = cursor.fetchone()
    return tag_id['id']


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
                   , {'name': new_data})


@connection.connection_handler
def write_to_question_tag(cursor, question_id, tag_id):
    cursor.execute("""
                    INSERT INTO question_tag (question_id, tag_id)
                    VALUES (%(question_id)s,%(tag_id)s)"""
                   , {'question_id': question_id, 'tag_id': tag_id})


@connection.connection_handler
def delete_question_tag(cursor, question_id, tag_id):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id = %(id)s AND tag_id = %(tag)s 
                    """, {'id': question_id, 'tag': tag_id})


@connection.connection_handler
def add_user_details_to_database(cursor, user_information):
    cursor.execute("""
                    INSERT INTO user_info(username, hash, email, creation_date, status)
                    VALUES ( %(username)s,%(hash)s,%(email)s,%(creation_date)s,%(status)s)""",
                   {'username': user_information['username'], 'hash': user_information['hash'],
                    'email': user_information['email'], 'creation_date': user_information['creation_date'],
                    'status': user_information['status']
                    })


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def verify_pwd(cursor, username):
    cursor.execute("""SELECT hash FROM user_info 
                    WHERE username = %(username)s""", {'username': username})
    result = cursor.fetchall()
    return result[0].get('hash')


@connection.connection_handler
def get_user_id_by_username(cursor, username):
    cursor.execute("""SELECT user_id FROM user_info WHERE username = %(username)s""", {'username': username})
    result = cursor.fetchone()
    return result.get('user_id')


@connection.connection_handler
def user_questions(cursor, user_id):
    cursor.execute("""
                    SELECT  * FROM question
                    INNER JOIN user_info on question.userid = user_info.user_id
                    WHERE question.userid = %(user_id)s AND user_info.user_id = %(user_id)s
    """, {'user_id': user_id})
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def user_answers(cursor, user_id):
    cursor.execute("""
                    SELECT  * FROM answer
                    INNER JOIN user_info on answer.userid = user_info.user_id
                    WHERE answer.userid = %(user_id)s AND user_info.user_id = %(user_id)s
    """, {'user_id': user_id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def user_comments(cursor, user_id):
    cursor.execute("""
                    SELECT  * FROM comment
                    INNER JOIN user_info on comment.userid = user_info.user_id
                    WHERE comment.userid = %(user_id)s AND user_info.user_id = %(user_id)s
    """, {'user_id': user_id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def list_of_users(cursor):
    cursor.execute("""SELECT username,email,creation_date FROM user_info ;""")
    users = cursor.fetchall()
    return users
