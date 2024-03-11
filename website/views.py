from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/measurement', methods=['GET', 'POST'])
@login_required
def measurement():
    if request.method == 'POST':
        pass
    else:
        return render_template("measurement.html", user=current_user)
    