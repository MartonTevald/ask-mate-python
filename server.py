from flask import Flask, render_template, request, redirect, url_for
import data_handler
import psycopg2
import os

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def first_five_question_by_date():
    questions = data_handler.get_all_details()
    last_questions = data_handler.get_first_five_question()
    if request.method == 'POST':
        if 'show_all' == request.form.get('show'):
            return render_template('list.html', questions=questions)
        elif 'show_latest' == request.form.get('show'):
            return render_template('list.html', questions=last_questions)
    elif request.method == 'GET':
        return render_template("list.html", questions=last_questions)


@app.route('/list', methods=['POST', 'GET'])
def list():
    questions = data_handler.get_all_details()
    return render_template('list.html', questions=questions)


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
    question_row = data_handler.get_question_for_id(id)
    answer_row = data_handler.get_answers_for_id(id)
    question_comments = data_handler.get_question_comments(id)
    answer_comments = data_handler.get_answer_comments()
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
                           question_comments=question_comments, answer_comments=answer_comments)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'POST':
        answer = {'id': answer_id,
                  'submission_time': data_handler.date_time(),
                  'vote_number': request.form.get('vote_number'),
                  'question_id': request.form.get('question_id'),
                  'message': request.form.get('message'),
                  'image': request.form.get('image'),
                  }
        data_handler.edit_answer_row(answer, answer_id)
        return redirect('/')
    if request.method == 'GET':
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
    data_handler.del_question_row(question_id)
    return redirect('/')


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    question_id = data_handler.get_question_id_for_answer_id(answer_id)
    data_handler.answer_delete_by_id(answer_id)
    return redirect(url_for('list_answers', id=question_id))


@app.route('/question/<question_id>/vote-up', methods=['POST', 'GET'])
def question_vote_up(question_id):
    data_handler.question_vote_up(question_id)
    return redirect(url_for('list_answers', id=question_id))


@app.route('/question/<question_id>/vote-down', methods=['POST', 'GET'])
def question_vote_down(question_id):
    data_handler.question_vote_down(question_id)
    return redirect(url_for('list_answers', id=question_id))


@app.route('/answer/<answer_id>/vote-up', methods=['POST', 'GET'])
def question_answer_up(answer_id):
    question_id = data_handler.get_question_id_for_answer_id(answer_id)
    data_handler.answer_vote_up(answer_id)
    return redirect(url_for('list_answers', id=question_id))


@app.route('/answer/<answer_id>/vote-down', methods=['POST', 'GET'])
def question_answer_down(answer_id):
    question_id = data_handler.get_question_id_for_answer_id(answer_id)
    data_handler.answer_vote_down(answer_id)
    return redirect(url_for('list_answers', id=question_id))


@app.route('/list/', methods=['POST', 'GET'])
def sort_questions():
    if request.method == 'POST':
        if 'sub_asc' == request.form.get('sort'):
            sorted_data = data_handler.sort_time_ascending()
            return render_template('list.html', questions=sorted_data)
        if 'sub_desc' == request.form.get('sort'):
            sorted_data = data_handler.sort_time_descending()
            return render_template('list.html', questions=sorted_data)
        if 'view_asc' == request.form.get('sort'):
            sorted_data = data_handler.view_ascending()
            return render_template('list.html', questions=sorted_data)
        if 'view_desc' == request.form.get('sort'):
            sorted_data = data_handler.view_descending()
            return render_template('list.html', questions=sorted_data)
        if 'vote_asc' == request.form.get('sort'):
            sorted_data = data_handler.vote_ascending()
            return render_template('list.html', questions=sorted_data)
        if 'vote_desc' == request.form.get('sort'):
            sorted_data = data_handler.vote_descending()
            return render_template('list.html', questions=sorted_data)
        else:
            redirect('/')


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
    return render_template('add-question-comment.html', comment=comment, button_title="Post New Comment")


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
    return render_template('add-answer-comment.html', comment=comment, button_title="Post New Comment")


@app.route('/search?q=<search_phrase>', methods=['GET', 'POST'])
def search(search_phrase):
    if request == 'POST':
        search_results = data_handler.get_search_results(search_phrase)
    print(search_results)
    return render_template('list.html', search_results=search_results)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
