from flask import Flask, render_template, request, redirect, url_for
import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list():
    questions = data_handler.get_all_details('question.csv')
    return render_template('list.html', questions=questions)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        empty_questions = {}
        return render_template('add-question.html',
                               question=empty_questions,
                               form_url=url_for('add_question'),
                               page_title='Add Questions',
                               button_title='Submit',
                               button_page='Return'
                               )

    if request.method == 'POST':
        question = {'id': data_handler.get_id('question.csv'),
                    'submission_time': data_handler.date_time(),
                    'view_number': request.form.get('view_number'),
                    'vote_number': request.form.get('vote_number'),
                    'title': request.form.get('title'),
                    'message': request.form.get('message'),
                    'image': request.form.get('image'),
                    }
        data_handler.write_to_file('question.csv', question)
        return redirect('/')


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def update_question(question_id):
    if request.method == 'POST':
        if request.form.get('id') != question_id:
            raise ValueError('The received id is not valid!')
        question = {'id': question_id,
                    'submission_time': request.form.get('submission_time'),
                    'view_number': request.form.get('view_number'),
                    'vote_number': request.form.get('vote_number'),
                    'title': request.form.get('title'),
                    'message': request.form.get('message'),
                    'image': request.form.get('image'),
                    }
        data_handler.edit_question_row(question)
        return redirect('/')

    question = data_handler.get_user_question('question.csv',question,)

    return render_template('add-question.html.html',
                           question=question,
                           form_url=url_for('update_question', question_id=question_id),
                           page_title='Update Question',
                           button_title='Update',
                           button_page='Delete '
                           )


@app.route('/question/<id>', methods=['GET', 'POST'])
def list_answers(id=None):
    question_row = data_handler.get_question_for_id('question.csv', id)
    answer_row = data_handler.get_answers_for_id('answer.csv', id)
    if request.method == 'POST':
        answers = {'id': data_handler.get_id('answer.csv'),
                   'submission_time': data_handler.date_time(),
                   'vote_number': 0,
                   'question_id': id,
                   'message': request.form['answer_message'],
                   'image': 0
                   }
        data_handler.write_to_answer_file('answer.csv', answers)
        return redirect(url_for('list_answers', id=id))
    return render_template('/question.html', question_row=question_row, answer_row=answer_row, id=id)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
