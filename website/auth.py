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
    # Check if the request method is POST (when form is submitted)
    if request.method == "POST":
        # Get the email and password from the form data
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if email and password fields are not empty
        if not email or not password:
            flash('Please fill in all the fields!', 'warning')
            return redirect('/login')

        # Query the database to find a user with the provided email
        user = User.query.filter_by(email=email).first()
        if user:
            # If a user is found, check if the provided password matches the hashed password stored in the database
            if check_password_hash(user.password, password):
                # If passwords match, log in the user and redirect to the home page
                flash('Logged in successfully!', 'success')
                login_user(user, remember=True)
                return redirect('/')
            else:
                # If passwords don't match, display an error message
                flash('Incorrect password, try again!')
        else:
            # If no user is found with the provided email, display an error message
            flash('Account does not exist!')

        # Redirect the user back to the login page after processing the login attempt
        return redirect('/login')
    else:
        # If the request method is GET (when accessing the login page), log out any currently logged-in user
        logout_user()
        # Render the login page template
        return render_template('login.html', user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # Check if the request method is POST (when form is submitted)
    if request.method == "POST":
        # Get the email, password, and password confirmation from the form data
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        
        # Check if any of the required fields are empty
        if not email or not password or not confirm:
            flash('Please fill in all the fields!', 'warning')
            return redirect('/sign-up')
        # Validate the password using a custom validation function
        elif not validate_password(password):
            flash('Please enter a valid password!', 'warning')
            return redirect('/sign-up')
        # Check if the password and confirmation match
        elif password != confirm:
            flash('Passwords do not match!', 'warning')
            return redirect('/sign-up')

        # Check if a user with the provided email already exists
        user = User.query.filter_by(email=email).first()
        if user:
            # If a user with the provided email already exists, display an error message
            flash('User already exists!')
            return redirect('/sign-up')

        # If all checks pass, create a new user object with the provided email and hashed password
        new_user = User(email=email, password=generate_password_hash(password))
        # Add the new user to the database session and commit the changes
        db.session.add(new_user)
        db.session.commit()

        # Log in the new user and redirect to the home page
        login_user(new_user, remember=True)
        flash('Account Created!', 'success')
        return redirect('/')
    else:
        # If the request method is GET (when accessing the signup page), log out any currently logged-in user
        logout_user()
        # Render the signup page template
        return render_template('sign-up.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    # Log out the currently logged-in user
    logout_user()
    # Flash a success message indicating successful logout
    flash('Logged out Successfully!', 'success')
    # Redirect the user to the login page
    return redirect('/login')

@auth.route('/settings', methods=["GET", "POST"])
@login_required
def settings():
    if request.method == 'POST':
        # Fetch the current user from the database
        user = User.query.filter_by(id=current_user.id).first()
        # Delete the user from the database
        db.session.delete(user)
        # Commit the changes
        db.session.commit()
        # Flash a success message to indicate successful account deletion
        flash('Account has been successfully deleted, we are sad to see you go!', 'success')
        # Redirect the user to the login page after account deletion
        return redirect('/login')
    else:
        # Render the settings page for the user
        return render_template('settings.html', user=current_user)


@auth.route('/change_email', methods=["GET", "POST"])
@login_required
def change_email():
    if request.method == "POST":
        # Get the new email from the form
        email = request.form.get('email')
        # Check if the email is already in use
        existing_user = User.query.filter_by(email=email).first()
        # Flash a warning if the email is empty
        if not email:
            flash('Please enter an email!', 'warning')
        # Flash a warning if the email is already in use
        if existing_user != None:
            flash("Email Address is in use!")
            # Redirect the user back to the change email page
            return redirect('/change_email')
        
        # Fetch the current user from the database
        user = User.query.filter_by(id=current_user.id).first()
        # Update the user's email
        user.email = email
        # Commit the changes to the database
        db.session.commit()
        # Flash a success message to indicate email update
        flash(f"Email has been updated to {email}!", "success")

        # Redirect the user to the settings page
        return redirect('/settings')
    else:
        # Render the change email page for the user
        return render_template("change_email.html", user=current_user)


@auth.route('/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        # Get the new password and confirmation from the form
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        # Check if both fields are filled
        if not password or not confirm:
            flash('Please fill in all the fields!', 'warning')
            return redirect('/change_password')
        # Check if the passwords match
        elif password != confirm:
            flash('Passwords do not match', 'warning')
            return redirect('/change_password')
        # Check if the password meets the validation criteria
        elif not validate_password(password):
            flash('Please enter a valid password!', 'warning')
            return redirect('/change_password')
        
        # Fetch the current user from the database
        user = User.query.filter_by(id=current_user.id).first()
        # Update the user's password with the hashed version of the new password
        user.password = generate_password_hash(password)
        # Commit the changes to the database
        db.session.commit()
        # Flash a success message to indicate password update
        flash("Password has been updated!", "success")

        # Redirect the user to the settings page
        return redirect('/settings')
    else:
        # Render the change password page for the user
        return render_template("change_password.html", user=current_user)
