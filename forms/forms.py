from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddBldForm(FlaskForm):
    name = StringField('Название блюда', validators=[DataRequired()])
    cat = SelectField('Категория', choices=['Супы', 'Напитки', '2-ые блюда', 'Десерты', 'Салаты', 'Выпечка'])
    img = FileField('Фото блюда')
    ingr = TextAreaField('Ингридиенты')
    rec = TextAreaField('Рецепт')
    submit = SubmitField('Добавить')