from flask import Blueprint, render_template, request, redirect, flash
import plotly.graph_objects as go
import pandas as pd
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

    fig.update_layout(plot_bgcolor='white')
    fig.update_traces(line_color='red')

    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        gridcolor='lightgrey'
    )

    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        gridcolor='lightgrey'
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
    