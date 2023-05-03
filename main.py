import datetime
import os
import sqlite3
from flask import Flask , render_template , redirect , request , Blueprint , jsonify , make_response , abort
from flask_login import LoginManager , login_user , logout_user , login_required , current_user
from flask_restful import Api
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms import PasswordField , BooleanField , SubmitField , EmailField , StringField , IntegerField , \
    SelectMultipleField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField , FileRequired , FileAllowed
from werkzeug.utils import secure_filename
from data import db_session
from data.categories import Categories
from data.products import Products
from data.user_resource import UsersResource , UsersListResource
from data.products_resource import ProductsResource , ProductsListResource
from data.users import User
from data import products_api , user_api

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg' , '.png' , '.gif']
app.config['UPLOAD_PATH'] = 'static/uploads'
login_manager = LoginManager()
login_manager.init_app(app)


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


def search_results(query):
    conn = sqlite3.connect('db/db_avito.db')
    cur = conn.cursor()
    results = cur.execute(f'SELECT * FROM products WHERE name LIKE "{query}%"').fetchall()
    conn.close()
    return results


file_storage = [str(i) for i in range(2 ** 16)]
last_stored = 0
db_session.global_init("db/db_avito.db")
dbs = db_session.create_session()
"""for el in dbs.query(Products):
    print(el.name)"""
dbs.commit()


class LoginForm(FlaskForm):
    email = EmailField('Почта' , validators=[DataRequired()])
    password = PasswordField('Пароль' , validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class notForm(FlaskForm):
    submit = SubmitField('Отправить сообщение владельцу')


class RegisterForm(FlaskForm):
    email = EmailField('Логин (email)' , validators=[DataRequired()])
    password = PasswordField('Пароль' , validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль' , validators=[DataRequired()])
    surname = StringField('Фамилия' , validators=[DataRequired()])
    name = StringField('Имя' , validators=[DataRequired()])
    address = StringField('Адрес' , validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class ProductForm(FlaskForm):
    name = StringField('Название товара' , validators=[DataRequired()])
    price = IntegerField('Цена' , validators=[DataRequired()])
    description = StringField('Описание товара' , validators=[DataRequired()])
    image = FileField('Фото товара' ,
                      validators=[DataRequired() , FileRequired() , FileAllowed(['jpg' , 'jpeg' , 'png'])])
    categories = SelectMultipleField('Категория товара' , choices=[] , validators=[DataRequired()])
    owner_email = SelectField('Владелец (email)' , choices=[] , validators=[DataRequired()])
    submit = SubmitField('Submit')


class balanceadd(FlaskForm):
    summ = IntegerField('Количество' , validators=[DataRequired()])
    submit = SubmitField('Submit')
    # card_number = IntegerField('номер карты', validators=[DataRequired()])


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    return render_template('handle_authentification.html')


@app.route("/profile")
def profile():
    return render_template('profile.html' , balance=current_user.balance)


@app.route("/balancee" , methods=['GET' , 'POST'])
def balance():
    form = balanceadd()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        bala = db_sess.query(User).filter(User.id == current_user.id).first()
        bala.balance += int(form.summ.data)
        db_sess.add(bala)
        db_sess.commit()
        return redirect('/profile')

    return render_template('add_balance.html' , form=form)


@app.route('/login' , methods=['GET' , 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user , remember=form.remember_me.data)
            return redirect("/all_products")
        else:
            return render_template('login.html' , message="Неправильный логин или пароль!" , form=form)
    return render_template('login.html' , title='Авторизация' , form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register' , methods=['GET' , 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html' , title='Register form' ,
                                   form=form ,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html' , title='Register form' ,
                                   form=form ,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data ,
            email=form.email.data ,
            surname=form.surname.data ,
            address=form.address.data ,
            balance=0)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html' , title='Register form' , form=form)


@app.route('/all_products')
@login_required
def all_products():
    db_sess = db_session.create_session()
    data = []
    note = False
    mala = []
    bala = db_sess.query(User).filter(User.id == current_user.id).first()
    for el in db_sess.query(Products):
        if el.notification:
            if el.owner == bala.id:
                note = True
                mala.append(el.name)
                boss = db_sess.query(Products).filter(Products.id == el.id).first()
                boss.notification = 0
                db_sess.add(boss)
                db_sess.commit()
    for el in db_sess.query(Products):
        if el.owner != current_user.id:
            data.append((el.id , el.name , el.price , el.description , el.image , el.categories , el.owner))
    categs = []
    for el in db_sess.query(Categories).all():
        categs.append([el.id , el.name])

    return render_template('allproducts.html' , itemData=parse(data) , categs=categs , message=note ,
                           name=', '.join(mala))


@app.route('/search' , methods=['POST'])
def search():
    query = request.form['query']
    products = []
    for el in search_results(query.lower()):
        products.append(el)
    return render_template('search_results.html' , query=query , products_table=parse(products))


@app.route('/display_category/<int:id>')
@login_required
def display_category(id):
    db_sess = db_session.create_session()
    data = []
    for el in db_sess.query(Products):
        if el.owner != current_user.id and str(id) in str(el.categories).split(", "):
            data.append((el.id , el.name , el.price , el.description , el.image , el.categories , el.owner))
    x = db_sess.query(Categories).filter(Categories.id == id).first().name
    categs = []
    for el in db_sess.query(Categories).all():
        categs.append([el.id , el.name])
    return render_template('display_category.html' , category=x , itemData=parse(data) , categs=categs)


@app.route('/product_description/<int:product_id>')
@login_required
def product_description(product_id):
    note = False
    form = notForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        bala = db_sess.query(Products).filter(Products.id == product_id).first()
        bala.notification = 1
        db_sess.add(bala)
        db_sess.commit()
        return redirect('/all_products')

    dbs = db_session.create_session()
    el = dbs.query(Products).filter(Products.id == product_id).first()
    product_data = (el.id , el.name , el.price , el.description , el.image , el.categories , el.owner)
    user = dbs.query(User).filter(User.id == el.owner).first()
    address = user.address
    owner = user.name + user.surname + '' + "\nКонтактные данные: " + user.email
    if current_user.id != el.owner:
        f = True
    else:
        f = False
    return render_template("product_description.html" , data=product_data , owner=owner , note=note ,
                           address=address , f=f , form=form)


@app.route('/add_product' , methods=['GET' , 'POST'])
@login_required
def add_product():
    global last_stored
    form = ProductForm()
    dbs = db_session.create_session()
    categs = dbs.query(Categories).all()
    for el in dbs.query(User).all():
        form.owner_email.choices.append(el.email)
    for el in categs:
        form.categories.choices.append(el.name)
    filename = ''
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        prod = Products()
        prod.owner = current_user.id
        prod.name = form.name.data

        f = form.image.data
        filename = secure_filename(f.filename)
        if filename == '':
            filename = f"/{file_storage[last_stored]}"
            last_stored += 1
        prod.image = filename
        f.save(os.path.join(app.config['UPLOAD_PATH'] , filename))

        prod.description = form.description.data
        prod.price = form.price.data
        categs_names = map(lambda x: x.name , categs)
        last_categ_id = max(map(lambda x: int(x.id) , categs))
        categories = []
        x = form.categories.data
        if x is None:
            x = []
        for el in x:
            categories.append(dbs.query(Categories).filter(Categories.name == el).first().id)
        prod.categories = (', '.join(map(str , categories)))
        db_sess.add(prod)
        db_sess.commit()
        return redirect("/all_products")
    return render_template('add_product.html' , form=form , filename=filename)


@app.route('/add_product/<int:id>' , methods=['GET' , 'POST'])
@login_required
def edit_prod(id):
    global last_stored
    form = ProductForm()
    dbs = db_session.create_session()
    categs = dbs.query(Categories).all()
    for el in dbs.query(User).all():
        form.owner_email.choices.append(el.email)
    for el in categs:
        form.categories.choices.append(el.name)
    filename = ""
    if request.method == "GET":
        prod = dbs.query(Products).filter((Products.id == id) , (Products.owner == current_user.id)).first()
        if prod:
            prod.owner = current_user.id
            prod.name = form.name.data
            f = form.image.data
            if f is not None:
                filename = secure_filename(f.filename)
                if filename == '':
                    filename = f"/{file_storage[last_stored]}"
                    last_stored += 1
                prod.image = filename
                f.save(os.path.join(app.config['UPLOAD_PATH'] , filename))

            prod.description = form.description.data
            prod.price = form.price.data

            categs_names = map(lambda x: x.name , categs)
            last_categ_id = max(map(lambda x: int(x.id) , categs))
            categories = []
            x = form.categories.data
            if x is None:
                x = []
            for el in x:
                categories.append(dbs.query(Categories).filter(Categories.name == el).first().id)
            prod.categories = ', '.join(map(str , categories))
            dbs.add(prod)
            dbs.commit()
        else:
            pass
    if form.validate_on_submit():
        dbs = db_session.create_session()
        prod = dbs.query(Products).filter((Products.id == id) , (Products.owner == current_user.id)).first()
        res = dbs.query(User).all()
        for el in res:
            form.owner_email.choices.append(el.email)
        if not res:
            return render_template('add_product.html' , message='Неверно указана почта' , form=form)
        if prod:
            prod.owner = current_user.id
            prod.name = form.name.data
            f = form.image.data
            if f is not None:
                filename = secure_filename(f.filename)
                if filename == '':
                    filename = f"/{file_storage[last_stored]}"
                    last_stored += 1
                prod.image = filename
                f.save(os.path.join(app.config['UPLOAD_PATH'] , filename))

            prod.description = form.description.data
            prod.price = form.price.data
            categories = []
            x = form.categories.data
            if x is None:
                x = []
            for el in x:
                categories.append(dbs.query(Categories).filter(Categories.name == el).first().id)
            prod.categories = ', '.join(map(str , categories))

            dbs.add(prod)
            dbs.commit()
            return redirect('/all_products')
        else:
            pass
    return render_template('add_product.html' , form=form , filename=filename)


@app.route('/delete_product/<int:id>' , methods=['GET' , 'POST'])
@login_required
def delete_prod(id):
    dbs = db_session.create_session()
    product = dbs.query(Products).filter((Products.id == id) , (Products.owner == current_user.id)).first()
    if product:
        dbs.delete(product)
        dbs.commit()
    else:
        pass
    return redirect('/all_products')


@app.route('/users_products')
@login_required
def users_products():
    db_sess = db_session.create_session()
    data = []
    for el in db_sess.query(Products):
        if el.owner == current_user.id:
            data.append((el.name , el.description , el.price , el.categories , el.id))
    return render_template('users_products.html' , data=data)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}) , 400)


if __name__ == '__main__':
    db_session.global_init("db/db_avito.db")
    app.register_blueprint(products_api.blueprint)
    app.register_blueprint(user_api.blueprint)
    api.add_resource(UsersListResource , '/api/v2/users')
    api.add_resource(UsersResource , '/api/v2/users/<int:user_id>')
    api.add_resource(ProductsListResource , '/api/v2/products')
    api.add_resource(ProductsResource , '/api/v2/products/<int:product_id>')
    app.run(port=8080 , host='127.0.0.1')
