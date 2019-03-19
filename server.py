from flask import Flask, render_template

import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list():
    questions = data_handler.get_all_details('question.csv')
    return render_template('list.html', questions=questions)


@app.route('/new-question')
def add_new_question():
    pass


@app.route('/answers/<id>')
def list_answers(id=None):
    pass


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
