from flask import Flask, render_template, request, redirect, url_for
import data_handler
import os

app = Flask(__name__)


@app.route('/')
def first_five_question_by_date():
    questions = data_handler.get_first_five_question()
    return render_template('list.html', questions=questions)


@app.route('/list')
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


@app.route('/question/<question_id>/edit', methods=['GET', 'POST', 'DELETE'])
def update_question(question_id):
    if request.method == 'POST':
        # if request.form.get('id') != question_id:
        #     raise ValueError('The received id is not valid!')
        question = {'id': question_id,
                    'submission_time': data_handler.date_time(),
                    'view_number': request.form.get('view_number'),
                    'vote_number': request.form.get('vote_number'),
                    'title': request.form.get('title'),
                    'message': request.form.get('message'),
                    'image': request.form.get('image'),
                    }
        data_handler.edit_question_row('question.csv', question, question_id)
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
    return render_template('/question.html', id=id, question_row=question_row, answer_row=answer_row)


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


@app.route('/<sort_by>/asc')
def sort_questions(sort_by):
    sorted_data = data_handler.sort_ascending(sort_by)
    return render_template('/list.html', questions=sorted_data)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
