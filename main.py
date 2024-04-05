from flask import Flask, render_template
from data import db_session


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('base.html')


@app.route('/soups')
def soups():
    return 'Soups'


@app.route('/drinks')
def drinks():
    return 'Drinks'


@app.route('/desserts')
def desserts():
    return 'desserts'


@app.route('/salads')
def salads():
    return 'salads'


@app.route('/second_dish')
def second_dish():
    return 'second dish'


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1')