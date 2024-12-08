import os
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from utils import *
from datetime import datetime
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Configure CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


# Configure SQLAlchemy for SQLite
# SQLite database file
# Get the directory of the current file (app.py)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the SQLite database URI to use the 'cruise.db' in the same directory
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'cruise.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Replace with a strong secret key
jwt = JWTManager(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Cruise Management System!"}), 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        # Retrieve the username from the form
        username = data.get('username')
        # Retrieve the password from the form
        password = data.get('password')

        # Query the database for the user by username (assumes username is unique)
        user = User.query.filter_by(username=username).first()
        print(User.query.all())
        # Validate the user and the hashed password
        if user and check_password_hash(user.password, password):
            # Generate JWT token
            token = create_access_token(identity={"id": user.user_id, "username": user.username, "user_type": user.user_type})
            # Ensure the token is a string
            if isinstance(token, bytes):
                token = token.decode('utf-8')
            # Store the user ID in the session
            session['user_id'] = user.user_id
            session['user_type']=user.user_type
            return jsonify({
                "message": "Login successful",
                "token": token,
                "user": {
                    "user_id": int(user.user_id),
                    "username": str(user.username),
                    "user_type": str(user.user_type)
                }
            }), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401



@app.route('/regist', methods=['POST'])
def register():
    data = request.json  # Parse JSON input from frontend
    
    # Extract user inputs
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    user_type = "passenger"  # Default user_type set to 'passenger'

    # Passenger-specific inputs
    passenger_fname = data.get('first_name')
    passenger_lname = data.get('last_name')
    birth_date = data.get('birth_date')  # Assume YYYY-MM-DD format
    gender = data.get('gender')
    nationality = data.get('nationality')
    phone = data.get('phone')
    street = data.get('street')
    addr_line_2 = data.get('addr_line_2')
    neighborhood = data.get('neighborhood')
    city = data.get('city')
    state_province = data.get('state_province')
    postal_code = data.get('postal_code')
    country = data.get('country')
    group_id = data.get('group_id')  # Optional, can handle None

    # Validate inputs
    if not all([username, email, password, confirm_password,
                passenger_fname, passenger_lname, birth_date, gender,
                nationality, phone, street, city, state_province, postal_code, country]):
        return jsonify({"message": "All fields are required."}), 400

    if password != confirm_password:
        return jsonify({"message": "Passwords do not match."}), 400

    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Check for existing username or email
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({"message": "Username or email already exists."}), 400

    try:
        # Create a new user instance
        new_user = User(username=username, email=email,
                        password=hashed_password, user_type=user_type)

        # Add and commit the new user to the database
        db.session.add(new_user)
        db.session.flush()  # Flush to get the new user's user_id

        # Create a new address instance
        new_address = Address(street=street, addr_line_2=addr_line_2,
                              neighborhood=neighborhood, city=city,
                              state_province=state_province, postal_code=postal_code,
                              country=country)
        db.session.add(new_address)
        db.session.flush()
        # Get address id
        address_id = new_address.addr_id
        print(address_id)
        # Determine group_id if not provided
        if not group_id:
            max_group_id = db.session.query(db.func.max(Passenger.group_id)).scalar()
            group_id = (max_group_id + 1) if max_group_id is not None else 1

        # Create a new passenger instance linked to the new user
        new_passenger = Passenger(
            birth_date=datetime_to_unix(datetime_str=birth_date),
            gender=gender,
            nationality=nationality,
            phone=phone,
            addr_id=int(address_id),
            group_id=int(group_id),
            passenger_fname=passenger_fname,
            passenger_lname=passenger_lname,
            user_id=new_user.user_id

        )

        # Add and commit the new passenger to the database
        db.session.add(new_passenger)
        db.session.commit()

        return jsonify({"message": "Registration successful!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred during registration: {e}"}), 500


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully."}), 200


@app.route('/Passenger/Self', methods=['GET', 'PUT'])
def get_or_modify_passenger():
    """
    Fetch and display passenger's information (GET) or update it (POST) by ID.
    """
    # check login state
    if 'user_id' not in session:
        return jsonify({"message": "You need to log in first."}), 401
    
    session_user_id = session.get('user_id')
    print(session_user_id,type(session_user_id))

    if request.method == 'GET':
        try:
            # Query the database for the passenger
            passenger = Passenger.query.filter_by(user_id=session_user_id).first_or_404()
            if not passenger:
                return jsonify({"message": "Passenger not found"}), 404
            
            address = Address.query.get_or_404(passenger.addr_id)
            if not address:
                return jsonify({"message": "Address not found"}), 404

            # Prepare the passenger data for the frontend
            passenger_data = {
                'id': passenger.passenger_id,
                'first_name': passenger.passenger_fname,
                'last_name': passenger.passenger_lname,
                'birth_date': unix_to_datetime(passenger.birth_date, include_time=False),
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

            return jsonify({"passenger": passenger_data}), 200
        except Exception as e:
            return jsonify({"message": f"An error occurred: {e}"}), 500

    elif request.method == 'PUT':
        try:
            # Ensure the logged-in user is authorized to edit this passenger's information
            print(session_user_id, Passenger.query.get(session_user_id))
            passenger = Passenger.query.filter_by(user_id=session_user_id).first_or_404()
            old_address = Address.query.get_or_404(passenger.addr_id)
            print(session_user_id, passenger.user_id)

            if session_user_id != passenger.user_id:
                return jsonify({"message": "You are not authorized to edit this information."}), 403

            # Retrieve updated information from the request body
            data = request.json
            passenger.passenger_fname = data.get('first_name', passenger.passenger_fname)
            passenger.passenger_lname = data.get('last_name', passenger.passenger_lname)
            passenger.phone = data.get('phone', passenger.phone)

            # Get new address details
            new_address_data = {
                'street': data.get('street'),
                'addr_line_2': data.get('addr_line_2'),
                'neighborhood': data.get('neighborhood'),
                'city': data.get('city'),
                'state_province': data.get('state_province'),
                'postal_code': data.get('postal_code'),
                'country': data.get('country'),
            }

            # Search for an existing address with the same details
            new_address = Address.query.filter_by(
                street=new_address_data['street'],
                addr_line_2=new_address_data.get('addr_line_2'),
                neighborhood=new_address_data.get('neighborhood'),
                city=new_address_data['city'],
                state_province=new_address_data['state_province'],
                postal_code=new_address_data['postal_code'],
                country=new_address_data['country']
            ).first()

            if new_address:
                # If the new address exists, update the passenger's address ID
                passenger.addr_id = new_address.addr_id
            else:
                # If the new address does not exist, create it
                new_address = Address(**new_address_data)
                db.session.add(new_address)
                db.session.commit()  # Commit to get the new address ID
                passenger.addr_id = new_address.addr_id

            # Check if the old address is used by other passengers
            other_passengers = Passenger.query.filter_by(addr_id=old_address.addr_id).count()
            if other_passengers == 0:
                # If no other passengers use the old address, delete it
                db.session.delete(old_address)

            # Commit the changes to the database
            db.session.commit()
            return jsonify({"message": "Your information has been updated successfully!"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"An error occurred while editing your information: {e}"}), 500
        


@app.route('/Passenger/MyTrip', methods=['GET'])
def view_my_trip():
    """
    Fetch and return trip information for a given passenger as JSON.
    """
    # check login state
    if 'user_id' not in session:
        return jsonify({"message": "You need to log in first."}), 401
    
    try:
        user_id=session.get('user_id')
        # Fetch the passenger by ID
        passenger = Passenger.query.filter_by(user_id=user_id).first_or_404()

        
        print(passenger.user_id,session.get('user_id'))
        # Ensure the current user is authorized to view this passenger's trips
        if passenger.user_id != session.get("user_id"):
            return jsonify({"message": "Unauthorized access."}), 403
        
        # Query trips associated with the passenger's group
        trips = Trip.query.join(Payment, Trip.trip_id == Payment.trip_id)\
                          .filter(Payment.group_id == passenger.group_id)\
                          .all()

        # Prepare data for the frontend
        trip_data = []
        for trip in trips:
            payment = Payment.query.filter_by(trip_id=trip.trip_id).first()
            trip_data.append({
                'trip_id': trip.trip_id,
                'start_date': unix_to_datetime(trip.start_date),
                'end_date': unix_to_datetime(trip.end_date),
                'start_port_id': trip.start_port_id,
                'end_port_id': trip.end_port_id,
                'payment_amount': float(payment.pay_amount) if payment else None,
                'payment_method': payment.payment_method if payment else 'N/A',
                'payment_date': unix_to_datetime(payment.payment_date) if payment else 0
            })

        # Return the trip data as JSON
        return jsonify({"trips": trip_data}), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred while retrieving trip information: {e}"}), 500



@app.route('/Admin/Board', methods=['GET', 'DELETE'])
@jwt_required()
def admin_manage_users():
    # Ensure only admins can access this route
    if session['user_type'] != 'admin':
        return jsonify({"message": "Access denied. Admins only."}), 403

    data = request.json
    passenger_id = data.get('passenger_id')
    # Handle the DELETE request to remove a passenger
    if request.method == 'DELETE':
        
        passenger = Passenger.query.get(passenger_id)

        if not passenger:
            return jsonify({"message": f"Passenger with ID {passenger_id} not found."}), 404

        try:
            db.session.delete(passenger)
            db.session.commit()
            return jsonify({"message": f"Passenger with ID {passenger_id} deleted successfully."}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {e}"}), 500

    # Handle the GET request to retrieve all passengers
    if request.method == 'GET':
        passengers = Passenger.query.all()
        passengers_data = [
            {
                "id": passenger.passenger_id,
                "first_name": passenger.passenger_fname,
                "last_name": passenger.passenger_lname,
                "phone": passenger.phone,
                "gender": passenger.gender,
                "nationality": passenger.nationality
            }
            for passenger in passengers
        ]

        return jsonify({"passengers": passengers_data}), 200

@app.route('/Passenger/Trip', methods=['GET'])
def get_trips_by_date():
    """Fetch trips based on start and end dates."""
    print(session)
    if 'user_id' not in session:
        return jsonify({"message": "You need to log in first."}), 401

    # Parse JSON data from the request body
    data = request.json
    print(data)
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    # Retrieve startDate and endDate from the JSON payload
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    print(start_date,end_date)

    # convert the date from YYYY-MM-DD to int
    start_date=datetime_to_unix(start_date)
    end_date=datetime_to_unix(end_date)

    if not start_date or not end_date:
        return jsonify({'error': 'startDate and endDate are required'}), 400

    # Query trips within the date range
    trips = Trip.query.filter(
        Trip.start_date >= start_date,
        Trip.end_date <= end_date
    ).all()

    if not trips:
        return jsonify({'error': 'No trips available for the given dates'}), 404

    # Fetch port names and return response
    trip_data = []
    for trip in trips:
        start_port = Port.query.get(trip.start_port_id)
        end_port = Port.query.get(trip.end_port_id)

        trip_data.append({
            'trip_id': trip.trip_id,
            'start_date': unix_to_datetime(trip.start_date),
            'end_date': unix_to_datetime(trip.end_date),
            'start_port_name': start_port.port_name if start_port else None,
            'end_port_name': end_port.port_name if end_port else None
        })

    return jsonify(trip_data), 200

@app.route('/Passenger/Package', methods=['GET'])
def get_packages():
    """
    Fetch all package details.
    """
    # check login state
    if 'user_id' not in session:
        return jsonify({"message": "You need to log in first."}), 401
    
    try:
        packages = Package.query.all()
        package_list = [
            {
                "package_id": package.package_id,
                "pkg_charge_type": package.pkg_charge_type,
                "pkg_price": package.pkg_price,
                "pkg_name": package.pkg_name,
            }
            for package in packages
        ]
        return jsonify(package_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/Passenger/Entertainment', methods=['GET'])
def get_entertainments():
    """
    Fetch all entertainment details.
    """
    # check login state
    if 'user_id' not in session:
        return jsonify({"message": "You need to log in first."}), 401
    
    try:
        entertainments = Entertainment.query.all()
        entertainment_list = [
            {
                "entertain_id": entertainment.entertain_id,
                "entertain_name": entertainment.entertain_name,
                "num_units": entertainment.num_units,
                "at_floor": entertainment.at_floor,
            }
            for entertainment in entertainments
        ]
        return jsonify(entertainment_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/Passenger/Restaurant', methods=['GET'])
def get_restaurants():
    """
    Fetch all restaurant details.
    """
    # check login state
    if 'user_id' not in session:
        return jsonify({"message": "You need to log in first."}), 401
    
    try:
        restaurants = Restaurant.query.all()
        restaurant_list = [
            {
                "restaurant_id": restaurant.restaurant_id,
                "restaurant_name": restaurant.restaurant_name,
                "serve_type": restaurant.serve_type,
                "opening_time": restaurant.opening_time,
                "closing_time": restaurant.closing_time,
                "at_floor": restaurant.at_floor,
            }
            for restaurant in restaurants
        ]
        return jsonify(restaurant_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

# Database Initialization
def create_tables():
    with app.app_context():
        db.create_all()



if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
