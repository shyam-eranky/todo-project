import functools

from flask import(Blueprint,flash,g,redirect,render_template,request,session,url_for)
from . import db
from todoapp.models import User
from todoapp.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user

bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('tasks.index'))


@bp.route('/login', methods=('GET','POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.index'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('tasks.index'))
        
    return render_template('auth/login.html',title='Sign In', form=form)


@bp.route('/register', methods=('GET','POST'))
def register():
    form = RegisterForm()
    error = None

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            error = "User {} already exists".format(form.username.data)

        if error is None:
            user = User(form.username.data,form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registered user {} successfully, email={}'.format(
            form.username.data, form.email.data))
            return redirect(url_for('auth.login'))
        else:
            flash(error)

    return render_template('auth/register.html',title='Register', form=form)
