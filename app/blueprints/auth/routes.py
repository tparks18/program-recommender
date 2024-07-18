from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import SignUpForm, LoginForm
from .models import User

@auth.route('/signup', methods=["GET", "POST"])
def signup():
    title = 'Sign Up'
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        signup_code = form.signup_code.data

        if signup_code != 'theFundAdmin2024!':
            flash('Invalid sign-up code', 'is-danger')
            return render_template('signup.html', title=title, form=form)

        users_with_that_info = User.query.filter((User.username == username) | (User.email == email)).all()
        if users_with_that_info:
            flash(f"There is already a user with that username and/or email. Please try again", "is-danger")
            return render_template('signup.html', title=title, form=form)

        new_user = User(email=email, username=username, password=password)
        
        flash(f"{new_user.username} has successfully signed up.", "is-success")
        return redirect(url_for('index'))

    return render_template('signup.html', title=title, form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Log In'
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'{user} has successfully logged in', 'is-success')
            return redirect(url_for('index'))
        else:
            flash('Username and/or password is incorrect', 'is-danger')
            
    return render_template('login.html', title=title, form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out', 'is-success')
    return redirect(url_for('index'))