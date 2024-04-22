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
    temp = [el.id for el in db_sess.query(RecCat).filter(RecCat.id_cats == 1).all()]
    soups = db_sess.query(Recipe).filter(Recipe.id.in_(temp)).all()
    return render_template('list_soups.html', soups=soups)


@app.route('/soup/<int:pk>')
def soup(pk):
    db_sess = db_session.create_session()
    img = db_sess.query(Image).filter(Image.id==db_sess.query(RecImage).filter(RecImage.id_rec==pk).first().id_images).first()
    print(img.file)
    soup = db_sess.query(Recipe).filter(Recipe.id==pk).first()
    return render_template('detail_soup.html', soup=soup, img=img.file)


@app.route('/drinks')
def drinks():
    db_sess = db_session.create_session()
    temp = [el.id for el in db_sess.query(RecCat).filter(RecCat.id_cats == 3).all()]
    drinks = db_sess.query(Recipe).filter(Recipe.id.in_(temp)).all()
    return render_template('list_drinks.html', drinks=drinks)


@app.route('/drink/<int:pk>')
def drink(pk):
    db_sess = db_session.create_session()
    drink = db_sess.query(Recipe).filter(Recipe.id==pk).first()
    return render_template('detail_drink.html', drink=drink)


@app.route('/desserts')
def desserts():
    db_sess = db_session.create_session()
    temp = [el.id for el in db_sess.query(RecCat).filter(RecCat.id_cats == 4).all()]
    desserts = db_sess.query(Recipe).filter(Recipe.id.in_(temp)).all()
    return render_template('list_desserts.html', desserts=desserts)


@app.route('/dessert/<int:pk>')
def dessert(pk):
    db_sess = db_session.create_session()
    dessert = db_sess.query(Recipe).filter(Recipe.id==pk).first()
    return render_template('detail_dessert.html', dessert=dessert)


@app.route('/salads')
def salads():
    db_sess = db_session.create_session()
    temp = [el.id for el in db_sess.query(RecCat).filter(RecCat.id_cats == 5).all()]
    salads = db_sess.query(Recipe).filter(Recipe.id.in_(temp)).all()
    return render_template('list_salads.html', salads=salads)


@app.route('/salad/<int:pk>')
def salad(pk):
    db_sess = db_session.create_session()
    salad = db_sess.query(Recipe).filter(Recipe.id==pk).first()
    return render_template('detail_salad.html', salad=salad)


@app.route('/second_dishes')
def second_dishes():
    db_sess = db_session.create_session()
    temp = [el.id for el in db_sess.query(RecCat).filter(RecCat.id_cats == 2).all()]
    second_dishes = db_sess.query(Recipe).filter(Recipe.id.in_(temp)).all()
    return render_template('list_second_dishes.html', second_dishes=second_dishes)


@app.route('/second_dish/<int:pk>')
def second_dish(pk):
    db_sess = db_session.create_session()
    second_dish = db_sess.query(Recipe).filter(Recipe.id==pk).first()
    return render_template('detail_second_dish.html', second_dish=second_dish)


if __name__ == '__main__':
    db_session.global_init("db/rec.db")
    app.run(port=8080, host='127.0.0.1')
