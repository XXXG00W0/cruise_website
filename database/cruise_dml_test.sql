truncate table cyz_address;
truncate table cyz_admin;
truncate table cyz_entertainment;
truncate table cyz_entertainment_trip;
truncate table cyz_group;
truncate table cyz_invoice;
truncate table cyz_itinerary;
truncate table cyz_package;
truncate table cyz_package_sale;
truncate table cyz_passenger;
truncate table cyz_payment;
truncate table cyz_port;
truncate table cyz_restaurant;
truncate table cyz_restaurant_trip;
truncate table cyz_stateroom;
truncate table cyz_stateroom_booking;
truncate table cyz_stateroom_price;
truncate table cyz_trip;
truncate table cyz_user;

INSERT INTO cyz_address (addr_id, street, addr_line_2, neighborhood, city, state_province, postal_code, country) VALUES
(1, '123 Main St', 'Apt 4B', 'Downtown', 'New York', 'NY', '10001', 'USA'),
(2, '456 Elm St', 'Suite 5A', 'Midtown', 'Los Angeles', 'CA', '90001', 'USA'),
(3, '789 Oak St', 'Floor 2', 'Uptown', 'Chicago', 'IL', '60601', 'USA'),
(4, '101 Pine St', 'Unit 3C', 'Suburb', 'Houston', 'TX', '77001', 'USA'),
(5, '202 Maple St', 'Room 1D', 'Old Town', 'Phoenix', 'AZ', '85001', 'USA');

INSERT INTO cyz_admin (admin_id, admin_phone, admin_pass, user_id, admin_fname, admin_lname) VALUES
(1, '123-456-7890', 'password', 1, 'John', 'Doe'),
(2, '234-567-8901', 'password', 2, 'Jane', 'Smith'),
(3, '345-678-9012', 'password', 3, 'James', 'Johnson'),
(4, '456-789-0123', 'password', 4, 'Jill', 'Jackson'),
(5, '567-890-1234', 'password', 5, 'Jack', 'Jenkins');

INSERT INTO cyz_entertainment (entertain_id, entertain_name, num_units, at_floor) VALUES
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

INSERT INTO cyz_entertainment_trip (entertain_id, trip_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

INSERT INTO cyz_group (group_id) VALUES
(1),
(2),
(3),
(4),
(5);

INSERT INTO cyz_invoice (invoice_id, payment_due, billing_date_time) VALUES
(1, 575.79, '2012-11-08 00:00:00'),
(2, 174.97, '2003-03-20 00:00:00'),
(3, 668.7, '2012-04-10 00:00:00'),
(4, 609.63, '2000-10-25 00:00:00'),
(5, 845.8, '2006-02-17 00:00:00');

INSERT INTO cyz_itinerary (itinerary_id, arrival_date_time, leaving_date_time, trip_id, port_id) VALUES
(1, '2015-07-31 00:00:00', '2006-10-13 00:00:00', 1, 1),
(2, '2023-02-26 00:00:00', '2006-09-09 00:00:00', 2, 2),
(3, '2021-10-29 00:00:00', '2003-03-29 00:00:00', 3, 3),
(4, '2020-10-27 00:00:00', '2004-05-11 00:00:00', 4, 4),
(5, '2023-12-12 00:00:00', '2019-12-14 00:00:00', 5, 5);

INSERT INTO cyz_package (package_id, pkg_charge_type, pkg_price, pkg_name) VALUES
(1, 'ugmdvpivdxfp', 555.98, 'wiqyijwjdeskowd'),
(2, 'khwtdngzwpwi', 448.62, 'mshnljtsedp'),
(3, 'tolgbqopuyzlpup', 532.32, 'vazphksfhkeqh'),
(4, 'kexdsvmxf', 261.4, 'hunxcc'),
(5, 'nwaorafwlipo', 536.98, 'vmmoony');
INSERT INTO cyz_package_sale (pkg_sale_id, package_id, group_id, invoice_id) VALUES
(1, 1, 1, 1),
(2, 2, 2, 2),
(3, 3, 3, 3),
(4, 4, 4, 4),
(5, 5, 5, 5);
INSERT INTO cyz_passenger (passenger_id, birth_date, gender, nationality, phone, cyz_address_addr_id, cyz_group_group_id, passenger_fname, passenger_lname, user_id) VALUES
(1, '2015-06-25 00:00:00', 'tajaydfohpqb', 'uentrms', 'mwnbuxfepvomg', 1, 1, 'hyhxraiolz', 'tnqacogc', 1),
(2, '2013-09-23 00:00:00', 'zjibovvnstrkiro', 'duvhvwcsy', 'cjihlpevxx', 2, 2, 'lelak', 'qhtmgmfeillbdqy', 2),
(3, '2020-07-03 00:00:00', 'ngcjygae', 'cdawqvylwcqzv', 'zwltdnmuwndpus', 3, 3, 'gsaixindsc', 'swdfkpeyvowhdrk', 3),
(4, '2014-11-18 00:00:00', 'xeyaiccyr', 'cdliwvkicm', 'ynufxlrfvjmydit', 4, 4, 'tjffzwlmjefyya', 'qtwuxwjriowwlgx', 4),
(5, '2004-08-18 00:00:00', 'optgriurirvm', 'mszfi', 'yhvtlzkrj', 5, 5, 'vcyxosaoku', 'dlljhjr', 5);
INSERT INTO cyz_payment (payment_id, payment_date, pay_amount, payment_method, trip_id, cyz_group_group_id, invoice_id) VALUES
(1, '2015-10-14 00:00:00', 807.12, 'kbyjc', 1, 1, 1),
(2, '2014-08-18 00:00:00', 760.65, 'swmatipdzsl', 2, 2, 2),
(3, '2016-08-28 00:00:00', 209.44, 'pxgwkbpi', 3, 3, 3),
(4, '2018-05-21 00:00:00', 414.5, 'hledfjw', 4, 4, 4),
(5, '2019-09-15 00:00:00', 356.23, 'jbcuaqfua', 5, 5, 5);
INSERT INTO cyz_port (port_id, nearest_airport, num_parking_spots, cyz_address_addr_id, port_name) VALUES
(1, 'yjoysbzyqvzx', 1, 1, 'ibbnyclpfepxk'),
(2, 'qxlrihxkhw', 2, 2, 'ozloqf'),
(3, 'ksrgxjot', 3, 3, 'aqggye'),
(4, 'jzuzjwkhtp', 4, 4, 'fypncjp'),
(5, 'ypgjcvzrmciqi', 5, 5, 'hurturwqikbt');
INSERT INTO cyz_restaurant (restaurant_id, restaurant_name, serve_type, opening_time, closing_time, at_floor) VALUES
(1, 'kmtgnkundakx', 'qajkmatia', '2023-06-14 00:00:00', '2008-09-12 00:00:00', 1),
(2, 'rdogqbjjtuc', 'deivxjheio', '2014-07-21 00:00:00', '2018-12-13 00:00:00', 2),
(3, 'lebbgneojh', 'xydgldlea', '2001-12-10 00:00:00', '2018-09-25 00:00:00', 3),
(4, 'swvvmbrvxqtdm', 'pcuizzewvetecs', '2016-02-20 00:00:00', '2019-01-20 00:00:00', 4),
(5, 'gojsv', 'mcvqfawao', '2010-07-18 00:00:00', '2018-05-29 00:00:00', 5);
INSERT INTO cyz_restaurant_trip (restaurant_id, trip_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);
INSERT INTO cyz_stateroom (stateroom_id, location, num_bed, num_bathroom, num_balcony, size_sqft, room_number) VALUES
(1, 'pdmmvtmhquudzi', 1, 666.36, 1, 553.53, 1),
(2, 'xqshviwj', 2, 910.0, 2, 783.04, 2),
(3, 'pdedxparxvxychr', 3, 671.44, 3, 975.92, 3),
(4, 'lxcbwnzvlodog', 4, 179.26, 4, 616.27, 4),
(5, 'pyvyni', 5, 588.21, 5, 53.67, 5);
INSERT INTO cyz_stateroom_booking (booking_id, group_id, invoice_id, price_id) VALUES
(1, 1, 1, 1),
(2, 2, 2, 2),
(3, 3, 3, 3),
(4, 4, 4, 4),
(5, 5, 5, 5);
INSERT INTO cyz_stateroom_price (price_id, cyz_stateroom_stateroom_id, price_per_night, trip_id, is_vacant) VALUES
(1, 1, 892.0, 1, 980.08),
(2, 2, 200.16, 2, 237.95),
(3, 3, 324.51, 3, 332.24),
(4, 4, 326.41, 4, 50.97),
(5, 5, 740.0, 5, 328.98);
INSERT INTO cyz_trip (trip_id, start_date, end_date, start_port_id, end_port_id) VALUES
(1, '2020-06-04 00:00:00', '2005-03-08 00:00:00', 1, 1),
(2, '2018-12-05 00:00:00', '2008-07-10 00:00:00', 2, 2),
(3, '2013-07-12 00:00:00', '2001-11-12 00:00:00', 3, 3),
(4, '2014-07-25 00:00:00', '2015-11-27 00:00:00', 4, 4),
(5, '2014-10-21 00:00:00', '2020-07-30 00:00:00', 5, 5);
INSERT INTO cyz_user (user_id, username, password, email, user_type) VALUES
(1, 'wixfcffbp', 'gxvfmivhndl', 'intscgvmtto', 'admin'),
(2, 'fnvaf', 'ncehiphbr', 'vgraqcuebgv', 'admin'),
(3, 'qkflbnrgpwz', 'dkcxm', 'qqpqiuvefwvkkm', 'admin'),
(4, 'chlbagvktkma', 'igklhawvvohxs', 'qugfaypxmopaleq', 'admin'),
(5, 'itbkiq', 'akmdknl', 'flisnwfb', 'admin');