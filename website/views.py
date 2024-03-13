from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from . import db
from .models import Measurement

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/measurement', methods=['GET', 'POST'])
@login_required
def measurement():
    if request.method == 'POST':
        items = request.form.items()

        for key, value in items:
            if value == '':
                flash('Please fill in all the fields!')
                return redirect('/measurement')

            try:
                value = float(value)
                if value < 0:
                    flash('Measurements cannot be negative!')
                    return redirect('/measurement')
            
            except ValueError:
                flash('Please enter valid values!')
                return redirect('/measurement')
            
            print(key, value)

         # Create a new Measurement instance and add it to the database
        measurements = Measurement(
            user_id=current_user.id,
            weight=request.form['weight'],
            shoulder=request.form['shoulder'],
            chest=request.form['chest'],
            arm=request.form['arm'],
            waist=request.form['waist'],
            leg=request.form['leg']
        )
        db.session.add(measurements)
        db.session.commit()

        flash('Measurements saved successfully!')
        return redirect('/measurement')
    else:
        return render_template("measurement.html", user=current_user)
    