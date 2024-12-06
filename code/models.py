from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Address Model
class Address(db.Model):
    __tablename__ = 'cyz_address'
    addr_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    addr_line_2 = db.Column(db.String(255))
    neighborhood = db.Column(db.String(255))
    city = db.Column(db.String(255), nullable=False)
    state_province = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(255), nullable=False)

# Admin Model
class Admin(db.Model):
    __tablename__ = 'cyz_admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_phone = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('cyz_user.user_id'), nullable=False)
    admin_fname = db.Column(db.String(255), nullable=False)
    admin_lname = db.Column(db.String(255), nullable=False)

# Entertainment Model
class Entertainment(db.Model):
    __tablename__ = 'cyz_entertainment'
    entertain_id = db.Column(db.Integer, primary_key=True)
    entertain_name = db.Column(db.String(255), nullable=False)
    num_units = db.Column(db.Integer, nullable=False)
    at_floor = db.Column(db.Integer, nullable=False)

# EntertainmentTrip Model
class EntertainmentTrip(db.Model):
    __tablename__ = 'cyz_entertainment_trip'
    entertain_id = db.Column(db.Integer, db.ForeignKey('cyz_entertainment.entertain_id'), primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('cyz_trip.trip_id'), primary_key=True)

# Group Model
class Group(db.Model):
    __tablename__ = 'cyz_group'
    group_id = db.Column(db.Integer, primary_key=True)

# Invoice Model
class Invoice(db.Model):
    __tablename__ = 'cyz_invoice'
    invoice_id = db.Column(db.Integer, primary_key=True)
    payment_due = db.Column(db.Numeric(7, 2), nullable=False)
    billing_date_time = db.Column(db.DateTime, nullable=False)

# Itinerary Model
class Itinerary(db.Model):
    __tablename__ = 'cyz_itinerary'
    itinerary_id = db.Column(db.Integer, primary_key=True)
    arrival_date_time = db.Column(db.DateTime)
    leaving_date_time = db.Column(db.DateTime)
    trip_id = db.Column(db.Integer, db.ForeignKey('cyz_trip.trip_id'), nullable=False)
    port_id = db.Column(db.Integer, db.ForeignKey('cyz_port.port_id'), nullable=False)

# Package Model
class Package(db.Model):
    __tablename__ = 'cyz_package'
    package_id = db.Column(db.Integer, primary_key=True)
    pkg_charge_type = db.Column(db.String(50), nullable=False)
    pkg_price = db.Column(db.Numeric(7, 2), nullable=False)
    pkg_name = db.Column(db.String(255), nullable=False)

# PackageSale Model
class PackageSale(db.Model):
    __tablename__ = 'cyz_package_sale'
    pkg_sale_id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('cyz_package.package_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('cyz_group.group_id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('cyz_invoice.invoice_id'), nullable=False)

# Passenger Model
class Passenger(db.Model):
    __tablename__ = 'cyz_passenger'
    passenger_id = db.Column(db.Integer, primary_key=True)
    birth_date = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    nationality = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    cyz_address_addr_id = db.Column(db.Integer, db.ForeignKey('cyz_address.addr_id'), nullable=False)
    cyz_group_group_id = db.Column(db.Integer, db.ForeignKey('cyz_group.group_id'), nullable=False)
    passenger_fname = db.Column(db.String(255), nullable=False)
    passenger_lname = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('cyz_user.user_id'), nullable=False)

# Payment Model
class Payment(db.Model):
    __tablename__ = 'cyz_payment'
    payment_id = db.Column(db.Integer, primary_key=True)
    payment_date = db.Column(db.DateTime, nullable=False)
    pay_amount = db.Column(db.Numeric(7, 2), nullable=False)
    payment_method = db.Column(db.String(255), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('cyz_trip.trip_id'), nullable=False)
    cyz_group_group_id = db.Column(db.Integer, db.ForeignKey('cyz_group.group_id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('cyz_invoice.invoice_id'), nullable=False)

# Port Model
class Port(db.Model):
    __tablename__ = 'cyz_port'
    port_id = db.Column(db.Integer, primary_key=True)
    nearest_airport = db.Column(db.String(255))
    num_parking_spots = db.Column(db.Integer, nullable=False)
    cyz_address_addr_id = db.Column(db.Integer, db.ForeignKey('cyz_address.addr_id'), nullable=False)
    port_name = db.Column(db.String(255), nullable=False)

# Restaurant Model
class Restaurant(db.Model):
    __tablename__ = 'cyz_restaurant'
    restaurant_id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(255), nullable=False)
    serve_type = db.Column(db.String(255), nullable=False)
    opening_time = db.Column(db.DateTime, nullable=False)
    closing_time = db.Column(db.DateTime, nullable=False)
    at_floor = db.Column(db.Integer, nullable=False)

# RestaurantTrip Model
class RestaurantTrip(db.Model):
    __tablename__ = 'cyz_restaurant_trip'
    restaurant_id = db.Column(db.Integer, db.ForeignKey('cyz_restaurant.restaurant_id'), primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('cyz_trip.trip_id'), primary_key=True)

# Stateroom Model
class Stateroom(db.Model):
    __tablename__ = 'cyz_stateroom'
    stateroom_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), nullable=False)
    num_bed = db.Column(db.Integer, nullable=False)
    num_bathroom = db.Column(db.Numeric(2, 1), nullable=False)
    num_balcony = db.Column(db.Integer, nullable=False)
    size_sqft = db.Column(db.Numeric(7, 2), nullable=False)
    room_number = db.Column(db.Integer, nullable=False)

# StateroomBooking Model
class StateroomBooking(db.Model):
    __tablename__ = 'cyz_stateroom_booking'
    booking_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('cyz_group.group_id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('cyz_invoice.invoice_id'), nullable=False)
    price_id = db.Column(db.Integer, db.ForeignKey('cyz_stateroom_price.price_id'), nullable=False)

# StateroomPrice Model
class StateroomPrice(db.Model):
    __tablename__ = 'cyz_stateroom_price'
    price_id = db.Column(db.Integer, primary_key=True)
    cyz_stateroom_stateroom_id = db.Column(db.Integer, db.ForeignKey('cyz_stateroom.stateroom_id'), nullable=False)
    price_per_night = db.Column(db.Numeric(7, 2), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('cyz_trip.trip_id'), nullable=False)
    is_vacant = db.Column(db.Numeric, nullable=False)

# Trip Model
class Trip(db.Model):
    __tablename__ = 'cyz_trip'
    trip_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    start_port_id = db.Column(db.Integer, db.ForeignKey('cyz_port.port_id'), nullable=False)
    end_port_id = db.Column(db.Integer, db.ForeignKey('cyz_port.port_id'), nullable=False)

# User Model
class User(db.Model):
    __tablename__ = 'cyz_user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)

__all__ = [
    'Address', 'Admin', 'Entertainment', 'EntertainmentTrip', 'Group',
    'Invoice', 'Itinerary', 'Package', 'PackageSale', 'Passenger', 'Payment',
    'Port', 'Restaurant', 'RestaurantTrip', 'Stateroom', 'StateroomBooking',
    'StateroomPrice', 'Trip', 'User'
]