from flask import Flask, render_template, request, redirect
from data import db_session
from data.users import User
from data.items import Items
from flask_login import LoginManager, login_user, current_user
from form.user import RegisterForm, LoginForm
from form.items import AddForm, DelForm, AddRentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'storage_yandex_secret_key'
db_session.global_init("db/storage.db")
login_manager = LoginManager()
login_manager.init_app(app)
items = Items()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("profile")
        return render_template('Unlogin.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('Unlogin.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('Registration.html',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('Registration.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('login')
    return render_template('Registration.html', form=form)


@app.route('/profile')
def profile():
    print('ll')
    return render_template('Profile.html',
                           name=current_user.name,
                           email=current_user.email,
                           index=current_user.id)


@app.route('/own_items')
def own_items():
    db_sess = db_session.create_session()
    items = db_sess.query(Items).filter(Items.owner_id == current_user.id)
    return render_template('own_items.html', items=items)


@app.route('/rent_items')
def rent_items():
    db_sess = db_session.create_session()
    items = db_sess.query(Items).filter(Items.rent_id == current_user.id)
    return render_template('rent_items.html', items=items)


@app.route('/add_own_item', methods=['GET', 'POST'])
def add_own_item():
    form = AddForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        new_item = Items(
            name=form.name.data,
            description=form.description.data,
            count=form.count.data,
            owner_id=current_user.id
        )
        db_sess.add(new_item)
        db_sess.commit()
        return redirect('own_items')
    return render_template('add_items.html', form=form)


@app.route('/del_own_item', methods=['GET', 'POST'])
def del_own_item():
    form = DelForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Items).filter(Items.name == form.name.data).first():
            del_item = db_sess.query(Items).filter(Items.name == form.name.data).first()
            db_sess.delete(del_item)
            db_sess.commit()
            return redirect('own_items')
        return render_template('del_items.html', form=form, message='Такого предмета на складе нет')
    return render_template('del_items.html', form=form)


@app.route('/del_rent_item', methods=['GET', 'POST'])
def del_rent_item():
    form = DelForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Items).filter(Items.name == form.name.data).first():
            del_item = db_sess.query(Items).filter(Items.name == form.name.data).first()
            del_item.rent_id = ''
            db_sess.commit()
            return redirect('rent_items')
        return render_template('del_items.html', form=form, message='Такого предмета на складе нет')
    return render_template('del_items.html', form=form)


@app.route('/add_rent_item', methods=['GET', 'POST'])
def add_rent_item():
    form = AddRentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Items).filter(Items.name == form.name.data).first():
            new_item = db_sess.query(Items).filter(Items.name == form.name.data).first()
            new_item.rent_id = current_user.id
            db_sess.commit()
            return redirect('rent_items')
        return render_template('add_rent_items.html', form=form, message='Такого предмета на складе нет')
    return render_template('add_rent_items.html', form=form)


def main():
    app.run()


if __name__ == '__main__':
    main()
