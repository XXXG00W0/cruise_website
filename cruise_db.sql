
drop database cruise_db;
create database cruise_db;
use cruise_db;

CREATE TABLE cyz_address (
    addr_id        INT NOT NULL,
    street         VARCHAR(255) NOT NULL,
    addr_line_2    VARCHAR(255),
    neighborhood   VARCHAR(255),
    city           VARCHAR(255) NOT NULL,
    state_province VARCHAR(255) NOT NULL,
    postal_code    VARCHAR(20) NOT NULL,
    country        VARCHAR(255) NOT NULL
);

ALTER TABLE cyz_address ADD CONSTRAINT address_pk PRIMARY KEY ( addr_id );

CREATE TABLE cyz_admin (
    admin_id    INT NOT NULL,
    admin_phone VARCHAR(30) NOT NULL,
    admin_pass  VARCHAR(12) NOT NULL,
    user_id     INT NOT NULL,
    admin_fname VARCHAR(255) NOT NULL,
    admin_lname VARCHAR(255) NOT NULL
);

ALTER TABLE cyz_admin ADD CONSTRAINT cyz_admin_pk PRIMARY KEY ( admin_id );

CREATE TABLE cyz_entertainment (
    entertain_id   INT NOT NULL,
    entertain_name VARCHAR(255) NOT NULL,
    num_units      INT NOT NULL,
    at_floor       INT NOT NULL
);

ALTER TABLE cyz_entertainment ADD CONSTRAINT entertainment_pk PRIMARY KEY ( entertain_id );

CREATE TABLE cyz_entertainment_trip (
    entertain_id INT NOT NULL,
    trip_id      INT NOT NULL
);

ALTER TABLE cyz_entertainment_trip ADD CONSTRAINT enter_trip_pk PRIMARY KEY ( entertain_id,
                                                                              trip_id );

CREATE TABLE cyz_group (
    group_id INT NOT NULL
);

ALTER TABLE cyz_group ADD CONSTRAINT group_pk PRIMARY KEY ( group_id );

CREATE TABLE cyz_invoice (
    invoice_id        INT NOT NULL,
    payment_due       DECIMAL(7, 2) NOT NULL,
    billing_date_time DATETIME NOT NULL
);

ALTER TABLE cyz_invoice ADD CONSTRAINT invoice_pk PRIMARY KEY ( invoice_id );

CREATE TABLE cyz_itinerary (
    itinerary_id      INT NOT NULL,
    arrival_date_time DATETIME,
    leaving_date_time DATETIME,
    trip_id           INT NOT NULL,
    port_id           INT NOT NULL
);

ALTER TABLE cyz_itinerary ADD CONSTRAINT itinerary_pk PRIMARY KEY ( itinerary_id );

CREATE TABLE cyz_package (
    package_id      INT NOT NULL,
    pkg_charge_type VARCHAR(50) NOT NULL,
    pkg_price       DECIMAL(7, 2) NOT NULL,
    pkg_name        VARCHAR(255) NOT NULL
);

ALTER TABLE cyz_package ADD CONSTRAINT package_pk PRIMARY KEY ( package_id );

CREATE TABLE cyz_package_sale (
    pkg_sale_id INT NOT NULL,
    package_id  INT NOT NULL,
    group_id    INT NOT NULL,
    invoice_id  INT NOT NULL
);

ALTER TABLE cyz_package_sale ADD CONSTRAINT package_sale_pk PRIMARY KEY ( pkg_sale_id );

CREATE TABLE cyz_passenger (
    passenger_id        INT NOT NULL,
    birth_date          DATETIME NOT NULL,
    gender              VARCHAR(1) NOT NULL,
    nationality         VARCHAR(255) NOT NULL,
    phone               VARCHAR(255) NOT NULL,
    cyz_address_addr_id INT NOT NULL,
    cyz_group_group_id  INT NOT NULL,
    passenger_fname     VARCHAR(255) NOT NULL,
    passenger_lname     VARCHAR(255) NOT NULL,
    user_id             INT NOT NULL
);

ALTER TABLE cyz_passenger ADD CONSTRAINT cyz_passenger_pk PRIMARY KEY ( passenger_id );

CREATE TABLE cyz_payment (
    payment_id         INT NOT NULL,
    payment_date       DATETIME NOT NULL,
    pay_amount         DECIMAL(7, 2) NOT NULL,
    payment_method     VARCHAR(255) NOT NULL,
    trip_id            INT NOT NULL,
    cyz_group_group_id INT NOT NULL,
    invoice_id         INT NOT NULL
);

ALTER TABLE cyz_payment ADD CONSTRAINT payment_pk PRIMARY KEY ( payment_id );

CREATE TABLE cyz_port (
    port_id             INT NOT NULL,
    nearest_airport     VARCHAR(255),
    num_parking_spots   INT NOT NULL,
    cyz_address_addr_id INT NOT NULL,
    port_name           VARCHAR(255) NOT NULL
);

ALTER TABLE cyz_port ADD CONSTRAINT port_pk PRIMARY KEY ( port_id );

CREATE TABLE cyz_restaurant (
    restaurant_id   INT NOT NULL,
    restaurant_name VARCHAR(255) NOT NULL,
    serve_type      VARCHAR(255) NOT NULL,
    opening_time    DATETIME NOT NULL,
    closing_time    DATETIME NOT NULL,
    at_floor        INT NOT NULL
);

ALTER TABLE cyz_restaurant ADD CONSTRAINT restaurant_pk PRIMARY KEY ( restaurant_id );

CREATE TABLE cyz_restaurant_trip (
    restaurant_id INT NOT NULL,
    trip_id       INT NOT NULL
);

ALTER TABLE cyz_restaurant_trip ADD CONSTRAINT rest_trip_pk PRIMARY KEY ( restaurant_id,
                                                                          trip_id );

CREATE TABLE cyz_stateroom (
    stateroom_id INT NOT NULL,
    location     VARCHAR(50) NOT NULL,
    num_bed      INT NOT NULL,
    num_bathroom DECIMAL(2, 1) NOT NULL,
    num_balcony  INT NOT NULL,
    size_sqft    DECIMAL(7, 2) NOT NULL,
    room_number  INT NOT NULL
);

ALTER TABLE cyz_stateroom ADD CONSTRAINT stateroom_pk PRIMARY KEY ( stateroom_id );

CREATE TABLE cyz_stateroom_booking (
    booking_id INT NOT NULL,
    group_id   INT NOT NULL,
    invoice_id INT NOT NULL,
    price_id   INT NOT NULL
);

ALTER TABLE cyz_stateroom_booking ADD CONSTRAINT cyz_stateroom_booking_pk PRIMARY KEY ( booking_id );

CREATE TABLE cyz_stateroom_price (
    price_id                   INT NOT NULL,
    cyz_stateroom_stateroom_id INT NOT NULL,
    price_per_night            DECIMAL(7, 2) NOT NULL,
    trip_id                    INT NOT NULL,
    is_vacant                  DECIMAL NOT NULL
);

ALTER TABLE cyz_stateroom_price ADD CONSTRAINT cyz_stateroom_price_pk PRIMARY KEY ( price_id );

CREATE TABLE cyz_trip (
    trip_id       INT NOT NULL,
    start_date    DATETIME NOT NULL,
    end_date      DATETIME NOT NULL,
    start_port_id INT NOT NULL,
    end_port_id   INT NOT NULL
);

ALTER TABLE cyz_trip ADD CONSTRAINT trip_pk PRIMARY KEY ( trip_id );

CREATE TABLE cyz_user (
    user_id   INT NOT NULL,
    username  VARCHAR(15) NOT NULL,
    password  VARCHAR(12) NOT NULL,
    email     VARCHAR(255) NOT NULL,
    user_type VARCHAR(10) NOT NULL
);

ALTER TABLE cyz_user
    ADD CONSTRAINT fkarc_1_lov CHECK ( user_type IN ( 'passenger', 'admin' ) );

/* COMMENT ON COLUMN cyz_user.user_type IS
    '''admin'' OR ''passenger'''; */

ALTER TABLE cyz_user
    ADD CONSTRAINT chk_user_type CHECK ( user_type IN ( 'admin', 'passenger' ) );

ALTER TABLE cyz_user ADD CONSTRAINT user_pk PRIMARY KEY ( user_id );

ALTER TABLE cyz_admin
    ADD CONSTRAINT cyz_admin_cyz_user_fk FOREIGN KEY ( user_id )
        REFERENCES cyz_user ( user_id );

ALTER TABLE cyz_trip
    ADD CONSTRAINT cyz_end_port_fk FOREIGN KEY ( end_port_id )
        REFERENCES cyz_port ( port_id );

ALTER TABLE cyz_entertainment_trip
    ADD CONSTRAINT cyz_enter_trip_enter_fk FOREIGN KEY ( entertain_id )
        REFERENCES cyz_entertainment ( entertain_id );

ALTER TABLE cyz_entertainment_trip
    ADD CONSTRAINT cyz_enter_trip_trip_fk FOREIGN KEY ( trip_id )
        REFERENCES cyz_trip ( trip_id );

ALTER TABLE cyz_itinerary
    ADD CONSTRAINT cyz_itinerary_cyz_trip_fk FOREIGN KEY ( trip_id )
        REFERENCES cyz_trip ( trip_id );

ALTER TABLE cyz_package_sale
    ADD CONSTRAINT cyz_pac_sale_cyz_group_fk FOREIGN KEY ( group_id )
        REFERENCES cyz_group ( group_id );

ALTER TABLE cyz_package_sale
    ADD CONSTRAINT cyz_pac_sale_cyz_inv_fk FOREIGN KEY ( invoice_id )
        REFERENCES cyz_invoice ( invoice_id );

ALTER TABLE cyz_package_sale
    ADD CONSTRAINT cyz_pac_sale_cyz_pac_fk FOREIGN KEY ( package_id )
        REFERENCES cyz_package ( package_id );

ALTER TABLE cyz_passenger
    ADD CONSTRAINT cyz_passenger_cyz_address_fk FOREIGN KEY ( cyz_address_addr_id )
        REFERENCES cyz_address ( addr_id );

ALTER TABLE cyz_passenger
    ADD CONSTRAINT cyz_passenger_cyz_group_fk FOREIGN KEY ( cyz_group_group_id )
        REFERENCES cyz_group ( group_id );

ALTER TABLE cyz_passenger
    ADD CONSTRAINT cyz_passenger_cyz_user_fk FOREIGN KEY ( user_id )
        REFERENCES cyz_user ( user_id );

ALTER TABLE cyz_payment
    ADD CONSTRAINT cyz_payment_cyz_group_fk FOREIGN KEY ( cyz_group_group_id )
        REFERENCES cyz_group ( group_id );

ALTER TABLE cyz_payment
    ADD CONSTRAINT cyz_payment_cyz_inv_fk FOREIGN KEY ( invoice_id )
        REFERENCES cyz_invoice ( invoice_id );

ALTER TABLE cyz_payment
    ADD CONSTRAINT cyz_payment_cyz_trip_fk FOREIGN KEY ( trip_id )
        REFERENCES cyz_trip ( trip_id );

ALTER TABLE cyz_port
    ADD CONSTRAINT cyz_port_cyz_addr_fk FOREIGN KEY ( cyz_address_addr_id )
        REFERENCES cyz_address ( addr_id );

ALTER TABLE cyz_restaurant_trip
    ADD CONSTRAINT cyz_rest_trip_rest_fk FOREIGN KEY ( restaurant_id )
        REFERENCES cyz_restaurant ( restaurant_id );

ALTER TABLE cyz_restaurant_trip
    ADD CONSTRAINT cyz_rest_trip_trip_fk FOREIGN KEY ( trip_id )
        REFERENCES cyz_trip ( trip_id );

ALTER TABLE cyz_stateroom_booking
    ADD CONSTRAINT cyz_sroom_book_group_fkv1 FOREIGN KEY ( group_id )
        REFERENCES cyz_group ( group_id );

ALTER TABLE cyz_stateroom_booking
    ADD CONSTRAINT cyz_sroom_book_inv_fkv1 FOREIGN KEY ( invoice_id )
        REFERENCES cyz_invoice ( invoice_id );

ALTER TABLE cyz_stateroom_booking
    ADD CONSTRAINT cyz_sroom_book_pri_fk FOREIGN KEY ( price_id )
        REFERENCES cyz_stateroom_price ( price_id );

ALTER TABLE cyz_stateroom_price
    ADD CONSTRAINT cyz_sroom_pri_sroom_fk FOREIGN KEY ( cyz_stateroom_stateroom_id )
        REFERENCES cyz_stateroom ( stateroom_id );

ALTER TABLE cyz_stateroom_price
    ADD CONSTRAINT cyz_sroom_pri_trip_fk FOREIGN KEY ( trip_id )
        REFERENCES cyz_trip ( trip_id );

ALTER TABLE cyz_trip
    ADD CONSTRAINT cyz_start_port_fk FOREIGN KEY ( start_port_id )
        REFERENCES cyz_port ( port_id );

ALTER TABLE cyz_itinerary
    ADD CONSTRAINT relation_24 FOREIGN KEY ( port_id )
        REFERENCES cyz_port ( port_id );

DELIMITER $$

-- CREATE TRIGGER arc_fkarc_1_cyz_passenger
-- BEFORE INSERT ON cyz_passenger
-- FOR EACH ROW
-- BEGIN
--     DECLARE d VARCHAR(10);

--     -- 查询 user_type
--     SELECT user_type
--     INTO d
--     FROM cyz_user
--     WHERE user_id = NEW.user_id;

--     -- 检查 user_type 是否为 'passenger'
--     IF d IS NULL OR d <> 'passenger' THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'FK CYZ_PASSENGER_CYZ_USER_FK in Table CYZ_PASSENGER violates Arc constraint on Table CYZ_USER - discriminator column USER_TYPE doesn''t have value ''passenger''';
--     END IF;
-- END$$

-- DELIMITER ;

-- -- MySQL Does not have EXCEPTION
-- -- EXCEPTION
-- --     WHEN no_data_found THEN
-- --         NULL;
-- --     WHEN OTHERS THEN
-- --         RAISE;
-- -- END;
-- -- /

-- DELIMITER $$

-- CREATE TRIGGER arc_fkarc_1_cyz_admin
-- BEFORE INSERT ON cyz_admin
-- FOR EACH ROW
-- BEGIN
--     DECLARE d VARCHAR(10);

--     -- Lookup user_type
--     SELECT user_type
--     INTO d
--     FROM cyz_user
--     WHERE user_id = NEW.user_id;

--     -- Check user_type is 'admin'
--     IF d IS NULL OR d <> 'admin' THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'FK CYZ_ADMIN_CYZ_USER_FK in Table CYZ_ADMIN violates Arc constraint on Table CYZ_USER - discriminator column USER_TYPE doesn''t have value ''admin''';
--     END IF;
-- END$$

-- DELIMITER ;

-- -- Ziyi Liang 2024-12-02 23:01:58 EST
-- -- Add triggers

-- -- Add birth_date constraint
-- DELIMITER $$

-- CREATE TRIGGER trg_passenger_birth_date
-- BEFORE INSERT ON cyz_passenger
-- FOR EACH ROW
-- BEGIN
--     IF NEW.birth_date > CURRENT_TIMESTAMP 
--        OR NEW.birth_date < DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 120 YEAR) THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'Birth date must be within a reasonable range.';
--     END IF;
-- END$$

-- DELIMITER ;

-- -- Add trigger to arrival date_time and leaving_date_time column
-- DELIMITER $$

-- CREATE TRIGGER cyz_itinerary_date_time_trg
-- BEFORE INSERT ON cyz_itinerary
-- FOR EACH ROW
-- BEGIN
--     DECLARE start_port_id INT;
--     DECLARE end_port_id INT;

--     -- Get trip start and end port ids
--     SELECT start_port_id, end_port_id
--     INTO start_port_id, end_port_id
--     FROM cyz_trip
--     WHERE trip_id = NEW.trip_id;

--     -- validate the case of arrival_date_time at start port
--     IF NEW.arrival_date_time IS NOT NULL AND NEW.port_id = start_port_id THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'Start port should not have arrival time.';
--     END IF;

--     -- Validate the case of leaving_date_time at end port 
--     IF NEW.leaving_date_time IS NOT NULL AND NEW.port_id = end_port_id THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'End port should not have leaving time.';
--     END IF;
-- END$$

-- DELIMITER ;

-- -- Add trigger to check if stateroom is vacant before booking
-- DELIMITER $$

-- CREATE TRIGGER check_stateroom_vacancy
-- BEFORE INSERT ON cyz_stateroom_booking
-- FOR EACH ROW
-- BEGIN
--     DECLARE is_vacant_status INT;

--     -- Check if the stateroom is vacant from cyz_stateroom_price table
--     SELECT is_vacant
--     INTO is_vacant_status
--     FROM cyz_stateroom_price
--     WHERE price_id = NEW.price_id;

--     -- If not vacant then raise an error
--     IF is_vacant_status = 0 THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'Stateroom is already booked.';
--     END IF;
-- END$$

-- DELIMITER ;

-- -- Add trigger to update stateroom vacancy status after booking
-- DELIMITER $$

-- CREATE TRIGGER set_stateroom_vacancy
-- AFTER INSERT ON cyz_stateroom_booking
-- FOR EACH ROW
-- BEGIN
--     -- Update the vacancy status of the booked stateroom
--     UPDATE cyz_stateroom_price
--     SET is_vacant = 0
--     WHERE price_id = NEW.price_id;
-- END$$

-- DELIMITER ;

-- -- Add trigger to prevent passenger under age 21 from buying alcohol package: Unlimited Bar (for adult age over 21)
-- DELIMITER $$

-- CREATE TRIGGER trg_alcohol_package_sale_age_limit
-- BEFORE INSERT ON cyz_package_sale
-- FOR EACH ROW
-- BEGIN
--     DECLARE passenger_age INT;

--     -- Calculate passenger age based on birth date
--     SELECT FLOOR(MONTHS_BETWEEN(CURRENT_TIMESTAMP, birth_date) / 12)
--     INTO passenger_age
--     FROM cyz_passenger
--     WHERE passenger_id = NEW.group_id;

--     -- Check if passenger is under 21 and trying to purchase alcohol package
--     IF passenger_age < 21 AND NEW.package_id = 1 THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'Passenger under 21 cannot purchase alcohol package.';
--     END IF;
-- END$$

-- DELIMITER ;

-- -- Add trigger to prevent passenger age under 5 years old from charging for a package
-- DELIMITER $$

-- CREATE TRIGGER trg_package_sale_age_limit
-- BEFORE INSERT ON cyz_package_sale
-- FOR EACH ROW
-- BEGIN
--     DECLARE eligible_passenger_count INT;
--     DECLARE current_purchase_count INT;

--     -- Count the number of eligible passengers (age 5 and above) in the group
--     SELECT COUNT(*)
--     INTO eligible_passenger_count
--     FROM cyz_passenger
--     WHERE group_id = NEW.group_id
--       AND FLOOR(MONTHS_BETWEEN(CURRENT_TIMESTAMP, birth_date) / 12) >= 5;

--     -- Count packages already purchased by the group
--     SELECT COUNT(*)
--     INTO current_purchase_count
--     FROM cyz_package_sale
--     WHERE group_id = NEW.group_id
--       AND package_id = NEW.package_id;

--     -- Check if the number of packages exceeds the number of eligible passengers
--     IF current_purchase_count >= eligible_passenger_count THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'Cannot purchase more packages than the number of eligible passengers (age 5 and above) in the group.';
--     END IF;
-- END$$

-- DELIMITER ;

-- -- Add trigger to prevent passenger age under 5 years old from charging for a stateroom
-- DELIMITER $$

-- CREATE TRIGGER trg_booking_age_limit
-- BEFORE INSERT ON cyz_stateroom_booking
-- FOR EACH ROW
-- BEGIN
--     DECLARE eligible_passenger_count INT;
--     DECLARE current_booking_count INT;

--     -- Count the number of eligible passengers (age 5 and above) in the group
--     SELECT COUNT(*)
--     INTO eligible_passenger_count
--     FROM cyz_passenger
--     WHERE group_id = NEW.group_id
--       AND FLOOR(MONTHS_BETWEEN(CURRENT_TIMESTAMP, birth_date) / 12) >= 5;

--     -- Count staterooms already booked by the group
--     SELECT COUNT(*)
--     INTO current_booking_count
--     FROM cyz_stateroom_booking
--     WHERE group_id = NEW.group_id
--       AND price_id = NEW.price_id;

--     -- Check if the number of staterooms exceeds the number of eligible passengers
--     IF current_booking_count >= eligible_passenger_count THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'Cannot book more staterooms than the number of eligible passengers (age 5 and above) in the group.';
--     END IF;
-- END$$

-- DELIMITER ;
