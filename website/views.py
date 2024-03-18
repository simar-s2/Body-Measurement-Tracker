from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from . import db
from .models import Measurement
import plotly.graph_objects as go

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    """
    Render the home page with a plot of measurements.

    Returns:
        rendered page: Renders the home page with a plot of measurements.

    Notes:
        This route fetches the measurements for the current user from the database
        and generates a plot based on the selected data type (e.g., weight, shoulder circumference).
        It retrieves the selected data type from the request parameters and uses predefined
        attributes to customize the plot title, data attribute, and y-axis label accordingly.
        The plot is created using Plotly, and its layout and appearance are customized before
        rendering the home page template.
    """
    measurements = Measurement.query.filter_by(user_id=current_user.id).all()

    selected_data = request.args.get('data', 'weight')

    # Define attributes for different data types
    data_attributes = {
        'weight': ('Weight', 'weight', 'Weight (kg)'),
        'shoulder': ('Shoulder Circumference', 'shoulder', 'Shoulder Circumference (inches)'),
        'chest': ('Chest Circumference', 'chest', 'Chest Circumference (inches)'),
        'arm': ('Arm Circumference', 'arm', 'Arm Circumference (inches)'),
        'waist': ('Waist Circumference', 'waist', 'Waist Circumference (inches)'),
        'leg': ('Leg Circumference', 'leg', 'Leg Circumference (inches)'),
    }

    # Retrieve data attributes based on selected data type
    title, data_attr, y_label = data_attributes.get(selected_data, ('Weight', 'weight', 'Weight (kg)'))
    x_values = [measurement.date for measurement in measurements]
    y_values = [getattr(measurement, data_attr) for measurement in measurements]

    # Create plot
    trace = go.Scatter(x=x_values, y=y_values, mode='lines+markers')
    layout = go.Layout(title=title, xaxis=dict(title='Date'), yaxis=dict(title=y_label))
    fig = go.Figure(data=[trace], layout=layout)

    # Customize plot layout
    fig.update_layout(plot_bgcolor='rgba(0,212,255,0.2)', paper_bgcolor='rgba(0,0,0,0)')
    fig.update_traces(line_color='#f3172d', line={'width': 1.5})
    fig.update_xaxes(mirror=True, ticks='outside', showline=True, linecolor='black', gridcolor='grey')
    fig.update_yaxes(mirror=True, ticks='outside', showline=True, linecolor='black', gridcolor='grey')

    chart_html = fig.to_html(full_html=False)

    return render_template('home.html', chart_html=chart_html, selected_data=selected_data, user=current_user)


@views.route('/measurement', methods=['GET', 'POST'])
@login_required
def measurement():
    """
    View for adding new measurements.

    Returns:
        rendered page: Renders the measurement page for adding new measurements.

    Notes:
        This route handles both GET and POST requests for adding new measurements.
        For POST requests, it validates the form data, saves new measurements to the database,
        and displays success or warning flash messages accordingly. For GET requests,
        it renders the measurement page.
    """
    if request.method == 'POST':
        # Validate and save new measurements
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

        # Create new Measurement instance and add it to the database
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
    """
    Delete a measurement entry.

    Args:
        measurement_id (int): The ID of the measurement entry to be deleted.

    Returns:
        redirected page: Redirects the user to the history page after successfully deleting the entry.

    Notes:
        This route handles POST requests to delete a specific measurement entry identified by its ID.
        It retrieves the measurement entry from the database, deletes it, and commits the changes.
        After successful deletion, a success flash message is displayed, and the user is redirected
        to the history page.
    """
    measurement = Measurement.query.get_or_404(measurement_id)
    db.session.delete(measurement)
    db.session.commit()
    flash('Entry deleted successfully!', 'success')
    return redirect('/history')


@views.route('/update_entry/<int:measurement_id>', methods=['GET', 'POST'])
def update_entry(measurement_id):
    """
    Update a measurement entry.

    Args:
        measurement_id (int): The ID of the measurement entry to be updated.

    Returns:
        rendered template: Renders the 'update_entry.html' template for updating a measurement entry.

    Notes:
        This route handles both GET and POST requests. When receiving a POST request, it updates the
        measurement entry with the provided data. If any fields are missing or invalid, appropriate flash
        messages are displayed. After successful update, it redirects the user to the history page. If
        receiving a GET request, it renders the 'update_entry.html' template for updating the measurement
        entry.
    """
    if request.method == "POST":
        # Retrieve the measurement entry to be updated
        measurements = Measurement.query.get_or_404(measurement_id)
        items = request.form.items()

        # Validate and update measurement data
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
    """
    View for displaying measurement history.

    Returns:
        rendered template: Renders the 'history.html' template with user's measurement history.
    """
    # Query all measurements belonging to the current user
    measurements = Measurement.query.filter_by(user_id=current_user.id).all()
    # Render the 'history.html' template with the user object and measurements
    return render_template('history.html', user=current_user, measurements=measurements)