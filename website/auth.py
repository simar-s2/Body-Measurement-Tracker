from flask import Blueprint, render_template, redirect, request, flash

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
    symbols = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
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
        print(f'{email} {password}')

        if not email or not password:
            flash('Please fill in all the fields')
        
        return redirect('/login')
    else:
        return render_template('login.html')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not email or not password or not confirm:
            flash('Please fill in all the fields')
        elif not validate_password(password):
            flash('Please enter a valid password')
        elif password != confirm:
            flash('Passwords do not match')

        
        
        return redirect('/sign-up')
    else:
        return render_template('sign-up.html')

@auth.route('/logout')
def logout():
    return redirect('/login')

