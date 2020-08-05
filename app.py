from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask_login import LoginManager
from UserModel import UserModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'KuTkUdAk'
db = SQLAlchemy(app)

login_manager = LoginManager(app)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    info = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    image__path = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Products %r>' % self.id


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<UserInfo %r' % self.id


@login_manager.user_loader
def load_user(user_id):
    return UserModel().FromDB(user_id, UserInfo)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/products')
def products__page():
    products = Products.query.order_by(Products.id).all()
    return render_template('products.html', products=products)


@app.route('/products/<int:id>')
def products__more__detail(id):
    product = Products.query.get(id)
    return render_template('about__product.html', product=product)


@app.route('/products/<int:id>/delete')
def product__delete(id):
    product = Products.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return redirect('/products')
    except:
        return "ERROR"


@app.route('/products/<int:id>/update', methods=['GET', 'POST'])
def product__update(id):
    product = Products.query.get(id)
    if request.method == "POST":
        product.name = request.form['name']
        product.date = request.form['date']
        product.info = request.form['info']
        temp__path = request.form['image']
        if temp__path != "":
            product.image__path = f"img/products/{temp__path}"
        try:
            db.session.commit()
            return redirect('/products')
        except:
            return "ERROR"
    else:
        return render_template('update__page.html', product=product)


@app.route('/products/append', methods=['GET', 'POST'])
def append__product():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        info = request.form['info']
        image__name = request.form['image']

        image__path = "img/products/" + image__name.split('/')[-1]
        new__product = Products(name=name, date=date, info=info, image__path=image__path)
        try:
            db.session.add(new__product)
            db.session.commit()
            return redirect('/products')
        except:
            return "ERROR"

    else:
        return render_template('append__product.html')


@app.route('/reviews')
def reviews__page():
    return render_template('reviews.html')


@app.route('/basket')
def shopping__basket__page():
    return render_template('basket.html')


@app.route('/about')
def about__page():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register__page():
    if request.method == 'POST':
        login = request.form['login']
        psw = request.form['psw']
        selector = set([user.login != login for user in UserInfo.query.order_by(UserInfo.login).all()])
        if len(selector) == 2:
            flash(message='This user is already used in system', category='error')
        else:
            user = UserInfo(login=login, password=psw)
            try:
                db.session.add(user)
                db.session.commit()
                flash('You are successful registered on the service', category='successful')
                return redirect('/')
            except:
                return "ERROR"
    return render_template('register__page.html')


@app.route('/login', methods=['GET', 'POST'])
def login__page():
    if request.method == 'POST':
        user__from__db = UserInfo.query
    else:
        flash('User successful entered', category='successful')
        return redirect('/')


if __name__ == '__main__':
    app.run()
