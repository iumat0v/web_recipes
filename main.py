import os

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

from flask_restful import reqparse, abort, Api, Resource

from data import db_session, recipes_resources
from data.recipes import Recipe
from data.cats import Cat
from data.rec_cats import RecCat
from data.images import Image
from data.rec_images import RecImage
from data.users import User
from forms.forms import RegisterForm, LoginForm, AddBldForm

UPLOAD_FOLDER = os.getcwd() + '\\static\\images'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main():
    return render_template('base.html', title='Книга рецептов')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_bld',  methods=['GET', 'POST'])
@login_required
def add_bld():
    form = AddBldForm()
    if request.method == 'POST':
        db_sess = db_session.create_session()
        rec = Recipe()
        image = Image()
        rec_cat = RecCat()
        rec_image = RecImage()
        rec.name = form.name.data
        rec.ingredients = form.ingr.data
        rec.recipe = form.rec.data
        db_sess.add(rec)
        db_sess.commit()

        file = request.files['img']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        image.file = 'images\\' + filename
        db_sess.add(image)
        db_sess.commit()
        id_rec = db_sess.query(Recipe).filter(Recipe.name == form.name.data).first().id
        id_cat = db_sess.query(Cat).filter(Cat.name == form.cat.data).first().id
        id_img = db_sess.query(Image).filter(Image.file == ('images\\' + filename)).first().id
        rec_cat.id_rec = id_rec
        rec_cat.id_cats = id_cat
        db_sess.add(rec_cat)
        rec_image.id_rec = id_rec
        rec_image.id_images = id_img
        db_sess.add(rec_image)
        db_sess.commit()
        return redirect('/')
    return render_template('add_bld.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/soups')
def soups():
    db_sess = db_session.create_session()
    temp = [el.id for el in db_sess.query(RecCat).filter(RecCat.id_cats == 1).all()]
    soups = db_sess.query(Recipe).filter(Recipe.id.in_(temp)).all()
    return render_template('list_soups.html', soups=soups, title='Супы')


@app.route('/soup/<int:pk>')
def soup(pk):
    db_sess = db_session.create_session()
    img = db_sess.query(Image).filter(
        Image.id == db_sess.query(RecImage).filter(RecImage.id_rec == pk).first().id_images).first()
    soup = db_sess.query(Recipe).filter(Recipe.id == pk).first()
    return render_template('detail_soup.html', soup=soup, img=img.file)


@app.route('/drinks')
def drinks():
    db_sess = db_session.create_session()
    temp = [el.id for el in db_sess.query(RecCat).filter(RecCat.id_cats == 3).all()]
    drinks = db_sess.query(Recipe).filter(Recipe.id.in_(temp)).all()
    return render_template('list_drinks.html', drinks=drinks, title='Напитки')


@app.route('/drink/<int:pk>')
def drink(pk):
    db_sess = db_session.create_session()
    img = db_sess.query(Image).filter(
        Image.id == db_sess.query(RecImage).filter(RecImage.id_rec == pk).first().id_images).first()
    drink = db_sess.query(Recipe).filter(Recipe.id==pk).first()
    return render_template('detail_drink.html', drink=drink, img=img.file)


@app.route('/desserts')
def desserts():
    db_sess = db_session.create_session()
    temp = [el.id for el in db_sess.query(RecCat).filter(RecCat.id_cats == 4).all()]
    desserts = db_sess.query(Recipe).filter(Recipe.id.in_(temp)).all()
    return render_template('list_desserts.html', desserts=desserts, title='Десерты')


@app.route('/dessert/<int:pk>')
def dessert(pk):
    db_sess = db_session.create_session()
    img = db_sess.query(Image).filter(
        Image.id == db_sess.query(RecImage).filter(RecImage.id_rec == pk).first().id_images).first()
    dessert = db_sess.query(Recipe).filter(Recipe.id == pk).first()
    return render_template('detail_dessert.html', dessert=dessert, img=img.file)


@app.route('/salads')
def salads():
    db_sess = db_session.create_session()
    temp = [el.id for el in db_sess.query(RecCat).filter(RecCat.id_cats == 5).all()]
    salads = db_sess.query(Recipe).filter(Recipe.id.in_(temp)).all()
    return render_template('list_salads.html', salads=salads, title='Салаты')


@app.route('/salad/<int:pk>')
def salad(pk):
    db_sess = db_session.create_session()
    img = db_sess.query(Image).filter(
        Image.id == db_sess.query(RecImage).filter(RecImage.id_rec == pk).first().id_images).first()
    salad = db_sess.query(Recipe).filter(Recipe.id == pk).first()
    return render_template('detail_salad.html', salad=salad, img=img.file)


@app.route('/second_dishes')
def second_dishes():
    db_sess = db_session.create_session()
    temp = [el.id for el in db_sess.query(RecCat).filter(RecCat.id_cats == 2).all()]
    second_dishes = db_sess.query(Recipe).filter(Recipe.id.in_(temp)).all()
    return render_template(
        'list_second_dishes.html', second_dishes=second_dishes, title='Вторые блюда')


@app.route('/second_dish/<int:pk>')
def second_dish(pk):
    db_sess = db_session.create_session()
    img = db_sess.query(Image).filter(
        Image.id == db_sess.query(RecImage).filter(RecImage.id_rec == pk).first().id_images).first()
    second_dish = db_sess.query(Recipe).filter(Recipe.id == pk).first()
    return render_template('detail_second_dish.html', second_dish=second_dish, img=img.file)


if __name__ == '__main__':
    db_session.global_init("db/rec.db")
    api.add_resource(recipes_resources.RecipeListResource, '/api/recipes')
    api.add_resource(recipes_resources.RecipeResource, '/api/recipes/<int:recipe_id>')
    api.add_resource(recipes_resources.RecipeListCategory, '/api/categoris/<int:category_id>')
    api.add_resource(recipes_resources.ListCategory, '/api/categoris')
    app.run(port=8080, host='127.0.0.1')
