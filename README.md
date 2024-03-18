# Body Measurement Tracker Web App
#### Video Demo: 
#### Description:
This web application allows users to track their body measurements over time. Users can log in, add new measurements, view their measurement history, update existing entries, and delete entries. The app provides visualizations to help users visualize their progress over time.

## Features
- User authentication: Users can create an account, log in, and log out securely.
- Add measurements: Users can input their weight, shoulder circumference, chest circumference, arm circumference, waist circumference, and leg circumference.
- View measurement history: Users can see their measurement history in a tabular format and visualize it using interactive charts.
- Update measurements: Users can edit existing measurements to correct any mistakes or update their data.
- Delete measurements: Users can remove unwanted measurement entries.

## Technologies Used
- Python Flask: Backend web framework for handling HTTP requests, routing, and database interaction.
- Flask-SQLAlchemy: ORM (Object-Relational Mapping) for interacting with the SQLite database.
- Plotly: Library for creating interactive charts and data visualizations.
- Bootstrap: Frontend framework for designing responsive and visually appealing web pages.
- Jinja2: Template engine for rendering dynamic content in HTML templates.
- Werkzeug: Security module for password hashing and authentication.
- Flask-Login: Extension for managing user sessions and authentication.

## Installation
1. Clone the repository: `git clone https://github.com/simar-s2/Body-Measurement-Tracker.git`
2. Navigate to the project directory: `cd Body-Measurement-Tracker`
3. Install dependencies: `pip install -r requirements.txt`
5. Run the Flask app: `python app.py` or `flask run`
6. Access the application in your web browser at `http://localhost:5000`

## Usage
1. Register for a new account or log in with existing credentials.
2. Navigate to the "Add Measurement" page and input your measurements.
3. View your measurement history and visualizations on the home page.
4. Update or delete existing measurements as needed.
5. Log out when finished.

## Routes:

1. **Home Route (`/`):**
   - The home route serves as the landing page of the application, providing users with an overview of their measurements over time.
   - Users are presented with interactive charts that visualize their measurements, allowing them to track their progress.
   - The route offers the flexibility for users to select different types of measurements, such as weight, shoulder circumference, etc., enhancing the visualization experience.
   - The implementation leverages the Plotly library, a powerful tool for generating dynamic and interactive charts, to visualize measurement data effectively.
   - Flask is utilized for routing and handling HTTP requests, SQLAlchemy for database operations, and Jinja templating engine for rendering dynamic content within HTML templates.

2. **Measurement Route (`/measurement`):**
   - This route facilitates the process of adding new measurements to the database.
   - Users are presented with a form where they can input measurements for different body parts, such as weight, shoulder circumference, etc.
   - Client-side and server-side validation mechanisms ensure that user input is accurate and complete before saving it to the database.
   - Upon successful submission, the measurements are stored in the database, allowing users to track their progress over time.
   - The implementation utilizes Flask for routing and handling HTTP requests, SQLAlchemy for ORM operations to interact with the database, and Jinja templating engine for rendering dynamic HTML forms.

3. **History Route (`/history`):**
   - This route is responsible for displaying the measurement history of the user.
   - It retrieves all measurements associated with the current user from the database and renders them on a dedicated page.
   - The history is presented in a tabular format, making it easy for users to view their past measurements at a glance.
   - The implementation leverages Flask to handle routing and database interaction, SQLAlchemy for ORM (Object-Relational Mapping) to interact with the database, and Jinja templating engine for rendering dynamic HTML content.

4. **Update Entry Route (`/update_entry/<int:measurement_id>`):**
   - The Update Entry route manages the process of updating existing measurement entries in the database.
   - Users can access this route to edit the values of their previous measurements using a user-friendly form interface.
   - Upon submission of the form, the route updates the corresponding measurement entry in the database with the new values provided by the user.
   - Flask handles the routing and processing of HTTP requests, while SQLAlchemy facilitates interaction with the database to retrieve and update measurement data.
   - Jinja templating engine is employed to dynamically render the HTML form for editing measurement entries, ensuring a seamless user experience.

5. **Delete Entry Route (`/delete_entry/<int:measurement_id>`):**
   - The Delete Entry route facilitates the removal of existing measurement entries from the database.
   - Users can access this route to delete unwanted measurements from their history, providing a mechanism for data management and cleanup.
   - Upon deletion, the corresponding measurement entry identified by its unique ID is permanently removed from the database.
   - Flask routes HTTP requests to this route, and SQLAlchemy executes the deletion operation on the database backend.

6. **Authentication Routes (`/login`, `/sign-up`, `/logout`, `/settings`, `/change_email`, `/change_password`):**
   - The authentication routes handle user authentication and account management functionalities.
   - **Login Route (`/login`):**
     - Renders a login form for users to enter their credentials (email and password).
     - Validates user input and authenticates users against stored credentials in the database using Flask-Login and password hashing with Werkzeug.
     - Upon successful login, users are redirected to the home page, and a session is initiated.
   - **Sign-up Route (`/sign-up`):**
     - Renders a sign-up form for new users to register by providing their email and password.
     - Validates user input and ensures that passwords meet certain criteria using custom validation functions.
     - Upon successful registration, user data is stored in the database after hashing the password.
   - **Logout Route (`/logout`):**
     - Logs out the current user by terminating the session and clearing session data.
     - Redirects the user to the login page after logging out.
   - **Settings Route (`/settings`):**
     - Renders the account settings page where users can manage their account preferences.
     - Allows users to delete their account permanently.
   - **Change Email Route (`/change_email`):**
     - Renders a form for users to change their email address associated with their account.
     - Validates user input and ensures the new email address is not already in use.
     - Updates the user's email address in the database upon successful validation.
   - **Change Password Route (`/change_password`):**
     - Renders a form for users to change their account password.
     - Validates user input and ensures that passwords meet certain criteria using custom validation functions.
     - Updates the user's password in the database after hashing the new password.

For more details about each route, please refer to the corresponding route handlers in the `views.py` and `auth.py` files.

## Models

The code defines SQLAlchemy models for the application's database schema. These models represent the tables and their relationships within the database.

**Measurement Model:**
- Represents a measurement entry recorded by a user.
- Attributes:
  - id: Primary key for the measurement entry.
  - user_id: Foreign key referencing the associated user.
  - weight: Measurement of the user's weight.
  - shoulder: Measurement of the user's shoulder circumference.
  - chest: Measurement of the user's chest circumference.
  - arm: Measurement of the user's arm circumference.
  - waist: Measurement of the user's waist circumference.
  - leg: Measurement of the user's leg circumference.
  - date: Timestamp indicating when the measurement was recorded.

**User Model:**
- Represents a user of the application.
- Attributes:
  - id: Primary key for the user.
  - email: Unique email address associated with the user's account.
  - password: Hashed password for user authentication.
- Relationships:
  - measurements: One-to-many relationship with the Measurement model, indicating that a user can have multiple measurements.

## Files and Folders:

1. **app.py:**
   - Initializes and runs the Flask application.
   - Imports the `create_app` function from the `website` package to create the Flask app.
   - Calls the `create_app` function to create the Flask app instance.

2. **auth.py:**
   - Contains routes related to user authentication (e.g., login, sign-up, logout).
   - Handles user registration, login, logout, and account management.

3. **views.py:**
   - Contains routes related to the main functionality of the application (e.g., adding, updating, deleting measurements, viewing history).
   - Handles interactions with measurement data and rendering of HTML templates.

4. **models.py:**
   - Defines the database models (User and Measurement) using SQLAlchemy.
   - Contains classes representing database tables and their relationships.

5. **`__init__.py`:**
   - create_app Function:
     - Creates and configures the Flask application.
     - Initializes the SQLAlchemy database and sets the database URI.
     - Registers blueprints for different parts of the application, such as views and authentication.
     - Configures the login manager to handle user authentication.
     - Returns the Flask application instance.

   - create_database Function:
     - Checks if the database file exists and creates it if not.
     - Invoked within the `create_app` function to ensure database tables are created when the application starts.

5. **templates/:**
   - Directory containing HTML templates used to render views.
   - Each route typically has a corresponding HTML template file for rendering the page content.

6. **static/:**
   - Directory containing static files such as CSS stylesheets, JavaScript files, and images.
   - Static files are served directly to the client and are not processed by the server.
