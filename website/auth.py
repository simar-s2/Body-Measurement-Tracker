from flask import Blueprint, render_template, redirect, request, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# Function to check if user entered a valid password
def validate_password(p):
    # Checking password length
    if len(p) < 8:
        return False
    # Variables to check password
    has_lower = False
    has_upper = False
    has_digit = False
    has_symbol = False
    symbols = r"!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    # For loop to loop through characters
    for character in p:
        # If there is a lower character
        if character.islower():
            has_lower = True
        # If there is an upper character
        if character.isupper():
            has_upper = True
        # If there is a digit
        if character.isdigit():
            has_digit = True
        # If there is a symbol
        if character in symbols:
            has_symbol = True
    # Returning true if all conditions are met else false
    return has_lower and has_upper and has_digit and has_symbol


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash('Please fill in all the fields!', 'warning')
            return redirect('/login')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', 'success')
                login_user(user, remember=True)
                return redirect('/')
            else:
                flash('Incorrect password, try again!')
        else:
            flash('Account does not exist!')

        return redirect('/login')
    else:
        return render_template('login.html', user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        
        if not email or not password or not confirm:
            flash('Please fill in all the fields!', 'warning')
            return redirect('/sign-up')
        elif not validate_password(password):
            flash('Please enter a valid password!', 'warning')
            return redirect('/sign-up')
        elif password != confirm:
            flash('Passwords do not match!', 'warning')
            return redirect('/sign-up')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists!')
            return redirect('/sign-up')

        new_user = User(email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user, remember=True)
        flash('Account Created!', 'success')
        return redirect('/')
    else:
        return render_template('sign-up.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out Successfully!', 'success')
    return redirect('/login')


@auth.route('/settings', methods=["GET", "POST"])
@login_required
def settings():
    if request.method == 'POST':
        user = User.query.filter_by(id=current_user.id).first()
        db.session.delete(user)
        db.session.commit()
        flash('Account has been successfully deleted, we are sad to see you go!', 'success')
        return redirect('/login')

    else:
        return render_template('settings.html', user=current_user)


@auth.route('/change_email', methods=["GET", "POST"])
@login_required
def change_email():
    if request.method == "POST":
        email = request.form.get('email')
        existing_user = User.query.filter_by(email=email).first()
        print(existing_user)
        if not email:
            flash('Please enter an email!', 'warning')
        if existing_user != None:
            flash("Email Address is in use!")
            return redirect('/change_email')
        
        user = User.query.filter_by(id=current_user.id).first()
        user.email = email
        db.session.commit()
        flash(f"Email has been updated to {email}!", "success")

        return redirect('/settings')
    else:
        return render_template("change_email.html", user=current_user)


@auth.route('/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if not password or not confirm:
            flash('Please fill in all the fields!', 'warning')
            return redirect('/change_password')
        elif password != confirm:
            flash('Passwords do not match', 'warning')
            return redirect('/change_password')
        elif not validate_password(password):
            flash('Please enter a valid password!', 'warning')
            return redirect('/change_password')
        
        user = User.query.filter_by(id=current_user.id).first()
        user.password = generate_password_hash(password)
        db.session.commit()
        flash("Password has been updated!", "success")

        return redirect('/settings')
    else:
        return render_template("change_password.html", user=current_user)
