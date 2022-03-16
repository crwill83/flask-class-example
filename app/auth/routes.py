from flask import Blueprint, render_template, redirect, request, url_for
# import forms and models
from .forms import LoginForm, UserCreationForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__, template_folder='auth_templates')

from app.models import db

@auth.route('/login', methods=["GET", "POST"])
def logMeIn():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            remember_me = form.remember_me.data

            # check if user exists
            user = User.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=remember_me)
                    return redirect(url_for('home'))
            return redirect(url_for('auth.logMeIn'))
    return render_template('login.html', form = form)

@auth.route('/signup', methods=["GET", "POST"])
def signMeUp():
    form = UserCreationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            # create an instance of our user
            user = User(username, email, password)

            # add instance to database
            db.session.add(user)
            # commit to databse
            db.session.commit()
            return redirect(url_for('auth.logMeIn'))

    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logMeOut():
    logout_user()
    return redirect(url_for('auth.logMeIn'))