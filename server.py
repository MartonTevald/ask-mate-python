from flask import Flask, render_template, request, redirect, url_for
import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list():
    questions = data_handler.get_all_details('question.csv')
    return render_template('list.html', questions=questions)


@app.route('/new_question', methods=['POST'])
def add_question():
    question_details = {'id': request.form.get('id'),
                        'submission_time': request.form.get('submission_time'),
                        'view_number': request.form.get('view_number'),
                        'vote_number': request.form.get('vote_number'),
                        'title': request.form.get('title'),
                        'message': request.form.get('message'),
                        'image': request.form.get('image'),
                        }
    data_handler.write_to_file('question.csv', question_details)
    labels = ['New Question', 'Post', 'Return']
    max_id = int(data_handler.get_id('question.csv'))
    return render_template('new_question.html', question=question_details, labels=labels, max_id=max_id)


@app.route('/answers/<id>')
def list_answers(id=None):
    pass


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
)