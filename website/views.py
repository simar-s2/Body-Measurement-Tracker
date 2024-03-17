from flask import Blueprint, render_template, request, redirect, flash, url_for
import plotly.graph_objects as go
from flask_login import login_required, current_user
from . import db
from .models import Measurement

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    measurements = Measurement.query.filter_by(user_id=current_user.id).all()

    selected_data = request.args.get('data', 'weight')

    data_attributes = {
        'weight': ('Weight', 'weight', 'Weight (kg)'),
        'shoulder': ('Shoulder Circumference', 'shoulder', 'Shoulder Circumference (inches)'),
        'chest': ('Chest Circumference', 'chest', 'Chest Circumference (inches)'),
        'arm': ('Arm Circumference', 'arm', 'Arm Circumference (inches)'),
        'waist': ('Waist Circumference', 'waist', 'Waist Circumference (inches)'),
        'leg': ('Leg Circumference', 'leg', 'Leg Circumference (inches)'),
    }

    title, data_attr, y_label = data_attributes.get(selected_data, ('Weight', 'weight', 'Weight (kg)'))
    x_values = [measurement.date for measurement in measurements]
    y_values = [getattr(measurement, data_attr) for measurement in measurements]

    trace = go.Scatter(x=x_values, y=y_values, mode='lines+markers')
    layout = go.Layout(title=title, xaxis=dict(title='Date'), yaxis=dict(title=y_label))
    fig = go.Figure(data=[trace], layout=layout)

    fig.update_layout(plot_bgcolor='rgba(0,212,255,0.2)', paper_bgcolor='rgba(0,0,0,0)')
    fig.update_traces(line_color='#f3172d', line={'width': 1.5})

    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='grey'
    )

    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='grey'
    )

    chart_html = fig.to_html(full_html=False)

    # Pass selected data to the template
    return render_template('home.html', chart_html=chart_html, selected_data=selected_data, user=current_user)

@views.route('/measurement', methods=['GET', 'POST'])
@login_required
def measurement():
    if request.method == 'POST':
        items = request.form.items()

        for key, value in items:
            if value == '':
                flash('Please fill in all the fields!', 'warning')
                return redirect('/measurement')
            try:
                value = float(value)
                if value < 0:
                    flash('Measurements cannot be negative!', 'warning')
                    return redirect('/measurement')
            except ValueError:
                flash('Please enter valid values!', 'warning')
                return redirect('/measurement')

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

        flash('Measurements saved successfully!', 'success')
        return redirect('/measurement')
    else:
        return render_template("measurement.html", user=current_user)

@views.route('/delete_entry/<int:measurement_id>', methods=["POST"])
def delete_entry(measurement_id):
    measurement = Measurement.query.get_or_404(measurement_id)
    db.session.delete(measurement)
    db.session.commit()
    flash('Entry deleted successfully!', 'success')
    return redirect('/history')

@views.route('/update_entry/<int:measurement_id>', methods=['GET', 'POST'])
def update_entry(measurement_id):
    if request.method == "POST":
        measurements = Measurement.query.get_or_404(measurement_id)
        items = request.form.items()

        for key, value in items:
            if value == '':
                flash('Please fill in all the fields!', 'warning')
                return render_template('update_entry.html', user=current_user)
            try:
                value = float(value)
                if value < 0:
                    flash('Measurements cannot be negative!', 'warning')
                    return render_template('update_entry.html', user=current_user)
            except ValueError:
                flash('Please enter valid values!', 'warning')
                return render_template('update_entry.html', user=current_user)

         # Update measurements
        measurements.weight = request.form['weight']
        measurements.shoulder = request.form['shoulder']
        measurements.chest = request.form['chest']
        measurements.arm = request.form['arm']
        measurements.waist = request.form['waist']
        measurements.leg = request.form['leg']
        
        db.session.commit()

        flash('Measurements updated successfully!', 'success')
        return redirect('/history')
    else:
        return render_template('update_entry.html', user=current_user)
    
@views.route('/history')
@login_required
def history():
    measurements = Measurement.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', user=current_user, measurements=measurements)

