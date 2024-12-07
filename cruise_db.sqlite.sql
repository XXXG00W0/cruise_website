CREATE TABLE cyz_address (
    addr_id        INTEGER PRIMARY KEY,
    street         TEXT NOT NULL,
    addr_line_2    TEXT,
    neighborhood   TEXT,
    city           TEXT NOT NULL,
    state_province TEXT NOT NULL,
    postal_code    TEXT NOT NULL,
    country        TEXT NOT NULL
);

CREATE TABLE cyz_admin (
    admin_id    INTEGER PRIMARY KEY,
    admin_phone TEXT NOT NULL,
    user_id     INTEGER NOT NULL,
    admin_fname TEXT NOT NULL,
    admin_lname TEXT NOT NULL,
    FOREIGN KEY ( user_id ) REFERENCES cyz_user ( user_id )
);

CREATE TABLE cyz_entertainment (
    entertain_id   INTEGER PRIMARY KEY,
    entertain_name TEXT NOT NULL,
    num_units      INTEGER NOT NULL,
    at_floor       INTEGER NOT NULL
);

CREATE TABLE cyz_entertainment_trip (
    entertain_id        INTEGER NOT NULL,
    trip_id             INTEGER NOT NULL,
    PRIMARY KEY ( entertain_id, trip_id ),
    FOREIGN KEY ( entertain_id ) REFERENCES cyz_entertainment ( entertain_id ),
    FOREIGN KEY ( trip_id ) REFERENCES cyz_trip ( trip_id )
);

CREATE TABLE cyz_group (
    group_id INTEGER PRIMARY KEY
);

CREATE TABLE cyz_invoice (
    invoice_id        INTEGER PRIMARY KEY,
    payment_due       REAL NOT NULL,
    billing_date_time INTEGER NOT NULL
);

CREATE TABLE cyz_itinerary (
    itinerary_id      INTEGER PRIMARY KEY,
    arrival_date_time INTEGER,
    leaving_date_time INTEGER,
    trip_id           INTEGER,
    port_id           INTEGER,
    FOREIGN KEY (trip_id) REFERENCES cyz_trip (trip_id),
    FOREIGN KEY (port_id) REFERENCES cyz_port (port_id)
);

CREATE TABLE cyz_package (
    package_id      INTEGER PRIMARY KEY,
    pkg_charge_type TEXT CHECK (pkg_charge_type IN ('per night', 'per trip')) NOT NULL,
    pkg_price       INTEGER NOT NULL,
    pkg_name        TEXT NOT NULL
);

CREATE TABLE cyz_package_sale (
    pkg_sale_id INTEGER PRIMARY KEY,
    package_id  INTEGER NOT NULL,
    group_id    INTEGER NOT NULL,
    invoice_id  INTEGER NOT NULL,
    FOREIGN KEY (package_id) REFERENCES cyz_package (package_id),
    FOREIGN KEY (group_id) REFERENCES cyz_group (group_id),
    FOREIGN KEY (invoice_id) REFERENCES cyz_invoice (invoice_id)
);

CREATE TABLE cyz_passenger (
    passenger_id        INTEGER PRIMARY KEY,
    birth_date          INTEGER NOT NULL,
    gender              TEXT CHECK (gender IN ('female', 'male', 'other')) NOT NULL, -- Female male or other
    nationality         TEXT NOT NULL,
    phone               TEXT NOT NULL,
    addr_id             INTEGER,
    group_id            INTEGER NOT NULL, -- Debatable whether this should be NOT NULL
    passenger_fname     TEXT NOT NULL,
    passenger_lname     TEXT NOT NULL,
    user_id             INTEGER NOT NULL,
    FOREIGN KEY (addr_id) REFERENCES cyz_address (addr_id),
    FOREIGN KEY (group_id) REFERENCES cyz_group (group_id),
    FOREIGN KEY (user_id) REFERENCES cyz_user (user_id)
);

CREATE TABLE cyz_payment (
    payment_id         INTEGER PRIMARY KEY,
    payment_date       INTEGER NOT NULL,
    pay_amount         REAL NOT NULL,
    payment_method     TEXT NOT NULL,
    trip_id            INTEGER NOT NULL,
    group_id           INTEGER NOT NULL,
    invoice_id         INTEGER NOT NULL,
    FOREIGN KEY (trip_id) REFERENCES cyz_trip (trip_id),
    FOREIGN KEY (group_id) REFERENCES cyz_group (group_id),
    FOREIGN KEY (invoice_id) REFERENCES cyz_invoice (invoice_id)
);

CREATE TABLE cyz_port (
    port_id             INTEGER PRIMARY KEY,
    nearest_airport     TEXT,
    num_parking_spots   INTEGER CHECK(num_parking_spots >= 0) NOT NULL,
    addr_id             INTEGER NOT NULL,
    port_name           TEXT NOT NULL,
    FOREIGN KEY (addr_id) REFERENCES cyz_address (addr_id)
);

CREATE TABLE cyz_restaurant (
    restaurant_id   INTEGER PRIMARY KEY,
    restaurant_name TEXT NOT NULL,
    serve_type      TEXT NOT NULL,
    opening_time    TEXT NOT NULL,
    closing_time    TEXT NOT NULL,
    at_floor        INTEGER NOT NULL
);

CREATE TABLE cyz_restaurant_trip (
    restaurant_id INTEGER NOT NULL,
    trip_id       INTEGER NOT NULL,
    PRIMARY KEY (restaurant_id, trip_id),
    FOREIGN KEY (restaurant_id) REFERENCES cyz_restaurant (restaurant_id),
    FOREIGN KEY (trip_id) REFERENCES cyz_trip (trip_id)
);

CREATE TABLE cyz_stateroom (
    stateroom_id INTEGER PRIMARY KEY,
    stateroom_type TEXT NOT NULL,
    location     TEXT CHECK (location IN ('forward', 'aft', 'left', 'right')) NOT NULL,
    num_bed INTEGER CHECK (num_bed >= 0) NOT NULL,
    num_bathroom INTEGER CHECK (num_bathroom >= 0) NOT NULL,
    num_balcony  INTEGER CHECK (num_balcony >= 0) NOT NULL,
    size_sqft    REAL NOT NULL,
    room_number  INTEGER NOT NULL
);

CREATE TABLE cyz_stateroom_booking (
    booking_id INTEGER PRIMARY KEY,
    group_id   INTEGER NOT NULL,
    invoice_id INTEGER NOT NULL,
    price_id   INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES cyz_group (group_id),
    FOREIGN KEY (invoice_id) REFERENCES cyz_invoice (invoice_id),
    FOREIGN KEY (price_id) REFERENCES cyz_stateroom_price (price_id)
);

CREATE TABLE cyz_stateroom_price (
    price_id                   INTEGER PRIMARY KEY,
    stateroom_id               INTEGER NOT NULL,
    price_per_night            REAL NOT NULL,
    trip_id                    INTEGER NOT NULL,
    is_vacant                  BOOLEAN NOT NULL,
    FOREIGN KEY (stateroom_id) REFERENCES cyz_stateroom (stateroom_id),
    FOREIGN KEY (trip_id) REFERENCES cyz_trip (trip_id)
);

CREATE TABLE cyz_trip (
    trip_id       INTEGER PRIMARY KEY,
    start_date    INTEGER NOT NULL,
    end_date      INTEGER NOT NULL,
    start_port_id INTEGER NOT NULL,
    end_port_id   INTEGER NOT NULL,
    FOREIGN KEY (start_port_id) REFERENCES cyz_port (port_id),
    FOREIGN KEY (end_port_id) REFERENCES cyz_port (port_id)
);

CREATE TABLE cyz_user (
    user_id   INTEGER PRIMARY KEY,
    username  TEXT NOT NULL UNIQUE,
    password  TEXT NOT NULL,
    email     TEXT NOT NULL UNIQUE,
    user_type TEXT CHECK ( user_type IN ( 'admin', 'passenger' ) ) NOT NULL
);

INSERT INTO cyz_restaurant (restaurant_id, restaurant_name, serve_type, opening_time, closing_time, at_floor)
VALUES 
(1, 'Common Buffett', 'Breakfast, Lunch, Dinner', '07:00', '21:00', 6),
(2, 'Italian Specialty', 'Dinner', '18:00', '22:00', 8),
(3, 'Mexican Specialty', 'Dinner', '18:00', '22:00', 7),
(4, 'La-carte Continental', 'Lunch, Dinner', '12:00', '20:00', 6),
(5, 'Tokyo Ramen Japanese', 'Lunch, Dinner', '12:00', '20:00', 5),
(6, 'Ming Wok Chinese', 'Lunch, Dinner', '12:00', '20:00', 5),
(7, 'Round Clock Café', 'Beverages, Light Food', '00:00', '23:59', 10),
(8, 'Pool Bar', 'Alcoholic Beverages', '10:00', '22:00', 10),
(9, 'Stout Bar', 'Alcoholic Beverages', '10:00', '22:00', 7);

INSERT INTO cyz_stateroom (stateroom_id, stateroom_type, location, size_sqft, num_bed, num_bathroom, num_balcony, room_number)
VALUES
(1, 'The Haven Suite', 'forward', 1000, 6, 3, 2, 1),
(2, 'The Haven Suite', 'aft', 1000, 6, 3, 2, 2),
(3, 'The Haven Suite', 'left', 1000, 6, 3, 2, 3),
(4, 'The Haven Suite', 'right',1000, 6, 3, 2, 4),
(5, 'Club Balcony Suite', 'forward', 800, 4, 2, 2, 5),
(6, 'Club Balcony Suite', 'aft', 800, 4, 2, 2, 6),
(7, 'Club Balcony Suite', 'left', 800, 4, 2, 2, 7),
(8, 'Club Balcony Suite', 'right', 800, 4, 2, 2, 8),
(9, 'Family Large Balcony', 'forward', 600, 4, 2, 1, 9),
(10, 'Family Large Balcony', 'aft', 600, 4, 2, 1, 10),
(11, 'Family Large Balcony', 'left', 600, 4, 2, 1, 11),
(12, 'Family Large Balcony', 'right', 600, 4, 2, 1, 12),
(13, 'Family Balcony', 'forward', 400, 4, 1.5, 1, 13),
(14, 'Family Balcony', 'aft', 400, 4, 1.5, 1, 14),
(15, 'Family Balcony', 'left', 400, 4, 1.5, 1, 15),
(16, 'Family Balcony', 'right', 400, 4, 1.5, 1, 16),
(17, 'Oceanview Window', 'forward', 300, 2, 1, 0, 17),
(18, 'Oceanview Window', 'aft', 300, 2, 1, 0, 18),
(19, 'Oceanview Window', 'left', 300, 2, 1, 0, 19),
(20, 'Oceanview Window', 'right', 300, 2, 1, 0, 20),
(21, 'Inside Stateroom', 'forward', 200, 2, 1, 0, 21),
(22, 'Inside Stateroom', 'aft', 200, 2, 1, 0, 22),
(23, 'Inside Stateroom', 'left', 200, 2, 1, 0, 23),
(24, 'Inside Stateroom', 'right', 200, 2, 1, 0, 24),
(25, 'Studio Stateroom', 'forward', 150, 1, 1, 0, 25),
(26, 'Studio Stateroom', 'aft', 150, 1, 1, 0, 26),
(27, 'Studio Stateroom', 'left', 150, 1, 1, 0, 27),
(28, 'Studio Stateroom', 'right', 150, 1, 1, 0, 28);

INSERT INTO cyz_entertainment (entertain_id, entertain_name, num_units, at_floor)
VALUES
(1, 'Theaters', 2, 8),
(2, 'Theaters', 2, 10),
(3, 'Casino', 1, 7),
(4, 'Library', 2, 3),
(5, 'Library', 2, 4),
(6, 'Children play', 1, 3),
(7, 'Gym', 1, 5),
(8, 'Outdoor pool', 1, 11),
(9, 'Indoor pool', 1, 9),
(10, 'Whirlpool', 2, 11),
(11, 'Whirlpool', 2, 9),
(12, 'Steam room', 1, 9),
(13, 'Sona room', 1, 9),
(14, 'Yoga room', 1, 5),
(15, 'Night Club', 2, 8),
(16, 'Night Club', 2, 11),
(17, 'Tennis court', 1, 11);

INSERT INTO cyz_package (package_id, pkg_name, pkg_charge_type, pkg_price)
VALUES
(1, 'Water and Non-Alcoholic', 'per night', 40),
(2, 'Unlimited Bar (21+)', 'per night', 80),
(3, 'Internet 200 minutes, 100 GB', 'per trip', 150),
(4, 'Unlimited Internet', 'per trip', 250),
(5, 'Specialty Dining', 'per night', 60);

INSERT INTO cyz_trip (trip_id, start_date, end_date, start_port_id, end_port_id)
VALUES
(1, '2025-01-01', '2025-01-05', 1, 5),
(2, '2025-01-06', '2025-01-10', 5, 1);

INSERT INTO cyz_port (port_id, nearest_airport, num_parking_spots, addr_id, port_name)
VALUES
(1, 'LAX', 100, 1, 'Los Angeles Port'),
(2, 'JFK', 100, 2, 'New York Port'),
(3, 'MIA', 100, 3, 'Miami Port'),
(4, 'SFO', 100, 4, 'San Francisco Port'),
(5, 'SEA', 100, 5, 'Seattle Port');

INSERT INTO cyz_address (addr_id, street, city, state_province, postal_code, country)
VALUES
(1, '1234 Main St', 'Los Angeles', 'CA', '90001', 'USA'),
(2, '5678 1st St', 'New York', 'NY', '10001', 'USA'),
(3, '9101 2nd St', 'Miami', 'FL', '20001', 'USA'),
(4, '1122 3rd St', 'San Francisco', 'CA', '30001', 'USA'),
(5, '3344 4th St', 'Seattle', 'WA', '40001', 'USA'),
(6, '5566 5th St', 'Vancouver', 'BC', '50001', 'Canada'),
(7, '7788 6th St', 'Toronto', 'ON', '60001', 'Canada'),
(8, '9900 7th St', 'Montreal', 'QC', '70001', 'Canada'),
(9, '1122 8th St', 'London', 'UK', '80001', 'UK'),
(10, '3344 9th St', 'Paris', 'FR', '90001', 'France');

INSERT INTO cyz_itinerary (itinerary_id, arrival_date_time, leaving_date_time, trip_id, port_id)
VALUES
(1, 1735718400, 1735754400, 1, 1),
(2, 1735804800, 1735840800, 1, 2),
(3, 1735891200, 1735927200, 1, 3),
(4, 1735977600, 1736013600, 1, 4),
(5, 1736064000, 1736100000, 1, 5),
(6, 1736150400, 1736186400, 2, 5),
(7, 1736236800, 1736272800, 2, 4),
(8, 1736323200, 1736359200, 2, 3),
(9, 1736409600, 1736445600, 2, 2),
(10, 1736496000, 1736532000, 2, 1);

INSERT INTO cyz_stateroom_price (price_id, stateroom_id, price_per_night, trip_id, is_vacant)
VALUES
(1, 1, 1000, 1, 1),
(2, 2, 1000, 1, 1),
(3, 3, 1000, 1, 1),
(4, 4, 1000, 1, 1),
(5, 5, 800, 1, 1),
(6, 6, 800, 1, 1),
(7, 7, 800, 1, 1),
(8, 8, 800, 1, 1),
(9, 9, 600, 1, 1),
(10, 10, 600, 1, 1),
(11, 11, 600, 1, 1),
(12, 12, 600, 1, 1),
(13, 13, 400, 1, 1),
(14, 14, 400, 1, 1),
(15, 15, 400, 1, 1),
(16, 16, 400, 1, 1),
(17, 17, 300, 1, 1),
(18, 18, 300, 1, 1),
(19, 19, 300, 1, 1),
(20, 20, 300, 1, 1),
(21, 21, 200, 1, 1),
(22, 22, 200, 1, 1),
(23, 23, 200, 1, 1),
(24, 24, 200, 1, 1),
(25, 25, 150, 1, 1),
(26, 26, 150, 1, 1),
(27, 27, 150, 1, 1),
(28, 28, 150, 1, 1),
(29, 1, 1000, 2, 1),
(30, 2, 1000, 2, 1),
(31, 3, 1000, 2, 1),
(32, 4, 1000, 2, 1),
(33, 5, 800, 2, 1),
(34, 6, 800, 2, 1),
(35, 7, 800, 2, 1),
(36, 8, 800, 2, 1),
(37, 9, 600, 2, 1),
(38, 10, 600, 2, 1),
(39, 11, 600, 2, 1),
(40, 12, 600, 2, 1),
(41, 13, 400, 2, 1),
(42, 14, 400, 2, 1),
(43, 15, 400, 2, 1),
(44, 16, 400, 2, 1),
(45, 17, 300, 2, 1),
(46, 18, 300, 2, 1),
(47, 19, 300, 2, 1),
(48, 20, 300, 2, 1),
(49, 21, 200, 2, 1),
(50, 22, 200, 2, 1),
(51, 23, 200, 2, 1),
(52, 24, 200, 2, 1),
(53, 25, 150, 2, 1),
(54, 26, 150, 2, 1),
(55, 27, 150, 2, 1),
(56, 28, 150, 2, 1);

INSERT INTO cyz_admin (admin_id, admin_phone, user_id, admin_fname, admin_lname)
VALUES
(1, '123-456-7890', 1, 'John', 'Doe'),
(2, '234-567-8901', 2, 'Jane', 'Doe');

INSERT INTO cyz_user (user_id, username, password, email, user_type)
VALUES
(1, 'admin1', 'pbkdf2:sha256:1000000$eB33M5nkfbrfjSCx$35222bcadbc86d016a44dbd9442e72e45000b5a1e980d1a5a0432228f7e42182', 'admin123@email.com', 'admin'),
(2, 'admin2', 'pbkdf2:sha256:1000000$w1WdtDFpOxIXWpCt$75b338e28f9fd518998f2975320c81987daa3adbfed13d1d362087ea0cf7591a', 'admin234@email.com', 'admin'),
(3, 'passenger1', 'pbkdf2:sha256:1000000$8xWbsuv9NVx9I04a$0013a2f48cc0234f3bef10f192441c73b812cec91fb23002193547eb4cc93cb7', 'passenger1@email.com', 'passenger'),
(4, 'passenger2', 'pbkdf2:sha256:1000000$a117d6Kg7K8Lx38R$07903237b1de2e4eb6041fccf5d552a94ef49aa4b91ac52501890a384e28aa3d', 'passenger2@email.com', 'passenger'),
(5, 'passenger3', 'pbkdf2:sha256:1000000$GiS0yVvgnvJ33pjb$7f515bcacf83bbe79b6f7b416448ef5d403eda7b4b055092a4e43095a64c3ad9', 'passenger3@email.com', 'passenger'),
(6, 'passenger4', 'pbkdf2:sha256:1000000$7TTTAOhtyOYOSIET$955d2e5e1d078eb1dd6b3f69e7694718ba4c824aefcb947e1c67a62877ac369e', 'passenger4@email.com', 'passenger');


INSERT INTO cyz_passenger (passenger_id, birth_date, gender, nationality, phone, addr_id, group_id, passenger_fname, passenger_lname, user_id)
VALUES
(1, 631152000, 'female', 'USA', '1234567890', 1, 1, 'Jane', 'Doe', 3),
(2, 487641600, 'male', 'Canada', '2345678901', 2, 1, 'John', 'Smith', 4),
(3, 953683200, 'other', 'UK', '3456789012', 3, 2, 'Alex', 'Taylor', 5),
(4, 1608854400, 'female', 'France', '4567890123', 4, 2, 'Sophia', 'Brown', 10);

INSERT INTO cyz_group (group_id)
VALUES
(1),
(2);

INSERT INTO cyz_stateroom_booking (booking_id, group_id, invoice_id, price_id)
VALUES
(1, 1, 1, 1),
(2, 2, 2, 2);

INSERT INTO cyz_invoice (invoice_id, payment_due, billing_date_time)
VALUES
(1, 1000, 1733054400),
(2, 1000, 1722801600);

INSERT INTO cyz_payment (payment_id, payment_date, pay_amount, payment_method, trip_id, group_id, invoice_id)
VALUES
(1, 1733076000, 1000, 'credit card', 1, 1, 1),
(2, 1723732800, 1000, 'credit card', 2, 2, 2);

INSERT INTO cyz_entertainment_trip (entertain_id, trip_id)
VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 1),
(5, 1),
(6, 1),
(7, 1),
(8, 1),
(9, 1),
(10, 1),
(11, 1),
(12, 1),
(13, 1),
(14, 1),
(15, 1),
(16, 1),
(17, 1),
(1, 2),
(2, 2),
(3, 2),
(4, 2),
(5, 2),
(6, 2),
(7, 2),
(8, 2),
(9, 2),
(10, 2),
(11, 2),
(12, 2),
(13, 2),
(14, 2),
(15, 2),
(16, 2),
(17, 2);

INSERT INTO cyz_restaurant_trip (restaurant_id, trip_id)
VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 1),
(5, 1),
(6, 1),
(7, 1),
(8, 1),
(9, 1),
(1, 2),
(2, 2),
(3, 2),
(4, 2),
(5, 2),
(6, 2),
(7, 2),
(8, 2),
(9, 2);

