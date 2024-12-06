from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from utils import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Configure SQLAlchemy for SQLite
# SQLite database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cruise_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('Home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve the username from the form
        username = request.form.get('username')
        # Retrieve the password from the form
        password = request.form.get('password')

        # Query the database for the user by username (assumes username is unique)
        user = User.query.filter_by(username=username).first()

        # Validate the user and the hashed password
        if user and check_password_hash(user.password, password):
            # Store user information in the session
            session['user_id'] = user.user_id
            session['username'] = user.username
            flash('Login successful!', 'success')

            # Redirect based on user_type
            if user.user_type == 'passenger':
                return redirect(url_for('passenger_page'))
            elif user.user_type == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Unknown user type.', 'warning')
                return redirect(url_for('main_page'))
        else:
            # Invalid login attempt
            flash('Invalid username or password.', 'danger')

    # Render the login page
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_type = "passenger"  # Default user_type set to 'passenger'

        # Validate form inputs
        if not username or not email or not password or not confirm_password:
            flash("All fields are required.", 'danger')
            return render_template('register.html')
        if password != confirm_password:
            flash("Passwords do not match.", 'danger')
            return render_template('register.html')

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')

        # Check for existing username or email
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)).first()
        if existing_user:
            flash(
                "Username or email already exists. Please choose a different one.", 'danger')
            return render_template('register.html')

        try:
            # Create a new user instance
            new_user = User(username=username, email=email,
                            password=hashed_password, user_type=user_type)

            # Add and commit the new user to the database
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred during registration: {e}", 'danger')

    return render_template('Regist.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/passenger/<int:id>', methods=['GET'])
def passenger_information(id):
    """
    Fetch and display passenger's information, including address details, by ID.
    """
    if 'user_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))
    
    try:
        # Query the database for the passenger
        passenger = Passenger.query.get_or_404(id)
        address = Address.query.get_or_404(passenger.cyz_address_addr_id)

        # Prepare the passenger data for the frontend
        passenger_data = {
            'id': passenger.passenger_id,
            'first_name': passenger.passenger_fname,
            'last_name': passenger.passenger_lname,
            'birth_date': passenger.birth_date.strftime('%Y-%m-%d'),
            'gender': passenger.gender,
            'nationality': passenger.nationality,
            'phone': passenger.phone,
            'address': {
                'street': address.street,
                'addr_line_2': address.addr_line_2 or '',
                'neighborhood': address.neighborhood or '',
                'city': address.city,
                'state_province': address.state_province,
                'postal_code': address.postal_code,
                'country': address.country
            }
        }

        return render_template('passenger_info.html', passenger=passenger_data)
    except Exception as e:
        flash(f"An error occurred while retrieving passenger information: {e}", 'danger')
        return redirect(url_for('home'))

@app.route('/group/<int:passenger_id>', methods=['GET'])
def group_information(passenger_id):
    """
    Fetch and display information of group members for a given passenger.
    """
    if 'user_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))
    
    try:
        # Fetch the passenger by ID
        passenger = Passenger.query.get_or_404(passenger_id)

        # Query all group members belonging to the same group
        group_members = Passenger.query.filter_by(cyz_group_group_id=passenger.cyz_group_group_id).all()

        # Prepare the data for the frontend
        group_data = [
            {
                'passenger_id': member.passenger_id,
                'name': f"{member.passenger_fname} {member.passenger_lname}"
            }
            for member in group_members
        ]

        return render_template('group_info.html', group_data=group_data, group_id=passenger.cyz_group_group_id)
    except Exception as e:
        flash(f"An error occurred while retrieving group information: {e}", 'danger')
        return redirect(url_for('home'))


@app.route('/passenger/<int:id>/edit', methods=['GET', 'POST'])
def edit_passenger_information(id):
    """
    Allow a passenger to modify their personal information, including managing address updates.
    """
    if 'user_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

    try:
        # Fetch the passenger and their current address
        passenger = Passenger.query.get_or_404(id)
        old_address = Address.query.get_or_404(passenger.cyz_address_addr_id)

        # Check if the passenger is authorized to edit
        if session.get('user_id') != passenger.user_id:
            flash('You are not authorized to edit this information.', 'danger')
            return redirect(url_for('home'))

        if request.method == 'POST':
            # Retrieve updated information from the form
            passenger.passenger_fname = request.form.get('first_name')
            passenger.passenger_lname = request.form.get('last_name')
            passenger.phone = request.form.get('phone')

            # Get new address details
            new_address_data = {
                'street': request.form.get('street'),
                'addr_line_2': request.form.get('addr_line_2'),
                'neighborhood': request.form.get('neighborhood'),
                'city': request.form.get('city'),
                'state_province': request.form.get('state_province'),
                'postal_code': request.form.get('postal_code'),
                'country': request.form.get('country'),
            }

            # Search for an existing address with the same details
            new_address = Address.query.filter_by(
                street=new_address_data['street'],
                addr_line_2=new_address_data['addr_line_2'],
                neighborhood=new_address_data['neighborhood'],
                city=new_address_data['city'],
                state_province=new_address_data['state_province'],
                postal_code=new_address_data['postal_code'],
                country=new_address_data['country']
            ).first()

            if new_address:
                # If the new address exists, update the passenger's address ID
                passenger.cyz_address_addr_id = new_address.addr_id
            else:
                # If the new address does not exist, create it
                new_address = Address(**new_address_data)
                db.session.add(new_address)
                db.session.commit()  # Commit to get the new address ID
                passenger.cyz_address_addr_id = new_address.addr_id

            # Check if the old address is used by other passengers
            other_passengers = Passenger.query.filter_by(cyz_address_addr_id=old_address.addr_id).count()
            if other_passengers == 0:
                # If no other passengers use the old address, delete it
                db.session.delete(old_address)

            # Commit the changes to the database
            db.session.commit()
            flash('Your information has been updated successfully!', 'success')
            return redirect(url_for('passenger_information', id=passenger.passenger_id))

        # Render the edit form with current data
        return render_template('edit_passenger_info.html', passenger=passenger, address=old_address)

    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while editing your information: {e}", 'danger')
        return redirect(url_for('home'))




# @app.route('/api/passenger', methods=['POST'])
# def add_passenger():
#     if 'user_id' not in session:
#         return jsonify({'message': 'Unauthorized'}), 401
#     try:
#         data = request.json
#         new_passenger = Passenger(
#             name=data['name'],
#             email=data['email'],
#             phone=data['phone']
#         )
#         db.session.add(new_passenger)
#         db.session.commit()
#         return jsonify({'message': 'Passenger added successfully!'}), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': f'Error: {e}'}), 400


# @app.route('/api/passenger/<int:id>', methods=['DELETE'])
# def delete_passenger(id):
#     if 'user_id' not in session:
#         return jsonify({'message': 'Unauthorized'}), 401
#     try:
#         passenger = Passenger.query.get_or_404(id)
#         db.session.delete(passenger)
#         db.session.commit()
#         return jsonify({'message': 'Passenger deleted successfully!'})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': f'Error: {e}'}), 400


@app.route('/api/passenger/<int:id>', methods=['PUT'])
def update_passenger(id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    try:
        data = request.json
        passenger = Passenger.query.get_or_404(id)
        passenger.name = data.get('name', passenger.name)
        passenger.email = data.get('email', passenger.email)
        passenger.phone = data.get('phone', passenger.phone)
        db.session.commit()
        return jsonify({'message': 'Passenger updated successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {e}'}), 400

# Database Initialization
@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
