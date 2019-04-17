from flask import Flask, render_template, request, redirect, url_for, session, flash
import data_handler

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['POST', 'GET'])
def list_of_questions():
    questions = data_handler.get_all_details()
    last_questions = data_handler.get_latest_five_questions()
    if 'username' in session:
        username = session['username']
        user = data_handler.get_user_id_by_username(username)

        if request.method == 'POST':
            if 'show_all' == request.form.get('show'):
                return render_template('list.html', questions=questions)
            elif 'show_latest' == request.form.get('show'):
                return render_template('list.html', questions=last_questions)
        return render_template("list.html", questions=last_questions, username=username, user=user)
    else:
        return render_template("list.html", questions=last_questions, username="")


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    username = session['username']
    if request.method == 'GET':
        empty_questions = {}
        return render_template('add-question.html',
                               question=empty_questions,
                               form_url=url_for('add_question'),
                               page_title='Add New Question',
                               button_title='Submit',
                               button_page='Return',
                               username=username)

    if request.method == 'POST':
        question = {'submission_time': data_handler.date_time(),
                    'view_number': request.form.get('view_number'),
                    'vote_number': request.form.get('vote_number'),
                    'title': request.form.get('title'),
                    'message': request.form.get('message'),
                    'image': request.form.get('image'),
                    'userid': data_handler.get_user_id_by_username(username),
                    }
        data_handler.add_new_question(question)
        return redirect(url_for('list_of_questions', username=username))


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def update_question(question_id):
    username = session['username']
    check_for_validation = data_handler.check_user_id_authentication_for_question(username, question_id)
    if check_for_validation:
        if request.method == 'POST':
            question = {'id': question_id,
                        'submission_time': data_handler.date_time(),
                        'view_number': request.form.get('view_number'),
                        'vote_number': request.form.get('vote_number'),
                        'title': request.form.get('title'),
                        'message': request.form.get('message'),
                        'image': request.form.get('image'),
                        }
            data_handler.edit_question_row(question, question_id)
            return redirect(url_for('list_answers', id=question_id, username=username))

        question = data_handler.get_question_for_id(question_id)
        return render_template('add-question.html',
                               question=question,
                               form_url=url_for('update_question', question_id=question_id),
                               page_title='Update Question',
                               button_title='Update',
                               button_page='Return ',
                               username=username
                               )
    else:
        return redirect(url_for('list_answers', id=question_id, username=username))


@app.route('/question/<id>', methods=['GET', 'POST'])
def list_answers(id=None):
    if 'username' in session:
        username = session['username']
        user = data_handler.get_user_id_by_username(username)
        time = request.args.get('time')  # answer comment edit time stamp
        q_c_time = request.args.get('q_c_time')
        question_row = data_handler.get_question_for_id(id)
        answer_row = data_handler.get_answers_for_id(id)
        question_comments = data_handler.get_question_comments(id)
        answer_comments = data_handler.get_answer_comments()
        tags = data_handler.get_all_tag_name_for_question(id)
        q_author = data_handler.get_username_by_question_id(id)
        check_for_valid_question = data_handler.check_user_id_authentication_for_question(username, id)
        if request.method == 'POST':
            answers = {'submission_time': data_handler.date_time(),
                       'vote_number': 0,
                       'question_id': id,
                       'message': request.form.get('answer_message'),
                       'image': request.form.get('image'),
                       'userid': data_handler.get_user_id_by_username(username),
                       }
            data_handler.add_new_answer(answers)
            return redirect(url_for('list_answers', id=id, username=username))
        data_handler.question_view_number_counter(id)
        return render_template('question.html', id=id, question_row=question_row, answer_row=answer_row,
                               question_comments=question_comments, answer_comments=answer_comments, time=time,
                               q_c_time=q_c_time, tags=tags, username=username, user=user, q_author=q_author,
                               check_edit_question=check_for_valid_question)
    else:
        return redirect(url_for('user_login'))


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    username = session['username']
    check_for_validation = data_handler.check_user_id_authentication_for_answer(username, answer_id)
    id = data_handler.get_question_id_for_answer_id(answer_id)
    if check_for_validation:
        if request.method == 'POST':
            answer = {'id': answer_id,
                      'submission_time': data_handler.date_time(),
                      'vote_number': request.form.get('vote_number'),
                      'question_id': request.form.get('question_id'),
                      'message': request.form.get('message'),
                      'image': request.form.get('image'),
                      }
            data_handler.edit_answer_row(answer, answer_id)
            return redirect(url_for('list_answers', id=id, username=username))

        answer = data_handler.get_answers_id_for_edit(answer_id)
        return render_template('edit-answer.html',
                               answer=answer,
                               form_url=url_for('edit_answer', answer_id=answer_id),
                               page_title='Update Answer',
                               button_title='Update',
                               button_page='Return ',
                               username=username,
                               )
    else:
        return redirect(url_for('list_answers', id=id, username=username))


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_rows(question_id):
    username = session['username']
    check_for_validation = data_handler.check_user_id_authentication_for_question(username, question_id)
    if check_for_validation:
        data_handler.get_all_comments_for_answer(question_id)
        data_handler.del_question_row(question_id)
        return redirect('/')
    else:
        return redirect(url_for('list_answers', id=question_id))


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    username = session['username']
    check_for_validation = data_handler.check_user_id_authentication_for_answer(username, answer_id)
    question_id = data_handler.get_question_id_for_answer_id(answer_id)
    if check_for_validation:
        data_handler.answer_delete_by_id(answer_id)
    return redirect(url_for('list_answers', id=question_id))


@app.route('/question/<question_id>/vote-up', methods=['POST', 'GET'])
def question_vote_up(question_id):
    data_handler.vote_up(question_id, 'question')
    return redirect(url_for('list_answers', id=question_id))


@app.route('/question/<question_id>/vote-down', methods=['POST', 'GET'])
def question_vote_down(question_id):
    data_handler.vote_down(question_id, 'question')
    return redirect(url_for('list_answers', id=question_id))


@app.route('/answer/<answer_id>/vote-up', methods=['POST', 'GET'])
def question_answer_up(answer_id):
    question_id = data_handler.get_question_id_for_answer_id(answer_id)
    data_handler.vote_up(answer_id, 'answer')
    return redirect(url_for('list_answers', id=question_id))


@app.route('/answer/<answer_id>/vote-down', methods=['POST', 'GET'])
def question_answer_down(answer_id):
    question_id = data_handler.get_question_id_for_answer_id(answer_id)
    data_handler.vote_down(answer_id, 'answer')
    return redirect(url_for('list_answers', id=question_id))


@app.route('/list/', methods=['POST', 'GET'])
def sort_questions():
    username = session['username']
    if request.method == 'POST':
        choices = request.form.get('sort')
        if 'asc' in choices:
            sorted_data = data_handler.ascending_order(choices)
            return render_template('list.html', questions=sorted_data, username=username)
        if 'desc' in choices:
            sorted_data = data_handler.descending_order(choices)
            return render_template('list.html', questions=sorted_data, username=username)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_question_comment(question_id=None):
    username = session['username']
    comment = data_handler.get_question_for_id(question_id)
    if request.method == 'POST':
        comment = {'submission_time': data_handler.date_time(),
                   'question_id': request.form.get('question_id'),
                   'answer_id': request.form.get('answer_id'),
                   'message': request.form.get('message'),
                   'edited_count': request.form.get('edited_count'),
                   'userid': data_handler.get_user_id_by_username(username),
                   }
        data_handler.add_new_comment(comment)
        return redirect(url_for('list_answers', id=question_id, username=username))
    return render_template('add-question-comment.html', comment=comment, edit_comment=None,
                           button_title="Post New Comment", username=username)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_answer_comment(answer_id=None):
    username = session['username']
    comment = data_handler.get_answers_for_answer_id(answer_id)
    question_id = data_handler.get_question_id_for_answer_id(answer_id)
    if request.method == 'POST':
        comment = {'submission_time': data_handler.date_time(),
                   'question_id': request.form.get('question_id'),
                   'answer_id': request.form.get('answer_id'),
                   'message': request.form.get('message'),
                   'edited_count': request.form.get('edited_count'),
                   'userid': data_handler.get_user_id_by_username(username),
                   }
        data_handler.add_new_comment(comment)
        return redirect(url_for('list_answers', id=question_id, username=username))
    return render_template('add-answer-comment.html', comment=comment, edit_comment=None,
                           button_title="Post New Comment", username=username)


@app.route('/question-comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_question_comment(comment_id):
    username = session['username']
    question_id = data_handler.get_question_id_by_comment_id(comment_id)
    check_for_validation = data_handler.check_user_id_authentication_for_comment(username, comment_id)
    if request.method == 'POST':
        comment = {'id': comment_id,
                   'submission_time': request.form.get('submission_time'),
                   'question_id': request.form.get('question_id'),
                   'answer_id': request.form.get('answer_id'),
                   'message': request.form.get('message'),
                   'edited_count': request.form.get('edited_count'),
                   }
        data_handler.update_comment(comment)
        q_c_time = data_handler.date_time()
        return redirect(url_for('list_answers', id=question_id, q_c_time=q_c_time, username=username))
    comment = data_handler.get_answer_comment_by_comment_id(comment_id)
    return render_template('add-question-comment.html', edit_comment=comment, comment=None, button_title="Edit Comment",
                           username=username)


@app.route('/answer-comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_answer_comment(comment_id):
    username = session['username']
    answer_id = data_handler.get_answer_id_by_comment_id(comment_id)
    question_id = data_handler.get_question_id_by_answer_id(answer_id)
    check_for_validation = data_handler.check_user_id_authentication_for_comment(username, comment_id)
    if check_for_validation:
        if request.method == 'POST':
            comment = {'id': comment_id,
                       'submission_time': request.form.get('submission_time'),
                       'question_id': request.form.get('question_id'),
                       'answer_id': request.form.get('answer_id'),
                       'message': request.form.get('message'),
                       'edited_count': request.form.get('edited_count'),
                       }
            data_handler.update_comment(comment)
            time = data_handler.date_time()
            return redirect(url_for('list_answers', id=question_id, time=time, username=username))
        comment = data_handler.get_answer_comment_by_comment_id(comment_id)
        return render_template('add-answer-comment.html', edit_comment=comment, comment=None,
                               button_title="Edit Comment",
                               username=username)
    else:
        return redirect(url_for('list_answers', id=question_id))


@app.route('/question-comment/<comment_id>/delete')
def delete_question_comment(comment_id):
    username = session['username']
    question_id = data_handler.get_question_id_by_comment_id(comment_id)
    check_for_validation = data_handler.check_user_id_authentication_for_comment(username, comment_id)
    if check_for_validation:
        data_handler.delete_comment_by_comment_id(comment_id)
    return redirect(url_for('list_answers', id=question_id))


@app.route('/answer-comment/<comment_id>/delete')
def delete_answer_comment(comment_id):
    username = session['username']
    answer_id = data_handler.get_answer_id_by_comment_id(comment_id)
    question_id = data_handler.get_question_id_by_answer_id(answer_id)
    check_for_validation = data_handler.check_user_id_authentication_for_comment(username, comment_id)
    if check_for_validation:
        data_handler.delete_comment_by_comment_id(comment_id)
    return redirect(url_for('list_answers', id=question_id))


@app.route('/search/', methods=['GET'])
def search():
    username = session['username']
    search_phrase = request.args.get('search_phrase')
    result = data_handler.do_search(search_phrase)
    return render_template('list.html', questions=result, username=username)


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def adding_tag_to_question(question_id):
    username = session['username']
    available_tags = data_handler.get_tags_for_select()
    if request.method == 'POST':
        new_tag = request.form.get('new_tag')
        add_tag = request.form.get('option')
        if not new_tag:
            tag_id = data_handler.get_tag_id_from_tag_name(add_tag)
            data_handler.write_to_question_tag(question_id, tag_id)
        else:
            data_handler.add_to_tag_table(new_tag)
            tag_id = data_handler.get_tag_id_from_tag_name(new_tag)
            data_handler.write_to_question_tag(question_id, tag_id)
        return redirect(url_for('list_answers', id=question_id, username=username))

    return render_template('add-tag.html', option_list=available_tags, button_title='Submit', question_id=question_id,
                           username=username)


@app.route('/question/<question_id>/tag/<tag_id>/delete', methods=['POST', 'GET'])
def delete_tag(question_id, tag_id):
    data_handler.delete_question_tag(question_id, tag_id)
    return redirect(url_for('list_answers', id=question_id))


@app.route('/registration', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        password = request.form.get('hash')
        hashed = data_handler.hash_password(password)
        user_info = {'username': request.form.get('username'),
                     'hash': hashed,
                     'email': request.form.get('email'),
                     'creation_date': data_handler.date_time(),
                     'status': request.form.get('status'),
                     }
        data_handler.add_user_details_to_database(user_info)
        return redirect('/')

    return render_template('registration.html')


@app.route('/login', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            hashed_password = data_handler.verify_pwd(username)
        except (ValueError, IndexError):
            return render_template('login.html', hashed=True)

        if data_handler.verify_password(password, hashed_password) is True:
            session['username'] = request.form['username']
            return redirect(url_for('list_of_questions', hashed=hashed_password))

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('list_of_questions'))


@app.route('/user/<user_id>', methods=['GET', 'POST'])
def user_page(user_id=None):
    username = session['username']
    user = data_handler.get_user_id_by_username(username)
    user_page_name = data_handler.get_username_by_user_id(user_id)
    questions = data_handler.user_questions(user_id)
    answers = data_handler.user_answers(user_id)
    comments = data_handler.user_comments(user_id)
    unaccepted_answers = data_handler.unaccepted_answers(user_id)
    return render_template('user-page.html', questions=questions,
                           answers=answers, comments=comments,
                           username=username, user=user, title=user_page_name, unaccepted=unaccepted_answers)


@app.route('/accept-answer/<answer_id>', methods=['GET', 'POST'])
def accept_answer(answer_id):
    username = session['username']
    user = data_handler.get_user_id_by_username(username)
    data_handler.accept_answer(answer_id)
    return redirect(url_for('user_page', user_id=user))


@app.route('/list-users', methods=['GET', 'POST'])
def list_of_users():
    username = session['username']
    user = data_handler.get_user_id_by_username(username)
    users_list = data_handler.list_of_users()
    return render_template('users-list.html', username=username, list_of_users=users_list, user=user)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
