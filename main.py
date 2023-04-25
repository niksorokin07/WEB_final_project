from flask import Flask, render_template, redirect, request, Blueprint, jsonify, make_response, abort
import os
import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, StringField, IntegerField
from wtforms import FileField, SelectField
from wtforms.validators import DataRequired
from data import db_session
from data.db_session import SqlAlchemyBase
from data.users import User
from data.products import Products
from data.categories import Categories
from data.user_resource import UsersResource, UsersListResource
import sqlalchemy
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'static/uploads'
login_manager = LoginManager()
login_manager.init_app(app)

blueprint = Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(4):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans


db_session.global_init("db/blogs.db")
dbs = db_session.create_session()
"""for el in dbs.query(Products):
    print(el.name)"""
dbs.commit()


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age')
    position = StringField('Position')
    speciality = StringField('Speciality')
    address = StringField("Address")
    submit = SubmitField('Register')


class ProductForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    description = StringField('Описание товара', validators=[DataRequired()])
    image = FileField('Фото товара', validators=[DataRequired()])
    category = StringField('Категория', default=0)
    owner_email = SelectField('Владелец (email)', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')


class balanceadd(FlaskForm):
    summ = IntegerField('Колтчество', validators=[DataRequired()])
    way = owner_email = SelectField('Владелец (email)', choices=['Карта', 'Киви кошелек'], validators=[DataRequired()])
    submit = SubmitField('Submit')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    return render_template('handle_authentification.html')


@app.route("/")
@app.route("/profile")
def profile():
    User.balance = 100
    return render_template('profile.html', balance=User.balance)


@app.route("/")
@app.route("/balancee", methods=['GET', 'POST'])
def balance():
    form = balanceadd()
    if form.validate_on_submit():
        User.balance = form.summ
        # User.balance += form.summ
        return redirect('/')
    return render_template('add_balance.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        else:
            return render_template('login.html', message="Неправильный логин или пароль!", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register form',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register form',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            address=form.address.data,
            speciality=form.speciality.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Register form', form=form)


@app.route('/all_products')
@login_required
def all_products():
    db_sess = db_session.create_session()
    data = []
    for el in db_sess.query(Products):
        data.append((el.id, el.name, el.price, el.description, el.image, el.category, el.owner))
    return render_template('allproducts.html', itemData=parse(data))


@app.route('/product_description/<int:product_id>')
@login_required
def product_description(product_id):
    dbs = db_session.create_session()
    el = dbs.query(Products).filter(Products.id == product_id).first()
    product_data = (el.id, el.name, el.price, el.description, el.image, el.category, el.owner)
    user = dbs.query(User).filter(User.id == el.owner).first()
    owner = user.name + user.surname + '' + "\nКонтактные данные: " + user.email
    return render_template("product_description.html", data=product_data, owner=owner)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    dbs = db_session.create_session()
    res = dbs.query(User).all()
    for el in res:
        form.owner_email.choices.append(el.email)
    filename = ''
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        prod = Products()
        prod.owner = current_user.id
        prod.name = form.name.data
        uploaded_file = form.image.data
        filename = uploaded_file.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            prod.image = filename
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        prod.description = form.description.data
        prod.price = form.price.data
        categ = Categories()
        categ.name = form.category.data
        prod.category.append(categ)
        db_sess.add(prod)
        db_sess.commit()
        return redirect("/all_products")
    return render_template('add_product.html', form=form, file=filename)


@app.route('/add_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = ProductForm()
    dbs = db_session.create_session()
    res = dbs.query(User).all()
    for el in res:
        form.owner_email.choices.append(el.email)
    if request.method == "GET":
        prod = dbs.query(Products).filter((Products.id == id), (Products.user == current_user)).first()
        if prod:
            prod.owner = current_user.id
            prod.name = form.name.data
            uploaded_file = form.image.data
            filename = uploaded_file.filename
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    abort(400)
                prod.image = filename
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            prod.description = form.description.data
            prod.price = form.price.data
            categ = Categories()
            categ.name = form.category.data
            prod.category.append(categ)
            dbs.add(prod)
            dbs.commit()
        else:
            pass
    if form.validate_on_submit():
        dbs = db_session.create_session()
        prod = dbs.query(Products).filter((Products.id == id), (Products.owner == current_user)).first()
        res = dbs.query(User).all()
        for el in res:
            form.owner_email.choices.append(el.email)
        if not res:
            return render_template('add_product.html', message='Неверно указана почта', form=form)
        if prod:
            prod.owner = current_user.id
            prod.name = form.name.data
            uploaded_file = form.image.data
            filename = uploaded_file.filename
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    abort(400)
                prod.image = filename
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            prod.description = form.description.data
            prod.price = form.price.data
            categ = Categories()
            categ.name = form.category.data
            prod.category.append(categ)
            dbs.add(prod)
            dbs.commit()
            return redirect('/all_products')
        else:
            pass
    return render_template('add_product.html', form=form)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    dbs = db_session.create_session()
    product = dbs.query(Products).filter((Products.id == id), (Products.owner == current_user)).first()
    if product:
        dbs.delete(product)
        dbs.commit()
    else:
        pass
    return redirect('/all_products')


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    api.add_resource(UsersListResource, '/api/v2/users')
    api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')
    app.run(port=8080, host='127.0.0.1')
