CREATE TABLE vehicle_types (
    id SERIAL PRIMARY KEY,
    vehicle_type VARCHAR(50) UNIQUE
);

INSERT INTO vehicle_types(vehicle_type) VALUES('motorcycle');
INSERT INTO vehicle_types(vehicle_type) VALUES('car');
INSERT INTO vehicle_types(vehicle_type) VALUES('truck');

CREATE TABLE sectors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(10) UNIQUE,
    vehicle_type_id INTEGER REFERENCES vehicle_types(id) NOT NULL,
    number_of_places SMALLINT NOT NULL,
    places_occupied SMALLINT NOT NULL DEFAULT 0
);

INSERT INTO sectors(name, vehicle_type_id, number_of_places)
VALUES ('A', 1, 20);
INSERT INTO sectors(name, vehicle_type_id, number_of_places)
VALUES ('B', 2, 30);
INSERT INTO sectors(name, vehicle_type_id, number_of_places)
VALUES ('C', 3, 10);

CREATE TABLE vehicle_types_tariffs (
    id SERIAL PRIMARY KEY,
    type_id INTEGER REFERENCES vehicle_types(id) NOT NULL,
    price_per_hour DECIMAL(8, 2) NOT NULL
);

INSERT INTO vehicle_types_tariffs(type_id, price_per_hour) VALUES(1, 2.5);
INSERT INTO vehicle_types_tariffs(type_id, price_per_hour) VALUES(2, 5);
INSERT INTO vehicle_types_tariffs(type_id, price_per_hour) VALUES(3, 10);

CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    type_id INTEGER REFERENCES vehicle_types(id) NOT NULL,
    license_plate VARCHAR(30) UNIQUE
);

CREATE TABLE vehicle_stays (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER REFERENCES vehicles(id) NOT NULL,
    sector_id INTEGER REFERENCES sectors(id) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NULL
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    stay_id INTEGER REFERENCES vehicle_stays(id) NOT NULL,
    amount DECIMAL(11, 2) NOT NULL
);

CREATE TYPE Bill AS
(
    stay_id INTEGER,
    tariff DECIMAL(8, 2),
    stay_duration INTEGER
);

CREATE OR REPLACE FUNCTION get_bill(plate_number VARCHAR)
RETURNS Bill AS $$
DECLARE
    my_current_time TIMESTAMP := CURRENT_TIMESTAMP;
    bill_object Bill;
BEGIN
    SELECT vs.id,
           vtt.price_per_hour,
           EXTRACT(EPOCH FROM (my_current_time - vs.start_time))::INTEGER
    INTO bill_object.stay_id, bill_object.tariff, bill_object.stay_duration
    FROM VEHICLE_STAYS vs
        JOIN vehicles v on v.id = vs.vehicle_id
        JOIN vehicle_types_tariffs vtt on v.type_id = vtt.type_id
    WHERE v.license_plate = plate_number
    AND END_TIME IS NULL;

    RETURN bill_object;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION finish_stay(arg_stay_id INTEGER,
                                       arg_stay_duration INTEGER,
                                       arg_payment DECIMAL(11, 2))
RETURNS BOOLEAN AS $$
DECLARE
    sector_id INTEGER;
    result BOOLEAN;
BEGIN
    UPDATE vehicle_stays
    SET end_time = start_time + (arg_stay_duration || ' seconds')::INTERVAL
    WHERE id = arg_stay_id;

    INSERT INTO payments(stay_id, amount) VALUES(arg_stay_id, arg_payment);

    SELECT s.id INTO sector_id
    FROM sectors s JOIN vehicle_stays vs on s.id = vs.sector_id
    WHERE vs.id = arg_stay_id;

    UPDATE sectors
        SET places_occupied = places_occupied - 1
    WHERE id = sector_id;

    result := true;

    RETURN result;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION new_stay(arg_type VARCHAR, arg_plate_number VARCHAR)
RETURNS VARCHAR(10) AS $$
DECLARE
    new_stay_vehicle_id INTEGER;
    new_stay_vehicle_type_id INTEGER;
    new_stay_sector_id INTEGER;
    new_stay_sector_name VARCHAR(10);
BEGIN
    SELECT s.id, s.name INTO new_stay_sector_id, new_stay_sector_name
    FROM sectors s JOIN vehicle_types vt on vt.id = s.vehicle_type_id
    WHERE vt.vehicle_type = arg_type
    ORDER BY s.places_occupied
    LIMIT 1;

    IF new_stay_sector_id IS NULL THEN
        return NULL;
    END IF;

    SELECT id INTO new_stay_vehicle_id FROM vehicles
    WHERE license_plate = arg_plate_number;

    IF new_stay_vehicle_id IS NULL THEN
        SELECT id INTO new_stay_vehicle_type_id
        FROM vehicle_types WHERE vehicle_type = arg_type;

        INSERT INTO vehicles(type_id, license_plate)
        VALUES(new_stay_vehicle_type_id, arg_plate_number);

        SELECT id INTO new_stay_vehicle_id FROM vehicles
        WHERE license_plate = arg_plate_number;
    END IF;

    INSERT INTO vehicle_stays(vehicle_id, sector_id, start_time, end_time)
    VALUES (new_stay_vehicle_id, new_stay_sector_id, CURRENT_TIMESTAMP, null);

    UPDATE sectors
        SET places_occupied = places_occupied + 1
    WHERE id = new_stay_sector_id;

    RETURN new_stay_sector_name;
END;
$$ LANGUAGE plpgsql;

-----------------------------------

DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS vehicle_stays;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS sectors;
DROP TABLE IF EXISTS vehicle_types_tariffs;
DROP TABLE IF EXISTS vehicle_types;

DROP FUNCTION IF EXISTS get_bill(plate_number VARCHAR);

DROP FUNCTION IF EXISTS finish_stay(arg_stay_id INTEGER,
                                             arg_stay_duration INTEGER,
                                             arg_payment DECIMAL(11, 2));

DROP FUNCTION IF EXISTS new_stay(arg_type VARCHAR, arg_plate_number VARCHAR);