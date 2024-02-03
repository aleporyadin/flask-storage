from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User, Role
from app.forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            form.username.errors.append('Invalid username or password')
            # Вместо flash и redirect используйте render_template
            return render_template('login.html', form=form)
        elif not user.check_password(form.password.data):
            form.password.errors.append('Invalid password')
            # Аналогично, отображаем шаблон с формой и ошибками
            return render_template('login.html', form=form)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_role = Role.query.filter_by(name='user').first()
        user = User(username=form.username.data, email=form.email.data, role=user_role)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
