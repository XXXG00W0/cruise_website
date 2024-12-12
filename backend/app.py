import os
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from utils import *
from datetime import datetime, timezone
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
# Replace with a strong secret key
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Cruise Management System!"}), 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        # Retrieve the username from the form
        username = sanitize_input(data.get('username'))
        # Retrieve the password from the form
        password = sanitize_input(data.get('password'))

        # Query the database for the user by username (assumes username is unique)
        user = User.query.filter_by(username=username).first()
        print(User.query.all())
        # Validate the user and the hashed password
        if user and check_password_hash(user.password, password):
            # Generate JWT token
            token = create_access_token(identity={
                                        "id": user.user_id, "username": user.username, "user_type": user.user_type})
            # Ensure the token is a string
            if isinstance(token, bytes):
                token = token.decode('utf-8')
            # Store the user ID in the session
            session['user_id'] = user.user_id
            session['user_type'] = user.user_type
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


@app.route('/register', methods=['POST'])
def register():
    data = request.json  # Parse JSON input from frontend

    # Extract user inputs
    username = sanitize_input(data.get('username'))
    email = sanitize_input(data.get('email'))
    password = sanitize_input(data.get('password'))
    confirm_password = sanitize_input(data.get('confirm_password'))
    user_type = "passenger"  # Default user_type set to 'passenger'

    # Passenger-specific inputs
    passenger_fname = sanitize_input(data.get('first_name'))
    passenger_lname = sanitize_input(data.get('last_name'))
    # Assume YYYY-MM-DD format
    birth_date = sanitize_input(data.get('birth_date'))
    gender = sanitize_input(data.get('gender'))
    nationality = sanitize_input(data.get('nationality'))
    phone = sanitize_input(data.get('phone'))
    street = sanitize_input(data.get('street'))
    addr_line_2 = sanitize_input(data.get('addr_line_2'))
    neighborhood = sanitize_input(data.get('neighborhood'))
    city = sanitize_input(data.get('city'))
    state_province = sanitize_input(data.get('state_province'))
    postal_code = sanitize_input(data.get('postal_code'))
    country = sanitize_input(data.get('country'))
    # Optional, can handle None
    group_id = sanitize_input(data.get('group_id'))

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
            max_group_id = db.session.query(
                db.func.max(Passenger.group_id)).scalar()
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
    print(session_user_id, type(session_user_id))

    if request.method == 'GET':
        try:
            # Query the database for the passenger
            passenger = Passenger.query.filter_by(
                user_id=session_user_id).first_or_404()
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
            print("Session user ID:", session_user_id)
            passenger = Passenger.query.filter_by(
                user_id=session_user_id).first_or_404()
            old_address = Address.query.get_or_404(passenger.addr_id)
            print("Passenger fetched:", passenger)
            print("Old address fetched:", old_address)

            if session_user_id != passenger.user_id:
                return jsonify({"message": "You are not authorized to edit this information."}), 403

            # Retrieve updated information from the request body
            data = request.json
            print("Received update data:", data)
            passenger.passenger_fname = sanitize_input(
                data.get('first_name', passenger.passenger_fname))
            passenger.passenger_lname = sanitize_input(
                data.get('last_name', passenger.passenger_lname))
            passenger.phone = sanitize_input(
                data.get('phone', passenger.phone))

            # Get new address details
            new_address_data = {
                'street': sanitize_input(data.get('street')),
                'addr_line_2': sanitize_input(data.get('addr_line_2')),
                'neighborhood': sanitize_input(data.get('neighborhood')),
                'city': sanitize_input(data.get('city')),
                'state_province': sanitize_input(data.get('state_province')),
                'postal_code': sanitize_input(data.get('postal_code')),
                'country': sanitize_input(data.get('country')),
            }
            print("New address data:", new_address_data)

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
                print("Existing address found:", new_address)
                passenger.addr_id = new_address.addr_id
            else:
                # If the new address does not exist, create it
                print("Creating a new address.")
                new_address = Address(**new_address_data)
                db.session.add(new_address)
                db.session.commit()  # Commit to get the new address ID
                passenger.addr_id = new_address.addr_id
                print("New address created with ID:", new_address.addr_id)

            # Check if the old address is used by other passengers
            other_passengers = Passenger.query.filter_by(
                addr_id=old_address.addr_id).count()
            print("Other passengers using old address:", other_passengers)
            if other_passengers == 0:
                print("Deleting unused old address:", old_address)
                # If no other passengers use the old address, delete it
                db.session.delete(old_address)

            # Commit the changes to the database
            db.session.commit()
            print("Passenger and address information updated successfully.")
            return jsonify({"message": "Your information has been updated successfully!"}), 200

        except Exception as e:
            db.session.rollback()
            print("Error during PUT request:", str(e))
            return jsonify({"message": f"An error occurred while editing your information: {e}"}), 500


@app.route('/Passenger/MyTrip', methods=['GET'])
def view_my_trip():
    """
    Fetch and return trip information for a given passenger as JSON, including multiple staterooms for a single trip.
    """
    # Check login state
    if 'user_id' not in session:
        return jsonify({"message": "You need to log in first."}), 401

    try:
        user_id = session.get('user_id')
        # Fetch the passenger by ID
        passenger = Passenger.query.filter_by(user_id=user_id).first_or_404()

        # Ensure the current user is authorized to view this passenger's trips
        if passenger.user_id != session.get("user_id"):
            return jsonify({"message": "Unauthorized access."}), 403

        # Query trips associated with the passenger's group
        trips = Trip.query.join(Payment, Trip.trip_id == Payment.trip_id)\
                          .filter(Payment.group_id == passenger.group_id)\
                          .all()

        trip_data = []
        for trip in trips:
            # Fetch associated stateroom bookings
            stateroom_bookings = StateroomBooking.query.join(StateroomPrice)\
                .filter(StateroomPrice.trip_id == trip.trip_id)\
                .filter(StateroomBooking.group_id == passenger.group_id)\
                .all()

            # Gather details for each stateroom
            staterooms_info = []
            for booking in stateroom_bookings:
                stateroom_price = StateroomPrice.query.get(booking.price_id)
                stateroom = Stateroom.query.get(
                    stateroom_price.stateroom_id) if stateroom_price else None
                if stateroom:
                    staterooms_info.append({
                        "stateroom_type": stateroom.stateroom_type,
                        "location": stateroom.location,
                        "num_bed": stateroom.num_bed,
                        "num_bathroom": stateroom.num_bathroom,
                        "num_balcony": stateroom.num_balcony,
                        "size_sqft": stateroom.size_sqft,
                        "room_number": stateroom.room_number
                    })

            # Fetch itinerary information
            itinerary = Itinerary.query.filter_by(trip_id=trip.trip_id).all()
            ports_info = [
                {
                    "port_name": Port.query.get(itinerary_item.port_id).port_name,
                    "arrival_date_time": unix_to_datetime(itinerary_item.arrival_date_time, True),
                    "leaving_date_time": unix_to_datetime(itinerary_item.leaving_date_time, True)
                }
                for itinerary_item in itinerary
            ] if itinerary else [{"message": "No itinerary available for this port."}]

            # Append trip data
            trip_data.append({
                "trip_id": trip.trip_id,
                "start_date": unix_to_datetime(trip.start_date),
                "end_date": unix_to_datetime(trip.end_date),
                "stateroom_information": staterooms_info,  # Now supports multiple rooms
                "ports": ports_info
            })

        # Return the data structured for the front-end interface
        return jsonify({"trips": trip_data}), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred while retrieving trip information: {e}"}), 500


@app.route('/Admin/UserManage', methods=['GET', 'DELETE'])
def admin_manage_users():
    # Ensure only admins can access this route
    if session['user_type'] != 'admin':
        return jsonify({"message": "Access denied. Admins only."}), 403

    # Handle the DELETE request to remove a passenger
    if request.method == 'DELETE':
        data = request.json
        passenger_id = sanitize_input(data.get('passenger_id'))
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


@app.route('/Admin/RoomPriceManage', methods=['GET', 'PUT', 'POST', 'DELETE'])
def admin_manage_room_prices():
    # Ensure only admins can access this route
    if session.get('user_type') != 'admin':
        return jsonify({"message": "Access denied. Admins only."}), 403

    # Handle the PUT request to update the price of a stateroom
    if request.method == 'PUT':
        data = request.json
        price_id = sanitize_input(data.get('price_id'))
        new_price = sanitize_input(data.get('price_per_night'))
        is_vacant = sanitize_input(data.get('is_vacant'))

        stateroom_price = StateroomPrice.query.get(price_id)

        if not stateroom_price:
            return jsonify({"message": f"Stateroom price with ID {price_id} not found."}), 404

        try:
            if new_price is not None:
                stateroom_price.price_per_night = new_price
            if is_vacant is not None:
                stateroom_price.is_vacant = is_vacant

            db.session.commit()
            return jsonify({"message": f"Stateroom price with ID {price_id} updated successfully."}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {e}"}), 500

    # Handle the GET request to retrieve all stateroom prices
    if request.method == 'GET':
        stateroom_prices = StateroomPrice.query.all()
        stateroom_prices_data = [
            {
                "price_id": price.price_id,
                "stateroom_id": price.stateroom_id,
                "price_per_night": price.price_per_night,
                "trip_id": price.trip_id,
                "is_vacant": price.is_vacant
            }
            for price in stateroom_prices
        ]

        return jsonify({"stateroom_prices": stateroom_prices_data}), 200
    
    # Handle the POST request to create a new stateroom price
    if request.method == 'POST':
        data = request.json
        stateroom_id = sanitize_input(data.get('stateroom_id'))
        price_per_night = sanitize_input(data.get('price_per_night'))
        trip_id = sanitize_input(data.get('trip_id'))
        is_vacant = sanitize_input(data.get('is_vacant'))

        if not all([stateroom_id, price_per_night, trip_id, is_vacant]):
            return jsonify({"message": "Missing required fields."}), 400

        try:
            new_stateroom_price = StateroomPrice(
                stateroom_id=stateroom_id,
                price_per_night=price_per_night,
                trip_id=trip_id,
                is_vacant=is_vacant
            )
            db.session.add(new_stateroom_price)
            db.session.commit()
            return jsonify({"message": "New stateroom price created successfully.", "price_id": new_stateroom_price.price_id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {e}"}), 500
        
    # Handle the DELETE request to delete a stateroom price
    if request.method == 'DELETE':
        data = request.json
        price_id = sanitize_input(data.get('price_id'))

        if not price_id:
            return jsonify({"message": "price_id is required."}), 400

        stateroom_price = StateroomPrice.query.get(price_id)

        if not stateroom_price:
            return jsonify({"message": f"Stateroom price with ID {price_id} not found."}), 404

        try:
            db.session.delete(stateroom_price)
            db.session.commit()
            return jsonify({"message": f"Stateroom price with ID {price_id} deleted successfully."}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {e}"}), 500

@app.route('/Admin/ManageTrip', methods=['GET', 'PUT', 'POST','DELETE'])
def admin_manage_trip():
    # Ensure only admins can access this route
    if session.get('user_type') != 'admin':
        return jsonify({"message": "Access denied. Admins only."}), 403

     # Handle the POST request to add a new trip
    if request.method == 'POST':
        data = request.json

        new_trip = Trip(
            start_date=datetime_to_unix(sanitize_input(data.get('start_date'))),
            end_date=datetime_to_unix(sanitize_input(data.get('end_date'))),
            start_port_id=sanitize_input(data.get('start_port_id')),
            end_port_id=sanitize_input(data.get('end_port_id'))
        )

        try:
            db.session.add(new_trip)
            db.session.commit()
            return jsonify({"message": f"New trip added with ID {new_trip.trip_id}."}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {e}"}), 500
        
    # Handle the DELETE request to delete a trip and its itineraries
    if request.method == 'DELETE':
        data = request.json
        trip_id = sanitize_input(data.get('trip_id'))
        trip = Trip.query.get(trip_id)
        if not trip:
            return jsonify({"message": f"Trip with ID {trip_id} not found."}), 404

        try:
            # Delete all itineraries associated with the trip
            Itinerary.query.filter_by(trip_id=trip_id).delete()
            # Delete the trip itself
            db.session.delete(trip)
            db.session.commit()
            return jsonify({"message": f"Trip with ID {trip_id} and its itineraries deleted successfully."}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {e}"}), 500
        
    # Handle the PUT request to update a trip's start and end dates
    if request.method == 'PUT':
        data = request.json
        trip_id = sanitize_input(data.get('trip_id'))
        new_start_date = sanitize_input(data.get('start_date'))
        new_end_date = sanitize_input(data.get('end_date'))

        trip = Trip.query.get(trip_id)

        if not trip:
            return jsonify({"message": f"Trip with ID {trip_id} not found."}), 404

        try:
            # assuming dates are in "YYYY-MM-DD" format
            if new_start_date is not None:
                trip.start_date = datetime_to_unix(new_start_date)
            if new_end_date is not None:
                trip.end_date = datetime_to_unix(new_end_date)

            db.session.commit()
            return jsonify({"message": f"Trip with ID {trip_id} updated successfully."}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {e}"}), 500

    # Handle the GET request to retrieve all trips
    if request.method == 'GET':
        trips = Trip.query.all()
        trips_data = [
            {
                "trip_id": trip.trip_id,
                "start_date": unix_to_datetime(trip.start_date),
                "end_date": unix_to_datetime(trip.end_date),
                "start_port_id": trip.start_port_id,
                "end_port_id": trip.end_port_id
            }
            for trip in trips
        ]

        return jsonify({"trips": trips_data}), 200

@app.route('/Admin/ManageItinerary', methods=['GET','POST','PUT','DELETE'])
def admin_manage_itinerary():
    # Ensure only admins can access this route
    if session.get('user_type') != 'admin':
        return jsonify({"message": "Access denied. Admins only."}), 403

    if request.method == 'POST':
        data = request.json
        arrival_date_time = sanitize_input(data.get('arrival_date_time'))
        leaving_date_time = sanitize_input(data.get('leaving_date_time'))
        trip_id = sanitize_input(data.get('trip_id'))
        port_id = sanitize_input(data.get('port_id'))

        # check if time conflicts exist
        existing_itineraries = Itinerary.query.filter_by(trip_id=trip_id).all()
        existing_itin_times = [(itinerary.arrival_date_time, itinerary.leaving_date_time) for itinerary in existing_itineraries]
        print(existing_itin_times)
        trip = Trip.query.get(trip_id)
        if not trip:
            return jsonify({"error": "Trip not found."}), 404
        trip_start_time = trip.start_date
        trip_end_time = trip.end_date
        print(validate_itinerary_times(arrival_date_time, leaving_date_time, trip_start_time, trip_end_time, existing_itin_times))
        if not validate_itinerary_times(arrival_date_time, leaving_date_time, trip_start_time, trip_end_time, existing_itin_times):
            return jsonify({"error": "Invalid itinerary times: Time conflict(s) with existing itineraries found!"}), 400
        
        # Create a new Itinerary instance
        new_itinerary = Itinerary(
            arrival_date_time=datetime_to_unix(arrival_date_time),
            leaving_date_time=datetime_to_unix(leaving_date_time),
            trip_id=trip_id,
            port_id=port_id
        )

        try:
            db.session.add(new_itinerary)
            db.session.commit()
            return jsonify({"message": "Itinerary added successfully."}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {e}"}), 500
    
    if request.method == 'GET':
        try:
            # Query all itineraries from the database
            itineraries = Itinerary.query.all()
            # Format the itineraries into a list of dictionaries
            itinerary_list = [
                {
                    "itinerary_id": itinerary.itinerary_id,
                    "arrival_date_time": unix_to_datetime(itinerary.arrival_date_time,True),
                    "leaving_date_time": unix_to_datetime(itinerary.leaving_date_time,True),
                    "trip_id": itinerary.trip_id,
                    "port_id": itinerary.port_id
                }
                for itinerary in itineraries
            ]

            return jsonify({"itineraries": itinerary_list}), 200
        except Exception as e:
            return jsonify({"message": f"Error: {e}"}), 500
        
    if request.method == 'PUT':
        data = request.json
        itinerary_id = sanitize_input(data.get('itinerary_id'))
        arrival_date_time = sanitize_input(data.get('arrival_date_time'))
        leaving_date_time = sanitize_input(data.get('leaving_date_time'))
        trip_id = sanitize_input(data.get('trip_id'))
        port_id = sanitize_input(data.get('port_id'))

        # Find the itinerary to update
        itinerary = Itinerary.query.get(itinerary_id)
        if not itinerary:
            return jsonify({"error": "Itinerary not found."}), 404

        # Check for time conflicts
        existing_itineraries = Itinerary.query.filter_by(trip_id=trip_id).filter(Itinerary.itinerary_id != itinerary_id).all()
        existing_itin_times = [(it.arrival_date_time, it.leaving_date_time) for it in existing_itineraries]
        trip = Trip.query.get(trip_id)
        if not trip:
            return jsonify({"error": "Trip not found."}), 404
        trip_start_time = trip.start_date
        trip_end_time = trip.end_date
        if not validate_itinerary_times(arrival_date_time, leaving_date_time, trip_start_time, trip_end_time, existing_itin_times):
            return jsonify({"error": "Invalid itinerary times: Time conflict(s) with existing itineraries found!"}), 400

        # Update the itinerary
        itinerary.arrival_date_time = datetime_to_unix(arrival_date_time)
        itinerary.leaving_date_time = datetime_to_unix(leaving_date_time)
        itinerary.trip_id = trip_id
        itinerary.port_id = port_id

        try:
            db.session.commit()
            return jsonify({"message": "Itinerary updated successfully."}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {e}"}), 500
        
    if request.method == 'DELETE':
        data = request.json
        itinerary_id = data.get('itinerary_id')

        # Find the itinerary to delete
        itinerary = Itinerary.query.get(itinerary_id)
        if not itinerary:
            return jsonify({"error": "Itinerary not found."}), 404

        try:
            db.session.delete(itinerary)
            db.session.commit()
            return jsonify({"message": "Itinerary deleted successfully."}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {e}"}), 500

@app.route('/Passenger/Trip', methods=['GET'])
def get_trips_by_date():
    """Fetch trips based on start and end dates."""
    print(session)
    if 'user_id' not in session:
        return jsonify({"message": "You need to log in first."}), 401

    # Retrieve startDate and endDate
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    print(start_date, end_date)

    # convert the date from YYYY-MM-DD to int
    start_date = datetime_to_unix(start_date)
    end_date = datetime_to_unix(end_date)
    print(start_date, end_date)

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


@app.route('/Passenger/RoomDetail', methods=['GET'])
def get_room_details_by_trip():
    """
    Fetch stateroom details and their prices for a specific trip ID.
    """
    # Check if the user is logged in
    if 'user_id' not in session:
        print("User is not logged in.")
        return jsonify({"message": "You need to log in first."}), 401

    # Get trip_id from the request arguments
    trip_id = request.args.get('trip_id', type=int)
    print(f"Received trip_id: {trip_id}")
    
    if not trip_id:
        print("No trip_id provided in the request.")
        return jsonify({"message": "Trip ID is required."}), 400

    try:
        # Query the staterooms and their prices for the given trip ID
        print("Querying stateroom prices...")
        stateroom_prices = db.session.query(Stateroom, StateroomPrice).join(
            StateroomPrice, Stateroom.stateroom_id == StateroomPrice.stateroom_id
        ).filter(StateroomPrice.trip_id == trip_id).all()
        
        print(f"Query result: {stateroom_prices}")
        
        if not stateroom_prices:
            print(f"No staterooms found for trip ID {trip_id}.")
            return jsonify({"message": f"No staterooms found for trip ID {trip_id}."}), 404

        # Convert the results into a structured list
        print("Formatting query results...")
        stateroom_list = [
            {
                "stateroom_id": stateroom.stateroom_id,
                "stateroom_type": stateroom.stateroom_type,
                "location": stateroom.location,
                "num_bed": stateroom.num_bed,
                "num_bathroom": stateroom.num_bathroom,
                "num_balcony": stateroom.num_balcony,
                "size_sqft": stateroom.size_sqft,
                "room_number": stateroom.room_number,
                "price_per_night": price.price_per_night,
                "is_vacant": price.is_vacant,
            }
            for stateroom, price in stateroom_prices
        ]

        print(f"Formatted stateroom list: {stateroom_list}")

        # Return the room details as a JSON response
        return jsonify(stateroom_list), 200
    except Exception as e:
        # Handle any errors during the process
        print(f"Exception occurred: {e}")
        import traceback
        print("Traceback:")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500



@app.route('/Passenger/PurchasePackage', methods=['GET', 'POST'])
def purchase_package():
    """
    Handle the purchase of a package.
    """
    # Check login state
    if 'user_id' not in session:
        return jsonify({"message": "You need to log in first."}), 401

    user_id = session['user_id']
    if request.method == 'GET':
        try:
            # Fetch passenger details
            passenger = Passenger.query.filter_by(user_id=user_id).first()
            if not passenger:
                return jsonify({"message": "Passenger not found for the given user ID."}), 404
            
            package_id = request.args.get('package_id', None)
            print("Received package_id:", package_id)


            if package_id:
                # Return the package information corresponding to the specified package_id
                print(Package.query.filter_by(package_id=package_id).first())
                pkg = Package.query.filter_by(package_id=package_id).first()
                
                if not pkg:
                    return jsonify({"message": "Package not found."}), 404

                package_info = {
                        "package_id": pkg.package_id,
                        "name": pkg.pkg_name,
                        "charge_type": pkg.pkg_charge_type,
                        "price": pkg.pkg_price,
                }

                return jsonify({
                    "message": "Package retrieved successfully.",
                    "package": package_info
                }), 200
            else:
                # Return the package information for all packages
                available_packages = Package.query.all()
                packages_info = [
                    {
                        "package_id": pkg.package_id,
                        "name": pkg.pkg_name,
                        "charge_type": pkg.pkg_charge_type,
                        "price": pkg.pkg_price,
                    }
                    for pkg in available_packages
                ]

                return jsonify({
                    "message": "Available packages retrieved successfully.",
                    "packages": packages_info
                }), 200

        except Exception as e:
            # Log error with traceback for better debugging
            import traceback
            error_details = traceback.format_exc()
            print(f"Error occurred in GET /Passenger/PurchasePackage: {error_details}")
            return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500


    if request.method == 'POST':
        data = request.get_json()

        # Validate input
        required_fields = ["package_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing required field: {field}"}), 400

        package_id = sanitize_input(data["package_id"])
        payment_method = sanitize_input(data.get("payment_method", "Unknown"))
        # Get group ID from Passenger model
        group_id = Passenger.query.filter_by(user_id=user_id).first().group_id
        # Get booking ID from StateroomBooking model, filtering by group ID
        booking_id = StateroomBooking.query.filter_by(group_id=group_id).first().booking_id
        # Get price ID from StateroomBooking model, using the obtained booking ID
        price_id = StateroomBooking.query.filter_by(booking_id=booking_id).first().price_id
        # Get trip ID from StateroomPrice model, using the obtained price ID
        trip_id = StateroomPrice.query.filter_by(price_id=price_id).first().trip_id

        try:
            # Fetch group_id based on the user_id
            passenger = Passenger.query.filter_by(user_id=user_id).first()
            if not passenger:
                return jsonify({"message": "Passenger not found for the given user ID."}), 404

            group_id = passenger.group_id

            # Fetch package details
            package = Package.query.filter_by(package_id=package_id).first()
            if not package:
                return jsonify({"message": "Package not found."}), 404

            # Calculate the billing date and payment due
            billing_date_time = int(datetime.now(timezone.utc).timestamp())
            payment_due = package.pkg_price

            # Create a new invoice
            new_invoice = Invoice(
                payment_due=payment_due,
                billing_date_time=billing_date_time
            )
            db.session.add(new_invoice)
            db.session.flush()  # Generate the invoice ID

            # Create a new package sale entry
            new_package_sale = PackageSale(
                package_id=package_id,
                group_id=group_id,
                invoice_id=new_invoice.invoice_id
            )
            db.session.add(new_package_sale)

            # Create a new payment
            payment_date = billing_date_time
            new_payment = Payment(
                payment_date=payment_date,
                pay_amount=payment_due,
                payment_method=payment_method,
                trip_id=trip_id,
                group_id=group_id,
                invoice_id=new_invoice.invoice_id
            )
            db.session.add(new_payment)

            # Commit all changes to the database
            db.session.commit()

            return jsonify({"message": "Package purchased successfully.", "invoice_id": new_invoice.invoice_id}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

@app.route('/Passenger/RoomOrder', methods=['GET', 'POST'])
def handle_room_order():
    """
    Handles fetching stateroom price details (GET) and booking a stateroom (POST).
    """
    # Check login state
    if 'user_id' not in session:
        return jsonify({"message": "You need to log in first."}), 401

    if request.method == 'GET':
        # Handle GET: Fetch stateroom price details
        trip_id = sanitize_input(request.args.get('tripId', type=int))
        stateroom_id = sanitize_input(request.args.get('stateroomId', type=int))
        print(trip_id,type(trip_id))

        if not trip_id or not stateroom_id:
            return jsonify({"message": "Both tripId and stateroomId are required."}), 400

        try:
            # Fetch trip details to calculate trip length
            trip = Trip.query.get(trip_id)
            if not trip:
                return jsonify({"message": "Trip not found."}), 404

            # Calculate trip length (in days)
            trip_length = (trip.end_date - trip.start_date) // (24 * 60 * 60)  # Convert seconds to days

            # Fetch stateroom prices for the trip and stateroom
            stateroom_prices = StateroomPrice.query.filter_by(trip_id=trip_id, stateroom_id=stateroom_id).all()

            if not stateroom_prices:
                return jsonify({"message": "No stateroom prices found for this trip or stateroom."}), 404

            # Compile stateroom details
            staterooms_data = []
            for stateroom_price in stateroom_prices:
                # Calculate the total price for the trip
                actual_price = stateroom_price.price_per_night * trip_length

                # Fetch stateroom details
                stateroom = Stateroom.query.get(stateroom_price.stateroom_id)
                if not stateroom:
                    continue  # Skip if stateroom details are missing

                # Fetch bookings for this stateroom in the trip
                bookings = StateroomBooking.query.filter_by(price_id=stateroom_price.price_id).all()

                # Compile booking details
                booking_details = [{
                    "bookingId": booking.booking_id,
                    "groupId": booking.group_id,
                    "invoiceId": booking.invoice_id
                } for booking in bookings]

                # Compile stateroom details
                staterooms_data.append({
                    "stateroomId": stateroom.stateroom_id,
                    "roomNumber": stateroom.room_number,
                    "stateroomType": stateroom.stateroom_type,
                    "location": stateroom.location,
                    "numBed": stateroom.num_bed,
                    "numBathroom": stateroom.num_bathroom,
                    "numBalcony": stateroom.num_balcony,
                    "sizeSqFt": stateroom.size_sqft,
                    "isVacant": stateroom_price.is_vacant,
                    "pricePerNight": stateroom_price.price_per_night,
                    "actualPrice": actual_price,
                    "bookings": booking_details
                })

            return jsonify({"code": 200, "tripLengthDays": trip_length, "staterooms": staterooms_data}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'POST':
        # Handle POST: Book a stateroom
        try:
            data = request.get_json()  # JSON 
            print(data)
            print(data.get('stateroomId'))
            stateroom_id = sanitize_input(data.get('stateroomId'))
            trip_id = sanitize_input(data.get('tripId'))
            pay_amount = sanitize_input(data.get('pay_amount'))
            payment_method = sanitize_input(data.get('payment_method'))
            
            # Ensure required fields are provided
            required_fields = {'stateroomId': stateroom_id, 'tripId': trip_id, 'pay_amount': pay_amount, 'payment_method': payment_method}
            missing_fields = [key for key, value in required_fields.items() if not value]
            if missing_fields:
                return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}"}), 400

            # Converpt numeric fields to appropriate tyes
            try:
                trip_id = int(trip_id)
                pay_amount = float(pay_amount)
                print(trip_id, pay_amount)
            except ValueError:
                return jsonify({"message": "Invalid data format for numeric fields."}), 400

            # Fetch trip details to calculate trip length
            trip = Trip.query.filter_by(trip_id=trip_id).first()
            if not trip:
                return jsonify({"message": "Trip not found."}), 400

            # Calculate trip length (in days)
            trip_length = (trip.end_date - trip.start_date) // (24 * 60 * 60)  # Convert seconds to days
            print("trip length", trip_length)
            if trip_length <= 0:
                return jsonify({"message": "Invalid trip dates."}), 400

            # Fetch stateroom price details
            stateroom_price = StateroomPrice.query.filter_by(
                stateroom_id=stateroom_id, trip_id=trip_id).first()
            if not stateroom_price or not stateroom_price.is_vacant:
                return jsonify({"message": "Stateroom is not available for booking."}), 400

            # Calculate total cost
            calculated_cost = stateroom_price.price_per_night * trip_length
            print("calculated cost", calculated_cost)
            if abs(pay_amount - calculated_cost) > 1e-2:  # Allow minor rounding differences
                return jsonify({
                    "message": f"Payment amount mismatch. Expected: {calculated_cost}, Provided: {pay_amount}"
                }), 400

            # Create invoice
            new_invoice = Invoice(
                payment_due=pay_amount,
                billing_date_time=int(datetime.now().timestamp())
            )
            db.session.add(new_invoice)
            db.session.flush()  # Generate invoice ID

            # Fetch group_id from database
            user_id = session.get('user_id')  # Assuming the user's ID is stored in the session
            user = Passenger.query.filter_by(user_id=user_id).first()
            if not user or not user.group_id:
                return jsonify({"message": "Group ID for the user not found."}), 400

            # Create stateroom booking
            new_booking = StateroomBooking(
                group_id=user.group_id,
                invoice_id=new_invoice.invoice_id,
                price_id=stateroom_price.price_id,
            )
            db.session.add(new_booking)

            # Create payment record
            new_payment = Payment(
                payment_date=int(datetime.now().timestamp()),
                pay_amount=pay_amount,
                payment_method=payment_method,
                trip_id=trip_id,
                group_id=session['user_id'],
                invoice_id=new_invoice.invoice_id
            )
            db.session.add(new_payment)

            # Update stateroom availability
            stateroom_price.is_vacant = False
            db.session.commit()

            # Return response with booking and payment details
            return jsonify({
                "code": 200,
                "message": "Booking successful.",
                "data": {
                    "invoice": {
                        "invoice_id": new_invoice.invoice_id,
                        "billing_date_time": new_invoice.billing_date_time,
                        "payment_due": new_invoice.payment_due,
                    },
                    "payment": {
                        "payment_id": new_payment.payment_id,
                        "payment_date": new_payment.payment_date,
                        "pay_amount": new_payment.pay_amount,
                        "payment_method": new_payment.payment_method,
                    },
                    "group": {
                        "group_id": new_booking.group_id,
                    }
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500



# Database Initialization
def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
