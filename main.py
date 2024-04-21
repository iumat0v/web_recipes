from flask import Flask, render_template
from data import db_session
from data.recipes import Recipe
from data.cats import Cat
from data.rec_cats import RecCat
from data.images import Image
from data.rec_images import RecImage


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('base.html')


@app.route('/soups')
def soups():
    db_sess = db_session.create_session()
    temp = [el.id for el in db_sess.query(RecCat).filter(RecCat.id_cats==1).all()]
    soups = db_sess.query(Recipe).filter(Recipe.id.in_(temp)).all()
    return render_template('list_soups.html', soups=soups)

@app.route('/soup/<int:pk>')
def soup(pk):
    db_sess = db_session.create_session()
    soup = db_sess.query(Recipe).filter(Recipe.id==pk).first()
    return render_template('detail_soup.html', soup=soup)
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
    db_session.global_init("db/rec.db")
    app.run(port=8080, host='127.0.0.1')