from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    @staticmethod
    def get_address_by_id(addr_id):
        return Address.query.filter_by(addr_id=addr_id).first()

class Admin(db.Model):
    __tablename__ = 'cyz_admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_phone = db.Column(db.String(30), nullable=False)
    admin_pass = db.Column(db.String(12), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('cyz_user.user_id'), nullable=False)
    admin_fname = db.Column(db.String(255), nullable=False)
    admin_lname = db.Column(db.String(255), nullable=False)

    @staticmethod
    def add_admin(admin_phone, admin_pass, user_id, admin_fname, admin_lname):
        admin = Admin(admin_phone=admin_phone, admin_pass=admin_pass, user_id=user_id, admin_fname=admin_fname, admin_lname=admin_lname)
        db.session.add(admin)
        db.session.commit()

    @staticmethod
    def delete_admin_by_id(admin_id):
        Admin.query.filter_by(admin_id=admin_id).delete()
        db.session.commit()

    @staticmethod
    def update_admin_phone_by_id(admin_id, admin_phone):
        admin = Admin.query.filter_by(admin_id=admin_id).first()
        admin.admin_phone = admin_phone
        db.session.commit()

    @staticmethod
    def update_admin_pass_by_id(admin_id, admin_pass):
        admin = Admin.query.filter_by(admin_id=admin_id).first()
        admin.admin_pass = admin_pass
        db.session.commit()

    # @staticmethod

    

class Entertainment(db.Model):
    __tablename__ = 'cyz_entertainment'
    entertain_id = db.Column(db.Integer, primary_key=True)
    entertain_name = db.Column(db.String(255), nullable=False)
    num_units = db.Column(db.Integer, nullable=False)
    at_floor = db.Column(db.Integer, nullable=False)

class EntertainmentTrip(db.Model):
    __tablename__ = 'cyz_entertainment_trip'
    entertain_id = db.Column(db.Integer, db.ForeignKey('cyz_entertainment.entertain_id'), primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('cyz_trip.trip_id'), primary_key=True)

class Group(db.Model):
    __tablename__ = 'cyz_group'
    group_id = db.Column(db.Integer, primary_key=True)

class Invoice(db.Model):
    __tablename__ = 'cyz_invoice'
    invoice_id = db.Column(db.Integer, primary_key=True)
    payment_due = db.Column(db.Numeric(7, 2), nullable=False)
    billing_date_time = db.Column(db.DateTime, nullable=False)

class Itinerary(db.Model):
    __tablename__ = 'cyz_itinerary'
    itinerary_id = db.Column(db.Integer, primary_key=True)
    arrival_date_time = db.Column(db.DateTime)
    leaving_date_time = db.Column(db.DateTime)
    trip_id = db.Column(db.Integer, db.ForeignKey('cyz_trip.trip_id'), nullable=False)
    port_id = db.Column(db.Integer, db.ForeignKey('cyz_port.port_id'), nullable=False)

class Package(db.Model):
    __tablename__ = 'cyz_package'
    package_id = db.Column(db.Integer, primary_key=True)
    pkg_charge_type = db.Column(db.String(50), nullable=False)
    pkg_price = db.Column(db.Numeric(7, 2), nullable=False)
    pkg_name = db.Column(db.String(255), nullable=False)

class PackageSale(db.Model):
    __tablename__ = 'cyz_package_sale'
    pkg_sale_id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('cyz_package.package_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('cyz_group.group_id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('cyz_invoice.invoice_id'), nullable=False)

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

class Payment(db.Model):
    __tablename__ = 'cyz_payment'
    payment_id = db.Column(db.Integer, primary_key=True)
    payment_date = db.Column(db.DateTime, nullable=False)
    pay_amount = db.Column(db.Numeric(7, 2), nullable=False)
    payment_method = db.Column(db.String(255), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('cyz_trip.trip_id'), nullable=False)
    cyz_group_group_id = db.Column(db.Integer, db.ForeignKey('cyz_group.group_id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('cyz_invoice.invoice_id'), nullable=False)

class Port(db.Model):
    __tablename__ = 'cyz_port'
    port_id = db.Column(db.Integer, primary_key=True)
    nearest_airport = db.Column(db.String(255))
    num_parking_spots = db.Column(db.Integer, nullable=False)
    cyz_address_addr_id = db.Column(db.Integer, db.ForeignKey('cyz_address.addr_id'), nullable=False)
    port_name = db.Column(db.String(255), nullable=False)

class Restaurant(db.Model):
    __tablename__ = 'cyz_restaurant'
    restaurant_id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(255), nullable=False)
    serve_type = db.Column(db.String(255), nullable=False)
    opening_time = db.Column(db.DateTime, nullable=False)
    closing_time = db.Column(db.DateTime, nullable=False)
    at_floor = db.Column(db.Integer, nullable=False)

class RestaurantTrip(db.Model):
    __tablename__ = 'cyz_restaurant_trip'
    restaurant_id = db.Column(db.Integer, db.ForeignKey('cyz_restaurant.restaurant_id'), primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('cyz_trip.trip_id'), primary_key=True)

class Stateroom(db.Model):
    __tablename__ = 'cyz_stateroom'
    stateroom_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), nullable=False)
    num_bed = db.Column(db.Integer, nullable=False)
    num_bathroom = db.Column(db.Numeric(2, 1), nullable=False)
    num_balcony = db.Column(db.Integer, nullable=False)
    size_sqft = db.Column(db.Numeric(7, 2), nullable=False)
    room_number = db.Column(db.Integer, nullable=False)

class StateroomBooking(db.Model):
    __tablename__ = 'cyz_stateroom_booking'
    booking_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('cyz_group.group_id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('cyz_invoice.invoice_id'), nullable=False)
    price_id = db.Column(db.Integer, db.ForeignKey('cyz_stateroom_price.price_id'), nullable=False)

class StateroomPrice(db.Model):
    __tablename__ = 'cyz_stateroom_price'
    price_id = db.Column(db.Integer, primary_key=True)
    cyz_stateroom_stateroom_id = db.Column(db.Integer, db.ForeignKey('cyz_stateroom.stateroom_id'), nullable=False)
    price_per_night = db.Column(db.Numeric(7, 2), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('cyz_trip.trip_id'), nullable=False)
    is_vacant = db.Column(db.Numeric, nullable=False)

class Trip(db.Model):
    __tablename__ = 'cyz_trip'
    trip_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    start_port_id = db.Column(db.Integer, db.ForeignKey('cyz_port.port_id'), nullable=False)
    end_port_id = db.Column(db.Integer, db.ForeignKey('cyz_port.port_id'), nullable=False)

class User(db.Model):
    __tablename__ = 'cyz_user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(10), nullable=False, check_constraint="user_type IN ('admin', 'passenger')")

    __table_args__ = (
        db.CheckConstraint("user_type IN ('admin', 'passenger')", name='chk_user_type'),
    )

    @staticmethod
    def create_user(username, password, email, user_type):
        user = User(username=username, password=password, email=email, user_type=user_type)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def get_password_by_id(user_id):
        return User.query.filter_by(user_id=user_id).first().password
    
    @staticmethod
    def delete_user_by_id(user_id):
        User.query.filter_by(user_id=user_id).delete()
        db.session.commit()

    @staticmethod
    def update_username_by_id(user_id, username):
        user = User.query.filter_by(user_id=user_id).first()
        user.username = username
        db.session.commit()

    @staticmethod
    def update_password_by_id(user_id, password):
        user = User.query.filter_by(user_id=user_id).first()
        user.password = password
        db.session.commit()

    @staticmethod
    def update_email_by_id(user_id, email):
        user = User.query.filter_by(user_id=user_id).first()
        user.email = email
        db.session.commit()


    
