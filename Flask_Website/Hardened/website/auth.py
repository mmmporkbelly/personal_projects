from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

# init blueprint
auth = Blueprint('auth', __name__)


# Define login, define what this page can receive. default is only get
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Query into sql
        user = User.query.filter_by(email=email).first()
        # Pass password hash into db and check
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # Remember user is logged in until logged out
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect username or password, try again', category='error')
        else:
            flash('Incorrect username or password, try again', category='error')
    data = request.form
    print(data)
    return render_template('login.html', user=current_user)


# Define logout, login_required decorator makes sure logout is not accessible unless logged in
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# Define signup
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        # input validation
        if user:
            flash('This email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif not strong_pw(password1):
            flash(
                'Passowrd must contain at least: one uppercase letter, one lowercase letter'
                ' one number, and one special character.'
            )
        else:
            # add user to db, make sure to hash pw
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            # Redirect to homepage
            return redirect(url_for('views.home'))
    return render_template('signup.html', user=current_user)


def strong_pw(password):
    special_char = '~`! @#$%^&*()_-+={[}]|\:;\"\'<,>.?/'
    strong_password = {
        'upper' : 0,
        'lower' : 0,
        'special': 0,
        'number': 0
    }
    for char in password:
        if char.isnumeric():
            strong_password['number'] += 1
        elif char.isalpha():
            if char.isupper():
                strong_password['upper'] += 1
            elif char.islower():
                strong_password['lower'] += 1
        elif char in special_char:
            strong_password['special'] += 1
    return all(True if y > 0 else False for x, y in strong_password.items())
