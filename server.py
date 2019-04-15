from flask import Flask, render_template, request, redirect, url_for
import data_handler

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def list_of_questions():
    questions = data_handler.get_all_details()
    last_questions = data_handler.get_latest_five_questions()
    if request.method == 'POST':
        if 'show_all' == request.form.get('show'):
            return render_template('list.html', questions=questions)
        elif 'show_latest' == request.form.get('show'):
            return render_template('list.html', questions=last_questions)
    user = request.args.get('user')
    return render_template("list.html", questions=last_questions)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        empty_questions = {}
        return render_template('add-question.html',
                               question=empty_questions,
                               form_url=url_for('add_question'),
                               page_title='Add New Question',
                               button_title='Submit',
                               button_page='Return'
                               )

    if request.method == 'POST':
        question = {'submission_time': data_handler.date_time(),
                    'view_number': request.form.get('view_number'),
                    'vote_number': request.form.get('vote_number'),
                    'title': request.form.get('title'),
                    'message': request.form.get('message'),
                    'image': request.form.get('image'),
                    }
        data_handler.add_new_question(question)
        return redirect('/')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def update_question(question_id):
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
        return redirect('/')

    question = data_handler.get_question_for_id(question_id)
    return render_template('add-question.html',
                           question=question,
                           form_url=url_for('update_question', question_id=question_id),
                           page_title='Update Question',
                           button_title='Update',
                           button_page='Return '
                           )


@app.route('/question/<id>', methods=['GET', 'POST'])
def list_answers(id=None):
    time = request.args.get('time')  # answer comment edit time stamp
    q_c_time = request.args.get('q_c_time')
    question_row = data_handler.get_question_for_id(id)
    answer_row = data_handler.get_answers_for_id(id)
    question_comments = data_handler.get_question_comments(id)
    answer_comments = data_handler.get_answer_comments()
    tags = data_handler.get_all_tag_name_for_question(id)
    if request.method == 'POST':
        answers = {'submission_time': data_handler.date_time(),
                   'vote_number': 0,
                   'question_id': id,
                   'message': request.form.get('answer_message'),
                   'image': request.form.get('image'),
                   }
        data_handler.add_new_answer(answers)
        return redirect(url_for('list_answers', id=id))
    data_handler.question_view_number_counter(id)
    return render_template('question.html', id=id, question_row=question_row, answer_row=answer_row,
                           question_comments=question_comments, answer_comments=answer_comments, time=time,
                           q_c_time=q_c_time, tags=tags)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    id = data_handler.get_question_id_for_answer_id(answer_id)
    if request.method == 'POST':
        answer = {'id': answer_id,
                  'submission_time': data_handler.date_time(),
                  'vote_number': request.form.get('vote_number'),
                  'question_id': request.form.get('question_id'),
                  'message': request.form.get('message'),
                  'image': request.form.get('image'),
                  }
        data_handler.edit_answer_row(answer, answer_id)
        return redirect(url_for('list_answers', id=id))
        # return redirect('/')

    answer = data_handler.get_answers_id_for_edit(answer_id)
    return render_template('edit-answer.html',
                           answer=answer,
                           form_url=url_for('edit_answer', answer_id=answer_id),
                           page_title='Update Answer',
                           button_title='Update',
                           button_page='Return '
                           )


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_rows(question_id):
    data_handler.get_all_comments_for_answer(question_id)
    data_handler.del_question_row(question_id)
    return redirect('/')


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    question_id = data_handler.get_question_id_for_answer_id(answer_id)
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
    if request.method == 'POST':
        choices = request.form.get('sort')
        if 'asc' in choices:
            sorted_data = data_handler.ascending_order(choices)
            return render_template('list.html', questions=sorted_data)
        if 'desc' in choices:
            sorted_data = data_handler.descending_order(choices)
            return render_template('list.html', questions=sorted_data)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_question_comment(question_id=None):
    comment = data_handler.get_question_for_id(question_id)
    if request.method == 'POST':
        comment = {'submission_time': data_handler.date_time(),
                   'question_id': request.form.get('question_id'),
                   'answer_id': request.form.get('answer_id'),
                   'message': request.form.get('message'),
                   'edited_count': request.form.get('edited_count'),
                   }
        data_handler.add_new_comment(comment)
        return redirect(url_for('list_answers', id=question_id))
    return render_template('add-question-comment.html', comment=comment, edit_comment=None,
                           button_title="Post New Comment")


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_answer_comment(answer_id=None):
    comment = data_handler.get_answers_for_answer_id(answer_id)
    question_id = data_handler.get_question_id_for_answer_id(answer_id)
    if request.method == 'POST':
        comment = {'submission_time': data_handler.date_time(),
                   'question_id': request.form.get('question_id'),
                   'answer_id': request.form.get('answer_id'),
                   'message': request.form.get('message'),
                   'edited_count': request.form.get('edited_count'),
                   }
        data_handler.add_new_comment(comment)
        return redirect(url_for('list_answers', id=question_id))
    return render_template('add-answer-comment.html', comment=comment, edit_comment=None,
                           button_title="Post New Comment")


@app.route('/question-comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_question_comment(comment_id):
    question_id = data_handler.get_question_id_by_comment_id(comment_id)
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
        return redirect(url_for('list_answers', id=question_id, q_c_time=q_c_time))
    comment = data_handler.get_answer_comment_by_comment_id(comment_id)
    return render_template('add-question-comment.html', edit_comment=comment, comment=None, button_title="Edit Comment")


@app.route('/answer-comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_answer_comment(comment_id):
    answer_id = data_handler.get_answer_id_by_comment_id(comment_id)
    question_id = data_handler.get_question_id_by_answer_id(answer_id)
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
        return redirect(url_for('list_answers', id=question_id, time=time))
    comment = data_handler.get_answer_comment_by_comment_id(comment_id)
    return render_template('add-answer-comment.html', edit_comment=comment, comment=None, button_title="Edit Comment")


@app.route('/question-comment/<comment_id>/delete')
def delete_question_comment(comment_id):
    question_id = data_handler.get_question_id_by_comment_id(comment_id)
    data_handler.delete_comment_by_comment_id(comment_id)
    return redirect(url_for('list_answers', id=question_id))


@app.route('/answer-comment/<comment_id>/delete')
def delete_answer_comment(comment_id):
    answer_id = data_handler.get_answer_id_by_comment_id(comment_id)
    question_id = data_handler.get_question_id_by_answer_id(answer_id)
    data_handler.delete_comment_by_comment_id(comment_id)
    return redirect(url_for('list_answers', id=question_id))


@app.route('/search/', methods=['GET'])
def search():
    search_phrase = request.args.get('search_phrase')
    result = data_handler.do_search(search_phrase)
    return render_template('list.html', questions=result)


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def adding_tag_to_question(question_id):
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
        return redirect(url_for('list_answers', id=question_id))

    return render_template('add-tag.html', option_list=available_tags, button_title='Submit', question_id=question_id)


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
        hashed_password = data_handler.verify_pwd(username)
        if data_handler.verify_password(password, hashed_password) is True:
            return redirect(url_for('list_of_questions', user=username))  # incomplete, this means login is successful
        return redirect(url_for('/', mode=2))  # incomplete, this means that login is unsuccessful

    return render_template('login.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
